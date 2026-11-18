# Kit autonome

Prérequis système : Python 3.11+, FFmpeg et ffprobe. Les bibliothèques Python
(Pillow, NumPy, ONNX Runtime) sont installées dans `.venv` à l’intérieur du skill
par `python3 scripts/setup_runtime.py`, à partir de `requirements.txt`.
Utiliser ensuite `/chemin/du/skill/.venv/bin/python`. Ce montage n’utilise pas
l’environnement d’un autre projet et ne nécessite pas SciPy.

`new_project.py` produit un dossier avec les polices, les modules de montage et
`clean_voice.py`. **`--animation-host hidden|popout|inset|behind`** choisit un seul
mode pour toutes les animations du film. `popout` et `behind` copient aussi
`matte_video.py`, le modèle RVM, sa licence et sa provenance. Le rendu applique
le mode global après la composition des animations, avant les sous-titres.
Les fonctions de scène ne doivent donc plus dessiner elles-mêmes l’orateur.
Lire [les quatre modes](presence-orateur.md) pour les réglages et la migration
d’un ancien projet. `--host-popout` reste un alias de `--animation-host popout`.
Il stocke des chemins vers les rushes et la musique ; copier aussi les médias
et réécrire ces chemins pour déplacer le projet sur un autre ordinateur.
Le skill lui-même n’exige aucun ancien dossier `montage_30_*`.

## Edit.json

Les temps sont des secondes sur la **timeline de sortie**. `source_in` est le
début dans le rush. Le kit lit une portion continue ; pour des coupes, d’abord
préparer un rush assemblé et une transcription recalée, ou adapter le Reader
avec une vraie liste de montage. Ne pas décaler seulement les sous-titres.

`scenes` est une liste triée, sans chevauchement. Les trous montrent l’orateur.
Il n’y a ni pied de page ni champ de titre général.

```json
{
  "type": "broll", "start": 8.0, "end": 10.5,
  "path": "assets/plan.mp4", "in": 2.0, "center": [0.5, 0.5]
}
```

`path` peut être absolu ou relatif au nouveau projet. Les vidéos et images sont
recadrées, jamais étirées. Inspecter le sujet avant de choisir son centre.

```json
{
  "type": "document_chain", "start": 14.14, "end": 18.74,
  "stamp_at": 14.72, "shrink_at": 15.20,
  "second_at": 15.52, "last_at": 17.74,
  "document": {"title": "DOCUMENT", "subtitle": "D’EXPÉDITION", "stamp": "FAUX ?"},
  "nodes": [
    {},
    {"path": "assets/train.mp4", "in": 4.38, "label": "PÉTROLE"},
    {"type": "coins", "label": "REVENTE", "count": 5}
  ]
}
```

Exemple de Concept 30 uniquement, à **réécrire pour le prochain sujet**.
Le premier nœud est le papier qui se réduit ; les suivants peuvent être une
photo, un clip, des pièces ou une silhouette si aucun média n’est fourni.
Les points d’entrée des clips commencent au moment d’apparition du nœud.
La hauteur des sous-titres reste stable pendant ce raccord.

```json
{
  "type": "relation", "start": 21.56, "end": 23.26, "second_at": 22.20,
  "nodes": [
    {"path": "assets/personne.jpg", "label": "PERSONNE A", "width": 195, "height": 225},
    {"label": "PERSONNE B"}
  ]
}
```

Les paramètres des scènes restent dans `edit.json`. Ajouter à `compose.py`
une simulation spécifique si elle explique mieux le propos : onde de parts,
livre qui s’ouvre, comparaison, etc. Le kit ne préprogramme pas tous les sujets.

## Sous-titres

`captions.json` : liste de groupes sans chevauchement. Le découpage stocke les
temps ; en mode `word`, une seule unité est visible, indépendamment de la
longueur du groupe. En mode `group`, deux lignes maximum.
Le moteur choisit la graisse selon les vrais temps de mots ; il ne les estime pas.

