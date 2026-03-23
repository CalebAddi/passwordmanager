"""
Responsibilities:
  - Serialize/deserialize the in-memory password store (dict -> JSON -> bytes)
  - Read the encrypted vault file from disk
  - Write the encrypted vault file to disk
  - Initialize a brand-new vault when none exists

Design notes:
  - This module knows nothing about the master password or GUI.
    It only accepts already-derived keys and already-encrypted bytes.
  - The on-disk format is:   [ 16-byte salt ][ encrypted JSON vault ]
    The salt is stored in plaintext (this is safe and standard — the salt
    is not a secret, it just ensures uniqueness).
  - Functions here are thin I/O wrappers — the heavy lifting is in crypto.py.

TODO: Implement these following tasks for the proj.
"""

from __future__ import annotations

import json
import os
from typing import Any

# The vault is a plain dict:  { service: { "username": ..., "password": ... } }
VaultData = dict[str, dict[str, str]]

#region I/O -----------------------------------------------|
def load_raw(vault_path: str) -> tuple[bytes, bytes] | None:
    """
    Read the vault file and split it into (salt, ciphertext).

    Returns:
        (salt, ciphertext) if the file exists, or None if it doesn't yet.
    """
    pass  # TODO


def save_raw(vault_path: str, salt: bytes, ciphertext: bytes) -> None:
    """
    Write (salt + ciphertext) to disk atomically.

    Need to write to a temp file first, then os.replace() — to prevent
    a corrupt vault if the process is interrupted mid-write.

    Args:
        vault_path:  Full path to the .enc vault file.
        salt:        16-byte Argon2 salt.
        ciphertext:  AES-GCM encrypted vault bytes.
    """
    pass  # TODO

#endregion -----------------------------------------------|


#region Serialization ------------------------------------|

def serialize(vault_data: VaultData) -> bytes:
    """
    Convert the vault dict to UTF-8 encoded JSON bytes for encryption.

    Args:
        vault_data: The in-memory vault dictionary.

    Returns:
        JSON-encoded bytes.
    """
    pass  # TODO


def deserialize(raw_bytes: bytes) -> VaultData:
    """
    Convert decrypted bytes back into the vault dictionary.

    Args:
        raw_bytes: UTF-8 encoded JSON bytes.

    Returns:
        The vault dictionary.
    """
    pass  # TODO

#endregion -------------------------------------------|


#region Vault Ops ------------------------------------|

def add_entry(vault: VaultData, service: str, username: str, password: str) -> VaultData:
    """
    Return a NEW vault dict with the entry added.

    Functional note: Do NOT mutate the input vault.
    Use dict unpacking or copy to return a new one.
    """
    pass  # TODO


def remove_entry(vault: VaultData, service: str) -> VaultData:
    """
    Return a NEW vault dict with the named service removed.
    """
    pass  # TODO


def get_entry(vault: VaultData, service: str) -> dict[str, str] | None:
    """
    Retrieve a single entry by service name, or None if not found.
    """
    pass  # TODO

#endregion -------------------------------------------|