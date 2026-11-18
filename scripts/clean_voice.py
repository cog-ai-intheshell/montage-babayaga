#!/usr/bin/env python3
"""Attenuate mouth clicks on an isolated voice WAV; never process the full mix."""
from pathlib import Path
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--wet', type=float, default=.9)
    parser.add_argument('--threshold', type=float, default=1.8)
    args = parser.parse_args()
    if not 0 <= args.wet <= 1 or not 1 <= args.threshold <= 100:
        parser.error('wet doit être entre 0 et 1 ; threshold entre 1 et 100.')
    if args.output.exists() or args.input.resolve() == args.output.resolve():
        parser.error('Choisir une nouvelle sortie pour préserver l’original.')
    if args.output.suffix.lower() != '.wav':
        parser.error('La voix traitée doit être conservée en WAV sans perte.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    graph = (f'[0:a]asplit[dry][wet];[wet]adeclick=w=55:o=75:a=2:t={args.threshold}'
             f':b=2.5:m=s[clean];[dry][clean]amix=inputs=2:weights={1-args.wet} {args.wet}'
             ':normalize=0:duration=first[out]')
    subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(args.input),
                    '-filter_complex', graph, '-map', '[out]', '-c:a', 'pcm_f32le',
                    str(args.output)], check=True)
    print(args.output)


if __name__ == '__main__':
    main()
