from app import create_app, db
from config import ProductionConfig, DevelopmentConfig
from flask_script import Manager
from flask_migrate import MigrateCommand
from app.models import *
import unittest
from werkzeug.security import generate_password_hash

app = create_app(ProductionConfig)
manage = Manager(app)
manage.add_command('db', MigrateCommand)


@manage.command
def test():
    """Run unit tests."""
    tests = unittest.TestLoader().discover('app/tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=1).run(tests)


@manage.command
def create_db():
    db.create_all()


@manage.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(username=input('Login: '), email=input('Email: '),
                        password=generate_password_hash(input('Password: ')), admin=True))
    db.session.commit()


if __name__ == '__main__':
    manage.run()
