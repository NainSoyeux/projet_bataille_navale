# 🛳️ Bataille Navale (version 1 joueur)

Projet Python collaboratif visant à implémenter une version simplifiée du jeu de **Bataille Navale**.  
L'objectif n’est pas de coder une partie à deux joueurs, mais de développer une **interface de jeu pour un seul joueur**, avec une grille et des bateaux à placer/tirer dessus.

---

## 🎯 Fonctionnalités attendues

- **Grille de jeu**
  - Définie par `C` colonnes et `L` lignes.
  - Affichage de la grille à tout moment.
  - Possibilité de tirer sur une case.

- **Gestion des bateaux**
  - Chaque bateau a une longueur.
  - Placement possible **horizontalement ou verticalement**.
  - Les bateaux ne peuvent :
    - pas dépasser de la grille,
    - pas se chevaucher.

- **État des cases**
  - `vierge` : case vide et non frappée,
  - `frappée` : case ciblée par un tir.

- **État des bateaux**
  - Détection lorsqu’un bateau est **touché** (et où).
  - Détection lorsqu’un bateau est **coulé**.

---

## 🛠️ Technologies utilisées
- **Langage :** Python 3.x
- **Gestion de version :** Git / GitHub

---

## 🚀 Installation & exécution

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton-compte/bataille-navale.git
   cd bataille-navale
