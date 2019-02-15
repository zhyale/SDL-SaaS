from django.contrib import admin
from models import *
# Register your models here.


class HansReplaceItemAdmin(admin.ModelAdmin):
    list_display = ('chn_word','replaced_by',)


class AsciiReplaceItemAdmin(admin.ModelAdmin):
    list_display = ('asc_char','replaced_by',)

class DiceCodeAdmin(admin.ModelAdmin):
    list_display = ('sn','word',)

admin.site.register(HansReplaceItem, HansReplaceItemAdmin)
admin.site.register(AsciiReplaceItem, AsciiReplaceItemAdmin)
admin.site.register(DiceCode, DiceCodeAdmin)
