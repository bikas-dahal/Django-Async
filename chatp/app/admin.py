from django.contrib import admin

from .models import Message, UserChannel

# Register your models here.
admin.site.register(Message)
admin.site.register(UserChannel)
