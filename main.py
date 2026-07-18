"""
Professional Scientific Calculator
Kivy 2.3.1 - Pydroid 3 Compatible
Later convertible to APK using Buildozer.
"""

import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window

# Background color (light theme)
Window.clearcolor = (0.10, 0.10, 0.12, 1)


class ScientificCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(8), spacing=dp(6), **kwargs)

        self.expression = ""
        self.memory = 0.0
        self.angle_mode_deg = True  # True = Degree, False = Radian

        # ---------- Display ----------
        self.display = TextInput(
            text="",
            font_size=dp(32),
            halign="right",
            multiline=False,
            readonly=True,
            background_color=(0.15, 0.15, 0.18, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            size_hint=(1, 0.18),
            padding=[dp(10), dp(20), dp(10), dp(10)],
        )
        self.add_widget(self.display)

        # Mode label (deg/rad + memory indicator)
        self.mode_label = Label(
            text="DEG | M:0",
            size_hint=(1, 0.05),
            color=(0.6, 0.8, 1, 1),
            font_size=dp(14),
            halign="right",
        )
        self.add_widget(self.mode_label)

        # Developer name label
        self.developer_label = Label(
            text="Developed by: Rana Haseeb",
            size_hint=(1, 0.04),
            color=(0.5, 0.9, 0.6, 1),
            font_size=dp(13),
            bold=True,
        )
        self.add_widget(self.developer_label)

        # ---------- Button grid ----------
        grid = GridLayout(cols=5, spacing=dp(5), size_hint=(1, 0.77))

        buttons = [
            "sin", "cos", "tan", "DEG", "AC",
            "asin", "acos", "atan", "(", ")",
            "log", "ln", "√", "^", "DEL",
            "π", "e", "1/x", "%", "÷",
            "7", "8", "9", "x!", "×",
            "4", "5", "6", "MC", "-",
            "1", "2", "3", "M+", "+",
            "0", ".", "MR", "M-", "=",
        ]

        for label in buttons:
            btn = Button(
                text=label,
                font_size=dp(20),
                background_normal="",
                background_color=self.get_btn_color(label),
                color=(1, 1, 1, 1),
            )
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)

        self.add_widget(grid)

    # -------- Button coloring for a more professional look --------
    def get_btn_color(self, label):
        operators = {"÷", "×", "-", "+", "="}
        scientific = {"sin", "cos", "tan", "asin", "acos", "atan",
                      "log", "ln", "√", "^", "π", "e", "1/x", "%", "x!"}
        memory_keys = {"MC", "MR", "M+", "M-"}
        if label == "AC":
            return (0.75, 0.15, 0.15, 1)
        elif label == "DEL":
            return (0.55, 0.25, 0.1, 1)
        elif label in operators:
            return (0.15, 0.45, 0.75, 1)
        elif label in scientific:
            return (0.25, 0.25, 0.35, 1)
        elif label in memory_keys:
            return (0.3, 0.5, 0.3, 1)
        elif label == "DEG":
            return (0.35, 0.35, 0.5, 1)
        else:
            return (0.2, 0.2, 0.22, 1)

    # -------- Core button logic --------
    def on_button_press(self, instance):
        key = instance.text

        if key == "AC":
            self.expression = ""
            self.update_display()
            return

        if key == "DEL":
            self.expression = self.expression[:-1]
            self.update_display()
            return

        if key == "DEG":
            self.angle_mode_deg = not self.angle_mode_deg
            self.update_mode_label()
            return

        if key == "=":
            self.calculate()
            return

        if key in ("MC", "MR", "M+", "M-"):
            self.handle_memory(key)
            return

        # Map display symbols to python-evaluatable expression pieces
        mapping = {
            "×": "*",
            "÷": "/",
            "π": "math.pi",
            "e": "math.e",
            "√": "sqrt(",
            "^": "**",
            "log": "log10(",
            "ln": "ln(",
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "asin": "asin(",
            "acos": "acos(",
            "atan": "atan(",
            "1/x": "1/(",
            "x!": "fact(",
            "%": "/100",
        }

        self.expression += mapping.get(key, key)
        self.update_display()

    # -------- Memory functions --------
    def handle_memory(self, key):
        try:
            current_value = float(self.evaluate_expression(self.expression)) if self.expression else 0.0
        except Exception:
            current_value = 0.0

        if key == "MC":
            self.memory = 0.0
        elif key == "MR":
            self.expression += self.format_number(self.memory)
        elif key == "M+":
            self.memory += current_value
        elif key == "M-":
            self.memory -= current_value

        self.update_display()
        self.update_mode_label()

    # -------- Helper math functions (respect DEG/RAD mode) --------
    def sin(self, x):
        return math.sin(math.radians(x)) if self.angle_mode_deg else math.sin(x)

    def cos(self, x):
        return math.cos(math.radians(x)) if self.angle_mode_deg else math.cos(x)

    def tan(self, x):
        return math.tan(math.radians(x)) if self.angle_mode_deg else math.tan(x)

    def asin(self, x):
        r = math.asin(x)
        return math.degrees(r) if self.angle_mode_deg else r

    def acos(self, x):
        r = math.acos(x)
        return math.degrees(r) if self.angle_mode_deg else r

    def atan(self, x):
        r = math.atan(x)
        return math.degrees(r) if self.angle_mode_deg else r

    def ln(self, x):
        return math.log(x)

    def fact(self, x):
        return math.factorial(int(x))

    # -------- Safe evaluation --------
    def evaluate_expression(self, expr):
        safe_dict = {
            "math": math,
            "sqrt": math.sqrt,
            "log10": math.log10,
            "ln": self.ln,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
            "fact": self.fact,
            "__builtins__": {},
        }
        return eval(expr, safe_dict)

    def calculate(self):
        try:
            result = self.evaluate_expression(self.expression)
            self.expression = self.format_number(result)
        except ZeroDivisionError:
            self.expression = "Error: /0"
        except Exception:
            self.expression = "Error"
        self.update_display()

    def format_number(self, value):
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(round(value, 8))
        return str(value)

    # -------- UI refresh --------
    def update_display(self):
        self.display.text = self.expression

    def update_mode_label(self):
        mode = "DEG" if self.angle_mode_deg else "RAD"
        self.mode_label.text = f"{mode} | M:{self.format_number(self.memory)}"


class CalculatorApp(App):
    def build(self):
        self.title = "Scientific Calculator - by Rana Haseeb"
        return ScientificCalculator()


if __name__ == "__main__":
    CalculatorApp().run()
