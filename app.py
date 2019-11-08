from flask import Flask
from routes.index import router as index_routes


def register_routes(app):
    app.register_blueprint(index_routes)


def config_app(app):
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    print(f'ENV is set to: {app.config["ENV"]}')


def create_app():
    app = Flask(__name__)
    # 注册路由
    config_app(app)
    register_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
