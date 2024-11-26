from django.urls import path
from .consumers import *

websocket_urlpatterns =[
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
]


# ↑ 定義了 WebSocket 路由，用於將 WebSocket 請求與 Django 中的 WebSocket 消費者（ChatroomConsumer）進行映射。具體來說，這是在配置 ASGI 應用 的 WebSocket 路由，並通過 path() 函數來設置 URL 模式。
#再問chat