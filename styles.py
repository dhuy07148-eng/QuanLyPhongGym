
import tkinter as tk
from tkinter import ttk

BG = "#F4F7FC"
WHITE = "#FFFFFF"
PRIMARY = "#2563EB"
DARK = "#172554"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#16A34A"
RED = "#DC2626"
ORANGE = "#EA580C"
PURPLE = "#7C3AED"


def setup_style(root):
    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=38,
        fieldbackground=WHITE,
        font=("Arial", 10),
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background="#E8EFFD",
        foreground=DARK,
        font=("Arial", 10, "bold"),
        padding=12,
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#DBEAFE")],
        foreground=[("selected", DARK)]
    )

    style.configure(
        "TCombobox",
        padding=7,
        font=("Arial", 10)
    )


def create_button(parent, text, command,
                  color=PRIMARY, width=14):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        bd=0,
        width=width,
        padx=8,
        pady=11
    )


def create_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg=MUTED,
        font=("Arial", 10)
    ).pack(anchor="w", padx=16, pady=(13, 5))

    label = tk.Label(
        card,
        text=value,
        bg=WHITE,
        fg=color,
        font=("Arial", 20, "bold")
    )
    label.pack(anchor="w", padx=16, pady=(0, 13))

    return card, label
