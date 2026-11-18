---
name: montage-babayaga
description: "Monter ou réviser des vidéos verticales parlées dans la DA Babayaga : animations explicatives, sous-titres mot par mot, mix sonore, B-roll, vraies captures et ressources d’environnement-montage. Utiliser pour le montage Babayaga sobre validé sur Concept 30 et affiné sur Concept 18 ; ne pas imposer cette DA à une autre marque."
---

# Montage Babayaga

Produire une vidéo finie, lisible sur téléphone, avec une narration forte et des
animations utiles. Garder la sobriété et les raccords de Concept 30, avec les
choix plus récents de Concept 18 : mots seuls fixes, cartouches unis et
compositions équilibrées. Une nouvelle consigne utilisateur prime sur ces défauts.

## Choix validés

- Vertical 9:16, 1080 × 1920, 30 i/s, H.264, AAC stéréo 48 kHz.
- Fond presque noir à points discrets ; bleu principal **#5D71FC**.
- Polices **Someone Extended Regular et Bold**. Sous-titre courant blanc
  **#FFFFFF**, gras. Aucun mot actif bleu.
- **Un seul mot à la fois** (`word`, défaut des nouveaux montages), aux vrais
  temps de la voix ; aucun cumul de mots ni reste de phrase gris. `group`
  reste disponible sur demande : mot actif blanc, autres mots **#A0A0A0**.
- **Centre identique pendant toute la vidéo**, sur tous les plans, y compris
  B-roll et schémas. Profil usuel `small-center` : **(540, 1080)** ; calque
  constant **640 × 88 px** en mode `word`. Centrer les lettres visibles,
  accents compris, sans saut entre les mots ni changement de position par scène.
  Recomposer les illustrations plutôt que déplacer les sous-titres.
