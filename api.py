import asyncio
import logging

from fastapi import APIRouter
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send

from gram import Gram

_logger = logging.getLogger(__name__)


class Message(BaseModel):
    receiver: str
    body: str


class Api:
    def __init__(self, gram: Gram):
        self._gram = gram
        self._fastapi = FastAPI(on_startup=[self._start_gram])
        self._router = APIRouter()
        self._router.add_api_route("/message", self._post_message, methods=["POST"])
        self._fastapi.include_router(self._router, prefix="/api")

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await self._fastapi(scope, receive, send)

    async def _start_gram(self):
        asyncio.create_task(self._gram.connect())
        _logger.debug('Starting Gram')

    async def _post_message(self, msg: Message):
        await self._gram.send(msg.receiver, msg.body)
