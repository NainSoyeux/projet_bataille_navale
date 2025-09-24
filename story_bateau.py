# User Story "chevauchement" : Positionner des bateaux sans chevauchement

from bateau import Bateau

def positions_communes(b1: Bateau, b2: Bateau):
    """Retourne l'ensemble des positions communes entre b1 et b2."""
    return set(b1.positions) & set(b2.positions)

def chevauchement(b1: Bateau, b2: Bateau) -> bool:
    """Retourne True si b1 et b2 partagent au moins une case."""
    return len(positions_communes(b1,b2)) > 0

def demo():
    print("=== Démo chevauchement de bateaux ===")

    # CAS 1 : chevauchement
    b1 = Bateau(2, 3, longueur=3)                 # [(2,3),(2,4),(2,5)]
    b2 = Bateau(1, 4, longueur=3, vertical=True)  # [(1,4),(2,4),(3,4)]
    chev1 = chevauchement(b1, b2)
    inter1 = positions_communes(b1, b2)
    print("\n-- Cas 1 : chevauchement attendu --")
    print(f"b1.positions = {b1.positions}")
    print(f"b2.positions = {b2.positions}")
    print(f"Chevauchent ? {chev1}")
    print(f"Positions communes : {sorted(inter1)}")
    assert chev1 is True
    assert (2, 4) in inter1

    # CAS 2 : pas de chevauchement
    b3 = Bateau(0, 0, longueur=2)                 # [(0,0),(0,1)]
    b4 = Bateau(3, 3, longueur=3, vertical=True)  # [(3,3),(4,3),(5,3)]
    chev2 = chevauchement(b3, b4)
    inter2 = positions_communes(b3, b4)
    print("\n-- Cas 2 : pas de chevauchement attendu --")
    print(f"b3.positions = {b3.positions}")
    print(f"b4.positions = {b4.positions}")
    print(f"Chevauchent ? {chev2}")
    print(f"Positions communes : {sorted(inter2)}")
    assert chev2 is False
    assert len(inter2) == 0

    print("\n✅ Démo terminée : comportements conformes à la user story.")

if __name__ == "__main__":
    demo()
