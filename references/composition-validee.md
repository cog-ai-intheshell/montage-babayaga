# Compositions validées — Concept 18

La [planche V13](../assets/reference/concept-18-cartouches-unis.jpg) complète la
référence de mouvement Concept 30. Elle montre les choix finaux : cartouches
unis, mots seuls immobiles, grilles centrées et fenêtre orateur modérée.
Ces valeurs sont des **exemples pour ce rush**, à adapter au contenu et au visage.

## Axes et espaces libres

- Centrer les groupes d’illustrations et leurs titres sur **x = 540**. Ne pas
  confondre cet axe avec le milieu x = 470 de la zone prudente asymétrique.
  Faire tenir les textes utiles dans cette zone en réduisant l’étendue de la
  composition ; éviter de les décaler un par un par un clamp automatique.
- Pour une grille, partager colonnes, lignes et distances objet → libellé.
  Centrer le dessin visible, après retrait des marges transparentes, sur sa
  cellule. Centrer le texte selon les lettres, pas les métriques de la police.
- Garder des espaces libres entre cartes, titres, diagrammes et sous-titres.
  Contrôler **les bords complets**, y compris accents, arrondis et mouvements.
  Viser une respiration d’environ 24–40 px entre petits blocs voisins plutôt
  que de les coller ; ce repère n’est pas un minimum universel.
- Les sous-titres restent à **(540,1080)**. Adapter le haut de la composition
  et la fenêtre orateur, sans exception de position à chaque plan.
- Des éléments décoratifs peuvent dépasser la zone des textes ; les noms,
  rangs, logos et détails nécessaires à la compréhension doivent rester lisibles.

Exemples du dernier montage, en 1080 × 1920 :

| Élément | Placement observé |
|---|---|
| Grilles de quatre logos / types d’unités | colonnes x=370/710 ; rangées y=440/760 |
| Libellés sous ces objets | y de la cellule +132 ; mêmes lignes |
| Titre d’un schéma de stratégie | centre (540,350) |
| Cercle du schéma | limites x=250–830, y=445–970 |
| Noms au-dessus de la simulation | ligne centrée sur (540,350), hauteur 64 |
| Simulation horizontale | x=92, y=420, 896×560 ; ratio natif préservé |
| Séparation noms → simulation | 38 px à l’arrêt ; vérifier aussi les transitions |
| Podium de quatre places | groupe centré, limites x=211–869, bas vers y=946 |

Ces dimensions ne justifient ni de déformer une capture ni de recopier quatre
colonnes ou quatre rangs sur un sujet différent. Un podium sert un classement
énoncé ; placer les vrais logos sur les marches, conserver les couleurs des
marques et ne pas ajouter de scores supposés.

## Cartouches et logos

Cartouches : **#5D71FC uni**, texte blanc, arrondi discret, sans dégradé, contour
clair ni halo. La transparence des bords anticrénelés et un fondu d’entrée ne
constituent pas un dégradé de remplissage. `motion.label` conserve un padding
transparent pour stabiliser les dimensions ; `centered_text` centre les pixels
visibles. Réutiliser le même bleu pour les cartouches personnalisés, y compris
les petites étiquettes d’une capture. L’éclairage d’un podium en volume est un
choix distinct du fond d’un cartouche.

Employer les fichiers originaux des marques, pas un symbole générique ni un
logo redessiné. Préserver proportions, transparence et couleurs. Ne pas retinter
Claude, Gemini, ChatGPT ou Grok pour les faire entrer dans la palette du schéma.
Inspecter le résultat à taille téléphone et documenter la page officielle source.

## Tête détourée

### Option « tête hors cadre — orateur légèrement rehaussé »

Activer cette variante sur les passages illustrés lorsque l’utilisateur demande
« tête hors cadre », « me faire dépasser du cadre » ou un rendu comme la
[capture fournie](../assets/reference/orateur-tete-hors-cadre.png).
La capture sert de référence de composition : fenêtre arrondie en bas contenant
le décor d’origine, silhouette détourée au premier plan et haut de la tête qui
dépasse nettement son bord supérieur. Rehausser légèrement l’orateur pour dégager
le visage, en gardant une échelle modérée et de la place pour l’illustration.
Les logos, textes et commandes du lecteur visibles dans la capture ne font pas
partie de cette option.

Ce mode est l’un des [quatre choix de présence de l’orateur](presence-orateur.md).
Une fois choisi, il s’applique à **toutes** les animations de la même vidéo.
Il ne modifie pas les plans face caméra plein écran ni les B-roll personnels.
En révision, préserver le mode global déjà validé sauf demande de changement.

### Cadrage et rehausse

La V13 fournit un point de départ plus discret que la première fenêtre agrandie :

```json
{
  "x": 42, "width": 996,
  "background_top": 1320, "background_bottom": 1872,
  "foreground_top": 1090,
  "source_zoom": 1.02,
  "source_anchor_y": 780, "screen_anchor_y": 1425
}
```

Placer ces réglages dans `animation_host.popout`, avec
`animation_host.mode: "popout"` et `animation_host.alpha: "assets/host_alpha.mkv"`.
Ces ancres supposent une source portrait déjà cadrée en 1080×1920 ; elles ne
conviennent pas automatiquement à une autre personne ou un autre rush.
Préserver la visibilité du visage au-dessus de la zone basse, sans en faire
le plus grand objet au détriment de l’explication. Les interfaces Instagram
varient : vérifier avec un guide local et, si disponible, un aperçu privé réel.

