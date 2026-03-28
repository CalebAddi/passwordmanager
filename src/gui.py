""" 
(Dev Note:) this is my first time really programming a GUI utilizing tkinter or with python as a whole (usually program GUI/Frontend work with JS frameworks).
This is a learning experience for me here on programming (even if minimal) a GUI utilizing python.
"""

from __future__ import annotations

import os
import pyperclip
import tkinter as tk
from tkinter import messagebox, ttk
from src import auth, vault, generator


#region Main App ---------------|
def launch(vault_path: str) -> None:
    root = tk.Tk()
    root.title("Password Manager")
    root.resizable(True, True)
    root.geometry("400x300") # min window size

    login_screen(root, vault_path) if os.path.exists(vault_path) else setup_screen(root, vault_path)

    root.mainloop()


#endregion -----------------------|

#region Screens ----------------|

def setup_screen(root: tk.Tk, vault_path: str) -> None:
    clear_frame(root)
    tk.Label(root, text = "Create Master Password").pack()
    pword_inst = tk.StringVar()
    confirm_inst = tk.StringVar()
    tk.Entry(root, textvariable = pword_inst, show = "*").pack()
    tk.Entry(root, textvariable = confirm_inst, show = "*").pack()

    def on_submit():
        password = pword_inst.get()
        confirm = confirm_inst.get()

        if password == "" or confirm == "":
            messagebox.showerror("Error", "Password fields cannot be empty...")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match...")
            return

        key, vault_data = auth.create_vault(vault_path, password)
        main_screen(root, vault_path, key, vault_data)
        tk.Button(root, text = "Create", command = on_submit).pack()


def login_screen(root: tk.Tk, vault_path: str) -> None:
    clear_frame(root)
    tk.Label(root, text = "Unlock Vault").pack()
    pword_inst = tk.StringVar()
    tk.Entry(root, textvariable = pword_inst, show = "*").pack()

    def on_submit():
        password = pword_inst.get()

        if password == "":
            messagebox.showerror("Error", "Password fields cannot be empty...")
            return

        result = auth.unlock_vault(vault_path, password)

        if result == None:
            messagebox.showerror("Error", "Invalid password")
        else:
            key, vault_data = result
            main_screen(root, vault_path, key, vault_data)

        tk.Button(root, text = "Unlock", command = on_submit).pack()
        root.bind("<Return>", lambda event: on_submit)


def main_screen(root: tk.Tk, vault_path: str, session_key: bytes, vault_data: vault.VaultData) -> None:
    clear_frame(root)

    frame = tk.Frame(root).pack(fill = tk.X, pady = 5)
    tk.Label(frame, text = "Password Managerizer").pack(side = tk.LEFT)
    tk.Button(frame, text = "Lock", command = lambda e: login_screen(root, vault_path)).pack(side = tk.RIGHT)

    # Password table
    tree = ttk.Treeview(root, columns = ("Service", "Username", "Password"), show = "headings")
    tree.heading("Service", text = "Service")
    tree.heading("Username", text = "Username")
    tree.heading("Password", text = "Password")

    for pair in vault_data.items():
        tree.insert("", tk.END, values = (pair.service, pair.username, "********")).pack(fill = tk.BOTH, expand = True)

    # Action buttons
    pass # TODO: finish main screen code

#endregion ---------------------|

#region Helpers ----------------|

def clear_frame(frame: tk.Frame) -> None:
    """Destroy all child widgets of a frame to prepare for a re-render."""
    for widget in frame.winfo_children():
        widget.destroy()

#endregion ---------------------|