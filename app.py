from flask import Flask
from flask_login import LoginManager

from routes.index import router as index_routes
from routes.error import page_not_found
from routes.api.v1 import router as api_routes
from models.base_model import db
from commands import initdb, forge, test, new_user
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
    app.cli.add_command(new_user)


def init_app(app):
    db.init_app(app)

    from models.user import User
    login_manager = LoginManager()
    login_manager.init_app(app)
    # 设置未登录时跳转到登录页面, 以及 flash message
    login_manager.login_view = 'index_bp.login'
    login_manager.login_message = 'Please log in first.'
    login_manager.login_message_category = 'danger'

    # 提供回调函数用于重新加载在 session 里面的用户
    @login_manager.user_loader
    def load_user(user_id):
        # 用 ID 作为 User 模型的主键查询对应的用户
        user = User.query.get(int(user_id))
        return user


def create_app():
    # 使用工厂模式注册 app
    app = Flask(__name__)
    config_app(app)
    init_app(app)
    # 注册路由, 上下文, 命令
    register_routes(app)
    register_context(app)
    register_commands(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
