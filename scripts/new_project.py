#!/usr/bin/env python3
"""Create a self-contained editable project; never overwrite an existing one."""
from pathlib import Path
import argparse
import json
import math
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--captions", type=Path)
    parser.add_argument("--music", type=Path)
    parser.add_argument("--caption-style", choices=("small-center", "large-bottom"),
                        default="small-center", help="Petits au centre ou grands en bas.")
    parser.add_argument("--caption-mode", choices=("group", "word"),
                        default="word", help="Un mot à la fois (défaut) ou phrase avec mot actif.")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--animation-host", choices=("hidden", "popout", "inset", "behind"),
                       help="Un mode orateur pour toutes les animations du film.")
    modes.add_argument("--host-popout", dest="animation_host", action="store_const", const="popout",
                       help="Alias de --animation-host popout.")
    parser.set_defaults(animation_host="inset")
    args = parser.parse_args()
    source = args.source.expanduser().resolve(strict=True)
    music = args.music.expanduser().resolve(strict=True) if args.music else None
    captions = json.loads(args.captions.read_text()) if args.captions else []
    if not isinstance(captions, list):
        parser.error("Les sous-titres doivent être une liste de groupes horodatés.")
    probe = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
        str(source)]))
    stream = next((s for s in probe["streams"] if s["codec_type"] == "video"), None)
    if not stream:
        parser.error("La source ne contient pas de vidéo.")
    source_duration = float(stream.get("duration", probe["format"]["duration"]))
    frames = math.ceil(source_duration * 30 - 1e-6)
    root = args.output.expanduser().resolve()
    if root.exists():
        parser.error(f"Le dossier existe déjà : {root}. Choisir une nouvelle version.")
    skill = Path(__file__).resolve().parents[1]
    root.mkdir(parents=True)
    for directory in ("assets", "work", "exports"):
        (root / directory).mkdir()
    shutil.copytree(skill / "assets/fonts", root / "assets/fonts")
    shutil.copytree(skill / "assets/sfx", root / "assets/sfx")
    for path in (skill / "assets/starter").glob("*.py"):
        shutil.copy2(path, root / path.name)
    shutil.copy2(skill / "scripts/clean_voice.py", root / "clean_voice.py")
    if args.animation_host in ("popout", "behind"):
        shutil.copytree(skill / "assets/matting", root / "assets/matting")
        shutil.copy2(skill / "scripts/matte_video.py", root / "matte_video.py")
    config = {
        "source": str(source), "duration": frames / 30, "fps": 30,
        "size": [1080, 1920], "captions": "captions.json",
        "caption_style": args.caption_style, "caption_mode": args.caption_mode,
        "caption_fixed": True,
        "source_in": 0, "host_center": [.55, .48], "host_filter": "",
        "scenes": [],
        "audio": {
            "voice_channel": None, "music": str(music) if music else None,
            "music_in": 0, "music_lufs": -24, "music_automation": [],
            "events": [], "target_lufs": -14.5, "true_peak": -1.8,
        },
        "audio_copy_from": None,
    }
    config["animation_host"] = {
        "mode": args.animation_host, "alpha": "assets/host_alpha.mkv",
        "inset": {"box": [42, 1320, 996, 552], "radius": 48, "center": [.5, .37]},
        "popout": {
            "x": 42, "width": 996, "background_top": 1320,
            "background_bottom": 1872, "foreground_top": 1136,
            "source_zoom": 1.02, "source_anchor_y": 780, "screen_anchor_y": 1425,
        },
        "behind": {"scale": 1.0, "x": 0, "y": 0},
    }
    (root / "edit.json").write_text(json.dumps(config, indent=2, ensure_ascii=False))
    (root / "captions.json").write_text(json.dumps(captions, indent=2, ensure_ascii=False))
    (root / "work/source_probe.json").write_text(json.dumps(probe, indent=2))
    (root / "exports/credits.txt").write_text(
        "CRÉDITS — À renseigner pour les médias effectivement utilisés.\n"
        "Vidéo principale : " + source.name + "\n"
        "DA : Babayaga ; Someone Extended Regular et Bold ; #5D71FC.\n"
        "Pour chaque média externe : titre, auteur, URL source, licence et adaptation.\n"
    )
    if args.animation_host in ("popout", "behind"):
        with (root / "exports/credits.txt").open("a") as credits:
            credits.write("Détourage : RobustVideoMatting MobileNetV3 fp32 ONNX, GPL-3.0. "
                          "https://github.com/PeterL1n/RobustVideoMatting — licence dans assets/matting.\n")
    print(json.dumps({
        "project": str(root), "source_seconds": source_duration,
        "output_frames": frames, "captions_groups": len(captions),
        "next": "Vérifier la transcription, choisir le canal voix et composer edit.json.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
