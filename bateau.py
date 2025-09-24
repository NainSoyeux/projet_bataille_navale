class Bateau:
    def __init__(self, ligne, colonne, longueur=1, vertical=False):
        """
        Représente un bateau sur la grille.
        """
        self.ligne = ligne
        self.colonne = colonne
        self.longueur = longueur
        self.vertical = vertical

    def __repr__(self):
        """
        Retourne la commande de création du bateau.
        """
        orientation = "vertical" if self.vertical else "horizontal"
        return f"Bateau(ligne={self.ligne}, colonne={self.colonne}, longueur={self.longueur}, {orientation})"

    @property
    def positions(self):
        """
        Retourne la liste des cases occupées par le bateau.
        """
        if self.vertical:
            return [(self.ligne + i, self.colonne) for i in range(self.longueur)]
        else:
            return [(self.ligne, self.colonne + i) for i in range(self.longueur)]
