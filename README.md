# MedChess Python

Ce projet implémente un jeu inspiré des échecs sur une grille 7x6 avec des pièces personnalisées.
Un bot basé sur l'apprentissage par renforcement (DQN) est fourni pour affronter le joueur humain.
Le plateau débute avec, côté IA, deux rangées de pièces : des chevaliers encadrant un général, un château et un second général, puis une ligne d'épéistes. Le joueur dispose de la même formation en bas du plateau.
L'IA choisit au hasard une personnalité (Aggressive, Équilibré ou Défensif) qui oriente ses premiers coups grâce à de petites ouvertures prédéfinies.

## Installation

Installez les dépendances avec `pip` :

```bash
pip install -r requirements.txt
```

## Lancement d'une partie

```bash
python -m medchess.game [-power N] [-max SECONDES]
```
`power` contrôle la profondeur de recherche du bot (1 à 10) et `max` le temps de réflexion maximum en secondes (30 par défaut).

Le joueur humain dispose de 30 secondes pour saisir un coup sous la forme :

```
fr fc tr tc
```

Où `fr`/`fc` représentent la case de départ et `tr`/`tc` la case d'arrivée (indices de 0 à 5 pour les lignes et de 0 à 6 pour les colonnes).
Si le temps imparti est dépassé ou si un coup invalide est joué, la partie est perdue.

Le modèle du bot est entraîné automatiquement si aucun fichier `model.zip` n'est présent.

## Interface graphique

Une interface utilisant Tkinter permet de jouer de façon visuelle. Lancez-la avec :

```bash
python -m medchess.gui [-power N] [-max SECONDES]
```
Les mêmes options `power` et `max` sont disponibles pour ajuster la force du bot.
