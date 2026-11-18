# Méthode sonore

## Voix

Mesurer et écouter les canaux avant de les sommer. Dans **Concept 30 seulement**,
le canal gauche contient la voix exploitable. Il a été recentré ; ce n’est pas
une règle « toujours prendre le gauche ». Choisir explicitement `voice_channel` :
`0`, `1` ou `mix`.

Repartir du rush ou d’une piste propre pour refaire un mix. Préréglage de départ :
coupe-bas vers 78 Hz, légère réduction à 270 Hz, présence modérée à 2,9 kHz,
compression douce 2:1, attaque 9 ms, relâchement 105 ms. Adapter au locuteur.
Ne pas appliquer automatiquement une forte réduction de bruit.

## Bruits de bouche

L’outil réutilisable est fourni dans **`scripts/clean_voice.py`**, et copié à la
racine des nouveaux projets. Il utilise le filtre `adeclick` de FFmpeg ; aucun
modèle ni environnement audio provenant d’un ancien montage n’est nécessaire.

```sh
python3 /chemin/du/skill/scripts/clean_voice.py \
  --input "/chemin/voix-isolee.wav" --output "/chemin/voix-nettoyee.wav" \
  --wet 0.9 --threshold 1.8
```

Ce script traite uniquement la voix isolée et préserve l’original. Il ne remixe
pas la musique et ne normalise pas le master. Réintégrer ensuite cette voix en
conservant les autres pistes d’une révision audio. Les réglages restent un point
de départ à contrôler, selon les précautions ci-dessous.


Intégrer leur contrôle à la préparation de la voix. Atténuer les claquements
et petits clics de salive gênants avec un traitement anti-clics ciblé, réglé
sur le rush ; préserver les consonnes, les attaques et les respirations naturelles.
Éviter de cumuler une forte réduction de bruit et une porte de bruit agressive.

Travailler sur le rush ou la piste de voix séparée, avant le mélange avec la
musique et les bruitages. Pour une révision, repartir de la voix avant nettoyage
plutôt que de cumuler les traitements sur le dernier mix encodé.

Point de départ utilisé sur **Concept 15 V2**, à adapter et non à appliquer
systématiquement à toute voix :

```text
adeclick=w=55:o=75:a=2:t=1.8:b=2.5:m=s
voix = 0.90 × voix_traitée + 0.10 × voix_originale
```

Le mode `m=s` conserve les échantillons non détectés ; une valeur `t` plus basse
rend la détection plus sensible. Les deux pistes du mélange doivent garder
la même fréquence, le même nombre d’échantillons et le même alignement.
Comparer à niveau égal ; si les consonnes deviennent molles ou si des artefacts
apparaissent, relever le seuil ou réduire la part traitée. Voir la
[documentation FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#adeclick).

**Révision limitée aux bruits de bouche** : conserver les pistes séparées de
musique et de bruitages ainsi que la chronologie. Remixer la voix nettoyée avec ces pistes,
normaliser puis réencoder l’AAC ; copier le flux vidéo sans réencodage et
conserver le SRT. Ne pas utiliser `audio_copy_from`, qui réintroduirait l’ancien
son. Livrer dans un nouveau dossier de version avec les paramètres du nettoyage.

Contrôler la durée, la synchronisation et les pics après encodage ; vérifier
l’identité du flux vidéo et du SRT lorsqu’ils doivent être conservés. Comparer
le timbre et les claquements à l’écoute sur plusieurs passages. Les mesures et
une transcription automatique ne remplacent pas cette écoute ; si elle est
impossible, consigner cette limite sans déclarer le son validé à l’oreille.

## Musique

« Le trésor » est la musique de la référence Concept 30 uniquement.
Pour un nouveau montage, suivre le choix de l’utilisateur ou comparer les
morceaux d’`environnement-montage/musique` selon le [protocole médias](medias.md).
L’extrait de référence commence à 59,8 s du morceau, révélation à 30,2 s du
montage : ces temps ne sont pas des réglages par défaut pour une autre vidéo.

Travailler en flottant avec environ 6 dB de marge **avant** l’égalisation.
L’ancienne chaîne avait saturé ; baisser le volume après saturation ne répare
pas le son. Alléger la zone de présence de la musique, fondre ses extrémités.

Point de départ de la référence : voix vers −16,4 LUFS, musique vers −24 LUFS
avant automation. Atténuer la musique sous la voix et préparer une révélation
avec une baisse brève. Ajuster selon l’écoute, pas uniquement les chiffres.

## Bruitages

Examiner les sons d’`environnement-montage/bruitage`, dont `bruitages.wav`
s’il est présent. Prélever les échantillons utiles, appliquer de petites rampes
aux extrémités et les caler sur les actions. Les sons du kit sont un complément.
Ne pas plaquer la piste entière d’un ancien montage sur une nouvelle chronologie.

Dans le fichier de Concept 30 : souffle 2,26–2,50 s ; clic 14,72–14,79 s.
Ces positions ne valent que pour ce fichier. Le kit accepte
`{at, file, in, duration, gain_db}`. Souffle pour déplacement, clic pour validation,
impact modéré pour révélation. Vérifier les attaques sous les consonnes.

## Finalisation

Cible habituelle : −14,5 LUFS intégrés, plafond −1,8 dBTP, AAC 320 kb/s, 48 kHz.
Normalisation en deux passes après le mix, mesure du MP4 encodé, écoute à faible
volume. Adapter à une éventuelle consigne précise de diffusion.

Pour une révision purement graphique, copier l’AAC validé via `audio_copy_from`.
Ne jamais utiliser cette option après une coupe ou un retiming.
