from bateau import Bateau


class Grille:
    def __init__(self, L: int, C: int):
        """Initialise une grille de taille L x C remplie de '~'."""
        self.lignes = L
        self.colonnes = C
        self.grille = ["~" for _ in range(C * L)]
        self.bateaux: list[Bateau] = []
        self._occupation: dict[tuple[int, int], Bateau] = {}
        self._tir_effectues: set[tuple[int, int]] = set()
        self._marques_bateaux: set[str] = set()

    def est_dans_grille(self, ligne: int, colonne: int) -> bool:
        return 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes

    def afficher(self, reveler: bool = False):
        """Affiche la grille (les bateaux non coulés restent masqués)."""
        for i in range(self.lignes):
            cases = []
            for j in range(self.colonnes):
                idx = i * self.colonnes + j
                symbole = self.grille[idx]
                bateau = self._occupation.get((i, j))

                if reveler:
                    cases.append(bateau.marque if bateau else symbole)
                    continue

                if bateau and bateau._est_coule:
                    cases.append(bateau.marque)
                elif bateau and symbole == bateau.marque:
                    cases.append("~")
                else:
                    cases.append(symbole)
            print(" ".join(cases))

    def peut_placer(self, longueur: int, ligne: int, colonne: int, vertical: bool) -> bool:
        """True si un bateau de 'longueur' peut être placé ici sans chevauchement."""
        for offset in range(longueur):
            i = ligne + offset if vertical else ligne
            j = colonne if vertical else colonne + offset
            if not self.est_dans_grille(i, j):
                return False
            if self.grille[i * self.colonnes + j] != "~":
                return False
        return True

    def ajoute(self, bateau: Bateau) -> bool:
        """Place un bateau si toutes ses positions tiennent dans la grille et sont libres."""
        for (i, j) in bateau.positions:
            if not self.est_dans_grille(i, j):
                return False
            idx = i * self.colonnes + j
            if self.grille[idx] != "~":
                return False

        for (i, j) in bateau.positions:
            idx = i * self.colonnes + j
            self.grille[idx] = bateau.marque
            self._occupation[(i, j)] = bateau

        self.bateaux.append(bateau)
        self._marques_bateaux.add(bateau.marque)
        return True

    def tirer(self, ligne: int, colonne: int, touche: str | None = None):
        """Effectue un tir et retourne un tuple (etat, bateau)."""
        if not self.est_dans_grille(ligne, colonne):
            print("Coordonnées hors de la grille")
            return "hors", None

        pos = (ligne, colonne)
        if pos in self._tir_effectues:
            print("Vous avez déjà ciblé cette case.")
            return "deja", self._occupation.get(pos)

        self._tir_effectues.add(pos)
        idx = ligne * self.colonnes + colonne
        bateau = self._occupation.get(pos)

        if bateau:
            symbole = touche if touche is not None else "💣"
            self.grille[idx] = symbole
            if bateau.coule(self):
                self.devoiler_bateau(bateau)
                return "coule", bateau
            return "touche", bateau

        symbole = touche if touche is not None else "x"
        self.grille[idx] = symbole
        return "manque", None

    def devoiler_bateau(self, bateau: Bateau):
        """Affiche définitivement le bateau sur la grille."""
        for (i, j) in bateau.positions:
            idx = i * self.colonnes + j
            self.grille[idx] = bateau.marque
