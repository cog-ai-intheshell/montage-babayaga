"""Channel inspection and an adaptable speech-first mix; FFmpeg + NumPy only."""
from pathlib import Path
import argparse
import json
import math
import re
import subprocess
import numpy as np
from render import ROOT, path, probe

SR = 48000


def config():
    return json.loads((ROOT / "edit.json").read_text())


def run(args):
    return subprocess.run(args, capture_output=True, check=True)


def decode(filename, duration, start=0, filters=""):
    args = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", str(filename),
            "-t", str(duration), "-vn"]
    if filters:
        args += ["-af", filters]
    args += ["-ar", str(SR), "-ac", "2", "-f", "f32le", "-"]
    data = np.frombuffer(run(args).stdout, dtype="<f4").reshape(-1, 2).copy()
    if not np.all(np.isfinite(data)):
        raise ValueError(f"Valeurs audio invalides dans {filename}")
    return data


def save(filename, samples):
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR),
        "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", str(filename)],
        input=np.asarray(samples, dtype="<f4").tobytes(), check=True)


def measure(filename, target=-14.5, peak=-1.8):
    result = run([
        "ffmpeg", "-hide_banner", "-i", str(filename), "-af",
        f"loudnorm=I={target}:TP={peak}:LRA=8:print_format=json", "-f", "null", "-"])
    found = re.search(r'\{\s*"input_i".*?\}', result.stderr.decode(), re.S)
    if not found:
        raise ValueError("Mesure loudness indisponible.")
    return json.loads(found.group())


def fit_duration(samples, count):
    if len(samples) < count:
        samples = np.pad(samples, ((0, count - len(samples)), (0, 0)))
    return samples[:count]


def fade(samples, attack=.005, release=.05):
    samples = samples.copy()
    a = min(len(samples), round(attack * SR))
    b = min(len(samples), round(release * SR))
    if a:
        samples[:a] *= np.linspace(0, 1, a)[:, None]
    if b:
        samples[-b:] *= np.linspace(1, 0, b)[:, None]
    return samples


