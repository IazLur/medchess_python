# MedChess Python

Ce projet implémente un jeu inspiré des échecs sur une grille 7x6 avec des pièces personnalisées.
Un bot basé sur l'apprentissage par renforcement (DQN) est fourni pour affronter le joueur humain.

## Installation

Installez les dépendances avec `pip` :

```bash
pip install -r requirements.txt
```

## Lancement d'une partie

```bash
python -m medchess.game
```

Le joueur humain dispose de 30 secondes pour saisir un coup sous la forme :

```
fr fc tr tc
```

Où `fr`/`fc` représentent la case de départ et `tr`/`tc` la case d'arrivée (indices de 0 à 5 pour les lignes et de 0 à 6 pour les colonnes).
Si le temps imparti est dépassé ou si un coup invalide est joué, la partie est perdue.

Le modèle du bot est entraîné automatiquement si aucun fichier `model.zip` n'est présent.
