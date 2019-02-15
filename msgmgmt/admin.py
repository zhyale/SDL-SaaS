from django.contrib import admin
from models import Message, CircleMessage
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender','receiver','body','viewed',)
    list_filter = ('receiver',)

class CircleMessageAdmin(admin.ModelAdmin):
    list_display = ('sender','body',)

admin.site.register(Message, MessageAdmin)
admin.site.register(CircleMessage, CircleMessageAdmin)