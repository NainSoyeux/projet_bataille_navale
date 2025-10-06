import pytest

import tui


class DummyShip:
    marque = "X"

    def __init__(self, message="Coulé !", coule=False):
        self.message_coule = message
        self._est_coule = coule


class DummyGrid:
    lignes = 2
    colonnes = 2

    def __init__(self):
        self.grille = ["~", "~", "~", "~"]
        self._occupation = {}
        self._next = ("manque", None)

    def set_next(self, state, ship=None):
        self._next = (state, ship)

    def tirer(self, ligne, colonne):
        return self._next

    def peut_placer(self, *_):
        return True

    def ajoute(self, ship):
        pass


def make_app(grid=None, fleet=None):
    app = tui.BattleshipTUI()
    app.focus_input = lambda: None
    app.grille = grid or DummyGrid()
    app.flotte = fleet or [DummyShip(coule=False), DummyShip(coule=True)]
    app.coups = 0
    app.finished = False
    app.revealed = False
    app.clear_input()
    return app


def test_shot_input_field_calls_enter_handler():
    field = tui.ShotInputField(width=8)
    seen = []
    field.add_enter_handler(seen.append)
    field.handle_key("3")
    field.handle_key(" ")
    field.handle_key("5")
    field.handle_key(tui.ptg_keys.ENTER)
    assert seen == ["3 5"]


def test_clear_input_resets_field():
    app = make_app()
    field = app.input_field
    field.handle_key("1")
    field.handle_key(" ")
    field.handle_key("2")
    history = getattr(field, "history", None) or getattr(field, "_history", None)
    if isinstance(history, list):
        history.append("1 2")
        attr_name = "history" if hasattr(field, "history") else "_history"
        setattr(field, attr_name, history)
    if hasattr(field, "history_index"):
        field.history_index = 0
    elif hasattr(field, "_history_index"):
        field._history_index = 0

    app.clear_input()

    assert field.value == ""
    history = getattr(field, "history", None) or getattr(field, "_history", None)
    if isinstance(history, list):
        assert history == []
    index = getattr(field, "history_index", getattr(field, "_history_index", -1))
    assert index == -1
    assert (field.cursor.row, field.cursor.col) == (0, 0)


def test_process_shot_updates_state():
    grid = DummyGrid()
    ship = DummyShip(coule=False)
    grid.set_next("touche", ship)
    app = make_app(grid=grid, fleet=[ship])
    app._process_shot("0 1")
    assert app.coups == 1
    assert "Touché" in app.message_label.value


def test_process_shot_invalid_tokens():
    app = make_app()
    app._process_shot("1 x")
    assert "Entrée invalide" in app.message_label.value
    assert app.coups == 0


def test_process_shot_finishes_game():
    ship = DummyShip(coule=True)
    grid = DummyGrid()
    grid.set_next("coule", ship)
    app = make_app(grid=grid, fleet=[ship])
    app._process_shot("0 0")
    assert app.finished
    assert app.revealed
    assert "Victoire" in app.message_label.value


def test_reveal_grid_ends_game():
    app = make_app()
    app.reveal_grid()
    assert app.revealed
    assert app.finished
    assert "Grille révélée" in app.message_label.value


def test_reveal_grid_second_call():
    app = make_app()
    app.reveal_grid()
    app.message_label.value = ""
    app.reveal_grid()
    assert "déjà révélée" in app.message_label.value
