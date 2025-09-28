# User Story "Plouf dans l'eau" : Pouvoir gérer les tirs de l'adversaire

"""Actions :
créer une grille à 5 lignes et 8 colonnes
afficher la grille à l'écran
demande à l'utilisateur de rentrer deux coordonnées x et y
tier à l'endroit indiqué sur la grille
retour en 2 (sortir en apputant sur q)"""

from grille import Grille

def ask_int_or_quit(prompt, min_val, max_val):
    """
    Demande un entier dans [min_val, max_val].
    Retourne l'entier, ou None si l'utilisateur entre 'q' (ou vide).
    Boucle tant que l'entrée n'est pas valide.
    """
    while True:
        s = input(prompt).strip().lower()
        if s in ("q", "quit", ""):
            return None
        try:
            val = int(s)
        except ValueError:
            print("Veuillez entrer un nombre valide (ou 'q' pour quitter).")
            continue
        if not (min_val <= val <= max_val):
            print(f"Veuillez entrer un nombre entre {min_val} et {max_val}.")
            continue
        return val

grille=Grille(5,8)
grille.afficher()

while True:
    print("\n Nouveau tir")
    print('Tapez "q" pour quitter à tout moment. \n')
    x=ask_int_or_quit("Entrez la ligne (0-4) : ", 0, 4)
    if x is None:
        print("Fin de la partie")
        break
    y=ask_int_or_quit("Entrez la colonne (0-7) : ", 0, 7)
    if y is None:
        print("Fin de la partie")
        break
    grille.tirer(x,y)
    grille.afficher()