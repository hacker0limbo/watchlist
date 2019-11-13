from flask import Blueprint

router = Blueprint('api_v1_bp', __name__)

# 需要在注册蓝图之后导入引用蓝图的包
from routes.api.v1 import movie
