# Ressources et illustrations

## Repérer la bibliothèque

Chercher `environnement-montage` dans le dossier du rush, le projet courant et
leurs parents proches. Réutiliser le dossier existant ; éviter d’en créer un
second dans chaque révision. S’il n’existe pas, le créer à la racine du projet.

Inventorier les sous-dossiers présents, y compris les noms contenant des espaces.
Les ressources habituelles sont :

| Dossier | Usage |
|---|---|
| `B-roll` | Plans déjà collectés et copies des vidéos retenues |
| `B-roll Augustin` | Plans personnels ; 1,5 s maximum par insertion par défaut |
| `B-roll Movies` | Extraits de cinéma fournis, pour une illustration ou une métaphore pertinente |
| `colored`, `images-illustration` | Images existantes à examiner avant réutilisation |
| `musique` | Morceaux à comparer pour un nouveau montage ou un changement de musique |
| `bruitage` | Sons à prélever et caler sur une action précise |

Examiner les images et plusieurs instants des clips candidats. Ne pas choisir
un média uniquement d’après son nom. Les dossiers personnels et cinéma sont
des ressources locales : les inspecter avant de les chercher comme services Web.
Utiliser ces ressources lorsqu’elles servent le propos ; ne pas forcer leur
présence dans chaque vidéo.

## Chercher et choisir

Pour un nouveau montage ou un enrichissement visuel, relever les idées, objets,
personnes, lieux et actions à montrer. Pour chaque passage à illustrer :

1. **Chercher d’abord dans les trois bibliothèques locales** : `B-roll Movies`,
   `B-roll` et `B-roll Augustin`. Examiner plusieurs instants des candidats pour
   choisir ceux qui correspondent réellement au propos. Un inventaire de noms
   de fichiers ne remplace pas leur visionnage.
2. **Si aucun plan local ne convient, chercher sur Internet un B-roll ciblé,
   le télécharger et le visionner.** Une recherche de photos ou de logos seule
   ne remplit pas cette étape. Respecter une consigne de travail hors ligne ;
   si aucun téléchargement exploitable n’est possible, signaler cette limite.
3. **Dans tous les cas, ranger chaque B-roll retenu dans
   `environnement-montage/B-roll`**, puis en garder une copie dans les `assets`
   du montage. Cette règle inclut les plans de `B-roll Movies` et de
   `B-roll Augustin`, dont les originaux restent dans leur bibliothèque.

Les plans personnels d’Augustin suivent donc la même recherche de pertinence,
le même visionnage et le même rangement. Un plan générique trouvé sur Internet
ne doit pas être présenté comme un plan personnel d’Augustin.
Les images fixes, logos et animations peuvent compléter les B-roll ou expliquer
une idée, mais ne dispensent pas d’effectuer cette recherche de plans.
Aucun quota de téléchargements ou d’insertions n’est imposé.

- Chercher des actions précises : un document examiné, une interface utilisée,
  une tâche manuelle, une étape de fabrication. Éviter de couvrir tous les sujets
  par des personnes qui tapent sur un clavier.
- Pour identifier un rapport, un produit ou un lieu, privilégier le document,
  l’image ou la page officielle. Pour une ambiance ou un geste, une banque
  d’images et de vidéos réutilisables peut convenir.
- Comparer le contenu téléchargé à la page source : sujet, interface, date,
  auteur et conditions d’utilisation. Le titre d’un résultat peut être inexact.
  Préserver les noms, chiffres et éléments utiles d’un document recadré.
- Conserver la provenance et les conditions de réutilisation constatées.
  Une vidéo visible sur YouTube ou un extrait de cinéma n’est pas automatiquement
  libre de droits. Les extraits fournis dans `B-roll Movies` peuvent illustrer
  une idée ; les créditer comme fiction, sans prétendre montrer une situation réelle.
- Une image fixe convient si elle identifie ou explique mieux le passage.
  Employer un cadrage ou un mouvement discret ; ne pas inventer des éléments
  du document ni transformer une illustration en preuve.

