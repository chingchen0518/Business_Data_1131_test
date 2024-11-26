from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        # 進行異步執行，將當前的用於將當前 WebSocket 的 channel_name 添加到指定的group
        # 用異步執行的原因是因爲有大量用戶連接時，當一個 WebSocket 連接等待數據時，服務器可以處理其他連接，而不會浪費資源
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        self.accept()

    # 從group移除chatroom
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event={
            'type':'message_handler',
            'message_id': message.id,
        }

        # 將一個事件發送到特定的聊天室組
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,event
        )

    def message_handler(self,event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }

        html = render_to_string("partials/chat_message_p.html", context=context)
        self.send(text_data=html)
