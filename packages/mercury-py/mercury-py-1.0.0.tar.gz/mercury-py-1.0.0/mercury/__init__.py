# coding=utf-8

from .services.database_sql import init_app as init_database_sql
from .services.database_nosql_mongo import init_app as init_database_nosql_mongo
from .services.auth import init_app as init_auth
from .services.tasks import init_app as init_tasks
from .services.tasks.notification import init_app as init_notification

from os import path, makedirs

from flask import Flask, send_from_directory
from flask_restful import Api

api = Api()


def create_app():
    """Application factory.

    :return: An application instance.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists
    try:
        if not path.isdir(app.instance_path):
            makedirs(app.instance_path)
            raise Exception('Directory not found, so just created. Put file "config.py" inside, please.')
    except OSError as ex:
        app.logger.error(str(ex))
    except Exception as ex:
        app.logger.exception(str(ex))

    from instance.config import ProductionConfig, DevelopmentConfig
    if app.env == 'production':
        app.config.from_object(ProductionConfig(app))  # Load the production instance config
    else:
        app.config.from_object(DevelopmentConfig(app))  # Load the development instance config

    init_database_sql(app)
    init_database_nosql_mongo(app)

    init_auth(app)

    # Load routes after load other services
    from .services.routes import init_api
    init_api(api)
    api.init_app(app)

    init_tasks(app)
    init_notification(app)

    # Base page for check if service is ready
    @app.route(f'/mercury/api/')
    def index():
        """Return Mercury index page.

        :return: Mercury index page.
        """
        return f'Mercury online!'

    @app.route('/favicon.ico')
    def favicon():
        """Return Mercury favicon.ico.

        :return: Mercury favicon.ico.
        """
        return send_from_directory(path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.cli.command('info')
    def info():
        """Print Mercury info.

        :return: Mercury info.
        """
        print(f'Mercury CLI ready!')

    return app
