"""
A simple desktop calculator built with tkinter (Python's built-in GUI library).
No extra installs needed — just run: python3 calculator.py
"""

import tkinter as tk

ALLOWED_CHARS = set("0123456789.+-*/() ")


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        self.expression = ""
        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ---------- UI setup ----------

    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Segoe UI", 28),
            justify="right",
            bd=0,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            state="readonly",
            readonlybackground="#1e1e1e",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20, ipady=20)

    def _build_buttons(self):
        buttons = [
            ("C", 1, 0, "op"), ("⌫", 1, 1, "op"), ("(", 1, 2, "op"), (")", 1, 3, "op"),
            ("7", 2, 0, "num"), ("8", 2, 1, "num"), ("9", 2, 2, "num"), ("/", 2, 3, "op"),
            ("4", 3, 0, "num"), ("5", 3, 1, "num"), ("6", 3, 2, "num"), ("*", 3, 3, "op"),
            ("1", 4, 0, "num"), ("2", 4, 1, "num"), ("3", 4, 2, "num"), ("-", 4, 3, "op"),
            ("0", 5, 0, "num"), (".", 5, 1, "num"), ("=", 5, 2, "eq"), ("+", 5, 3, "op"),
        ]

        colors = {
            "num": ("#2d2d2d", "white"),
            "op": ("#3d3d3d", "#f0a500"),
            "eq": ("#f0a500", "black"),
        }

        for (text, row, col, kind) in buttons:
            bg, fg = colors[kind]
            btn = tk.Button(
                self,
                text=text,
                font=("Segoe UI", 18),
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                bd=0,
                relief="flat",
                command=lambda t=text: self.on_button(t),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4, ipady=14)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def _bind_keyboard(self):
        self.bind("<Key>", self._on_key)
        self.bind("<Return>", lambda e: self.on_button("="))
        self.bind("<KP_Enter>", lambda e: self.on_button("="))
        self.bind("<BackSpace>", lambda e: self.on_button("⌫"))
        self.bind("<Escape>", lambda e: self.on_button("C"))

    def _on_key(self, event):
        if event.char and event.char in ALLOWED_CHARS:
            self.on_button(event.char)

    # ---------- Logic ----------

    def on_button(self, key):
        if key == "C":
            self.expression = ""
        elif key == "⌫":
            self.expression = self.expression[:-1]
        elif key == "=":
            self.evaluate()
            return
        else:
            self.expression += key

        self.display_var.set(self.expression if self.expression else "0")

    def evaluate(self):
        expr = self.expression.strip()
        if not expr:
            return

        if not set(expr) <= ALLOWED_CHARS:
            self.display_var.set("Error")
            self.expression = ""
            return

        try:
            result = eval(expr, {"__builtins__": {}}, {})
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by 0")
            self.expression = ""
            return
        except Exception:
            self.display_var.set("Error")
            self.expression = ""
            return

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        self.expression = str(result)
        self.display_var.set(self.expression)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
