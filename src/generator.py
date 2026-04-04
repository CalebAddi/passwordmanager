from __future__ import annotations

import secrets
import string


#region Char Constants ---------------|

LOWERCASE   = string.ascii_lowercase          
UPPERCASE   = string.ascii_uppercase          
DIGITS      = string.digits                   
SYMBOLS     = string.punctuation         

#endregion ----------------------------|

#region Pword Generation -------------|

def generate_password(
    length: int = 20,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    char_pool = LOWERCASE
    guaranteed = list(secrets.choice(LOWERCASE))

    if use_uppercase: 
        char_pool += UPPERCASE
        guaranteed.append(secrets.choice(UPPERCASE))

    if use_digits:
        char_pool += DIGITS
        guaranteed.append(secrets.choice(DIGITS))

    if use_symbols:
        char_pool += SYMBOLS
        guaranteed.append(secrets.choice(SYMBOLS))

    remaining = list(secrets.choice(char_pool) for _ in range(length - len(guaranteed)))
    password_list = guaranteed + remaining
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)

#endregion ----------------------------|