Choisir le profil à la création avec `--caption-style`, ou dans `edit.json` :

```json
{"caption_style": "small-center", "caption_mode": "word", "caption_fixed": true}
```

| Profil | Taille nominale / minimum | Largeur utile | Centre du bloc |
|---|---|---|---|
| `small-center` — petits au centre | 44 / 40 px | 600 px | x = 540, y = 1080 |
| `large-bottom` — grands en bas | 58 / 48 px | 720 px | x = 540, y = 1450 |

Le petit profil est placé légèrement sous le milieu géométrique de l’image
pour dégager la bouche sur une face caméra. Le calque mesure respectivement
640 ou 760 px de large. Le moteur mesure les
limites des lettres, accents compris, dans les deux graisses. Il centre chaque
ligne sur x = 540 et le bloc entier sur son ancre verticale. Il réserve les
largeurs Regular/Bold et une enveloppe commune au groupe pour éviter que le texte
se déplace au changement de mot actif. Une ligne et deux lignes ont le même
centre vertical, pas le même bord supérieur.

Le profil choisi conserve la taille nominale autant que possible ; au-delà de
deux lignes au minimum prévu, scinder le groupe sur ses vrais temps de mots.
Ne pas forcer un seul mot trop large ni réduire indéfiniment.

Le mode d’apparition est indépendant du profil ; **`word` est le défaut**
des nouveaux projets :

- `group` : le groupe entier reste visible ; le mot courant passe en blanc
  gras, les autres mots sont gris.
- `word` : **seul le mot courant** apparaît, blanc gras et centré. Le mot
  suivant le remplace à son vrai instant de début ; le dernier disparaît à
  la fin du groupe. Aucun affichage avant le premier mot, aucun cumul progressif
  de la phrase. Les trous entre groupes restent vides.

Le SRT exporté suit le mode choisi : une entrée par groupe ou une entrée par
mot, avec les mêmes intervalles que l’image. Les deux modes utilisent le même
`captions.json` et la même narration. Dans
`word`, la taille est choisie pour le mot le plus long du groupe ; un calque
constant pour tout le profil (640×88 ou 760×102), et le centrage des pixels
visibles, évitent les sauts de position et de taille
à chaque activation. Un groupe long n’a pas à tenir entier dans le mode `word`,
mais chaque mot doit tenir seul à la taille minimale du profil.

Exemples à la création :

```sh
python3 scripts/new_project.py --source "/chemin/rush.mp4" --output "/chemin/petits-mots" --caption-style small-center --caption-mode word
python3 scripts/new_project.py --source "/chemin/rush.mp4" --output "/chemin/grandes-phrases" --caption-style large-bottom --caption-mode group
```

`caption_fixed: true` est écrit par le générateur. Le même centre s’applique
sur tous les plans, y compris les B-roll. Supprimer les anciens `y` des groupes
et `caption_y` des scènes : le chargement les refuse lorsque ce verrou est actif.
Recomposer les illustrations pour dégager le visage et les mots.

Les overrides historiques restent possibles pour une demande explicite de
placement variable, avec `caption_fixed: false` : `caption_y` définit le **haut**
du calque ; `y` du groupe prend le dessus. Ne pas employer cette compatibilité
pour réintroduire les déplacements de la version abandonnée. L’absence de
`caption_fixed` conserve le fonctionnement des anciens projets.

Sans `caption_style`, le kit garde le placement historique `legacy`
(58–48 px, x = 470, haut y = 1060) pour ne pas déplacer un ancien projet.
Les nouveaux projets utilisent `small-center`, `word` et `caption_fixed: true`.
Sans `caption_mode`, l’affichage reste en `group`.

Le contrôle emploie la [zone locale du profil](plateformes.md). Le profil
`large-bottom` descend plus bas que le guide prudent publicitaire ; vérifier
l’interface de destination si le montage comporte une légende ou un bouton bas.
Les schémas avec une fenêtre orateur en bas doivent être recomposés si ce
profil couvre le visage, sans déplacer les mots entre les plans.

