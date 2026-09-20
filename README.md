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
| `Q` / `D` ou flèches | Se déplacer |
| `Espace` | Sauter |
| `A` | Attirer à gauche |
| `Z` | Repousser à gauche |
| `O` | Attirer à droite |
| `P` | Repousser à droite |
| `E` | Activer le générateur |
| `R` | Recommencer |

Le but du premier niveau est de récupérer deux cellules d'énergie, puis d'activer la machine située à la fin du parcours.

## Tests

```bash
python -m unittest discover -s tests
```
