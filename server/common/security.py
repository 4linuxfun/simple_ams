import logging

from loguru import logger
from datetime import datetime, timedelta
from fastapi import Request, WebSocket, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.websockets import WebSocket

from ..settings import settings

# to get a string like this run:
# openssl rand -hex 32


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_check(request: Request = None, ws: WebSocket = None):
    """
    检查是否有token信息，并在request.state中添加uid值
    :param request:
    :param ws:
    :return:
    """
    # websocket不需要验证
    if ws:
        return None
    logger.info(f'request url:{request.url} method:{request.method}')
    for url in settings['no_verify_url']:
        if url == request.url.path.lower():
            logger.debug(f"{request.url.path} 在白名单中，不需要权限验证")
            return True
    authorization: str = request.headers.get("Authorization")
    schema, param = get_authorization_scheme_param(authorization)
    if not authorization or schema.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")

    try:
        playload = jwt.decode(param, settings['secret_key'], settings['algorithm'])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    uid = playload.get('uid')
    # 在Request对象中设置用户对象，这样在其他地方就能通过request.state.uid获取当前用户id了
    request.state.uid = uid


def create_access_token(data):
    """
    生成token
    :param data:
    :return:
    """
    expires_delta = timedelta(minutes=settings['access_token_expire_minutes'])
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings['secret_key'], algorithm=settings['algorithm'])
    return encoded_jwt