```json
[
  {"start": 0.10, "end": 0.90, "words": [
    {"word": "Voici", "start": 0.10, "end": 0.35},
    {"word": "l’exemple.", "start": 0.35, "end": 0.75}
  ]}
]
```

Pour transcrire, réutiliser une transcription vérifiée ou un outil de
reconnaissance disponible. Vérifier à l’écoute noms, chiffres, négations,
conditionnels et temps ; ne pas inventer des timestamps à partir du nombre de
mots. `assets/reference/captions-concept-30.json` sert seulement de référence
de structure et de test local.

## Son

`audio.voice_channel` doit être choisi après inspection : 0, 1 ou `"mix"`.
`audio.music_in` se mesure dans la musique ; `music_automation` est une liste
`[temps_sortie, gain_en_dB]`. Les événements prennent les fichiers de bruitages :

Le projet reçoit `assets/sfx/tap.wav` et `assets/sfx/air.wav`, extraits du
`bruitages.wav` utilisé sur la série ; leur provenance est jointe. Ils peuvent
servir à un premier mix, avec `in: 0`, puis être remplacés ou enrichis.

```json
{"at": 14.72, "file": "assets/bruitages.wav", "in": 14.72, "duration": 0.07, "gain_db": -4}
```

L’exemple pointe vers un son précis de Concept 30 ; écouter un autre fichier
avant de reprendre ces temps. Les fondus très courts évitent les clics de coupe.

## Commandes dans le dossier créé

```sh
python3 audio.py inspect
python3 render.py preview --times 0.5 5.9 14.9 15.4 16.8 28.6
python3 render.py preview --safe-zones --times 0.5 5.9 14.9 15.4 16.8 28.6
python3 audio.py mix
python3 render.py render
python3 render.py finish
python3 render.py verify
python3 audio.py audit
```

`preview` et `render` exigent une vraie transcription ; le mix exige un canal
explicitement choisi. Renseigner les crédits des médias utilisés. Pour une
révision visuelle avec timeline identique, `audio_copy_from` peut désigner le
précédent MP4 : sa piste audio est copiée au moment de `finish`.

Les commandes réécrivent les fichiers de travail du **projet courant**.
Créer une nouvelle version avant d’écraser un export déjà validé.
Conserver les rendus de test dans un dossier séparé des livrables utilisateur.

## Cartouches et détourage

`motion.label` produit un cartouche bleu uni #5D71FC, sans dégradé ni halo ;
`motion.centered_text` centre les lettres visibles. Les cartouches personnalisés
utilisent le même remplissage plein, sans reprendre le dégradé d’une ancienne version.

`motion.popout_panel` fournit l’option **« tête hors cadre — orateur légèrement
rehaussé »** pour les passages illustrés. Une fois le cadrage adapté au rush,
diminuer `screen_anchor_y` remonte le RGB et son masque ensemble à échelle
constante ; garder le cadre arrondi fixe et vérifier les marges autour de la tête.
La fenêtre simple `panel` utilise par défaut x=42, y=1320, 996×552 ; adapter le
centre du recadrage au visage pour ne pas couper le front.
`motion.animation_presenter` sélectionne globalement animation seule, fenêtre
simple, tête hors cadre ou silhouette devant la simulation. Le dernier mode
utilise tout le masque et aucun cadre. Calculer le masque pour les deux modes
détourés, puis régler le cadrage sur le rush. Lire [les quatre modes](presence-orateur.md)
et [la recette de détourage](composition-validee.md#tête-détourée).
Le Reader vidéo ordinaire recadre au format portrait ; préparer un lecteur natif
pour une capture horizontale ou un masque, afin de conserver tout leur contenu.
Le B-roll accepte `shade: false` pour préserver sa luminosité, sans modifier la
position des mots. Le fond noir des mots n’est activé que par `backdrop` explicite.
