
import math
import re

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


# =====================================
# ROUNDED BUTTON
# =====================================

class RoundedButton(Button):

    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:

            self.bg_instruction = Color(*self.bg_color)

            self.rounded_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(13)] * 4
            )

        self.bind(
            pos=self.update_rectangle,
            size=self.update_rectangle,
            bg_color=self.update_button_color
        )

    def update_rectangle(self, *args):

        self.rounded_rect.pos = self.pos
        self.rounded_rect.size = self.size

    def update_button_color(self, *args):

        self.bg_instruction.rgba = self.bg_color

    def set_style(self, bg, fg):

        self.bg_color = list(bg)
        self.color = fg


# =====================================
# CALCULATOR APP
# =====================================

class CalculatorApp(App):

    def build(self):

        self.dark_mode = False
        self.scientific_open = False

        self.expression = ""
        self.history = []
        self.all_buttons = []

        self.palette = self.get_palette()

        # MAIN LAYOUT
        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(7)
        )

        self.root_layout = root

        with root.canvas.before:

            self.root_color = Color(*self.palette["bg"])

            self.root_rectangle = Rectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # TOP AREA
        self.top_area = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(46),
            spacing=dp(6)
        )

        root.add_widget(self.top_area)

        # TOOLBAR
        toolbar = BoxLayout(
            size_hint_y=None,
            height=dp(46),
            spacing=dp(8)
        )

        self.top_area.add_widget(toolbar)

        self.add_button(
            toolbar,
            "History",
            self.show_history,
            "soft",
            sp(16)
        )

        self.scientific_button = self.add_button(
            toolbar,
            "Scientific +",
            self.toggle_scientific,
            "soft",
            sp(16)
        )

        # SCIENTIFIC PANEL
        self.scientific_panel = GridLayout(
            cols=4,
            rows=2,
            spacing=dp(6),
            size_hint_y=None,
            height=dp(108),
            row_force_default=True,
            row_default_height=dp(51)
        )

        scientific_buttons = [

            ("x^3", self.cube),
            ("cbrt", self.cube_root),
            ("x^y", lambda: self.append("**")),
            ("pi", lambda: self.append(str(math.pi))),

            ("sin", self.sine),
            ("cos", self.cosine),
            ("tan", self.tangent),
            ("Theme", self.change_theme)
        ]

        for text, command in scientific_buttons:

            self.add_button(
                self.scientific_panel,
                text,
                command,
                "soft",
                sp(17)
            )

        # DISPLAY
        self.display = Label(
            text="0",
            font_size=sp(42),
            color=self.palette["text"],
            halign="right",
            valign="middle",
            size_hint_y=None,
            height=dp(90)
        )

        self.display.bind(
            size=self.update_display_size
        )

        root.add_widget(self.display)

        # MAIN KEYPAD
        keypad = GridLayout(
            cols=4,
            rows=6,
            spacing=dp(6)
        )

        root.add_widget(keypad)

        buttons = [

            ("%", self.percentage, "soft"),
            ("CE", self.clear_display, "soft"),
            ("C", self.clear_display, "soft"),
            ("DEL", self.backspace, "soft"),

            ("1/x", self.reciprocal, "soft"),
            ("x^2", self.square, "soft"),
            ("sqrt", self.square_root, "soft"),
            ("/", lambda: self.append("/"), "soft"),

            ("7", lambda: self.append("7"), "normal"),
            ("8", lambda: self.append("8"), "normal"),
            ("9", lambda: self.append("9"), "normal"),
            ("*", lambda: self.append("*"), "soft"),

            ("4", lambda: self.append("4"), "normal"),
            ("5", lambda: self.append("5"), "normal"),
            ("6", lambda: self.append("6"), "normal"),
            ("-", lambda: self.append("-"), "soft"),

            ("1", lambda: self.append("1"), "normal"),
            ("2", lambda: self.append("2"), "normal"),
            ("3", lambda: self.append("3"), "normal"),
            ("+", lambda: self.append("+"), "soft"),

            ("+/-", self.plus_minus, "normal"),
            ("0", lambda: self.append("0"), "normal"),
            (".", lambda: self.append("."), "normal"),
            ("=", self.calculate, "accent")
        ]

        for text, command, role in buttons:

            self.add_button(
                keypad,
                text,
                command,
                role,
                sp(22)
            )

        return root

    # =================================
    # THEME COLORS
    # =================================

    def get_palette(self):

        if self.dark_mode:

            return {
                "bg": (0.12, 0.13, 0.14, 1),
                "text": (1, 1, 1, 1),
                "normal": (0.20, 0.21, 0.23, 1),
                "soft": (0.17, 0.18, 0.20, 1),
                "accent": (0.54, 0.70, 0.96, 1),
                "accent_text": (0.08, 0.09, 0.12, 1)
            }

        return {
            "bg": (0.95, 0.95, 0.95, 1),
            "text": (0.12, 0.12, 0.12, 1),
            "normal": (1, 1, 1, 1),
            "soft": (0.91, 0.92, 0.93, 1),
            "accent": (0.00, 0.40, 0.75, 1),
            "accent_text": (1, 1, 1, 1)
        }

    # =================================
    # BUTTON CREATOR
    # =================================

    def add_button(
        self,
        parent,
        text,
        command,
        role="normal",
        font_size=None
    ):

        if font_size is None:
            font_size = sp(20)

        button = RoundedButton(
            text=text,
            font_size=font_size,
            color=self.palette["text"]
        )

        self.set_button_style(button, role)

        button.bind(
            on_release=lambda instance: command()
        )

        parent.add_widget(button)

        self.all_buttons.append((button, role))

        return button

    def set_button_style(self, button, role):

        if role == "accent":

            bg = self.palette["accent"]
            fg = self.palette["accent_text"]

        else:

            bg = self.palette[role]
            fg = self.palette["text"]

        button.set_style(bg, fg)

    # =================================
    # BACKGROUND
    # =================================

    def update_background(self, instance, value):

        self.root_rectangle.pos = instance.pos
        self.root_rectangle.size = instance.size

    def update_display_size(self, instance, value):

        instance.text_size = value

    # =================================
    # DISPLAY
    # =================================

    def update_display(self):

        self.display.text = (
            self.expression if self.expression else "0"
        )

    # =================================
    # INSERT VALUE
    # =================================

    def append(self, value):

        if self.expression == "Error":

            self.expression = ""

        if value == ".":

            last_number = re.split(
                r"[+\-*/()]",
                self.expression
            )[-1]

            if "." in last_number:
                return

        self.expression += value

        self.update_display()

    # =================================
    # CLEAR
    # =================================

    def clear_display(self):

        self.expression = ""

        self.update_display()

    # =================================
    # BACKSPACE
    # =================================

    def backspace(self):

        self.expression = self.expression[:-1]

        self.update_display()

    # =================================
    # FORMAT RESULT
    # =================================

    def format_result(self, result):

        if isinstance(result, float):

            result = round(result, 8)

            if result.is_integer():

                result = int(result)

        return str(result)

    # =================================
    # CALCULATE
    # =================================

    def calculate(self):

        if not self.expression:
            return

        try:

            if not re.fullmatch(
                r"[0-9+\-*/(). ]+",
                self.expression
            ):

                raise ValueError("Invalid expression")

            result = eval(
                self.expression,
                {"__builtins__": {}},
                {}
            )

            if not isinstance(result, (int, float)):

                raise ValueError("Invalid result")

            if not math.isfinite(result):

                raise ValueError("Invalid result")

            old_expression = self.expression

            result = self.format_result(result)

            self.history.append(
                f"{old_expression} = {result}"
            )

            self.expression = result

            self.update_display()

        except Exception:

            self.expression = "Error"

            self.update_display()

    # =================================
    # UNARY OPERATIONS
    # =================================

    def apply_operation(self, operation):

        try:

            number = float(self.expression)

            result = operation(number)

            if not math.isfinite(result):

                raise ValueError("Invalid result")

            self.expression = self.format_result(result)

            self.update_display()

        except Exception:

            self.expression = "Error"

            self.update_display()

    # =================================
    # BASIC FUNCTIONS
    # =================================

    def square(self):

        self.apply_operation(lambda x: x ** 2)

    def square_root(self):

        self.apply_operation(math.sqrt)

    def cube(self):

        self.apply_operation(lambda x: x ** 3)

    def cube_root(self):

        self.apply_operation(
            lambda x: math.copysign(abs(x) ** (1/3), x)
        )

    def reciprocal(self):

        self.apply_operation(lambda x: 1 / x)

    def percentage(self):

        self.apply_operation(lambda x: x / 100)

    def plus_minus(self):

        try:

            number = float(self.expression)

            self.expression = self.format_result(-number)

            self.update_display()

        except Exception:

            self.expression = "Error"

            self.update_display()

    # =================================
    # TRIGONOMETRY
    # =================================

    def sine(self):

        self.apply_operation(
            lambda x: math.sin(math.radians(x))
        )

    def cosine(self):

        self.apply_operation(
            lambda x: math.cos(math.radians(x))
        )

    def tangent(self):

        self.apply_operation(
            lambda x: math.tan(math.radians(x))
        )

    # =================================
    # SCIENTIFIC MENU
    # =================================

    def toggle_scientific(self):

        if self.scientific_open:

            self.top_area.remove_widget(
                self.scientific_panel
            )

            self.top_area.height = dp(46)

            self.scientific_button.text = "Scientific +"

            self.scientific_open = False

        else:

            self.top_area.add_widget(
                self.scientific_panel
            )

            self.top_area.height = dp(160)

            self.scientific_button.text = "Scientific -"

            self.scientific_open = True

    # =================================
    # THEME CHANGE
    # =================================

    def change_theme(self):

        self.dark_mode = not self.dark_mode

        self.palette = self.get_palette()

        self.root_color.rgba = self.palette["bg"]

        self.display.color = self.palette["text"]

        for button, role in self.all_buttons:

            self.set_button_style(button, role)

    # =================================
    # HISTORY
    # =================================

    def show_history(self):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        history_label = Label(
            text=(
                "\n".join(self.history)
                if self.history
                else "No history available"
            ),
            color=self.palette["text"],
            halign="left",
            valign="top"
        )

        history_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        content.add_widget(history_label)

        actions = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )

        def clear_history():

            self.history.clear()

            history_label.text = "No history available"

        self.add_button(
            actions,
            "Clear",
            clear_history,
            "soft",
            sp(15)
        )

        self.add_button(
            actions,
            "Close",
            lambda: popup.dismiss(),
            "accent",
            sp(15)
        )

        content.add_widget(actions)

        popup = Popup(
            title="Calculation History",
            content=content,
            size_hint=(0.9, 0.65),
            background_color=self.palette["bg"]
        )

        popup.open()


# =====================================
# RUN APP
# =====================================

if __name__ == "__main__":

    CalculatorApp().run()

