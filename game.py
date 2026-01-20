import os
import sys
from enum import Enum, auto

import arcade
from pyglet import image
from pyglet.graphics import Batch

from grid import Grid

# The following sets the correct path for pyinstaller
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

window = arcade.Window(width=680, height=600, title="Tetris", center_window=True)
icon_png = image.load("assets/icon.png")
window.set_icon(icon_png)

arcade.load_font("assets/pixelmix.ttf")
arcade.load_font("assets/NotoSansMath-Regular.ttf")


class States(Enum):
    PAUSE = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.grid = Grid()
        self.timer = 0
        self.state = States.PLAYING
        self.frequency_of_fall = 2

    def restart(self) -> None:
        self.grid = Grid()
        self.timer = 0
        self.state = States.PLAYING
        self.frequency_of_fall = 2

    def on_key_press(self, symbol, modifiers) -> None:
        if self.state == States.GAME_OVER:
            if symbol == arcade.key.ENTER:
                self.restart()

            return

        if self.state == States.PAUSE:
            if symbol == arcade.key.SPACE:
                self.state = States.PLAYING

            return

        # only accessable for PLAYING state
        match symbol:
            case arcade.key.SPACE:
                self.state = States.PAUSE

            case arcade.key.UP:
                self.grid.rotate_letter()

            case arcade.key.LEFT:
                self.grid.move_left()

            case arcade.key.RIGHT:
                self.grid.move_right()

            case arcade.key.DOWN:
                self.frequency_of_fall *= 3

    def on_key_release(self, symbol, modifiers) -> None:
        if self.state != States.PLAYING:  # no need to consider pause here
            return

        if symbol == arcade.key.DOWN:
            if self.frequency_of_fall <= 2:  # initial freq of fall
                return

            self.frequency_of_fall //= 3

    def draw_controls(self) -> None:
        controls = Batch()

        controls_text = arcade.Text(
            "Controls:",
            490,
            175,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        left_right_arr = arcade.Text(
            "← →",
            490,
            160,
            arcade.color.ARTICHOKE,
            9,
            font_name="Noto Sans Math",
            batch=controls,
        )

        left_right = arcade.Text(
            "Move",
            520,
            160,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        up_arr = arcade.Text(
            "↑",
            490,
            145,
            arcade.color.ARTICHOKE,
            9,
            font_name="Noto Sans Math",
            batch=controls,
        )

        up = arcade.Text(
            "Rotate",
            505,
            145,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        down_arr = arcade.Text(
            "↓",
            490,
            130,
            arcade.color.ARTICHOKE,
            9,
            font_name="Noto Sans Math",
            batch=controls,
        )

        down = arcade.Text(
            "Accelerate",
            505,
            130,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        space_key = arcade.Text(
            "[SPACE]",
            490,
            115,
            arcade.color.ARTICHOKE,
            8,
            font_name="Noto Sans Math",
            batch=controls,
        )

        space = arcade.Text(
            "Pause/Play",
            540,
            115,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        enter_key = arcade.Text(
            "[ENTER]",
            490,
            100,
            arcade.color.ARTICHOKE,
            8,
            font_name="Noto Sans Math",
            batch=controls,
        )

        enter = arcade.Text(
            "Restart",
            540,
            100,
            arcade.color.ARTICHOKE,
            9,
            font_name="Pixelmix",
            batch=controls,
        )

        controls.draw()

    def draw_fixed_text(self) -> None:
        fixed_text = Batch()

        title_text = arcade.Text(
            "TETRIS",
            510,
            500,
            arcade.color.BATTLESHIP_GREY,
            24,
            font_name="pixelmix",
            # bold=True,
            batch=fixed_text,
        )
        scores_fixed_text = arcade.Text(
            "Score: ",
            490,
            475,
            arcade.color.BATTLESHIP_GREY,
            10,
            font_name="pixelmix",
            batch=fixed_text,
        )

        next_letter = arcade.Text(
            "Next piece:",
            490,
            400,
            arcade.color.AMBER,
            10,
            font_name="pixelmix",
            bold=True,
            batch=fixed_text,
        )

        fixed_text.draw()

        self.draw_controls()

    def draw_dynamic_text(self) -> None:
        # status
        match self.state:
            case States.PAUSE:
                game_status_paused = arcade.Text(
                    "PAUSED",
                    600,
                    10,
                    arcade.color.BUFF,
                    font_name="pixelmix",
                    bold=True,
                )
                game_status_paused.draw()
            case States.PLAYING:
                game_status_playing = arcade.Text(
                    "RUNNING",
                    590,
                    10,
                    arcade.color.BUD_GREEN,
                    font_name="pixelmix",
                    bold=True,
                )
                game_status_playing.draw()
            case States.GAME_OVER:
                game_status_game_over = arcade.Text(
                    "GAME OVER!",
                    560,
                    10,
                    arcade.color.RUBY_RED,
                    font_name="pixelmix",
                    bold=True,
                )
                game_status_game_over.draw()

        # score
        scores_dynamic_text = arcade.Text(
            f"{self.grid.scores.points}",
            550,
            475,
            arcade.color.ALMOND,
            10,
            font_name="pixelmix",
        )
        scores_dynamic_text.draw()

    def on_draw(self) -> None:
        self.clear()
        self.grid.draw_all()
        self.draw_fixed_text()
        self.draw_dynamic_text()

    def on_update(self, delta_time: float) -> None:
        if self.state != States.PLAYING:
            return

        if self.grid.game_over:
            self.state = States.GAME_OVER
            return

        self.timer += delta_time

        if self.timer * self.frequency_of_fall > 1:
            self.grid.move_down()
            self.timer = 0

        if self.frequency_of_fall == 0:
            # print(f'time: {self.timer} && freq. of fall: {self.frequency_of_fall}')
            self.state = States.PAUSE


game = GameView()
window.show_view(game)
arcade.run()
