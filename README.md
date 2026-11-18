# Montage Babayaga

Skill Codex de montage vidéo vertical Babayaga : animations, sous-titres mot par
mot, mix audio, réduction des bruits de bouche et détourage temporel.
Les instructions du skill sont dans [SKILL.md](SKILL.md).

## Installation

Prérequis : Python 3.11+, FFmpeg et ffprobe. L’accès à ce dépôt privé nécessite
un compte GitHub autorisé.

Sur une machine où le skill n’est pas encore installé :

```sh
gh repo clone cog-ai-intheshell/montage-babayaga ~/.codex/skills/montage-babayaga
cd ~/.codex/skills/montage-babayaga
python3 scripts/setup_runtime.py
```

L’environnement Python est créé dans `.venv`. Ses dépendances sont décrites dans
`requirements.txt` ; l’environnement et les caches ne sont pas versionnés.

## Créer un projet

Depuis le dossier du skill :

```sh
.venv/bin/python scripts/new_project.py \
  --source "/chemin/concept.mp4" --output "/chemin/montage" \
  --animation-host popout
.venv/bin/python /chemin/montage/matte_video.py --project /chemin/montage
```

Préparer ensuite la transcription horodatée et la composition du projet selon
[le mode d’emploi](references/kit.md). Le script ne choisit pas l’histoire et
ne transcrit pas le rush.

Un seul mode de présence s’applique à toutes les animations d’une vidéo :

| Mode | Présence de l’orateur |
|---|---|
| `hidden` | Animation seule |
| `popout` | Tête détourée dépassant du cadre |
| `inset` | Incrustation classique |
| `behind` | Silhouette détourée, simulation derrière |

Seuls `popout` et `behind` nécessitent le calcul du masque. Les réglages et
références sont dans [Présence de l’orateur](references/presence-orateur.md).

## Ressources incluses

- Scripts de création, détourage, nettoyage de voix et installation du runtime.
- Moteur de composition, sous-titrage, rendu et mix audio.
- Modèle RVM MobileNetV3 ONNX, [licence](assets/matting/LICENSE) et
  [provenance](assets/matting/provenance.json).
- Polices, bruitages et références visuelles du skill.

Les rushes, musiques et exports des projets restent dans leurs dossiers de
montage. `references/local-project.json` contient des repères locaux facultatifs ;
ils ne sont pas nécessaires à l’exécution des outils.
