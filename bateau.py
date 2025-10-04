class Bateau:
    def __init__(self, ligne, colonne, longueur=1, vertical=False):
        """
        Représente un bateau sur la grille.
        """
        self.ligne = ligne
        self.colonne = colonne
        self.longueur = longueur
        self.vertical = vertical

    @property
    def positions(self):
        """
        Retourne la liste des cases occupées par le bateau.
        """
        if self.vertical:
            return [(self.ligne + i, self.colonne) for i in range(self.longueur)]
        else:
            return [(self.ligne, self.colonne + i) for i in range(self.longueur)]
        
    def coule(self, grille):
        """True si toutes les cases du bateau sont ≠ '~'."""
        for (i, j) in self.positions:
            if grille.grille[i * grille.colonnes + j] in ("~","⛵"):
                return False
        return True