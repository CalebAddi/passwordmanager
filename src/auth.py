from __future__ import annotations

import os
from src import crypto, vault
from cryptography.exceptions import InvalidTag


#region Authentication ---------------|

def create_vault(vault_path: str, master_password: str) -> tuple[bytes, vault.VaultData]:
    new_salt = crypto.generate_salt()
    cipher_key = crypto.derive_key(master_password, new_salt)

    vault_dict = {}
    serialized_bytes = vault.serialize(vault_dict)
    ciphertext = crypto.encrypt(cipher_key, serialized_bytes)

    dir_name = os.path.dirname(vault_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    vault.save_raw(vault_path, new_salt, ciphertext)
    return cipher_key, vault_dict


def unlock_vault(vault_path: str, master_password: str) -> tuple[bytes, vault.VaultData] | None:
    if not os.path.isfile(vault_path):
        return None

    raw = vault.load_raw(vault_path)
    if raw is None:
        return None

    salt, ciphertext = raw

    cipher_key = crypto.derive_key(master_password, salt)

    try:
        decrypted_bytes = crypto.decrypt(cipher_key, ciphertext)
    except (InvalidTag, ValueError):
        return None

    return cipher_key, vault.deserialize(decrypted_bytes)


def change_master_password(vault_path: str, old_password: str, new_password: str) -> bool:
    pass # TODO

#endregion --------------------------------|