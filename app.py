from flask import Flask
from routes.index import router as index_routes
from routes.error import page_not_found
from routes.api.v1 import router as api_routes
from models.base_model import db
from commands import initdb, forge, test
from context import register_context


def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(api_routes, url_prefix='/api/v1')
    # error pages
    app.register_error_handler(404, page_not_found)


def config_app(app):
    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
        # 自动 reload 模板引擎
        app.jinja_env.auto_reload = True
    print(f'ENV is set to: {app.config["ENV"]}')


def register_commands(app):
    app.cli.add_command(initdb)
    app.cli.add_command(forge)
    app.cli.add_command(test)


def create_app():
    # 使用工厂模式注册 app
    app = Flask(__name__)
    config_app(app)
    db.init_app(app)
    # 注册路由, 上下文, 命令
    register_routes(app)
    register_context(app)
    register_commands(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
