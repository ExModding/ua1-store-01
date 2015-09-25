from app import app, db, models
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

def make_shell_context():
    return dict(app=app, db=db)


manager = Manager(app)

manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
