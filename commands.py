import click
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
    name = 'Limboer'
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

    User.new({
        'name': name
    })
    for m in movies:
        Movie.new({
            'title': m['title'],
            'year': m['year'],
        })
    click.echo('Mock data generated.')