Garder la face caméra aux passages où elle porte l’idée. Choisir les points
d’entrée et de sortie selon la phrase et l’action visible. Les plans personnels
d’Augustin restent brefs : viser environ 1 à 1,5 s, vérifier le plafond de 1,5 s
dans l’export, et intercaler d’autres images plutôt que d’enchaîner ses plans.
Adapter la durée des autres médias à leur lisibilité, sans leur imposer cette limite.

## Ranger et documenter

Créer uniquement les dossiers nécessaires :

- Tous les B-roll retenus, locaux ou téléchargés : `environnement-montage/B-roll`,
  y compris les copies provenant de `B-roll Movies` et de `B-roll Augustin`.
- Images d’illustration retenues : `environnement-montage/images-illustration`.
- Documents sources utilisés : `environnement-montage/documents`.
- Inventaire : réutiliser le manifeste existant du projet ; à défaut,
  `environnement-montage/sources/<concept>_<revision>.json`.

Conserver les originaux dans leur bibliothèque, notamment `B-roll Augustin`,
`B-roll Movies` et `colored`. Pour les vidéos, la copie dans le `B-roll` commun
est obligatoire même si le fichier a déjà été copié dans les `assets` du projet.
Si une copie identique existe déjà dans `B-roll`, la réutiliser. Pour les autres
médias, utiliser les dossiers ci-dessus et les `assets` du projet.
Ne pas dupliquer les mêmes téléchargements sous plusieurs noms ni écraser un
média d’une version livrée.
Nommer les fichiers avec le concept, le sujet et, si utile, l’auteur ou l’identifiant.

Pour chaque média utilisé, noter les chemins bibliothèque/projet, l’auteur,
l’URL source ou le chemin d’origine fourni, la licence constatée ou la provenance,
les adaptations, le point d’entrée et les passages dans la timeline.
Pour les B-roll, consigner les trois emplacements : original ou URL,
copie dans `B-roll`, copie dans les `assets`. Avant le rendu, vérifier que chaque
plan retenu existe dans `B-roll` et que son point d’entrée a été inspecté.
Distinguer original et dérivé pour un recadrage ou un insert animé.
Reporter les crédits et les liens dans `exports/credits.txt`, sans note sur la vidéo.
Ne pas annoncer un téléchargement, une licence ou une vérification non effectuée.

## Musique et bruitages

Pour un nouveau montage, comparer les morceaux disponibles dans `musique` et
choisir celui qui accompagne le propos et laisse la voix intelligible, sauf
choix explicite de l’utilisateur. Puis appliquer le [protocole audio](audio.md).
Utiliser les sons pertinents de `bruitage`, avec les extraits du kit en complément.
Sur une révision visuelle sans changement de durée, conserver la piste audio
existante sans réencodage au lieu de relancer un choix musical.

## Logos officiels et vraies simulations

Pour identifier une marque ou une IA, employer son vrai logo depuis son kit de
presse ou une ressource officielle. Conserver proportions, couleurs et alpha ;
choisir un fond qui préserve sa lisibilité. Ne pas remplacer les marques par le
même pictogramme recoloré ni par une génération approximative. Dans un classement,
réutiliser les logos sur un podium si cela clarifie les rangs racontés.

Quand l’utilisateur fournit du code, inspecter et exécuter son moteur pour les
captures utiles ; préserver le ratio de la simulation. Noter version, réglages,
mode des commandants et points d’entrée. Un mode Mock peut fournir une vraie
simulation du moteur sans constituer un test des modèles annoncés. Si l’utilisateur
accepte ces simulations, les incorporer comme illustrations, sans inventer les
replays ni attribuer au tournage des résultats d’expérience absents. Documenter
la distinction dans les crédits, sans ajouter une note décorative à l’image.

Pour un lieu personnel comme le MIT, préférer le plan fourni où Augustin et un
repère reconnaissable sont visibles ensemble. Évaluer le plan sur son contenu,
pas son nom ; limiter sa durée et vérifier les raccords selon
[la composition validée](composition-validee.md#raccord-avec-un-b-roll-personnel).
