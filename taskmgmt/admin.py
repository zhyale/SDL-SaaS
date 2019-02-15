from django.contrib import admin
from taskmgmt.models import *


# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('assign_time','project', 'name', 'leader', 'status')
    list_filter = ('project',)


class TaskApprovalAdmin(admin.ModelAdmin):
    list_display = ('task', 'handler')


class CheckItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'flow', 'sort_no','product_type',)
    list_filter = ('flow',)
    ordering = ('flow', 'product_type', 'sort_no',)


class CheckResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'check_item', 'result',)
    list_filter = ('task',)


class CustomCheckResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'check_item', 'result',)
    list_filter = ('task',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskApproval, TaskApprovalAdmin)
admin.site.register(CheckItem, CheckItemAdmin)
admin.site.register(CheckResult, CheckResultAdmin)
admin.site.register(CustomCheckResult, CustomCheckResultAdmin)
