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

print("vault.py       ✓  all tests passed")


# ── generator tests ─────────────────────────────────────────────
import string
from src.generator import generate_password

# default generation — correct type and length
pw = generate_password()
assert isinstance(pw, str),              "password must be a string"
assert len(pw) == 20,                    "default length should be 20"

# custom length
pw = generate_password(length=32)
assert len(pw) == 32,                    "custom length not respected"

# character set guarantees — at least one from each enabled category
pw = generate_password(length=16, use_uppercase=True, use_digits=True, use_symbols=True)
assert any(c in string.ascii_uppercase for c in pw), "missing uppercase"
assert any(c in string.digits          for c in pw), "missing digit"
assert any(c in string.punctuation     for c in pw), "missing symbol"

# disabling categories
pw_no_symbols = generate_password(length=16, use_symbols=False)
assert not any(c in string.punctuation for c in pw_no_symbols), "symbols should be absent"

pw_no_digits = generate_password(length=16, use_digits=False)
assert not any(c in string.digits for c in pw_no_digits),       "digits should be absent"

# two generated passwords should essentially never be identical
pw_a = generate_password(length=24)
pw_b = generate_password(length=24)
assert pw_a != pw_b,                     "two passwords should not be identical"

# edge case — length below minimum should raise ValueError
try:
    generate_password(length=4)
    assert False, "should have raised ValueError for length < 8"
except ValueError:
    pass

print("generator.py   ✓  all tests passed")


# ── auth tests ──────────────────────────────────────────────────
import tempfile, os
from src.auth import create_vault, unlock_vault

with tempfile.TemporaryDirectory() as tmp_dir:
    vpath = os.path.join(tmp_dir, "test_vault.enc")

    # create a brand new vault
    key, data = create_vault(vpath, "master1234")
    assert isinstance(key, bytes),       "session key must be bytes"
    assert isinstance(data, dict),       "initial vault data must be a dict"
    assert data == {},                   "new vault should be empty"
    assert os.path.exists(vpath),        "vault file should exist on disk after creation"

    # unlock with the correct password
    result = unlock_vault(vpath, "master1234")
    assert result is not None,           "correct password should unlock successfully"
    unlocked_key, unlocked_data = result
    assert unlocked_key == key,          "session key should be deterministic for same password+salt"
    assert unlocked_data == {},          "unlocked vault data should match what was saved"

    # wrong password must return None — not raise
    bad = unlock_vault(vpath, "wrongpassword")
    assert bad is None,                  "wrong password should return None, not raise"

    # missing vault file must return None — not raise
    missing = unlock_vault("/tmp/no_vault_here.enc", "anypassword")
    assert missing is None,              "missing vault file should return None"

print("auth.py        ✓  all tests passed")