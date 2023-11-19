import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import config
from identity_manager import IdentityManager


class Gram:

    def __init__(self, identity_manager: IdentityManager):
        self._idm = identity_manager
        self._bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
        self._dp = Dispatcher(storage=MemoryStorage())
        self._router = Router()
        self._dp.include_router(self._router)
        self._router.message.register(self.message_handler)
        self._router.channel_post.register(self.message_handler)

    async def connect(self):
        await self._bot.delete_webhook(drop_pending_updates=True)
        await self._dp.start_polling(self._bot, allowed_updates=self._dp.resolve_used_update_types())

    async def send(self, receiver: str, msg: str):
        _logger.debug(f"Send a message '{msg}' to {receiver}")
        if receiver not in self._idm:
            raise ReceiverNotFound(f'Receiver {receiver} not found')
        await self._bot.send_message(self._idm[receiver], msg)

    async def message_handler(self, msg: Message):
        _logger.debug(f"Got a message '{msg!r}'")
        if msg.from_user is not None:
            self._idm[f'@{msg.from_user.username}'] = msg.from_user.id
            _logger.debug(f"Add the user name '{msg.from_user.username}'")
        if msg.chat is not None and msg.chat.id < 0:
            self._idm[f'#{msg.chat.full_name}'] = msg.chat.id
        _logger.debug(f"Add the group/channel name '{msg.chat.full_name}'")
        if msg.chat is not None and msg.chat.id > 0:
            self._idm[f'@{msg.chat.username}'] = msg.chat.id
            _logger.debug(f"Add the user name '{msg.chat.username}'")
        self._idm.save()

    async def _start_polling(self):
        await self._dp.start_polling(self._bot, allowed_updates=self._dp.resolve_used_update_types())


class ReceiverNotFound(Exception):
    pass


_logger = logging.getLogger(__name__)
