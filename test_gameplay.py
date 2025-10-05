import builtins
from collections import Counter

import pytest

import main
from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from grille import Grille


def test_tirer_coule_devoile():
    g = Grille(4, 4)
    bateau = Torpilleur(1, 1, vertical=False)  # (1,1) et (1,2)
    assert g.ajoute(bateau)

    etat, cible = g.tirer(1, 1)
    assert etat == "touche"
    assert cible is bateau

    etat, cible = g.tirer(1, 2)
    assert etat == "coule"
    assert cible is bateau

    # Le bateau doit désormais être affiché sur toutes ses cases.
    for (i, j) in bateau.positions:
        idx = i * g.colonnes + j
        assert g.grille[idx] == bateau.marque


def test_tirer_deja_effectue():
    g = Grille(3, 3)
    bateau = SousMarin(0, 0, vertical=False)
    assert g.ajoute(bateau)

    etat, _ = g.tirer(0, 0)
    assert etat == "touche"

    etat, _ = g.tirer(0, 0)
    assert etat == "deja"


def test_placements_possibles():
    g = Grille(5, 5)
    options = main.placements_possibles(g, longueur=3)

    assert (0, 0, False) in options           # placement horizontal classique
    assert (0, 3, False) not in options        # dépassement à droite
    assert (2, 0, True) in options             # placement vertical
    assert (3, 0, False) in options            # encore de la place


def test_placer_flotte_sans_chevauchement(monkeypatch):
    # Choix déterministes pour chacune des 4 poses.
    queue = [
        (0, 0, False),  # Porte-avion
        (1, 0, False),  # Croiseur
        (2, 0, False),  # Torpilleur
        (3, 0, False),  # Sous-marin
    ]

    def fake_choice(options):
        decision = queue.pop(0)
        assert decision in options
        return decision

    monkeypatch.setattr(main.random, "choice", fake_choice)

    g = Grille(8, 10)
    flotte = main.placer_flotte(g)

    # Toutes les marques attendues sont présentes une seule fois.
    marques = Counter(b.marque for b in flotte)
    assert marques == Counter({"🚢": 1, "⛴": 1, "🚣": 1, "🐟": 1})

    # Vérifie l’absence de chevauchement.
    cases = set()
    for bateau in flotte:
        for pos in bateau.positions:
            assert pos not in cases
            cases.add(pos)


def test_partie_complete(monkeypatch, capsys):
    # Placements déterministes identiques au test précédent.
    queue = [
        (0, 0, False),
        (1, 0, False),
        (2, 0, False),
        (3, 0, False),
    ]

    def fake_choice(options):
        decision = queue.pop(0)
        assert decision in options
        return decision

    monkeypatch.setattr(main.random, "choice", fake_choice)

    # Séquence de tirs qui coule tous les navires (11 coups).
    tirs = iter(
        [
            "0 0",
            "0 1",
            "0 2",
            "0 3",  # porte-avion
            "1 0",
            "1 1",
            "1 2",  # croiseur
            "2 0",
            "2 1",  # torpilleur
            "3 0",
            "3 1",  # sous-marin
        ]
    )

    def fake_input(_prompt):
        return next(tirs)

    monkeypatch.setattr(builtins, "input", fake_input)

    main.partie()
    out = capsys.readouterr().out

    assert "Victoire !" in out
    assert "11 coups" in out
