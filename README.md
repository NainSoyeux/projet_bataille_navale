# 🛳️ Bataille Navale (version 1 joueur)

Implémentation Python d’une bataille navale solo, jouable soit en console classique, soit via une interface PyTermGUI entièrement interactive. Le but est de couler la flotte générée aléatoirement en un minimum de tirs.

---

## 🎯 Fonctionnalités

- **Grille de jeu**
  - Format par défaut : 8 lignes × 10 colonnes.
  - Affichage console et TUI, avec options de révélation et disposition finale.
  - Validation des tirs (coordonnées dans la grille, case déjà ciblée, etc.).

- **Gestion des bateaux**
  - Porte-avions, croiseur, torpilleur, sous-marin (longueur spécifique, placement horizontal/vertical).
  - Placement aléatoire sans chevauchement, reproductible via une graine (`--seed`).

- **Retour d’état**
  - Messages distincts pour `manqué`, `touché`, `coulé`.
  - Suivi du nombre de coups et affichage de la flotte une fois la partie gagnée.
  - Dans la TUI : bouton « Révéler » disponible à tout moment (met fin à la partie).

---

## 🛠️ Technologies

- Python 3.11+
- PyTermGUI (TUI)
- Pytest (tests unitaires)

---

## 🚀 Installation & exécution

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/ton-compte/bataille-navale.git
   cd bataille-navale
   ```

2. Créer / activer un environnement virtuel :
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   .venv\Scripts\activate         # Windows
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancer le jeu :
   - **Mode console :**
     ```bash
     python main.py
     ```
   - **Mode TUI PyTermGUI :**
     ```bash
     python main.py --tui
     ```
   - (Optionnel) reproduire un placement :
     ```bash
     python main.py --seed 42
     ```

---

## ✅ Tests

Exécuter la suite Pytest :
```bash
pytest -q
```

---

Bon jeu ! 🎯
