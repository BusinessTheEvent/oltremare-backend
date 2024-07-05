from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Receive, Scope, Send


class AuthCookieMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        ## FIXME: do not know if it works also with httpS, check it later
        if scope['type'] == 'http':
            request = Request(scope, receive=receive)
            auth_token = request.cookies.get("auth_token")

            if auth_token:
                ## NOTE: 'authorization' must be all lowercase to work
                scope['headers'].append((b'authorization', f'{auth_token}'.encode()))

        await self.app(scope, receive, send)
    
    