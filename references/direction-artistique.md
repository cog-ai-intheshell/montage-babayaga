# DA et arbitrages éditoriaux

Référence de mouvement : `concept_30_epure.mp4`. Les choix visuels récents
de Concept 18 V13 priment pour les mots fixes, les cartouches et la composition ;
voir [la composition validée](composition-validee.md). La planche est conservée dans le
skill ; le dossier source est indiqué dans `local-project.json`.

## Valeurs à 1080 × 1920

| Élément | Valeur de départ |
|---|---|
| Fond | #05070B, halo bleu léger, points espacés d’environ 25 px |
| Couleur principale | #5D71FC |
| Texte actif | #FFFFFF, Someone Extended Bold |
| Texte inactif | #A0A0A0, Someone Extended Regular |
| Papier | #F4F5F9, filets gris et bleus |
| Sous-titres petits au centre | 44 px, minimum 40 px ; largeur utile 600 px ; deux lignes maximum |
| Sous-titres grands en bas | 58 px, minimum 48 px ; largeur utile 720 px ; deux lignes maximum |
| Alignement | Lettres visibles centrées ; calque constant pour les mots seuls |
| Position sous-titres | Centre réel x = 540 ; centre du bloc y = 1080 ou 1450 selon le profil |
| Zone des textes de schéma | x = 90–850, y = 280–1240 ; bloc entier, ombre comprise |
| Fenêtre orateur | Exemple récent : x 42, fond y 1320–1872, largeur 996, rayon 48 ; cadrage adapté au visage |
| Cartouche | Bleu uni #5D71FC, rayon 10, sans contour ni halo ; texte blanc centré |
| Libellé de schéma | 28–32 px au départ ; contrôler sa lisibilité après transformation |

Ces marges sont un choix prudent du kit, pas des dimensions officielles garanties.
Lire [les règles Reels/TikTok](plateformes.md) pour adapter la composition à
l’interface et au contenu. Ne jamais étirer un B-roll pour remplir le cadre.

## Sous-titres

Par défaut, afficher **un seul mot blanc et gras à la fois** (`word`), aux
vrais temps de la transcription. Conserver un centre unique sur toute la
vidéo : (540,1080), ou (540,1450) si le profil bas est demandé. En mode mot,
le calque reste de dimensions constantes (640×88 ou 760×102), même avec accents
et mots longs ; centrer le dessin des lettres et retirer leurs marges invisibles.
Aucun placement par groupe ou par scène par défaut. Si un mot couvre un objet
utile, recomposer le plan plutôt que déplacer les sous-titres.

`group` reste possible sur demande : mot actif blanc gras, autres gris, largeur
réservée selon les deux graisses. Ne pas changer de profil dans une révision
sans consigne. Les fonds noirs sur les B-roll personnels ne sont pas le défaut ;
privilégier une ombre discrète et un recadrage lisible. Aucun mot actif bleu.

La taille minimale est 40 ou 48 px selon le profil. Ne pas inventer des timings
ni changer la voix pour faire rentrer une phrase ; les intervalles de durée
nulle d’un alignement doivent être réexaminés à l’écoute, pas étirés arbitrairement.
Ne pas transformer « il aurait réussi » en affirmation.

## Libellé utile ou titre superflu

Garder ce qui lève une ambiguïté : nom sous une personne, nom de l’entreprise
dans le schéma de parts, « Pétrole » pour le contenu des citernes, « Parts » et
« Cession » pour les deux nœuds, graduation « > 100 m » pour une ligne de mesure.

Retirer le bandeau qui décrit seulement le thème : « Détournement présumé »,
« Associés », « Fortune », ou « 25 ans » au-dessus du sous-titre qui le dit déjà.
Les bandeaux de chapitre achat/revente ont également été retirés.
Un nom ou un rang utile doit rester aligné avec l’illustration qu’il identifie.
Les noms Chelsea/Eclipse restent comme identifiants des objets montrés ; ce
n’est pas une obligation de conserver toutes les étiquettes.

## Choix abandonnés

Ne pas réintroduire par défaut Copperplate, Dantes, #74A7FF, les mots actifs
bleus, les contours blancs, les grands titres ou les notes en bas de l’image.
Lorsqu’on reprend une animation ancienne, conserver la DA actuelle.
`exemple.mov` inspire la mise en mouvement, pas les couleurs ni le contenu.

Ne pas réintroduire les dégradés ou halos des anciens cartouches, les phrases
affichées par défaut, ni les déplacements de sous-titres entre schémas et B-roll.
