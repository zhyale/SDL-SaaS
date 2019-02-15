from django.contrib import admin
from models import *


class WikiAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'expression')

admin.site.register(Wiki, WikiAdmin)
