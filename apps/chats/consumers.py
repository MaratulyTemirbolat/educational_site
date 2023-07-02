import json
from channels.generic.websocket import AsyncWebsocketConsumer
from typing import (
    Optional,
    Dict,
    Any,
)

from chats.models import (
    Message,
    PersonalChat,
)


class ChatConsumer(AsyncWebsocketConsumer):
    """ChatConsumer."""

    async def connect(
        self,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> None:
        """Get in touch with chat."""
        print("You are connected")
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.chat: Optional[PersonalChat] = None
        try:
            self.chat = await PersonalChat.objects.aget(id=self.chat_id)
        except Exception:
            self.chat = None

        if self.chat:
            self.chat_group_name = f'chat_{self.chat_id}'

            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )

            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'You are now connected!'
            }))

    # async def disconnect(
    #     self,
    #     code: int,
    #     *args: tuple[Any],
    #     **kwargs: dict[Any, Any]
    # ) -> None:
    #     """Disconnect."""
    #     if self.chat_group_name:
    #         await self.channel_layer.group_discard(
    #             self.chat_group_name,
    #             self.channel_name
    #         )
    #     else:
    #         return await super().disconnect(code)

    async def receive(
        self,
        text_data=None,
        bytes_data=None,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> None:
        """receive."""
        data: Dict[str, Any] = json.loads(s=text_data)
        content: Optional[str] = data.get('content', None)
        chat_id: Optional[int] = data.get('chat_id', None)
        user_id: Optional[int] = data.get('user_id', None)
        user: Optional[Any] = data.get('user', None)

        if content and user_id and chat_id and self.chat:
            await self.save_message(
                chat_id=chat_id,
                user_id=user_id,
                content=content
            )

            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'content': content,
                    'chat_id': chat_id,
                    'user_id': user_id,
                    'user': user,
                }
            )

    async def chat_message(self, event) -> None:
        """chat_message."""
        content: str = event['content']
        chat_id: int = event['chat_id']
        user_id: int = event['user_id']
        user: Any = event['user']

        await self.send(text_data=json.dumps(
            {
                'content': content,
                'chat': chat_id,
                'user_id': user_id,
                'user': user,
                "accepted": True
            }
        ))

    async def save_message(
        self,
        chat_id: int,
        user_id: int,
        content: str
    ) -> Any:
        """Save message in db."""
        return await Message.objects.acreate(
            content=content,
            to_chat_id=chat_id,
            owner_id=user_id
        )
