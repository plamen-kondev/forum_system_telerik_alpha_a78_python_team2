from app.database import read_query, insert_query, update_query
from app.models.user import User, Role

# Column order must match User.from_row()
_USER_COLUMNS = "id, first_name, last_name, email, username, password_hash, role, is_blocked, created_at"


def _first_or_none(rows: list[tuple]) -> User | None:
    return User.from_row(rows[0]) if rows else None



def get_by_id(user_id: int) -> User | None:
    rows = read_query(f"SELECT {_USER_COLUMNS} FROM users WHERE id = ?", (user_id,))
    return _first_or_none(rows)


def get_by_username(username: str) -> User | None:
    rows = read_query(f"SELECT {_USER_COLUMNS} FROM users WHERE username = ?", (username,))
    return _first_or_none(rows)


def get_by_email(email: str) -> User | None:
    rows = read_query(f"SELECT {_USER_COLUMNS} FROM users WHERE email = ?", (email,))
    return _first_or_none(rows)


def search(query: str, limit: int = 50, offset: int = 0) -> list[User]:
    pattern = f"%{query}%"
    rows = read_query(
        f"""SELECT {_USER_COLUMNS} FROM users
            WHERE username LIKE ? OR email LIKE ? OR first_name LIKE ? OR last_name LIKE ?
            ORDER BY username
            LIMIT ? OFFSET ?""",
        (pattern, pattern, pattern, pattern, limit, offset),
    )
    return [User.from_row(row) for row in rows]


def count_all() -> int:
    return read_query("SELECT COUNT(*) FROM users")[0][0]



def create(first_name: str, last_name: str, email: str, username: str, password_hash: str) -> int:
    return insert_query(
        """INSERT INTO users (first_name, last_name, email, username, password_hash)
           VALUES (?, ?, ?, ?, ?)""",
        (first_name, last_name, email, username, password_hash),
    )


def update_profile(user_id: int, first_name: str, last_name: str, email: str) -> int:
    return update_query(
        "UPDATE users SET first_name = ?, last_name = ?, email = ? WHERE id = ?",
        (first_name, last_name, email, user_id),
    )


def set_blocked(user_id: int, is_blocked: bool) -> int:
    return update_query("UPDATE users SET is_blocked = ? WHERE id = ?", (is_blocked, user_id))


def set_role(user_id: int, role: Role) -> int:
    return update_query("UPDATE users SET role = ? WHERE id = ?", (role.value, user_id))


def delete(user_id: int) -> int:
    return update_query("DELETE FROM users WHERE id = ?", (user_id,))