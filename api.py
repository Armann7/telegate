import asyncio
import logging

from fastapi import APIRouter
from fastapi import FastAPI
from starlette.requests import Request
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send

from gram import Gram


class Api:
    def __init__(self, gram: Gram):
        self._gram = gram
        self._fastapi = FastAPI(on_startup=[self._start_gram])
        self._router = APIRouter()
        self._router.add_api_route("/message/{receiver}", self._post_message, methods=["POST"])
        self._fastapi.include_router(self._router, prefix="/api")

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self._fastapi(scope, receive, send)

    async def _start_gram(self):
        asyncio.create_task(self._gram.connect())
        _logger.debug('Starting Gram')

    async def _post_message(self, receiver: str, request: Request):
        """
        Format of receiver:
            started with @ - username
            otherwise - group or channel name
        """
        if not receiver.startswith('@'):
            receiver = '#' + receiver
        body = await request.body()
        body_decoded = body.decode('utf8')
        _logger.debug(f"Got a message for {receiver}. Body:\n{body_decoded!r}")
        await self._gram.send(receiver, body_decoded)


_logger = logging.getLogger(__name__)
