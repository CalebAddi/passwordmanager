import os
from src import gui

VAULT_PATH = os.path.join(os.path.dirname(__file__), "data", "vault.enc")

def main() -> None:
    """Bootstrap and launch application."""
    gui.launch(vault_path=VAULT_PATH)

if __name__ == "__main__":    
    main()