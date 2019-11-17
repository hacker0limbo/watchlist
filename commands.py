import click
from coverage import Coverage
from flask.cli import with_appcontext

from models.base_model import db
from models.user import User
from models.movie import Movie

# 使用 click + with_appcontext 防止循环引用
@click.command()
@click.option('--drop', is_flag=True, help='Create after drop')
@with_appcontext
def initdb(drop):
    """初始化数据库表的 schema"""
    if drop:
        # 如果命令为 initdb --drop, 删除所有表并重新建立
        db.drop_all()
    # 普通情况下 initdb 创建数据库表
    db.create_all()
    click.echo('Initialized database.')


@click.command()
@with_appcontext
def forge():
    """产生 mock 数据"""
    username = 'admin'
    password = 'admin'

    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    # 生成一个测试用户
    u = User.new(username=username)
    u.set_hash_password(password)

    for m in movies:
        form = {
            'title': m['title'],
            'year': m['year'],
        }
        Movie.new(form)
    click.echo('Mock data generated.')


@click.command()
@with_appcontext
def test():
    """运行测试"""
    import unittest
    from tests.test_app import TestApp
    from tests.test_db import TestDb
    from tests.test_commands import TestCommands
    from tests.test_index_page import TestIndexPage
    from tests.test_settings_page import TestSettingsPage
    from tests.test_error_page import TestErrorPage

    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDb))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestApp))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCommands))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIndexPage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSettingsPage))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestErrorPage))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    click.echo('All tests finished')


@click.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
@with_appcontext
def new_user(username, password):
    """手动生成新的用户数据"""
    click.echo('Creating new user...')
    user = User.new(username=username)
    user.set_hash_password(password)
    click.echo('Done.')


@click.command()
@click.option('--html', is_flag=True, help='generate html report')
@click.pass_context
@with_appcontext
def coverage(ctx, html):
    """输出覆盖率测试"""
    cov = Coverage(
        source=["app", "commands", "routes/", "models"],
        omit=["*__init__*"])
    cov.start()
    # 触发测试命令
    ctx.invoke(test)
    cov.stop()
    cov.save()

    click.echo('Coverage summary:')
    cov.report()
    if html:
        cov.html_report(directory="reports/coverage/")
    cov.erase()
