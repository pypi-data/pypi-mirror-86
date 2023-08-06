import asyncio
import logging
from operator import attrgetter
from pathlib import Path
from typing import Dict, Final, List, Optional, Union

import aiojobs
import attr
from aiojobs_protocols import SchedulerProtocol
from aiotgbot import (BaseFilter, BaseStorage, Bot, BotUpdate, Chat, Message,
                      ParseMode)
from aiotgbot.api_types import (InputMediaAudio, InputMediaDocument,
                                InputMediaPhoto, InputMediaVideo, User)

logger = logging.getLogger('feedback_bot')

ALBUM_WAIT_TIMEOUT = 1


def user_name(user_chat: Union[User, Chat]) -> str:
    if user_chat.first_name is None:
        raise RuntimeError('First name of private chat must be not empty')
    if user_chat.last_name is not None:
        return f'{user_chat.first_name} {user_chat.last_name}'
    else:
        return user_chat.first_name


def user_link(user_chat: Union[User, Chat]) -> str:
    return f'<a href="tg://user?id={user_chat.id}">{user_name(user_chat)}</a>'


async def set_chat(storage: BaseStorage, key: str,
                   chat: Optional[Chat] = None) -> None:
    await storage.set(key, chat.to_dict() if chat is not None else None)


async def get_chat(storage: BaseStorage, key: str) -> Optional[Chat]:
    data = await storage.get(key)
    return Chat.from_dict(data) if data is not None else None


async def set_chat_list(storage: BaseStorage, key: str,
                        chat_list: List[Chat]) -> None:
    await storage.set(key, [chat.to_dict() for chat in chat_list])


async def get_chat_list(storage: BaseStorage, key: str) -> List[Chat]:
    return [Chat.from_dict(item) for item in await storage.get(key)]


async def send_from_message(bot: Bot, chat_id: int, from_chat: Chat) -> None:
    await bot.send_message(chat_id, f'От {user_link(from_chat)}',
                           parse_mode=ParseMode.HTML)


@attr.s(slots=True)
class FromUserFilter(BaseFilter):

    async def check(self, bot: Bot, update: BotUpdate) -> bool:
        if 'admin_username' not in bot:
            raise RuntimeError('Admin username not set')

        return (update.message is not None and
                update.message.from_ is not None and
                update.message.from_.username != bot['admin_username'])


@attr.s(slots=True)
class FromAdminFilter(BaseFilter):

    async def check(self, bot: Bot, update: BotUpdate) -> bool:
        if 'admin_username' not in bot:
            raise RuntimeError('Admin username not set')

        return (update.message is not None and
                update.message.from_ is not None and
                update.message.from_.username == bot['admin_username'])


class AlbumForwarder:

    __slots__ = ('_queues', '_scheduler', '_bot')

    def __init__(self, bot: Bot) -> None:
        self._queues: Final[Dict[str, asyncio.Queue]] = {}
        self._scheduler: Optional[SchedulerProtocol] = None
        self._bot: Final[Bot] = bot

    async def add_message(self, message: Message,
                          chat_id: Optional[int] = None,
                          add_from_info: bool = False) -> None:
        if self._scheduler is None:
            raise RuntimeError('Album forwarder not started')
        if message.media_group_id is None:
            raise RuntimeError('Message in album must have media_group_id')
        if message.media_group_id in self._queues:
            self._queues[message.media_group_id].put_nowait(message)
        elif chat_id is not None:
            self._queues[message.media_group_id] = asyncio.Queue()
            self._queues[message.media_group_id].put_nowait(message)
            await self._scheduler.spawn(
                self._send(message.media_group_id, chat_id, add_from_info))
        else:
            logger.warning('Skip media group item as latecomer %s', message)

    async def _send(self, media_group_id: str, chat_id: int,
                    add_from_info: bool = False) -> None:
        assert media_group_id in self._queues
        media: List[Union[InputMediaAudio, InputMediaPhoto, InputMediaVideo,
                          InputMediaDocument]] = []
        from_chat: Optional[Chat] = None
        message_count: int = 0
        while True:
            try:
                message = await asyncio.wait_for(
                    self._queues[media_group_id].get(),
                    timeout=ALBUM_WAIT_TIMEOUT)
            except asyncio.TimeoutError:
                break
            assert isinstance(message, Message)
            message_count += 1
            from_chat = message.chat
            if message.audio is not None:
                media.append(InputMediaAudio(
                    media=message.audio.file_id,
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                    duration=message.audio.duration,
                    performer=message.audio.performer,
                    title=message.audio.title
                ))
            elif message.document is not None:
                media.append(InputMediaDocument(
                    media=message.document.file_id,
                    caption=message.caption,
                    caption_entities=message.caption_entities
                ))
            elif message.photo is not None:
                media.append(InputMediaPhoto(
                    media=max(message.photo,
                              key=attrgetter('file_size')).file_id,
                    caption=message.caption,
                    caption_entities=message.caption_entities
                ))
            elif message.video is not None:
                media.append(InputMediaVideo(
                    media=message.video.file_id,
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                    width=message.video.width,
                    height=message.video.height,
                    duration=message.video.duration
                ))
        if len(media) > 0:
            assert from_chat is not None
            if add_from_info:
                await send_from_message(self._bot, chat_id, from_chat)
            await self._bot.send_media_group(chat_id, media)
            await self._bot.send_message(
                from_chat.id, f'Переслано элементов группы: {len(media)}')
            logger.debug('Forwarded %d media group items', len(media))
        elif from_chat is not None:
            await self._bot.send_message(
                from_chat.id, 'Не удалось переслать элементов '
                              f'непоодерживаемого типа: {message_count}')
            logger.debug('Failed to forward %d media group items of '
                         'unsupported type', message_count)
        else:
            logger.debug('No media group items to forward')
        self._queues.pop(media_group_id)

    async def start(self) -> None:
        self._scheduler = await aiojobs.create_scheduler(
            close_timeout=float('inf'),
            exception_handler=self._scheduler_exception_handler)

    async def stop(self) -> None:
        if self._scheduler is None:
            raise RuntimeError('Album forwarder not started')
        await self._scheduler.close()
        assert len(self._queues) == 0

    @staticmethod
    def _scheduler_exception_handler(_, context):
        logger.exception('Album forward error', exc_info=context['exception'])


def path(_str: str) -> Path:
    return Path(_str)
