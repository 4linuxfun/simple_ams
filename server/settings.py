import casbin_sqlalchemy_adapter
import casbin
from typing import List
from pathlib import Path
from pydantic import BaseSettings
from sqlmodel import create_engine


class APISettings(BaseSettings):
    # token加密相关参数
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CASBIN_MODEL_PATH: str = "server/model.conf"
    # sql数据库信息
    DATABASE_URI = "mysql+pymysql://root:123456@192.168.137.129/devops"
    # 白名单，不需要进行任何验证即可访问
    NO_VERIFY_URL: List = [
        '/',
        '/api/login',
    ]


settings = APISettings()

engine = create_engine(settings.DATABASE_URI, future=False)
adapter = casbin_sqlalchemy_adapter.Adapter(engine)
casbin_enforcer = casbin.Enforcer(settings.CASBIN_MODEL_PATH, adapter)