Pour rehausser légèrement l’orateur, diminuer **`screen_anchor_y`** à partir du
cadrage adapté au rush, en conservant `source_zoom` et les limites de la fenêtre
(`x`, `width`, `background_top`, `background_bottom`). Le helper déplace ainsi
le RGB et le masque ensemble à échelle constante. Par exemple, une diminution
de 40 px est un premier essai à 1080×1920, à ajuster après aperçu ; ce n’est pas
un décalage obligatoire ni une valeur à cumuler à chaque révision.

Adapter `foreground_top` si nécessaire pour ne pas rogner les cheveux pendant
les mouvements. Garder un espace visible entre la tête, les illustrations et
les sous-titres, dont la position reste fixe. Si le visage les touche, réduire
la rehausse ou recomposer la fenêtre. Vérifier que la translation ne découvre
aucun bord vide du rush au bas du cadre. Ne pas déplacer uniquement un morceau
de tête : le raccord avec le cou et le buste doit rester continu.

### Masque et intégration

Le skill contient le modèle **RVM MobileNetV3 fp32 ONNX**, sa licence et sa
provenance dans `assets/matting`, ainsi que `scripts/matte_video.py`.
Aucun fichier technique d’un ancien montage n’est nécessaire.

Pour un nouveau projet :

```sh
/chemin/du/skill/.venv/bin/python /chemin/du/skill/scripts/new_project.py \
  --source "/chemin/rush.mp4" --output "/chemin/montage" --animation-host popout
/chemin/du/skill/.venv/bin/python /chemin/montage/matte_video.py \
  --project "/chemin/montage"
```

Le modèle et le script sont copiés dans le projet. Pour une révision existante,
appeler directement `scripts/matte_video.py --project /chemin/montage` depuis le
skill ; ajouter `animation_host` et reprendre l’intégration du starter sans écraser
le compositeur du projet. Les coordonnées données plus haut sont un point de
départ à adapter, pas un cadrage automatique.

Le script lit `source`, `source_in`, `duration`, `host_center` et `host_filter`
dans `edit.json`, conserve le même recadrage que `render.Reader`, puis infère un
masque 720×1280 sans étirer le rush. Le masque commence au **temps zéro de la
timeline**, même lorsque `source_in` est non nul. `MatteReader` le décode à sa
définition native par numéro d’image ; le rapport JSON adjacent vérifie que sa
fréquence, sa durée et son cadrage correspondent toujours au projet.

Le rendu applique le [mode global](presence-orateur.md) à toutes les animations,
y compris une scène personnalisée. Celle-ci fournit le fond et l’animation ;
elle ne dessine plus sa propre fenêtre orateur. Le helper `motion.popout_panel`
reste la primitive du mode tête hors cadre. Lors de l’intégration :

1. Calculer le masque avec le script fourni (états récurrents conservés entre
   les images). Inspecter cheveux, lunettes et mouvements. Garder sa licence et
   sa provenance dans le projet ; ne pas régénérer le visage.
2. Conserver même portion de rush, mêmes images et fréquence que la narration.
   Stocker l’alpha en niveaux de gris sans perte, par exemple FFV1/MKV ; ne pas
   passer ce masque dans le Reader portrait qui le recadre ou le déforme.
3. Décoder l’alpha dans sa définition native et le transmettre avec les réglages :

   ```python
   host.info['matte'] = alpha_frame  # PIL L, même instant que host
   host.info['popout'] = framing    # dictionnaire de cadrage ci-dessus, adapté
   motion.popout_panel(image, host)
   ```

4. Appliquer exactement la même transformation spatiale au RGB et au masque.
   Le décor est opaque sous son bord arrondi ; seule la silhouette dépasse.
   Une tête redimensionnée séparément produirait une couture visible au raccord.
5. Contrôler l’alignement au début, au milieu et à la fin. Le lecteur fourni
   sélectionne les images par index pour éviter l’arrondi des timestamps MKV.
   Si un ancien masque est réutilisé, vérifier son origine temporelle avant
   l’intégration ; ne pas lui appliquer deux fois `source_in`.

Avant l’export, contrôler un court aperçu en mouvement : contours des cheveux
et des lunettes stables, dépassement visible sans tête coupée, raccord invisible
au bord arrondi, absence de halo et de collision avec les mots. Comparer aussi
une image où la tête est à son point le plus haut avec la capture de référence.

Pour une simple révision de taille ou de placement avec le même rush, réutiliser
le masque existant ; ne pas relancer l’inférence. Garder le cadrage validé sur
tous les autres plans. Sans changement de durée, conserver l’audio validé sans
réencodage via `audio_copy_from`, ainsi que les temps et positions des sous-titres.

## Raccord avec un B-roll personnel

Choisir le plan où le lieu ou l’action est reconnaissable. Pour le MIT, la
signalétique visible dans le plan d’Augustin a été préférée à une image générique
du campus. Garder l’inscription lisible et ne pas l’utiliser pour affirmer plus
que le contexte raconté.

Couper sur le début de l’idée et revenir dans une respiration naturelle.
La fin du plan face caméra doit toucher le début du B-roll : pas de bref
retour à un zoom différent avant la coupe. Conserver la voix et ses temps,
sans fond noir de sous-titres sur ce plan ; une ombre légère des lettres suffit
si la lecture reste bonne. Ne pas déplacer les mots pour contourner le panneau :
adapter le recadrage ou le plan. La limite personnelle de 1,5 s reste applicable.
