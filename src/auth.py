"""
Responsibilities:
  - Handle first-time vault creation (set a master password)
  - Handle subsequent logins (verify master password by attempting decryption)
  - Return a session key on success, or raise/return None on failure

Design notes:
  - Do NOT store the master password or its hash anywhere.
    Verification works by: derive key -> attempt to decrypt vault -> if
    the AES-GCM tag is valid, the password was correct.
  - This is a clean cryptographically sound design — there's no separate
    pass hash that could be attacked. The vault itself IS the proof.
  - Keep the derived key in memory only. Never write it to disk.

TODO: Implement the following functions.
"""

from __future__ import annotations

from src import crypto, vault


#region Authentication ---------------|

def create_vault(vault_path: str, master_password: str) -> tuple[bytes, vault.VaultData]:
    """
    Initialize a brand-new encrypted vault with an empty password store.

    Steps:
      1. Generate a fresh salt
      2. Derive a key from the master password + salt
      3. Serialize an empty vault dict
      4. Encrypt it
      5. Save salt + ciphertext to disk
      6. Return (key, empty_vault) for the session

    Args:
        vault_path:      Path where the vault file will be created.
        master_password: The chosen master password (plaintext).

    Returns:
        (session_key, empty_vault_dict)
    """
    pass  # TODO


def unlock_vault(vault_path: str, master_password: str) -> tuple[bytes, vault.VaultData] | None:
    """
    Attempt to unlock an existing vault with the provided master password.

    Steps:
      1. Load (salt, ciphertext) from disk
      2. Derive a key from the master password + salt
      3. Attempt to decrypt — if AES-GCM tag is invalid, password is wrong
      4. Deserialize the plaintext bytes into a vault dict
      5. Return (session_key, vault_dict) on success, None on failure

    Args:
        vault_path:      Path to the existing vault file.
        master_password: The master password attempt (plaintext).

    Returns:
        (session_key, vault_dict) on success, or None on wrong password.
    """
    pass  # TODO

#endregion --------------------------------|