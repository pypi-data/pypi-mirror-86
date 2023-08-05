from sqlalchemy.ext.declarative import DeclarativeMeta
from tornado.web import RequestHandler
from tornado.log import app_log
from tornado_models.sqlalchemy import SessionMixin, SQLAlchemy
from tornado_models.redis import RedisMixin, Redis
from tornado_models import as_future
from xml.etree import cElementTree as ET
from munch import munchify
import functools
import json


# 异步用户认证
def authenticated_async(f):
    @functools.wraps(f)
    async def wrapper(self, *args, **kwargs):
        self._auto_finish = False
        self.current_user = await self.get_current_user_async()
        if self.current_user is None:
            self.set_status(401, '登录超时')
            self.write_json(dict(code=401, status='FAIL', message='登录超时, 请重新登录', data=''))
        elif self.current_user is False:
            self.set_status(403, '禁止访问')
            self.write_json(dict(code=403, status='FAIL', message='Forbidden', data=''))
        else:
            await f(self, *args, **kwargs)
    return wrapper


class BaseRequestHandler(RedisMixin, SessionMixin, RequestHandler):
    def get(self):
        self.post()

    def post(self):
        self.forbidden()

    def forbidden(self):
        self.set_status(403, '禁止访问')
        ret_data = dict(code=403, status='FAIL', message='Forbidden', data='')
        self.write_json(data=ret_data)

    # 返回json格式字符串
    def write_json(self, data:dict):
        if isinstance(data, dict): data = json.dumps(data, ensure_ascii=False)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(data)

    # 返回xml格式字符串
    def write_xml(self, data:str):
        self.set_header("Content-Type", "text/xml; charset=UTF-8")
        self.finish(data)

    # 获取json格式请求参数
    def get_json_arguments(self):
        params = self.request.body
        if isinstance(params, bytes): params = params.decode('utf8')
        try:
            params = json.loads(params, encoding='utf8')
            params = isinstance(params, dict) and munchify(params) or {}
        except Exception as e:
            app_log.error(e)
            params = {}
        return params

    # 获取xml格式请求参数
    def get_xml_arguments(self):
        params = self.request.body
        if isinstance(params, bytes): params = params.decode('utf8')
        try:
            params = ET.fromstring(params)
        except Exception as e:
            app_log.error(e)
            params = None
        return params

    # 获取当前用户信息
    def get_current_user_async(self):
        pass


class BaseDBModel(SessionMixin):
    def __init__(self, db:SQLAlchemy=None):
        self.config = dict(db=db)
        super(BaseDBModel, self).__init__()


class BaseRedisModel(RedisMixin):
    def __init__(self, redis:Redis=None):
        self.config = dict(redis=redis)
        super(BaseRedisModel, self).__init__()
