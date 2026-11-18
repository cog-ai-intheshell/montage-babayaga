#!/usr/bin/env python3
"""Generate a timeline-aligned lossless RVM mask using a project's edit.json."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        import numpy as np
        import onnxruntime as ort
    except ImportError as error:
        parser.error(f'{error}. Exécuter scripts/setup_runtime.py puis utiliser .venv/bin/python.')
    project = args.project.expanduser().resolve(strict=True)
    config = json.loads((project / 'edit.json').read_text())
    if config['fps'] != 30 or config['size'] != [1080, 1920]:
        parser.error('Ce kit attend une timeline 1080×1920 à 30 i/s.')
    def resolve(value):
        p = Path(value).expanduser()
        return p if p.is_absolute() else project / p
    source = resolve(config['source'])
    presentation = config.get('animation_host', config.get('host_popout', {}))
    output = resolve(args.output or presentation.get('alpha', 'assets/host_alpha.mkv'))
    model = args.model or project / 'assets/matting/rvm_mobilenetv3_fp32.onnx'
    if not model.is_file() and args.model is None:
        model = Path(__file__).resolve().parents[1] / 'assets/matting/rvm_mobilenetv3_fp32.onnx'
    if not model.is_file():
        parser.error('Modèle absent du projet et du skill.')
    if output.suffix.lower() != '.mkv':
        parser.error('Utiliser .mkv pour le masque FFV1 sans perte.')
    if output.exists() and not args.overwrite:
        parser.error(f'Masque existant : {output}. Réutiliser ou demander --overwrite.')
    if output.resolve() in (source.resolve(), model.resolve()):
        parser.error('La sortie doit être distincte des sources.')
    width, height, fps = 720, 1280, 30
    count = round(config['duration'] * fps)
    if count <= 0:
        parser.error('Durée vide.')
    center = config.get('host_center', [.5, .5])
    # Match render.Reader before reducing resolution; never stretch a landscape rush.
    filters = ('scale=1080:1920:force_original_aspect_ratio=increase,'
               f'crop=1080:1920:(iw-ow)*{center[0]}:(ih-oh)*{center[1]}')
    if config.get('host_filter'):
        filters += ',' + config['host_filter']
    filters += f',fps=30,tpad=stop_mode=clone:stop_duration=0.05,scale={width}:{height}'
    options = ort.SessionOptions()
    options.intra_op_num_threads = 4
    options.inter_op_num_threads = 1
    options.enable_mem_pattern = False
    session = ort.InferenceSession(str(model), sess_options=options,
                                   providers=['CPUExecutionProvider'])
    recurrent = [np.zeros((1, 1, 1, 1), np.float32) for _ in range(4)]
    ratio = np.array([.375], np.float32)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.stem + '.partial.mkv')
    decoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-threads', '2', '-ss', str(config.get('source_in', 0)),
        '-i', str(source), '-an', '-vf', filters, '-frames:v', str(count),
        '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    encoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray',
        '-s', f'{width}x{height}', '-r', str(fps), '-i', '-', '-an', '-c:v', 'ffv1',
        '-level', '3', '-threads', '2', str(temporary)], stdin=subprocess.PIPE)
    started = time.monotonic()
    success = False
    try:
        for i in range(count):
            data = decoder.stdout.read(width * height * 3)
            if len(data) != width * height * 3:
                raise RuntimeError(f'Fin du rush à l’image {i}/{count}.')
            rgb = np.frombuffer(data, np.uint8).reshape(height, width, 3)
            src = rgb.transpose(2, 0, 1)[None].astype(np.float32) / 255
            alpha, *recurrent = session.run(['pha', 'r1o', 'r2o', 'r3o', 'r4o'], {
                'src': src, **{f'r{j + 1}i': r for j, r in enumerate(recurrent)},
                'downsample_ratio': ratio})
            mask = np.clip(alpha[0, 0] * 255 + .5, 0, 255).astype(np.uint8)
            encoder.stdin.write(mask.tobytes())
            if i % 120 == 0:
                print(f'Masque {i}/{count}', flush=True)
        decoder.stdout.close()
        if decoder.wait() != 0:
            raise RuntimeError('Décodage du rush échoué.')
        encoder.stdin.close()
        if encoder.wait() != 0:
            raise RuntimeError('Encodage du masque échoué.')
        temporary.replace(output)
        success = True
    finally:
        for process in (decoder, encoder):
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        if not success:
            temporary.unlink(missing_ok=True)
    report = {
        'model': 'RobustVideoMatting MobileNetV3 fp32 ONNX', 'license': 'GPL-3.0',
        'source_url': 'https://github.com/PeterL1n/RobustVideoMatting',
        'model_sha256': hashlib.sha256(model.read_bytes()).hexdigest(),
        'source': str(source), 'source_in': config.get('source_in', 0),
        'host_center': center, 'host_filter': config.get('host_filter', ''),
        'timeline_aligned': True, 'width': width, 'height': height, 'fps': fps,
        'frames': count, 'downsample_ratio': .375, 'recurrent_states_recycled': True,
        'elapsed_seconds': time.monotonic() - started,
    }
    output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    main()
