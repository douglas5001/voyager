from api import db
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    profile = db.relationship("Profile")

    def encrypt_password(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def show_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)
