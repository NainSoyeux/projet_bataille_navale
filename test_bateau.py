import inspect
import pytest
from bateau import Bateau

# ---------- Tests sur le constructeur ----------

def test_signature_constructeur():
    sig = inspect.signature(Bateau.__init__)
    params = sig.parameters
    # ordre attendu : (self), ligne, colonne, longueur=1, vertical=False
    names = list(params.keys())
    assert names[:4] == ["self", "ligne", "colonne", "longueur"]
    assert names[4] == "vertical"

    # pas de valeur par défaut pour ligne/colonne
    assert params["ligne"].default is inspect._empty
    assert params["colonne"].default is inspect._empty

    # valeurs par défaut pour longueur/vertical
    assert params["longueur"].default == 1
    assert params["vertical"].default is False

def test_constructeur_valeurs_par_defaut():
    b = Bateau(2, 3)
    assert b.ligne == 2
    assert b.colonne == 3
    assert b.longueur == 1
    assert b.vertical is False

def test_constructeur_valeurs_personnalisees():
    b = Bateau(1, 4, longueur=3, vertical=True)
    assert b.ligne == 1
    assert b.colonne == 4
    assert b.longueur == 3
    assert b.vertical is True

# ---------- Tests sur positions (property) ----------

def test_positions_horizontal_longueur3():
    b = Bateau(2, 3, longueur=3)
    assert b.positions == [(2, 3), (2, 4), (2, 5)]

def test_positions_vertical_longueur3():
    b = Bateau(2, 3, longueur=3, vertical=True)
    assert b.positions == [(2, 3), (3, 3), (4, 3)]

@pytest.mark.parametrize(
    "ligne,col,longueur,vertical,attendu",
    [
        (0, 0, 1, False, [(0, 0)]),
        (0, 0, 1, True,  [(0, 0)]),
        (5, 7, 2, False, [(5, 7), (5, 8)]),
        (5, 7, 2, True,  [(5, 7), (6, 7)]),
    ],
)
def test_positions_parametrise(ligne, col, longueur, vertical, attendu):
    b = Bateau(ligne, col, longueur=longueur, vertical=vertical)
    assert b.positions == attendu

def test_positions_ordre_croissant():
    # horizontal -> colonnes croissantes
    b_h = Bateau(3, 2, longueur=4)
    lignes = [l for (l, c) in b_h.positions]
    cols   = [c for (l, c) in b_h.positions]
    assert lignes == [3, 3, 3, 3]
    assert cols == sorted(cols)

    # vertical -> lignes croissantes
    b_v = Bateau(1, 5, longueur=4, vertical=True)
    lignes = [l for (l, c) in b_v.positions]
    cols   = [c for (l, c) in b_v.positions]
    assert cols == [5, 5, 5, 5]
    assert lignes == sorted(lignes)

def test_positions_reagit_aux_changements_attributs():
    b = Bateau(2, 3, longueur=2)  # [(2,3),(2,4)]
    assert b.positions == [(2, 3), (2, 4)]

    # On modifie l'orientation et la longueur, positions doit suivre
    b.vertical = True
    b.longueur = 3
    # attendu : [(2,3),(3,3),(4,3)]
    assert b.positions == [(2, 3), (3, 3), (4, 3)]
