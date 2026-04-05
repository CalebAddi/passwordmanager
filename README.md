# Password Managerizer

This is a secure local password manager utilizing AES-256-GCM encryption and Argon2id key derivation. Passwords are stored in an encrypted vault file on disk... the master password is never stored or hashed anywhere. The vault itself acts as the proof of authentication: if decryption succeeds, the password was correct.

---

## Requirements

- Python 3.10+
- pip

---

## Installation

```bash
git clone https://github.com/CalebAddi/passwordmanager.git
cd passwordmanager
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip3 install -r requirements.txt
```

---

### First Launch — Creating Your Vault

When you run the app for the first time, no vault file exists yet. You will be prompted to create one.

1. Enter a master password in the first field.
2. Confirm it in the second field.
3. Click **Create**.

A new encrypted vault is created at `data/vault.enc` and you are taken directly to the main screen.

<img width="400" height="300" alt="createvault" src="https://github.com/user-attachments/assets/15bfa65b-1d6c-4ed6-93bb-cef2949b2a39" />

---

### Main Screen

The main screen displays a table of all stored entries with columns for **Service**, **Username**, and **Password**. Passwords are masked as `********` in the table at all times.

---

### Adding a Password Entry

1. Click **Add Entry**.
2. Fill in the **Service** (e.g. `github`), **Username**, and **Password** fields.
   - Alternatively, check **Generate password** to auto-fill a cryptographically secure random password.
3. Click **Save**.

The vault is re-encrypted and saved to disk. The table refreshes with the new entry.

---

### Copying a Password

1. Click on a row in the table to select it.
2. Click **Copy Password**.

The real password is retrieved from the vault and copied to your clipboard. A confirmation message will appear. The password is never displayed on screen.

---

### Deleting a Password Entry

1. Click on the entry you want to remove.
2. Click **Delete Entry**.
3. Confirm the deletion in the dialog that appears.

The entry is removed, the vault is re-encrypted, and the table refreshes.

---

### Changing Your Master Password

1. Click **Change Master Password**.
2. Enter your **current** master password.
3. Enter and confirm your **new** master password.
4. Click **Change Password**.

If the current password is incorrect you will see an error and the dialog stays open. On success, the entire vault is re-encrypted under the new password with a freshly generated salt.

---

### Locking the Vault

Click **Lock** in the top right corner of the main screen. This returns you to the login screen. The session key is discarded and the vault cannot be accessed again without the master password.

---

<img width="400" height="300" alt=pwordmanagerexample src="https://github.com/user-attachments/assets/fce8ef42-e84a-45df-ad94-04136ff3bfd1" />

---

<img width="400" height="300" alt="changepw" src="https://github.com/user-attachments/assets/abc179b7-a7fb-4a3b-8a44-a7c2e8960f40" />
