"""Preview/render the configured timeline, then mux and verify the final file."""
from pathlib import Path
import argparse
import json
import math
import subprocess
import functools
from PIL import Image
import motion
import compose

ROOT = Path(__file__).resolve().parent


def path(value):
    p = Path(value).expanduser()
    return p if p.is_absolute() else ROOT / p


@functools.lru_cache(maxsize=32)
def probe(filename):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
        str(filename)]))


def load():
    config = json.loads((ROOT / "edit.json").read_text())
    style = config.get("caption_style", "legacy")
    motion.caption_style(style)
    mode = motion.caption_mode(config.get("caption_mode", "group"))
    groups = json.loads(path(config["captions"]).read_text())
    if config["size"] != [1080, 1920] or config["fps"] != 30:
        raise ValueError("Adapter le compositeur pour changer de format ; base fournie en 1080×1920/30.")
    if not path(config["source"]).is_file():
        raise ValueError("Rush introuvable.")
    presentation = motion.animation_host_settings(config)
    if presentation["mode"] in ("popout", "behind"):
        alpha = path(presentation["alpha"])
        if not alpha.is_file():
            raise ValueError("Préparer le masque avec matte_video.py --project avant le rendu.")
        metadata = json.loads(alpha.with_suffix(".json").read_text())
        if (not metadata.get("timeline_aligned") or metadata["fps"] != config["fps"]
                or metadata["frames"] != round(config["duration"] * config["fps"])
                or metadata["source_in"] != config.get("source_in", 0)
                or metadata["host_center"] != config["host_center"]
                or metadata["host_filter"] != config.get("host_filter", "")):
            raise ValueError("Le masque ne correspond plus à la timeline ou au recadrage.")
    source_metadata = probe(str(path(config["source"])))
    source_duration = float(source_metadata["format"]["duration"])
    if (config["duration"] <= 0 or config.get("source_in", 0) < 0 or
            config.get("source_in", 0) + config["duration"] > source_duration + 1 / 30):
        raise ValueError("La portion demandée dépasse le rush.")
    if not groups:
        raise ValueError("Préparer captions.json avec les vrais mots et leurs temps avant le rendu.")
    if config.get("caption_fixed", False):
        if any("y" in group for group in groups) or any(
                "caption_y" in scene for scene in config["scenes"]):
            raise ValueError("Sous-titres fixes : supprimer les placements y par groupe "
                             "et caption_y par scène ; recomposer les illustrations.")
    last_end = 0
    for group in groups:
        if not (last_end <= group["start"] < group["end"] <= config["duration"] + .05):
            raise ValueError("Temps des groupes invalides ou groupes qui se chevauchent.")
        if not group.get("words"):
            raise ValueError("Groupe de sous-titres vide.")
        last_word = group["start"]
        for word in group["words"]:
            # Some real alignments give a very short word equal start/end values.
            # Activation uses its start and the next word's start, without inventing a duration.
            if not (last_word <= word["start"] <= word["end"] <= group["end"] + .05):
                raise ValueError("Temps des mots invalides.")
            last_word = word["end"]
        last_end = group["end"]
    last_end = 0
    for scene in config["scenes"]:
        if not (last_end <= scene["start"] < scene["end"] <= config["duration"] + .001):
            raise ValueError("Scènes non triées, chevauchantes ou hors durée.")
        if scene["type"] not in ("host", "broll", "document_chain", "relation"):
            raise ValueError(f"Type de scène à implémenter : {scene['type']}")
        if scene["type"] == "document_chain":
            if len(scene["nodes"]) != 3:
                raise ValueError("Le parcours document utilise trois nœuds.")
            ordered = [scene["start"], scene["stamp_at"], scene["shrink_at"],
                       scene["second_at"], scene["last_at"], scene["end"]]
            if ordered != sorted(ordered):
                raise ValueError("Ordre des événements du parcours incohérent.")
        if scene["type"] == "relation" and len(scene["nodes"]) != 2:
            raise ValueError("La scène relation utilise deux nœuds.")
        for item in [scene] + scene.get("nodes", []):
            if item.get("path") and not path(item["path"]).is_file():
                raise ValueError(f"Média introuvable : {item['path']}")
        last_end = scene["end"]
    # Validate complete caption blocks before decoding/encoding the timeline.
    # A group keeps one position even when it spans a scene boundary.
    boundaries = sorted({0., config["duration"]} |
                        {s[k] for s in config["scenes"] for k in ("start", "end")})
    for group in groups:
        words = tuple(w["word"] for w in group["words"])
        try:
            layer = motion.caption_card(words, 0, style, mode)
        except ValueError as error:
            raise ValueError(f"Sous-titres à {group['start']} s : {error}") from error
        times = [group["start"]] + [t for t in boundaries if group["start"] < t < group["end"]]
        positions = set()
        for time in times:
            scene = next((s for s in config["scenes"] if s["start"] <= time < s["end"]), {})
            y = group.get("y", scene.get("caption_y"))
            positions.add(motion.caption_position(layer, y, style))
        if len(positions) > 1:
            raise ValueError(f"Le groupe à {group['start']} s change de position en cours de phrase. "
                             "Fixer son champ y ou déplacer la transition entre deux groupes.")
    return config, groups


