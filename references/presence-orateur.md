# Présence de l’orateur pendant les animations

Choisir **un seul mode pour toute la vidéo**. Le conserver sur chaque animation,
schéma, illustration et simulation, y compris les scènes personnalisées. Les
plans face caméra plein écran et les B-roll restent des types de plans distincts.
Une entrée ou une sortie animée ne doit pas servir à alterner entre ces modes.

| Choix utilisateur | Réglage | Résultat |
|---|---|---|
| Ne pas apparaître | `hidden` | Animation seule, avec la voix et les sous-titres ; aucun orateur incrusté. |
| Haut détouré | `popout` | Fenêtre arrondie avec décor d’origine ; tête détourée dépassant son bord supérieur, orateur légèrement rehaussé. |
| Incrustation normale | `inset` | Vidéo de l’orateur entièrement contenue dans une fenêtre arrondie, décor d’origine conservé ; aucun dépassement. |
| Simulation derrière soi | `behind` | Silhouette entière détourée au premier plan, sans fenêtre ; animation derrière elle. |

Le dernier mode suit la [capture fournie](../assets/reference/simulation-derriere-orateur.png)
pour l’ordre des calques et l’effet de profondeur. Ne pas reprendre les textes,
la typographie, les miniatures ni l’interface du téléphone de cette capture.
Le starter remplace le décor d’origine par le fond graphique Babayaga.

Reprendre le choix demandé ou déjà validé dans la vidéo. Pour un nouveau montage
sans préférence, le générateur utilise `inset` ; annoncer le choix retenu avant
le rendu. Ne pas demander à nouveau un mode déjà précisé dans la conversation.
Une demande ultérieure de changement de mode porte sur toutes les animations
de cette vidéo, sauf nouvelle consigne explicite de l’utilisateur.

## Réglage global et commandes

```sh
/chemin/du/skill/.venv/bin/python /chemin/du/skill/scripts/new_project.py \
  --source "/chemin/rush.mp4" --output "/chemin/montage" \
  --animation-host behind
```

`--animation-host` accepte `hidden`, `popout`, `inset` et `behind`.
`--host-popout` reste un alias de `--animation-host popout`.
Les modes `popout` et `behind` copient le modèle et le script de détourage.
Calculer ensuite le masque avec `matte_video.py --project /chemin/montage` en
utilisant le Python du skill ; voir [le protocole du masque](composition-validee.md#masque-et-intégration).
`hidden` et `inset` ne demandent aucun masque.

Le choix se trouve **uniquement à la racine d’`edit.json`** :

```json
{
  "animation_host": {
    "mode": "behind",
    "alpha": "assets/host_alpha.mkv",
    "behind": {"scale": 1.0, "x": 0, "y": 0}
  }
}
```

Le générateur fournit aussi `animation_host.inset` pour la fenêtre simple et
`animation_host.popout` pour les ancres du mode tête hors cadre. Ajuster ces
paramètres sur le rush et garder le même cadrage de référence pendant les
animations du film. En `behind`, `x` et `y` désignent le coin supérieur gauche
du rush redimensionné ; le RGB et son alpha subissent la même transformation.

## Composition et vérification

Les fonctions de scène de `compose.py` dessinent **seulement le fond et les
animations**. `render.frame` applique ensuite `motion.animation_presenter` à
tout type de scène autre que `host` et `broll`, puis dessine les sous-titres.
Pour une nouvelle simulation, brancher son type au compositeur et à sa validation,
sans recréer une incrustation dans la fonction de scène.

En `behind`, l’ordre est : **fond → animation → silhouette → sous-titres**.
Le masque couvre toute la silhouette visible, cheveux et mains compris, sans
bord rectangulaire autour du corps. Contrôler aussi le microphone s’il chevauche
un élément animé. Recomposer les éléments importants pour que ni le visage,
ni le buste, ni les mains ne cachent un nom, une valeur ou l’action à comprendre.
Les sous-titres gardent leur position validée. Vérifier plusieurs instants en
mouvement ; un dessin lisible sur une seule image ne suffit pas.

En `hidden`, employer l’espace libéré pour l’animation si cela améliore la
lecture. En `inset` et `popout`, réserver la zone basse à la fenêtre. Pour le
dépassement de tête et sa rehausse, suivre [les réglages existants](composition-validee.md#cadrage-et-rehausse).

Le moteur rejette les champs `animation_host`, `host_mode` ou `host_popout` placés
dans une scène. Pour reprendre un ancien projet, migrer le réglage global
`host_popout` vers `animation_host`, retirer les anciens appels d’incrustation
dans les scènes et leurs exceptions locales. Ne pas écraser le montage livré ;
créer une nouvelle version et préserver le son et les temps de sous-titres.
