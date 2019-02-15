from django.db import models
from django.contrib import admin
from models import Page, Comment
from django import forms


class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {
            'widget': forms.Textarea(attrs={'rows':6, 'cols':80})
        },
    }
    list_display = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('time', 'page', 'commenter', 'content',)


admin.site.register(Page, PageAdmin)
admin.site.register(Comment, CommentAdmin)