class Reader:
    def __init__(self, filename, start=0, center=(.5, .5), grade=""):
        vf = ("scale=1080:1920:force_original_aspect_ratio=increase,"
              f"crop=1080:1920:(iw-ow)*{center[0]}:(ih-oh)*{center[1]}")
        if grade:
            vf += "," + grade
        vf += ",fps=30,tpad=stop_mode=clone:stop_duration=0.05"
        self.process = subprocess.Popen([
            "ffmpeg", "-v", "error", "-threads", "2", "-ss", str(start),
            "-i", str(filename), "-an", "-vf", vf, "-pix_fmt", "rgb24",
            "-f", "rawvideo", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def read(self):
        expected = 1080 * 1920 * 3
        data = self.process.stdout.read(expected)
        if len(data) != expected:
            raise RuntimeError("Fin du média trop tôt : contrôler sa durée et ses points d’entrée.")
        return Image.frombytes("RGB", (1080, 1920), data)

    def close(self):
        self.process.terminate()
        self.process.stdout.close()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
        self.process.stderr.close()


class MatteReader(Reader):
    """Read the exact indexed mask frame, retaining its native resolution."""
    def __init__(self, filename, frame_index=0):
        stream = next(s for s in probe(str(filename))["streams"]
                      if s["codec_type"] == "video")
        self.size = (stream["width"], stream["height"])
        # Frame selection avoids the millisecond-rounded timestamps of MKV.
        self.process = subprocess.Popen([
            "ffmpeg", "-v", "error", "-threads", "2", "-i", str(filename),
            "-an", "-vf", f"select=gte(n\\,{frame_index})", "-fps_mode", "passthrough",
            "-pix_fmt", "gray", "-f", "rawvideo", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def read(self):
        expected = self.size[0] * self.size[1]
        data = self.process.stdout.read(expected)
        if len(data) != expected:
            raise RuntimeError("Masque de détourage trop court.")
        return Image.frombytes("L", self.size, data)


class Media:
    def __init__(self):
        self.images, self.readers, self.mattes = {}, {}, {}

    def matte(self, value, frame_index):
        old = self.mattes.get(value)
        if old and frame_index == old[1]:
            return old[2]
        if old and frame_index == old[1] + 1:
            reader = old[0]
        else:
            if old:
                old[0].close()
            reader = MatteReader(path(value), frame_index)
        mask = reader.read()
        self.mattes[value] = (reader, frame_index, mask)
        return mask

    def frame(self, value, time, center=(.5, .5)):
        filename = path(value)
        if filename.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            if value not in self.images:
                self.images[value] = Image.open(filename).convert("RGB")
            return self.images[value]
        key = (value, tuple(center))
        old = self.readers.get(key)
        if old and abs(time - old[1]) < 1e-5:
            return old[2]
        if old and abs(time - old[1] - 1 / 30) < 1e-4:
            reader = old[0]
        else:
            if old:
                old[0].close()
            reader = Reader(filename, time, center)
        frame = reader.read()
        self.readers[key] = (reader, time, frame)
        return frame

    def close(self):
        for reader, _, _ in self.readers.values():
            reader.close()
        for reader, _, _ in self.mattes.values():
            reader.close()


def frame(t, host, media, config, groups):
    scene = next((s for s in config["scenes"] if s["start"] <= t < s["end"]),
                 {"type": "host"})
    presentation = motion.animation_host_settings(config)
    animated = scene["type"] not in ("host", "broll")
    if animated and presentation["mode"] in ("popout", "behind"):
        host.info["matte"] = media.matte(presentation["alpha"], round(t * config["fps"]))
    image, y = compose.compose(t, host, scene, media)
    if animated:
        motion.animation_presenter(image, host, presentation)
    style = config.get("caption_style", "legacy")
    motion.captions(image, t, groups, y if style == "legacy" else scene.get("caption_y"),
                    style, config.get("caption_mode", "group"))
    return image.convert("RGB")


def preview(times, safe_zones=False):
    config, groups = load()
    if not times:
        times = [0.3] + [(s["start"] + s["end"]) / 2 for s in config["scenes"]]
    times = [t for t in times if 0 <= t < config["duration"]]
    if not times:
        raise ValueError("Aucun instant d’aperçu dans la durée du montage.")
    sheet = Image.new("RGB", (324 * min(4, len(times)), 576 * math.ceil(len(times) / 4)), motion.INK)
    media = Media()
    try:
        for i, time in enumerate(times):
            reader = Reader(path(config["source"]), config.get("source_in", 0) + time,
                            config["host_center"], config.get("host_filter", ""))
            try:
                image = frame(time, reader.read(), media, config, groups)
            finally:
                reader.close()
            if safe_zones:
                image = motion.safe_zone_guide(image, config.get("caption_style", "legacy"))
            suffix = "_safe" if safe_zones else ""
            image.save(ROOT / "work" / f"preview{suffix}_{time:.2f}.jpg", quality=95)
            sheet.paste(image.resize((324, 576), Image.Resampling.LANCZOS), ((i % 4) * 324, (i // 4) * 576))
    finally:
        media.close()
    filename = ROOT / "work" / ("preview_safe.jpg" if safe_zones else "preview.jpg")
    sheet.save(filename, quality=95)
    print(filename)


def render():
    config, groups = load()
    count = round(config["duration"] * 30)
    host = Reader(path(config["source"]), config.get("source_in", 0),
                  config["host_center"], config.get("host_filter", ""))
    media = Media()
    log = (ROOT / "work/render.log").open("w")
    encoder = subprocess.Popen([
        "ffmpeg", "-v", "warning", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", "1080x1920", "-r", "30", "-i", "-", "-an", "-c:v", "libx264",
        "-preset", "fast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(ROOT / "work/visuals.mp4")],
        stdin=subprocess.PIPE, stderr=log)
    try:
        for i in range(count):
            encoder.stdin.write(frame(i / 30, host.read(), media, config, groups).tobytes())
            if i % 120 == 0:
                print(f"Image {i}/{count}", flush=True)
    finally:
        host.close()
        media.close()
        encoder.stdin.close()
        code = encoder.wait()
        log.close()
    if code:
        raise RuntimeError("Échec d’encodage : consulter work/render.log.")


def srt_time(t):
    milliseconds = round(t * 1000)
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def finish():
    config, groups = load()
    audio = path(config["audio_copy_from"]) if config.get("audio_copy_from") else ROOT / "work/final_mix.wav"
    if not audio.is_file():
        raise ValueError("Préparer le mix avec audio.py mix, ou renseigner audio_copy_from.")
    if config.get("audio_copy_from"):
        stream = next(s for s in probe(str(audio))["streams"] if s["codec_type"] == "audio")
        if stream["codec_name"] != "aac":
            raise ValueError("audio_copy_from attend une piste AAC validée ; préparer un mix pour les autres formats.")
        if abs(float(stream["duration"]) - config["duration"]) > .08:
            raise ValueError("La piste copiée doit avoir la même durée que la timeline.")
    codec = ["-c:a", "copy"] if config.get("audio_copy_from") else ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "work/visuals.mp4"),
        "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
        *codec, "-t", str(config["duration"]), "-movflags", "+faststart",
        str(ROOT / "exports/final.mp4")], check=True)
    subtitles = []
    entries = []
    for group in groups:
        if config.get("caption_mode", "group") == "word":
            for j, word in enumerate(group["words"]):
                end = (group["words"][j + 1]["start"]
                       if j + 1 < len(group["words"]) else group["end"])
                if round(end * 1000) > round(word["start"] * 1000):
                    entries.append((word["start"], end, word["word"]))
        else:
            entries.append((group["start"], group["end"],
                            " ".join(w["word"] for w in group["words"])))
    for i, (start, end, text) in enumerate(entries, 1):
        subtitles.append(f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
    (ROOT / "exports/subtitles.srt").write_text("\n".join(subtitles))
    print(ROOT / "exports/final.mp4")


def verify():
    config, _ = load()
    filename = ROOT / "exports/final.mp4"
    metadata = probe(str(filename))
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    audio = next(s for s in metadata["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"], video["r_frame_rate"]) == (1080, 1920, "30/1")
    assert int(video["nb_frames"]) == round(config["duration"] * 30)
    assert abs(float(video["duration"]) - float(audio["duration"])) < .08
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(filename), "-f", "null", "-"], check=True)
    report = {"video": video, "audio": audio, "decode": "passed"}
    (ROOT / "work/verification.json").write_text(json.dumps(report, indent=2))
    print("Décodage, format et durée contrôlés. Inspecter et écouter le MP4 final.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["preview", "render", "finish", "verify"])
    parser.add_argument("--times", nargs="*", type=float)
    parser.add_argument("--safe-zones", action="store_true",
                        help="Aperçu des marges de travail Reels/TikTok, jamais ajouté à l’export.")
    args = parser.parse_args()
    if args.command == "preview":
        preview(args.times, args.safe_zones)
    else:
        globals()[args.command]()
