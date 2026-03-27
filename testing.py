# ── crypto tests ────────────────────────────────────────────────
from src.crypto import generate_salt, derive_key, encrypt, decrypt

salt = generate_salt()
key  = derive_key("mypassword", salt)
ct   = encrypt(key, b"hello world")
pt   = decrypt(key, ct)
assert pt == b"hello world", "decrypt did not return original plaintext"

wrong_key = derive_key("wrongpassword", salt)
try:
    decrypt(wrong_key, ct)
    assert False, "should have raised on bad key"
except Exception:
    pass  # expected — InvalidTag bubbled up correctly

print("crypto.py  ✓  all tests passed")


# ── vault tests ─────────────────────────────────────────────────
import os, tempfile
from src.vault import (
    serialize, deserialize,
    load_raw, save_raw,
    add_entry, remove_entry, get_entry,
)

# serialize / deserialize round-trip
original = {"github": {"username": "alice", "password": "s3cr3t"}}
raw      = serialize(original)
assert isinstance(raw, bytes),           "serialize must return bytes"
restored = deserialize(raw)
assert restored == original,             "deserialize must round-trip correctly"

# add_entry is non-mutating
vault0  = {}
vault1  = add_entry(vault0, "github", "alice", "s3cr3t")
vault2  = add_entry(vault1, "gmail",  "alice", "passw0rd")
assert "github" not in vault0,           "add_entry must not mutate the original vault"
assert "github" in vault1
assert "gmail"  in vault2

# get_entry
entry = get_entry(vault2, "github")
assert entry == {"username": "alice", "password": "s3cr3t"}
assert get_entry(vault2, "nonexistent") is None

# remove_entry is non-mutating
vault3 = remove_entry(vault2, "github")
assert "github" not in vault3,           "remove_entry must not mutate the original vault"
assert "github" in vault2,               "original vault should still contain the entry"
assert "gmail"  in vault3

# save_raw / load_raw round-trip using a real temp file
with tempfile.NamedTemporaryFile(delete=False) as tmp:
    tmp_path = tmp.name

try:
    save_raw(tmp_path, salt, ct)
    loaded_salt, loaded_ct = load_raw(tmp_path)
    assert loaded_salt == salt,          "loaded salt does not match"
    assert loaded_ct   == ct,            "loaded ciphertext does not match"
finally:
    os.unlink(tmp_path)

# load_raw returns None when file is absent
assert load_raw("/tmp/does_not_exist_xyz.enc") is None

print("vault.py   ✓  all tests passed")