from django.urls import path
from chat.views import chat

app_name = 'chat'

urlpatterns = [
    path('', chat, name='chat')
]
