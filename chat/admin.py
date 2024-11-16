from django.contrib import admin
from .models import PublicChatRoom, Message, PrivateChatRoom, PrivateMessage
# Register your models here.
admin.site.register(PublicChatRoom)
admin.site.register(Message)
admin.site.register(PrivateChatRoom)
admin.site.register(PrivateMessage)