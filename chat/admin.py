from django.contrib import admin
from .models import PublicChatRoom, Message
# Register your models here.
admin.site.register(PublicChatRoom)
admin.site.register(Message)