import os


DEBUG = True

# Configuração do banco de dados PostgreSQL
USERNAME = "root"
PASSWORD = "SenhaForte123"
SERVER = "localhost"
PORT = "5432"
DB = "jpa"

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "aplicacao_flask"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
USER_AVATAR_DIR = os.path.join(UPLOADS_DIR, "avatars")

MAX_CONTENT_LENGTH = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}