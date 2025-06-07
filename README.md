# MedChess Python

Ce projet implémente un jeu inspiré des échecs sur une grille 7x6 avec des pièces personnalisées.
Un bot basé sur l'apprentissage par renforcement (DQN) est fourni pour affronter le joueur humain.
Le plateau débute avec, côté IA, deux rangées de pièces : des chevaliers encadrant un général, un château et un second général, puis une ligne d'épéistes. Le joueur dispose de la même formation en bas du plateau.
L'IA choisit au hasard une personnalité (Aggressive, Équilibré ou Défensif) qui oriente ses premiers coups grâce à de petites ouvertures prédéfinies.

## Système de points

L'évaluation de l'IA repose sur un système simple :

- un épéiste ou un chevalier vaut **1 point** lorsqu'il est capturé ;
- un général vaut **2,5 points** ;
- l'avancement d'un épéiste vers le château adverse rapporte **0,1 point** par case parcourue (et en perdre autant en reculant).

Ces valeurs permettent au bot de privilégier les échanges avantageux et de gagner de l'espace vers le château adverse.

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

Les pièces du joueur apparaissent en bleu dans l'interface, celles de l'adversaire en rouge pour mieux les distinguer.

## Entraînement du modèle

Un utilitaire permet d'entraîner le bot manuellement :

```bash
python -m medchess.train [-max SECONDES]
```

L'option `-max` limite la durée de l'apprentissage (30 secondes par défaut). Le modèle est sauvegardé dans `medchess/model.zip` et l'entraînement peut être repris en relançant la même commande.
