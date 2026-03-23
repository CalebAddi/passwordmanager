"""
Responsibilities:
  - Generate cryptographically secure random passwords
  - Allow configurable character sets and length

Design notes:
  - Use the `secrets` module — not `random`. The `random` module is not used for passwords or keys.
  - Functions here are pure — same configuration options can produce
    different outputs each call, but there are no side effects.

TODO: Implement the following functions.
"""

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
    """
    Generate a cryptographically secure random password.

    Args:
        length:        Number of characters in the password.
        use_uppercase: Include uppercase letters.
        use_digits:    Include numeric digits.
        use_symbols:   Include special characters.

    Returns:
        A random password string.

    Raises:
        ValueError if the resulting character pool is empty or length < 8.

    After building the character pool, I will need to make sure that
        at least one character from each selected category appears in the
        output. gotta do that without making the rest of the
        password predictable. (secrets.SystemRandom().shuffle or
        build a list and shuffle it.)
    """
    pass  # TODO

#endregion ----------------------------|