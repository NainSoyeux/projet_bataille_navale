import pytest
from grille import Grille
from bateau import Bateau

# ---------- Utilitaires locaux pour les attentes d'affichage ----------

def grille_str_attendue(L, C, marque=None):
    """
    Construit la chaîne attendue pour l'affichage d'une grille LxC.
    'marque' peut être un set de positions {(i, j)} à afficher en 'x'.
    """
    marque = marque or set()
    lignes = []
    for i in range(L):
        row = []
        for j in range(C):
            row.append('x' if (i, j) in marque else '~')
        lignes.append(' '.join(row))
    return '\n'.join(lignes) + '\n'  # print ajoute un \n par ligne

# ---------- Tests constructeur / état initial ----------

def test_init_dimensions_et_contenu_initial():
    g = Grille(3, 4)
    assert g.lignes == 3
    assert g.colonnes == 4
    # La grille interne contient L*C éléments, tous '~'
    assert isinstance(g.grille, list)
    assert len(g.grille) == 3 * 4
    assert set(g.grille) == {'~'}

# ---------- Tests d'affichage (capture stdout via capsys) ----------

def test_afficher_grille_vierge(capsys):
    g = Grille(2, 3)
    g.afficher()
    out = capsys.readouterr().out
    attendu = grille_str_attendue(2, 3)
    assert out == attendu

def test_afficher_apres_tir(capsys):
    g = Grille(2, 3)
    g.tirer(1, 2)  # position valide
    g.afficher()
    out = capsys.readouterr().out
    attendu = grille_str_attendue(2, 3, marque={(1, 2)})
    assert out == attendu

# ---------- Tests tirer : positions valides ----------

@pytest.mark.parametrize(
    "L,C,ligne,col",
    [
        (1, 1, 0, 0),
        (2, 3, 0, 1),
        (2, 3, 1, 2),
        (5, 8, 4, 7),
    ],
)
def test_tirer_valide_modifie_la_case(L, C, ligne, col):
    g = Grille(L, C)
    idx = ligne * C + col
    assert g.grille[idx] == '~'
    g.tirer(ligne, col)
    assert g.grille[idx] == 'x'

# ---------- Tests tirer : positions invalides (hors grille) ----------

@pytest.mark.parametrize(
    "L,C,ligne,col",
    [
        (2, 3, -1, 0),
        (2, 3, 2, 0),   # ligne hors borne sup
        (2, 3, 0, -1),
        (2, 3, 0, 3),   # colonne hors borne sup
    ],
)
def test_tirer_hors_grille_ne_modifie_rien_et_message(capsys, L, C, ligne, col):
    g = Grille(L, C)
    avant = g.grille.copy()
    g.tirer(ligne, col)
    # La grille ne change pas
    assert g.grille == avant
    # Un message d'erreur est affiché
    out = capsys.readouterr().out
    assert "Coordonnées hors de la grille" in out

# ---------- Test "scénario user story" minimal ----------

def test_scenario_plouf_affichage_avant_apres(capsys):
    """
    Reproduit l'esprit de la user story : afficher, tirer, ré-afficher.
    """
    L, C = 5, 8
    g = Grille(L, C)
    g.afficher()
    out1 = capsys.readouterr().out
    assert out1 == grille_str_attendue(L, C)

    # Tir valide puis nouvel affichage
    g.tirer(2, 3)
    g.afficher()
    out2 = capsys.readouterr().out
    assert out2 == grille_str_attendue(L, C, marque={(2, 3)})

def test_ajoute_horizontal_ok():
    g = Grille(2, 3)
    g.ajoute(Bateau(1, 0, longueur=2, vertical=False))
    attendu = ["~", "~", "~", "⛵", "⛵", "~"]
    assert g.grille == attendu

def test_ajoute_vertical_hors_grille():
    g = Grille(2, 3)
    avant = g.grille.copy()
    g.ajoute(Bateau(1, 0, longueur=2, vertical=True))
    assert g.grille == avant  

def test_ajoute_trop_long():
    g = Grille(2, 3)
    avant = g.grille.copy()
    g.ajoute(Bateau(1, 0, longueur=4, vertical=True))
    assert g.grille == avant  