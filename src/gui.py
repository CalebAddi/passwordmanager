"""
Responsibilities:
  - Render the login/setup screen
  - Render the main vault management screen
  - Route user actions to auth/vault/generator functions
  - Display feedback (success, error, copied to clipboard)

Design notes:
  - GUI is a thin layer. It should contain zero business logic.
    Every meaningful action delegates to src/auth, src/vault, or src/generator.
  - Screens are implemented as functions that clear and rebuild the window
    contents (a simple "frame swap" pattern), keeping things manageable
    without classes.

TODO: Build out each screen as the underlying modules are completed.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from src import auth, vault, generator


#region Main App ---------------|
def launch(vault_path: str) -> None:
    """
    Create the root Tk window and show the appropriate first screen.

    Logic:
      - If the vault file exists  → show the login screen
      - If it doesn't exist yet   → show the setup/create-vault screen

    Args:
        vault_path: Path to the vault file (passed in from main.py).
    """
    root = tk.Tk()
    root.title("Password Manager")
    root.resizable(False, False)

    # TODO: Check if vault exists and route to setup_screen or login_screen
    # os.path.exists(vault_path)

    root.mainloop()


#endregion -----------------------|

#region Screens ----------------|

def setup_screen(root: tk.Tk, vault_path: str) -> None:
    """
    First-time setup: ask the user to create a master password.
    On success, call auth.create_vault() and transition to main_screen().
    """
    pass  # TODO


def login_screen(root: tk.Tk, vault_path: str) -> None:
    """
    Login screen: ask for the master password.
    On success, call auth.unlock_vault() and transition to main_screen().
    On failure, show an error — do not reveal whether vault exists.
    """
    pass  # TODO


def main_screen(root: tk.Tk, vault_path: str, session_key: bytes, vault_data: vault.VaultData) -> None:
    """
    Main password manager screen.

    Features to build here (in order of complexity):
      1. List all stored services
      2. Add a new entry (service, username, password or generate one)
      3. Copy a password to clipboard
      4. Delete an entry
      5. Lock (return to login screen, clear key from memory)

    Note:
      vault_data should be treated as immutable within this function.
      When an add/remove happens, get a NEW vault dict back from vault.py,
      persist it, and re-render the screen with the new data.
    """
    pass  # TODO

#endregion ---------------------|

#region Helpers ----------------|

def clear_frame(frame: tk.Frame) -> None:
    """Destroy all child widgets of a frame to prepare for a re-render."""
    for widget in frame.winfo_children():
        widget.destroy()

#endregion ---------------------|