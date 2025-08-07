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


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}