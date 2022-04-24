import os
from flask import Flask
from flask import g, request
from flask_sqlalchemy import SQLAlchemy

from config import Config

from app.utils.toolkit import create_id
from app.utils.api_expections import *

BASE_DIR = os.getcwd()
print(BASE_DIR)


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
config = Config()
config.init_app(app)
db = SQLAlchemy()
db.init_app(app)


"""
WEB 异常处理
"""


@app.errorhandler(413)
def handle_not_found_413(e):
    if request.path.startswith('/api/v1/'):
        return RequestEntityTooLarge('请求体过大，服务器无法完成对应操作')
    return e


@app.errorhandler(414)
def handle_not_found_414(e):
    if request.path.startswith('/api/v1/'):
        return QueryParamsTooLong('参数过长，服务器无法处理')
    return e


@app.errorhandler(404)
def handle_not_found_404(e):
    if request.path.startswith('/api/v1/'):
        return URLNotFound('URL 不存在，请检查 URL')
    return e


@app.errorhandler(405)
def handle_request_method_405(e):
    if request.path.startswith('/api/v1/'):
        return RequestMethodError("请求方法有误，暂不支持该请求方法")
    return e


@app.errorhandler(500)
def handle_internal_server_error(e):
    """500 错误打印堆栈信息"""
    print("<InternalServerError>:[detail: %s]" % str(e))
    return InternalServerError(message="内部服务器错误")


@app.errorhandler(APIException)
def handle_api_error(e):
    return e


@app.before_request
def before_set():
    """每个请求前设置 traceId"""
    try:
        trace_id = request.headers['TRACE_ID']
    except:
        trace_id = "trace_id-{0}".format(create_id())
    g.trace_id = trace_id


@app.after_request
def after_set(response):
    response.headers['TRACE_ID'] = g.trace_id
    return response


@app.after_request
def cors_headers(response):
    origin = request.headers.get('Origin')
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"] = "Authorization,Access-Control-Allow-Origin,Content-Type,Cookie," \
                                          "Cache-Control,Connection,Accept-Language,Accept-Encoding,Accept," \
                                          "Pragma,Referer,User-Agent,Host,Accept-Charset"
    response.headers[
        "Access-Control-Allow-Methods"] = "GET,POST,HEAD,OPTIONS,TRACE,CONNECT,PROXY"
    response.headers["Access-Control-Allow-Origin"] = origin
    return response


