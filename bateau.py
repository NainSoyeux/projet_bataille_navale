class Bateau:
    LONGUEUR = 1
    MARQUE = "⛵"
    MESSAGE_COULE = "Un bateau a coulé !"

    def __init__(self, ligne, colonne, longueur=1, vertical=False, marque=None):
        """Représente un bateau sur la grille."""
        self.ligne = ligne
        self.colonne = colonne
        self.longueur = longueur
        self.vertical = vertical
        self.marque = marque if marque is not None else self.MARQUE
        self.message_coule = getattr(self, "MESSAGE_COULE", "Un bateau a coulé !")
        self._est_coule = False

    @property
    def positions(self):
        """Retourne la liste des cases occupées par le bateau."""
        if self.vertical:
            return [(self.ligne + i, self.colonne) for i in range(self.longueur)]
        return [(self.ligne, self.colonne + i) for i in range(self.longueur)]

    def coule(self, grille):
        """True si toutes les cases du bateau ont été touchées."""
        if self._est_coule:
            return True

        for (i, j) in self.positions:
            etat = grille.grille[i * grille.colonnes + j]
            if etat in ("~", self.marque):
                return False

        self._est_coule = True
        return True


class PorteAvion(Bateau):
    LONGUEUR = 4
    MARQUE = "🚢"
    MESSAGE_COULE = "Porte-avion coulé !"

    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(
            ligne,
            colonne,
            longueur=self.LONGUEUR,
            vertical=vertical,
            marque=self.MARQUE,
        )


class Croiseur(Bateau):
    LONGUEUR = 3
    MARQUE = "⛴"
    MESSAGE_COULE = "Croiseur à pic !"

    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(
            ligne,
            colonne,
            longueur=self.LONGUEUR,
            vertical=vertical,
            marque=self.MARQUE,
        )


class Torpilleur(Bateau):
    LONGUEUR = 2
    MARQUE = "🚣"
    MESSAGE_COULE = "Torpilleur neutralisé !"

    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(
            ligne,
            colonne,
            longueur=self.LONGUEUR,
            vertical=vertical,
            marque=self.MARQUE,
        )


class SousMarin(Bateau):
    LONGUEUR = 2
    MARQUE = "🐟"
    MESSAGE_COULE = "Sous-marin éliminé !"

    def __init__(self, ligne, colonne, vertical=False):
        super().__init__(
            ligne,
            colonne,
            longueur=self.LONGUEUR,
            vertical=vertical,
            marque=self.MARQUE,
        )
