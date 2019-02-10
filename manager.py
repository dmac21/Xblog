# -*- coding: utf-8 -*-
# @Author  : dmac


from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from config import config
from app import create_app, db
from app.models import Role, User, Article, Comment, Articletype, Articlesource

app = create_app(config)

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Article=Article, Comment=Comment, Articletype=Articletype, Articlesource=Articlesource)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()