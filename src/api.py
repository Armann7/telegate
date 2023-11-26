import asyncio
import logging

from aiogram.utils import formatting
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
        Format of body:
            The first line - is a title
            The rest - is a message
        """
        if not receiver.startswith('@'):
            receiver = '#' + receiver
        body = await request.body()
        body_decoded = body.decode('utf8')
        lines = body_decoded.splitlines()
        _logger.debug(f"Got a message for {receiver}. Body:\n{body_decoded!r}")
        if len(lines) == 0:
            _logger.debug("Empty body")
            return
        if len(lines) > 1:
            msg = formatting.as_section(lines[0].strip(), '\n'.join(lines[1:]))
        else:
            msg = formatting.Text(body_decoded)
        await self._gram.send(receiver, msg)


_logger = logging.getLogger(__name__)
