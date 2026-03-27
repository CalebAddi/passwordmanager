from src.crypto import generate_salt, derive_key, encrypt, decrypt

salt = generate_salt()
key = derive_key("mypassword", salt)
ct = encrypt(key, b"hello world")
pt = decrypt(key, ct)
assert pt == b"hello world"
print("crypto works!")