import os


# DEBUG = True

# Configuração do banco de dados PostgreSQL
# USERNAME = "root"
# PASSWORD = "SenhaForte123"
# SERVER = "localhost"
# PORT = "5432"
# DB = "jpa"

DEBUG = os.getenv("FLASK_ENV") == "development"

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
SERVER = os.getenv("DB_SERVER")
PORT = os.getenv("DB_PORT")
DB = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv("SECRET_KEY")


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024