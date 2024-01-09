from flask import Flask
from models import User, db
from werkzeug.security import  generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        user1 = User(username = 'odmen', password = generate_password_hash('12345'), email = 'odmen@odmen.odmen', role = 'admin')

        db.session.add_all([user1])
        db.session.commit()