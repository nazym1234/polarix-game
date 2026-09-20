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

Les objets métalliques mobiles sont prioritaires : `A` ou `O` les attirent vers le robot, tandis que `Z` ou `P` les repoussent. Les lettres de gauche agissent sur l'objet situé à gauche et celles de droite sur celui situé à droite. Lorsqu'aucun objet mobile n'est à portée, les mêmes commandes permettent au robot de s'attirer vers une structure métallique fixe.

La première énigme consiste à pousser une poutre métallique dans le vide pour construire un pont.

## Tests

```bash
python -m unittest discover -s tests
```
