# Placement des textes — Instagram Reels et TikTok

## Base commune en 1080 × 1920

Pour les textes de schéma, le kit utilise une **zone de travail prudente choisie pour Babayaga** :
`x = 90 à 850`, `y = 280 à 1240`. Elle laisse 90 px à gauche, 230 px à
droite, 280 px en haut et 680 px en bas. Son centre est x = 470 ;
ce n’est pas l’axe de centrage des sous-titres ni celui d’un groupe
d’illustrations centré sur la vidéo. Faire tenir les textes dans la zone
prudente en composant autour de x=540, plutôt qu’en décalant chaque libellé.
Ces valeurs ne constituent pas une spécification officielle universelle.

Les interfaces varient selon l’appareil, la longueur de la légende, les boutons,
les traductions et le format publicitaire. Les recommandations publicitaires
ci-dessous servent de repère prudent pour un montage organique commun aux deux
plateformes ; elles ne garantissent pas tous les états d’affichage. Une légende
développée ou des commentaires ouverts peuvent recouvrir la vidéo.

## Deux placements de sous-titres

Les deux profils ont le même axe horizontal **x = 540**, au centre de la vidéo.
Les rectangles ci-dessous sont des choix locaux de composition, pas des
garanties officielles de visibilité dans toutes les interfaces.

| Profil | Calque / texte utile | Centre du bloc | Zone locale de contrôle |
|---|---|---|---|
| Petits au centre, `small-center` | 640 / 600 px | (540, 1080) | x = 90–900 ; y = 280–1240 |
| Grands en bas, `large-bottom` | 760 / 720 px | (540, 1450) | x = 90–940 ; y = 280–1600 |

Le texte petit fait 44 px, minimum 40 px ; le grand fait 58 px, minimum 48 px.
Le bloc est centré selon les lettres et accents des deux graisses : ne pas
placer son bord supérieur au centre de l’image. Les limites gauche/droite du
calque restent symétriques par rapport à x = 540, même si la zone de contrôle
ne l’est pas.

Le profil bas répond au choix éditorial « grands en bas » : il ne respecte pas
le retrait inférieur publicitaire de 35 % cité plus bas. Pour une publicité
ou une interface avec légende/bouton couvrant cette zone, utiliser le profil
central ou adapter le placement au gabarit de destination. Ne pas présenter le
profil bas comme universellement sûr. Aucun déplacement automatique vers la
gauche pour le faire tenir.

- Si deux lignes ne suffisent pas au minimum prévu, scinder la phrase sur ses
  vrais temps de mots. Ne pas fabriquer des timings ni rapetisser indéfiniment.
- Réserver la largeur maximale Regular/Bold pour chaque mot. Conserver le
  même point de centrage pendant toute la vidéo. En mode `word`, le calque
  a une taille constante pour tout le profil, y compris entre groupes.
- Vérifier le **rectangle complet**, avec accents, ombre, fond et éventuel
  mouvement d’entrée ; une ancre à l’intérieur ne suffit pas.

## Composer avec le sujet

Éviter les yeux, la bouche et l’objet que le spectateur doit regarder. Le
placement des mots est fixe par défaut : adapter l’échelle et le cadrage des
illustrations ou de l’orateur. Le changement de position par groupe est réservé
à une demande explicite, pas à une correction automatique.
Le kit ne détecte pas les visages.

Les noms, chiffres, logos et autres textes indispensables des schémas suivent
la zone prudente x = 90–850, y = 280–1240.
Raccourcir un libellé, déplacer le nœud ou montrer le détail en gros plan si
nécessaire. Dans une photo, un graphique ou un document importé, recadrer le
contenu à lire à l’intérieur de la zone ; le contrôle du moteur ne détecte pas
ces textes. Les décors et traits de liaison peuvent dépasser.

Pour un schéma animé, contrôler les coordonnées **après** zoom et déplacement
de caméra. Une entrée/sortie peut traverser les marges, mais le temps où le texte
doit être lu doit montrer le libellé entier dans la zone. Garder assez de temps
pour le lire à taille téléphone ; éviter les libellés qui se chevauchent.

Les couvertures et vignettes de profil nécessitent une composition propre à
leur recadrage. Ne pas supposer que la zone du lecteur 9:16 protège une vignette.

## Contrôle dans le kit

```sh
python3 render.py preview --safe-zones --times 0.5 2.8 5.0
python3 render.py preview --times 0.5 2.8 5.0
```

Choisir les temps réels : accroche, groupe à deux lignes, mot le plus long,
chaque type de scène et étapes du déplacement des libellés. La version
`work/preview_safe.jpg` colore en rouge les marges du profil sélectionné et
trace son axe de centrage ; c’est un guide
de travail, pas une reproduction de l’interface. Il n’apparaît jamais dans
`render` ni dans le MP4 final.

Les anciens projets sans `caption_style` conservent leur zone historique,
leur centre x = 470 et leur haut y = 1060. Les migrer explicitement vers un
profil, en retirant les anciennes hauteurs systématiques si elles ne servent plus.

Le chargement du projet refuse les placements par groupe/scène quand
`caption_fixed` est actif, les groupes trop longs, les blocs de sous-titres
hors zone et un changement de position au milieu d’un groupe. `put_safe_text`
maintient les cartouches du kit dans la zone, après transformation de caméra
dans le parcours documentaire. Ces garde-fous ne détectent
pas les collisions avec les visages, les autres textes ou les textes intégrés
aux médias ; inspecter visuellement les aperçus et le MP4 final.

Vérifier aussi une image sans guide réduite à environ 360 × 640 : contraste
sur les plans clairs, lisibilité des gris, accents et séparation avec les
illustrations. Renforcer localement l’ombre ou le fond si nécessaire.

Si une prévisualisation privée dans les applications est disponible, vérifier
la vidéo avec la légende et les boutons prévus, sans publier. Pour une publicité,
un bouton d’action, un lien/ancrage ou une interface différente, consulter le
gabarit officiel correspondant et adapter la zone du projet. En l’absence
d’accès, signaler que la vérification utilise le guide local.

## Sources et portée

Consultées le 20 octobre 2026 :

- [TikTok — Auction In-Feed Ads](https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads),
  mis à jour en juin 2026 : la zone dépend du format, de la longueur de la
  légende et des éléments supplémentaires ; gabarits distincts avec ancrage,
  et différences possibles entre aperçu et affichage réel.
- [Guide Reels de Meta, copie du PDF, page 4](https://d3m889aznlr23d.cloudfront.net/img/events/458925814/assets/e042d2be.reels_ads_guide1.pdf) :
  éviter les éléments essentiels, textes et logos dans les 35 % inférieurs des
  publicités Reels. Cela représente 672 px sur une hauteur de 1920 px.
  Les autres marges du kit sont des choix de composition, pas des valeurs
  attribuées à ce document.

Reconsulter les sources quand la plateforme ou son interface change.
