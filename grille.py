class Grille:
    def __init__(self, L: int, C: int):
        
        """Initialise une grille de taille L x C remplie de '.'"""
        self.lignes = L
        self.colonnes = C
        self.grille = ['.' for _ in range(C*L)]
    
    def afficher(self):
        """Affiche la grille à l'écran"""
        for i in range(self.lignes):
            print(' '.join(self.grille[i*self.colonnes:(i+1)*self.colonnes]))

    def tirer(self, ligne: int, colonne: int):
        """Tire à la position (x, y) en marquant un 'x', 
        Attention : les lignes (resp colonnes) vont de 0 à L-1 (C-1)"""
        if 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes:
            self.grille[ligne * self.colonnes + colonne] = 'x'
        else:
            print("Coordonnées hors de la grille")