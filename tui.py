import random
from collections.abc import Callable

import pytermgui as ptg
from pytermgui.input import keys as ptg_keys

from bateau import PorteAvion, Croiseur, Torpilleur, SousMarin
from grille import Grille

FLOTTE_TYPES = (PorteAvion, Croiseur, Torpilleur, SousMarin)
SHOT_FEEDBACK = {
    "manque": "[cyan]Plouf ! Rien ici.",
    "touche": "[green]Touché !",
    "coule": "[bold green]Touché-coulé ![/] {message}",
}
INVALID_FEEDBACK = {
    "hors": "[red]Coordonnées hors grille.",
    "deja": "[yellow]Case déjà ciblée.",
}


# ---------- Champ de saisie spécialisé ----------
class ShotInputField(ptg.InputField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enter_handlers: list[Callable[[str], None]] = []

    def add_enter_handler(self, handler: Callable[[str], None]) -> None:
        self._enter_handlers.append(handler)

    def handle_key(self, key: str) -> bool:
        if key == ptg_keys.ENTER:
            if self._enter_handlers:
                for handler in self._enter_handlers:
                    handler(self.value)
                return True
            submit = getattr(self, "submit_callback", None)
            if callable(submit):
                submit(self.value)
                return True
            handlers = getattr(self, "handlers", None)
            callback = handlers.get("submit") if isinstance(handlers, dict) else None
            if callable(callback):
                callback(self.value)
                return True

        handled = super().handle_key(key)

        if handled and key != ptg_keys.ENTER:
            try:
                self.move_cursor((0, len(self.value)), absolute=True)
            except TypeError:
                self.move_cursor((0, len(self.value)))
            if hasattr(self, "_selection_length"):
                self._selection_length = 1

        return handled


# ---------- Application TUI ----------
class BattleshipTUI:
    def __init__(self):
        self.manager = ptg.WindowManager()
        self.grid_label = ptg.Label("")
        self.coups_label = ptg.Label("Coups : 0")
        self.message_label = ptg.Label("Entrez un tir (ligne colonne).")
        self.input_field = ShotInputField(placeholder="ex: 3 5", width=12)
        self.fire_button = ptg.Button("Tirer", self.submit_from_button)
        self.reveal_button = ptg.Button("Révéler", self.reveal_grid)
        self.reset_button = ptg.Button("Nouvelle partie", self.reset_game)
        self.quit_button = ptg.Button("Quitter", lambda *_: self.manager.stop())
        self._register_submit(self.input_field, self.on_submit)

        self.grille: Grille | None = None
        self.flotte: list | None = None
        self.coups = 0
        self.finished = False
        self.revealed = False

        self.reset_game()

    # ---------- Cycle de vie ----------
    def run(self):
        with self.manager:
            self.manager.add(self._build_window())
            self.focus_input()

    def focus_input(self):
        focusers = (
            getattr(self.manager.layout, "focus", None),
            getattr(self.manager, "set_focus", None),
        )
        for focuser in focusers:
            if callable(focuser):
                try:
                    focuser(self.input_field)
                    break
                except Exception:
                    continue

    def clear_input(self):
        field = self.input_field

        setter = getattr(field, "set_value", None)
        if callable(setter):
            setter("")
        else:
            if hasattr(field, "_lines"):
                field._lines = [""]
                field._styled_cache = None

        for attr in ("history", "_history"):
            history = getattr(field, attr, None)
            if hasattr(history, "clear"):
                history.clear()
        for attr in ("history_index", "_history_index"):
            if hasattr(field, attr):
                setattr(field, attr, -1)

        if hasattr(field, "_selection_length"):
            field._selection_length = 1

        cursor = getattr(field, "cursor", None)
        if cursor is not None:
            cursor.row = 0
            cursor.col = 0

        mover = getattr(field, "move_cursor", None)
        if callable(mover):
            mover((0, 0), absolute=True)

        refresher = getattr(field, "refresh", None)
        if callable(refresher):
            refresher()

    # ---------- Gestion des callbacks ----------
    def _register_submit(self, widget: ptg.InputField, callback: Callable):
        enter_handler = getattr(widget, "add_enter_handler", None)
        if callable(enter_handler):
            enter_handler(callback)
            return
        set_handler = getattr(widget, "set_handler", None)
        if callable(set_handler):
            try:
                set_handler("submit", callback)
                return
            except Exception:
                pass
        handlers = getattr(widget, "handlers", None)
        if isinstance(handlers, dict):
            handlers["submit"] = callback
            return
        submit_attr = getattr(widget, "submit", None)
        if callable(submit_attr):
            widget.submit = callback
            return
        widget.submit_callback = callback

    def submit_from_button(self, *_):
        value = getattr(self.input_field, "value", "")
        self.on_submit(value)

    def on_submit(self, value=None, *_, **__):
        if value is None:
            value = getattr(self.input_field, "value", "")
        self._process_shot(str(value or ""))

    # --- Logique de jeu -------------------------------------------------------------
    def _process_shot(self, raw_value: str):
        if self.finished:
            if self.revealed and self.flotte and any(not ship._est_coule for ship in self.flotte):
                self.message_label.value = "[yellow]Grille révélée. Lancez une nouvelle partie pour rejouer."
            else:
                self.message_label.value = "[yellow]La partie est déjà terminée."
            self.clear_input()
            self.focus_input()
            return

        tokens = raw_value.replace(",", " ").split()
        if len(tokens) < 2:
            self.message_label.value = "[yellow]Entrez une coordonnée avant de valider."
            self.focus_input()
            return
        try:
            ligne, colonne = map(int, tokens[:2])
        except ValueError:
            self.message_label.value = "[red]Entrée invalide. Utilisez 'ligne colonne'."
            self.clear_input()
            self.focus_input()
            return

        etat, bateau = self.grille.tirer(ligne, colonne)
        if etat in INVALID_FEEDBACK:
            self.message_label.value = INVALID_FEEDBACK[etat]
            self.clear_input()
            self.focus_input()
            return

        self.coups += 1
        self.coups_label.value = f"Coups : {self.coups}"
        message = SHOT_FEEDBACK[etat]
        self.message_label.value = message.format(message=bateau.message_coule if etat == "coule" else "")
        self.update_grid()

        if all(bt._est_coule for bt in self.flotte):
            self.finished = True
            self.revealed = True
            self.update_grid()
            self.message_label.value = f"[bold green]Victoire ![/] Flotte détruite en {self.coups} coups."

        self.clear_input()
        self.focus_input()

    def reset_game(self, *_):
        self.grille = Grille(8, 10)
        self.flotte = self._placer_flotte(self.grille)
        self.coups = 0
        self.finished = False
        self.revealed = False
        self.coups_label.value = "Coups : 0"
        self.message_label.value = "Entrez un tir (ligne colonne)."
        self.update_grid()
        self.clear_input()
        self.focus_input()

    def reveal_grid(self, *_):
        if self.revealed:
            self.message_label.value = "[yellow]La grille est déjà révélée. Lancez une nouvelle partie pour rejouer."
            self.focus_input()
            return
        self.revealed = True
        self.finished = True
        self.update_grid()
        self.message_label.value = "[yellow]Grille révélée. Lancez une nouvelle partie pour rejouer."
        self.clear_input()
        self.focus_input()

    # ---------- Affichage ----------
    def update_grid(self):
        lignes = []
        for i in range(self.grille.lignes):
            cases = []
            for j in range(self.grille.colonnes):
                symbol = self.grille.grille[i * self.grille.colonnes + j]
                bateau = self.grille._occupation.get((i, j))
                visible = self.revealed or not bateau or bateau._est_coule or symbol != bateau.marque
                cases.append(self._pad(symbol if visible else "~"))
            lignes.append("".join(cases))
        self.grid_label.value = "\n".join(lignes)

    @staticmethod
    def _pad(symbol: str) -> str:
        return symbol if len(symbol) > 1 else f"{symbol} "

    # ---------- Placement de la flotte ----------
    @staticmethod
    def _placer_flotte(grille: Grille):
        flotte = []
        for bateau_cls in FLOTTE_TYPES:
            placements = BattleshipTUI._placements_possibles(grille, bateau_cls.LONGUEUR)
            ligne, colonne, vertical = random.choice(placements)
            bateau = bateau_cls(ligne, colonne, vertical=vertical)
            grille.ajoute(bateau)
            flotte.append(bateau)
        return flotte

    @staticmethod
    def _placements_possibles(grille: Grille, longueur: int):
        placements = []
        for vertical in (False, True):
            for ligne in range(grille.lignes):
                for colonne in range(grille.colonnes):
                    if grille.peut_placer(longueur, ligne, colonne, vertical):
                        placements.append((ligne, colonne, vertical))
        return placements

    # ---------- Construction de la fenêtre ----------
    def _build_window(self) -> ptg.Window:
        self.input_row = ptg.Container(self.input_field, self.fire_button, box="EMPTY", horizontal=True)
        return ptg.Window(
            "[bold]Bataille navale[/bold]",
            self.grid_label,
            ptg.Container(self.coups_label, box="EMPTY"),
            ptg.Container(self.message_label, box="EMPTY"),
            ptg.Container("[dim]Saisissez 'ligne colonne' puis validez[/dim]", self.input_row, box="EMPTY"),
            ptg.Container(self.reset_button, self.reveal_button, self.quit_button, box="EMPTY", horizontal=True),
            box="DOUBLE",
            width=60,
            height=20,
        )
