from django.contrib import admin
from models import *
# Register your models here.

class RemindAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'remind_method', 'is_finished',)
    list_filter = ('is_finished', 'remind_method', )


class DeadlineRemindAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'remind_method', )
    list_filter = ('is_finished', )


class PeriodRemindAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'remind_method', )
    list_filter = ('is_finished', )


class OneTimeRemindAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'remind_method', )
    list_filter = ('is_finished', )


class RemindLogAdmin(admin.ModelAdmin):
    list_display = ('log_time', 'remind', 'seconds_delta', )


admin.site.register(Remind, RemindAdmin)
admin.site.register(DeadlineRemind, DeadlineRemindAdmin)
admin.site.register(PeriodRemind, PeriodRemindAdmin)
admin.site.register(OneTimeRemind, OneTimeRemindAdmin)
admin.site.register(RemindLog, RemindLogAdmin)
