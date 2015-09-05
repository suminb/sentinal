import os

from flask import Flask


def create_app(name=__name__, config={},
               static_folder='sentinal/static',
               template_folder='sentinal/templates'):

    app = Flask(name, static_folder=static_folder,
                template_folder=template_folder)
    app.secret_key = 'fc683cd9ed1990ca2ea10b84e5e6fba048c24929'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

    app.config.update(config)

    from sentinal.models import db
    db.init_app(app)

    from sentinal.main import main_module
    app.register_blueprint(main_module, url_prefix='/')

    return app