def inspect():
    cfg = config()
    source = path(cfg["source"])
    stream = next(s for s in probe(str(source))["streams"] if s["codec_type"] == "audio")
    data = decode(source, min(cfg["duration"], 20), cfg.get("source_in", 0))
    rms = np.sqrt(np.mean(data ** 2, axis=0))
    peaks = np.max(np.abs(data), axis=0)
    correlation = (float(np.corrcoef(data.T)[0, 1])
                   if np.all(rms > 1e-7) else None)
    result = {
        "source_channels": stream.get("channels"),
        "decoded_rms_dbfs": (20 * np.log10(np.maximum(rms, 1e-10))).tolist(),
        "decoded_peaks_dbfs": (20 * np.log10(np.maximum(peaks, 1e-10))).tolist(),
        "correlation": correlation,
        "next": "Écouter les canaux et choisir voice_channel dans edit.json.",
    }
    (ROOT / "work/channels.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


def mix():
    cfg = config()
    audio = cfg["audio"]
    duration, count = cfg["duration"], round(cfg["duration"] * SR)
    selected = audio.get("voice_channel")
    if selected not in (0, 1, "mix"):
        raise ValueError("Choisir voice_channel : 0, 1 ou 'mix' après inspection et écoute.")
    source = path(cfg["source"])
    channels = next(s for s in probe(str(source))["streams"] if s["codec_type"] == "audio")["channels"]
    if isinstance(selected, int) and selected >= channels:
        raise ValueError("Ce canal n’existe pas dans la source.")
    if selected != "mix":
        pan = f"pan=stereo|c0=c{selected}|c1=c{selected},"
    else:
        combined = "+".join(f"{1/channels:.8f}*c{i}" for i in range(channels))
        pan = f"pan=stereo|c0={combined}|c1={combined},"
    shaping = ("aformat=sample_fmts=fltp,volume=0.8,highpass=f=78,"
               "equalizer=f=270:t=q:w=1:g=-1.8,equalizer=f=2900:t=q:w=0.9:g=1.4,"
               "acompressor=threshold=0.10:ratio=2:attack=9:release=105:knee=3:makeup=1")
    voice = fit_duration(decode(source, duration, cfg.get("source_in", 0),
                               pan + audio.get("voice_filter", shaping)), count)
    voice_file = ROOT / "work/voice.wav"
    save(voice_file, voice)
    voice_measure = measure(voice_file, -16.4)
    loudness = float(voice_measure["input_i"])
    if not math.isfinite(loudness):
        raise ValueError("Voix silencieuse ou trop courte pour une mesure fiable.")
    voice = fade(voice * 10 ** ((audio.get("voice_lufs", -16.4) - loudness) / 20))
    save(voice_file, voice)

    music = np.zeros((count, 2), np.float32)
    if audio.get("music"):
        music = decode(path(audio["music"]), duration, audio.get("music_in", 0),
                       "aformat=sample_fmts=fltp,volume=0.5,highpass=f=55,"
                       "equalizer=f=2400:t=q:w=0.7:g=-3,lowpass=f=14500")
        if len(music) < count - SR * .1:
            raise ValueError("Extrait musical trop court : choisir un autre point d’entrée ou préparer une boucle.")
        music = fit_duration(music, count)
        music_file = ROOT / "work/music.wav"
        save(music_file, music)
        music_measure = measure(music_file, -24)
        source_i = float(music_measure["input_i"])
        if not math.isfinite(source_i):
            raise ValueError("Musique silencieuse ou mesure indisponible.")
        music *= 10 ** ((audio.get("music_lufs", -24) - source_i) / 20)
        automation = audio.get("music_automation", [])
        if automation:
            times = [p[0] for p in automation]
            if times != sorted(times) or len(set(times)) != len(times):
                raise ValueError("Les points d’automation doivent être triés et distincts.")
            curve = np.interp(np.arange(count) / SR, times, [p[1] for p in automation])
            music *= (10 ** (curve / 20))[:, None]
        music = fade(music, .08, .65)
        save(music_file, music)
        ducked = ROOT / "work/music_ducked.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(music_file), "-i", str(voice_file),
             "-filter_complex",
             "[0:a][1:a]sidechaincompress=threshold=0.07:ratio=2.7:attack=14:release=230:makeup=1[bed]",
             "-map", "[bed]", "-c:a", "pcm_f32le", str(ducked)])
        music = fit_duration(decode(ducked, duration), count)

    effects = np.zeros((count, 2), np.float32)
    for event in audio.get("events", []):
        if event["at"] < 0 or event["at"] >= duration or event["duration"] <= 0:
            raise ValueError("Événement sonore hors du montage.")
        clip = decode(path(event["file"]), event["duration"], event.get("in", 0))
        if len(clip) == 0:
            raise ValueError("Extrait de bruitage vide.")
        clip = fade(clip, .002, .005) * 10 ** (event.get("gain_db", 0) / 20)
        at = round(event["at"] * SR)
        length = min(len(clip), count - at)
        effects[at:at + length] += clip[:length]
    save(ROOT / "work/effects.wav", effects)
    premix = ROOT / "work/premix.wav"
    save(premix, voice + music + effects)
    target, peak = audio.get("target_lufs", -14.5), audio.get("true_peak", -1.8)
    measurements = measure(premix, target, peak)
    fields = {"measured_I": "input_i", "measured_TP": "input_tp",
              "measured_LRA": "input_lra", "measured_thresh": "input_thresh",
              "offset": "target_offset"}
    parameters = ":".join(f"{k}={measurements[v]}" for k, v in fields.items())
    filters = f"loudnorm=I={target}:TP={peak}:LRA=8:{parameters}:linear=true:print_format=json"
    result = run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(premix), "-af", filters,
        "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s24le", str(ROOT / "work/final_mix.wav")])
    (ROOT / "work/audio_mix.log").write_bytes(result.stderr)
    (ROOT / "work/audio_measure.json").write_text(json.dumps({
        "source_voice": voice_measure, "premix": measurements,
        "master": measure(ROOT / "work/final_mix.wav", target, peak),
    }, indent=2))
    print(ROOT / "work/final_mix.wav")


def audit():
    measurements = measure(ROOT / "exports/final.mp4")
    (ROOT / "work/encoded_loudness.json").write_text(json.dumps(measurements, indent=2))
    print(json.dumps(measurements, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["inspect", "mix", "audit"])
    globals()[parser.parse_args().command]()
