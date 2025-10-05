import random

from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from grille import Grille


def placements_possibles(grille: Grille, longueur: int):
    """Calcule toutes les positions/ orientations valides pour un bateau."""
    placements = []
    for vertical in (False, True):
        for ligne in range(grille.lignes):
            for colonne in range(grille.colonnes):
                if grille.peut_placer(longueur, ligne, colonne, vertical):
                    placements.append((ligne, colonne, vertical))
    return placements


def placer_flotte(grille: Grille):
    """Place un exemplaire de chaque type de bateau sans chevauchement."""
    flotte = []

    for bateau_cls in (PorteAvion, Croiseur, Torpilleur, SousMarin):
        longueur = bateau_cls.LONGUEUR
        placements = placements_possibles(grille, longueur)
        if not placements:
            raise RuntimeError(f"Impossible de placer {bateau_cls.__name__} sur la grille.")
        ligne, colonne, vertical = random.choice(placements)
        bateau = bateau_cls(ligne, colonne, vertical=vertical)
        grille.ajoute(bateau)
        flotte.append(bateau)

    return flotte


def demander_coordonnees(grille: Grille):
    """Demande à l'utilisateur une coordonnée valide."""
    while True:
        saisie = input("Tir (ligne colonne) : ").strip()
        try:
            ligne_str, colonne_str = saisie.split()
            ligne, colonne = int(ligne_str), int(colonne_str)
        except ValueError:
            print("Entrée invalide, merci de fournir deux entiers séparés par un espace.")
            continue

        if grille.est_dans_grille(ligne, colonne):
            return ligne, colonne
        print("Coordonnées hors de la grille, recommencez.")


def partie():
    grille = Grille(8, 10)
    flotte = placer_flotte(grille)
    coups = 0

    print("=== Bataille navale ===")
    print("Objectif : coulez les 4 bateaux le plus vite possible !")

    while any(not bateau._est_coule for bateau in flotte):
        print()
        grille.afficher()
        ligne, colonne = demander_coordonnees(grille)
        etat, bateau = grille.tirer(ligne, colonne)

        if etat == "hors":
            continue
        if etat == "deja":
            continue

        coups += 1

        match etat:
            case "manque":
                print("Plouf ! Rien ici.")
            case "touche":
                print("Touché ! Continuez comme ça.")
            case "coule":
                print("Touché-coulé !")
                print(bateau.message_coule)

    print()
    print(f"Victoire ! Tous les navires ont été détruits en {coups} coups.")
    print("Disposition finale :")
    grille.afficher(reveler=True)


if __name__ == "__main__":
    partie()