- Le profil `large-bottom` reste disponible si demandé : centre **(540, 1450)**,
  calque de mots **760 × 102 px**. En révision, conserver le profil validé.
  Voir [les réglages du kit](references/kit.md#sous-titres).
- Cartouches de texte **bleu uni #5D71FC**, arrondis, texte blanc centré,
  **sans dégradé, halo ni contour clair**. Les réserver aux identifiants utiles.
  Ce choix concerne les cartouches, pas l’éclairage d’un objet en volume.
- Titres utiles, illustrations et grilles suivent un axe cohérent, généralement
  **x = 540**. Espacements réguliers et espace libre lisible entre cartouches,
  illustrations, sous-titres et tête. Contrôler les limites visibles et les
  transformations animées, pas seulement les centres des calques.
- **Aucun grand titre décoratif, aucune note en bas d’image.** Provenance et
  crédits dans `exports/credits.txt`.
- Employer les **vrais logos** pour identifier les marques. Pour un classement,
  préférer un podium avec logos si le propos s’y prête ; ne pas inventer les rangs.
- Accepter les B-roll plein écran ; pas de fond noir de sous-titres sur les
  plans personnels par défaut. Une ombre discrète des lettres peut aider.
- B-roll personnels d’Augustin : **1,5 s maximum par insertion** par défaut,
  sans juxtaposer ses plans pour prolonger la même séquence. Choisir le plan
  montrant le mieux le lieu ou l’action, puis soigner entrée et retour à la voix.
- **Un seul mode de présence de l’orateur pour toutes les animations d’une vidéo** :
  animation seule (`hidden`), tête hors cadre rehaussée (`popout`), incrustation
  classique (`inset`) ou silhouette détourée avec simulation derrière (`behind`).
  Conserver ce choix sur tous les schémas, illustrations et simulations ; ne pas
  alterner les modes selon les scènes. Suivre [les quatre modes et leurs références](references/presence-orateur.md).
  Préserver la place des animations, du visage et des sous-titres.
- Bruitages ponctuels sur les mouvements et musique sous la voix ; pas de clic
  à chaque mot. Préserver les versions livrées dans des dossiers distincts.
- Atténuer les bruits de bouche gênants (claquements, petits clics de salive)
  sur la voix isolée, en préservant les consonnes et le timbre naturel.
  Suivre [le traitement ciblé](references/audio.md#bruits-de-bouche).

## Point de départ

Lire [la DA](references/direction-artistique.md). Pour une composition avec
schémas, logos, podium ou tête détourée, lire
[les compositions validées](references/composition-validee.md) et regarder
[la planche récente](assets/reference/concept-18-cartouches-unis.jpg).
Pour le mouvement objet → schéma, conserver
[la référence Concept 30](assets/reference/concept-30-epure.jpg) et
[son raccord animé](assets/reference/transition-validee.mp4).
Les [chemins locaux](references/local-project.json) sont des repères facultatifs,
pas des dépendances ni des médias à réutiliser sur un autre sujet.

**Révision existante** : partir de la dernière version autorisée, inspecter le
code et ne changer que la demande. Une révision visuelle sans retiming conserve
la piste audio validée **sans réencodage** via `audio_copy_from`.

**Nouveau montage** : inspecter le rush et l’audio, puis créer un projet autonome :

```sh
python3 /chemin/du/skill/scripts/new_project.py \
  --source "/chemin/rush.mp4" --output "/chemin/montage" \
  --music "/chemin/musique.mp3" \
  --caption-style small-center --caption-mode word
```

Le générateur refuse un dossier existant et copie les polices, deux bruitages,
les modules de montage et `clean_voice.py`. `--captions` accepte une transcription
horodatée vérifiée ; sans elle, préparer les vrais temps avant le rendu.
Choisir **`--animation-host hidden|popout|inset|behind`** pour toute la vidéo
(`inset` par défaut). Les modes `popout` et `behind` copient le modèle RVM et son
script. `--host-popout` reste un alias du mode `popout`.
Le kit ne transcrit pas le rush et ne choisit pas l’histoire.

Les outils sont regroupés dans ce skill : modèle et licence dans
`assets/matting`, scripts dans `scripts`, dépendances dans `requirements.txt`.
Utiliser **`.venv/bin/python`** dans le dossier du skill ; si cet environnement
manque, lancer `python3 scripts/setup_runtime.py` une fois (accès aux paquets
Python nécessaire). Python 3.11+ et FFmpeg/ffprobe restent des prérequis système.
Voir [les commandes de détourage](references/composition-validee.md#masque-et-intégration).
Ne pas chercher les scripts, modèles ou environnements d’un ancien montage.

## Médias et composition

Pour un nouveau montage ou un enrichissement visuel, lire
[la sélection des médias](references/medias.md). Pour les illustrations, chercher
**d’abord des B-roll adaptés dans `B-roll Movies`, `B-roll` et `B-roll Augustin`**
d’`environnement-montage`, et visionner les candidats. Si aucun plan local ne
convient au passage, chercher un B-roll pertinent sur Internet et le télécharger.
**Tout B-roll retenu doit être présent dans `environnement-montage/B-roll`**,
y compris une copie des plans issus de `B-roll Movies` et de `B-roll Augustin` ;
conserver les originaux et copier aussi les plans dans les `assets` du montage.
Les photos, logos et animations complètent ce travail de recherche de B-roll.
Une correction de couleur, de placement, de sous-titres ou de son ne déclenche
pas une nouvelle recherche de médias. Respecter une consigne de travail hors ligne.

- Découper par idée : chaque insertion doit identifier, expliquer, montrer une
  action ou apporter une preuve pertinente. Garder la face caméra lorsqu’elle
  porte le propos ; peu d’éléments simultanés, mouvements lisibles.
- Quand du code est fourni, capturer **son véritable moteur ou interface** pour
  illustrer la simulation. Documenter les modes Mock et autres limites dans
  les crédits ; ne pas présenter ces captures comme les résultats exacts
  d’expériences absentes. L’accord pour des simulations suffit à les utiliser.
- Vérifier noms, chiffres, négations et conditionnels. Fixer les coupes avant
  de recaler mots, animations et son ; une coupe nécessite un recalage commun.
- Suivre [les recettes de mouvement](references/mouvement.md) et
  [les marges de travail](references/plateformes.md). Un raccord de B-roll ne
  doit pas introduire un bref retour à un autre zoom ou recadrage avant la coupe.
- Préparer le son selon [le protocole audio](references/audio.md), puis regarder
  et écouter un extrait à taille téléphone.

## Kit et contrôle

Lire [le mode d’emploi](references/kit.md) pour les scènes, les mots et le son.
`motion.py` fournit les cartouches unis, le centrage et la composition détourée ;
`compose.py` se réécrit pour le sujet ; `render.py` prévisualise, assemble et
vérifie ; `audio.py` inspecte et mixe. `scripts/matte_video.py` prépare le masque
temporel avec le modèle fourni, selon [la recette](references/composition-validee.md#tête-détourée).
Ne pas copier le sujet, le classement ni les timestamps d’une référence.

- Vérifier que le même mode orateur est appliqué à toutes les animations.
  Examiner plusieurs instants de chaque type de plan, y compris pendant les
  entrées, zooms et déplacements. Vérifier centrage, lignes de grille,
  dimensions des cartouches et respiration entre tous les blocs.
- Inspecter avec les marges locales, puis sans guide à taille téléphone.
  Les contrôles du kit ne détectent pas tous les chevauchements ni les textes
  déjà inscrits dans des images. Le guide n’est pas une garantie d’interface Instagram.
- Vérifier dans le **MP4 final** : mots fixes, marques lisibles, raccords,
  début et fin de phrases, cadrage du visage et durée des B-roll personnels.
- Décoder entièrement le MP4, contrôler format, fréquence, durée, flux et
  synchronisation ; mesurer le son après encodage et écouter le mix. Sur une
  révision visuelle, vérifier aussi l’identité de la piste AAC copiée.
- Livrer MP4, SRT adapté au mode choisi et crédits séparés. Garder sources et
  configuration. Ouvrir le MP4 dans Codex si disponible, avec un lien absolu.
  Ne jamais publier ou envoyer la vidéo sans demande.
