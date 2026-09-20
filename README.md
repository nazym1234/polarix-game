# Polarix

**Polarix** est un prototype de jeu de plateforme 2D développé en Python avec Pygame. Le joueur contrôle un petit robot capable d'attirer ou repousser indépendamment les éléments métalliques situés à sa gauche et à sa droite.

## Installation

```bash
python -m venv .venv
```

Sous Windows :

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Commandes

| Touche | Action |
|---|---|
| `A` / `D` ou flèches | Se déplacer sur QWERTY |
| `Q` / `D` | Alternative sur AZERTY |
| `Espace` | Sauter |
| `J` | Attirer l'objet situé à gauche |
| `K` | Repousser l'objet situé à gauche |
| `O` | Attirer à droite |
| `P` | Repousser à droite |
| `E` | Activer le générateur |
| `R` | Recommencer |

Le but du premier niveau est de récupérer deux cellules d'énergie, puis d'activer la machine située à la fin du parcours.

Tous les éléments métalliques visibles peuvent être déplacés. `J/K` contrôlent l'objet situé à gauche et `O/P` celui situé à droite. Ils restent en place jusqu'à leur première manipulation, puis réagissent à la gravité et aux collisions.

La première énigme consiste à pousser une poutre métallique dans le vide pour construire un pont.

## Tests

```bash
python -m unittest discover -s tests
```
