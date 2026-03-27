from __future__ import annotations

import json
import os
from .crypto import SALT_LEN
from typing import Any

# The vault is a plain dict:  { service: { "username": ..., "password": ... } }
VaultData = dict[str, dict[str, str]]

#region I/O -----------------------------------------------|
def load_raw(vault_path: str) -> tuple[bytes, bytes] | None:
    if not os.path.exists(vault_path):
        return None

    with open(vault_path, "rb") as f:
        data = f.read()
        return (data[:SALT_LEN], data[SALT_LEN:])


def save_raw(vault_path: str, salt: bytes, ciphertext: bytes) -> None:
    tmp_path = f"{vault_path}.tmp"

    with open(tmp_path, "wb") as f:
        f.write(salt + ciphertext)

    os.replace(tmp_path, vault_path)

#endregion -----------------------------------------------|


#region Serialization ------------------------------------|

def serialize(vault_data: VaultData) -> bytes:
    return json.dumps(vault_data).encode()


def deserialize(raw_bytes: bytes) -> VaultData:
    return json.loads(raw_bytes.decode())

#endregion -------------------------------------------|


#region Vault Ops ------------------------------------|

def add_entry(vault: VaultData, service: str, username: str, password: str) -> VaultData:
    entry = {"username": username, "password": password}
    return {**vault, service: entry}


def remove_entry(vault: VaultData, service: str) -> VaultData:
    return {key: val for key, val in vault.items() if key != service}


def get_entry(vault: VaultData, service: str) -> dict[str, str] | None:
    return vault.get(service)

#endregion -------------------------------------------|