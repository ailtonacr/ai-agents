import bcrypt
from model.user import User


class AuthService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def verify_password(plain_password: str, hashed_password_with_salt: bytes) -> bool:
        plain_password_bytes = plain_password.encode('utf-8')
        try:
            return bcrypt.checkpw(plain_password_bytes, hashed_password_with_salt)
        except ValueError:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')

    def register_user(self, username: str, password: str, email: str | None = None) -> tuple[bool, str]:
        if not username or not password:
            return False, 'Usuário e senha são obrigatórios.'
        if len(password) < 6:
            return False, 'Senha deve ter pelo menos 6 caracteres.'

        hashed_password = self.get_password_hash(password)
        is_first_user = self.db.count_users() == 0
        role = 'admin' if is_first_user else 'user'

        user = User(username, None, email, role, True, hashed_password)

        if self.db.create_user(user):
            if is_first_user:
                return True, f'Usuário admin "{username}" registrado com sucesso! Faça o login.'
            return True, f'Usuário "{username}" registrado com sucesso! Faça o login.'
        else:
            return False, 'Nome de usuário ou email já existe.'

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.db.get_user_by_username(username)
        if not user:
            return None
        if not user.is_active:
            return None
        row = self.db.fetch_one('SELECT hashed_password FROM users WHERE username = %s', (username,))
        if not row:
            return None
        stored_hashed_password_bytes = row['hashed_password'].encode('utf-8')
        if not self.verify_password(password, stored_hashed_password_bytes):
            return None
        return user
