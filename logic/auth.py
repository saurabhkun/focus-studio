import hashlib
from logic.database import get_user_by_username, create_user

def hash_password(password: str) -> str:
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(username: str, password: str, display_name: str, avatar_color: str) -> tuple[bool, str]:
    """Registers a new user."""
    if not username or not password:
        return False, "Username and password cannot be empty."
    
    existing = get_user_by_username(username)
    if existing:
        return False, "Username already exists."
    
    hashed = hash_password(password)
    try:
        create_user(username, hashed, display_name, avatar_color)
        return True, "Registration successful."
    except Exception as e:
        return False, f"Error creating user: {e}"

def login(username: str, password: str) -> tuple[bool, str, dict]:
    """Validates login and returns user dictionary if successful."""
    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password.", None
    
    hashed = hash_password(password)
    if user['password_hash'] == hashed:
        return True, "Login successful.", user
    else:
        return False, "Invalid username or password.", None
