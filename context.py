def register_context(app):
    # 注册全局的 context 变量

    @app.context_processor
    def inject_values():
        return dict(
            author_name_en='Limboer',
            author_name_zh='小夜勃',
        )
