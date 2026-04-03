""" 
(Dev Note:) this is my first time really programming a GUI utilizing tkinter or with python as a whole (usually program GUI/Frontend work with JS frameworks).
This is a learning experience for me here on programming (even if minimal) a GUI utilizing python.
"""

from __future__ import annotations

import os
import pyperclip
import tkinter as tk
from tkinter import messagebox, ttk
from src import auth, vault, generator, crypto


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
    pword_inst, confirm_inst = tk.StringVar(), tk.StringVar()
    tk.Entry(root, textvariable = pword_inst, show = "*").pack()
    tk.Entry(root, textvariable = confirm_inst, show = "*").pack()

    def on_submit():
        password, confirm = pword_inst.get(), confirm_inst.get()

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
    root.bind("<Return>", lambda event: on_submit())


def main_screen(root: tk.Tk, vault_path: str, session_key: bytes, vault_data: vault.VaultData) -> None:
    clear_frame(root)

    frame = tk.Frame(root)
    frame.pack(fill = tk.X, pady = 5)
    tk.Label(frame, text = "Password Managerizer").pack(side = tk.LEFT)
    tk.Button(frame, text = "Lock", command = lambda e: login_screen(root, vault_path)).pack(side = tk.RIGHT)

    # Password table
    tree = ttk.Treeview(root, columns = ("Service", "Username", "Password"), show = "headings")
    tree.heading("Service", text = "Service")
    tree.heading("Username", text = "Username")
    tree.heading("Password", text = "Password")

    for pair in vault_data.items():
        tree.insert("", tk.END, values = (pair.service, pair.username, "********"))
        tree.pack(fill = tk.BOTH, expand = True)

    # Action buttons
    action_frame = tk.Frame(root)
    action_frame.pack(fill = tk.X, pady = 5)
    tk.Button(action_frame, text = "Add Entry", command = add_entry_dialog).pack(side = tk.LEFT, padx = 5)
    tk.Button(action_frame, text = "Copy Password", command = copy_password).pack(side = tk.LEFT, padx = 5)
    tk.Button(action_frame, text = "Delete Entry", command = delete_entry).pack(side = tk.LEFT, padx = 5)


    def add_entry_dialog():
        popup = tk.Toplevel(root)
        popup.title("Add Entry")
        svc_var, user_var, pword_var = tk.StringVar(), tk.StringVar(), tk.StringVar()

        for label, var, show in [("Service", svc_var, None), ("Username", user_var, None), ("Password", pword_var, "*")]:
            tk.Label(popup, text = label).pack()
            tk.Entry(popup, textvariable = var, show = show).pack()

        gen_var = tk.BooleanVar()
        tk.Checkbutton(popup, text = "Generate password", variable = gen_var, command = on_toggle).pack()
        
        def on_toggle():
            if gen_var.get():
                pword_var.set(generator.generate_password())
            else:
                pword_var.set("")

        def on_save():
            salt = vault.load_raw()
            service, username, password = svc_var.get(), user_var.get(), pword_var.get()

            if service == '' or username == '' or password == '':
                return

            new_vault = vault.add_entry(vault_data, service, username, password)
            raw = vault.serialize(new_vault)
            ct = crypto.encrypt(session_key, raw)

            vault.save_raw(vault_path, salt, ct)
            popup.destroy()
            main_screen(root, vault_path, session_key, new_vault)

        tk.Button(popup, text = "Save", command = on_save).pack()


    def copy_password():
        pass # TODO


    def delete_entry():
        pass # TODO


#endregion ---------------------|

#region Helpers ----------------|

def clear_frame(frame: tk.Frame) -> None:
    """Destroy all child widgets of a frame to prepare for a re-render."""
    for widget in frame.winfo_children():
        widget.destroy()

#endregion ---------------------|