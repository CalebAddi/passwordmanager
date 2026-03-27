from __future__ import annotations

import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

#region Constants ------------------------------------|
ARG2_TIME_COST = 3 
ARG2_MEM_COST = 64 * 1024 # 64 MB
ARG2_PARALLELISM = 4 # Parallel threads
ARG2_HASH_LEN = 32 # Output key length 32 bytes (256 bits)
ARG2_TYPE = Type.ID

SALT_LEN = 16 # Bytes for Argon2 salt
NONCE_LENG = 12 # Bytes for AES-GCM nonce 

#endregion -------------------------------------------|

#region Key Derivation -------------------------------|

def derive_key(m_password: str, salt: bytes) -> bytes:
    m_password_bytes = m_password.encode()

    return hash_secret_raw(
        secret = m_password_bytes,
        salt = salt,
        time_cost = ARG2_TIME_COST,
        memory_cost = ARG2_MEM_COST,
        parallelism = ARG2_PARALLELISM,
        hash_len = ARG2_HASH_LEN,
        type = ARG2_TYPE
    )

def generate_salt() -> bytes:
    return os.urandom(SALT_LEN)

#endregion -------------------------------------------|

#region Encrypt / Decrypt ----------------------------|

def encrypt(key: bytes, plaintext: bytes) -> bytes:
    nonce = os.urandom(NONCE_LENG)
    cipher_inst = AESGCM(key)
    return nonce + cipher_inst.encrypt(nonce, plaintext, None)

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    nonce = ciphertext[:NONCE_LENG]
    actual_ciphertext = ciphertext[NONCE_LENG:]
    cipher_inst = AESGCM(key)
    return cipher_inst.decrypt(nonce, actual_ciphertext, None)

#endregion -------------------------------------------|