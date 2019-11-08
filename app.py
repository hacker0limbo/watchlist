from flask import Flask
from routes.index import router as index_routes
from models.base_model import db
from commands import initdb, forge


def register_routes(app):
    app.register_blueprint(index_routes)


def config_app(app):
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    print(f'ENV is set to: {app.config["ENV"]}')


def register_commands(app):
    app.cli.add_command(initdb)
    app.cli.add_command(forge)


def create_app():
    app = Flask(__name__)

    # 注册路由
    with app.app_context():
        config_app(app)
        register_routes(app)
        db.init_app(app)

        register_commands(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
