from models.user import User


def register_context(app):
    # 注册全局的 context 变量

    @app.context_processor
    def inject_values():
        user = User.query.first()
        return dict(
            user=user,
            author_name='小夜勃',
        )
