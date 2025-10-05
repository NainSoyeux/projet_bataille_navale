from bateau import Bateau

class Grille:
    def __init__(self, L: int, C: int):
        
        """Initialise une grille de taille L x C remplie de '.'"""
        self.lignes = L
        self.colonnes = C
        self.grille = ['~' for _ in range(C*L)]
    
    def afficher(self):
        """Affiche la grille à l'écran"""
        for i in range(self.lignes):
            print(' '.join(self.grille[i*self.colonnes:(i+1)*self.colonnes]))

    def tirer(self, ligne: int, colonne: int, touche = 'x'):
        """Tire à la position (x, y) en marquant un 'x', 
        Attention : les lignes (resp colonnes) vont de 0 à L-1 (C-1)"""
        if 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes:
            self.grille[ligne * self.colonnes + colonne] = touche
        else:
            print("Coordonnées hors de la grille")
            
    def ajoute(self, bateau: Bateau):
        """Place un bateau si toutes ses positions tiennent dans la grille."""
        positions = bateau.positions
        for (i, j) in positions:
            if not (0 <= i < self.lignes and 0 <= j < self.colonnes):
                return  
        for (i, j) in positions:
            idx = i * self.colonnes + j
            self.grille[idx] = bateau.marque