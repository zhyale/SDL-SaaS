from django.contrib import admin
from flowmgmt.models import *


# Register your models here.
class ProjectFlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProjectPhaseAdmin(admin.ModelAdmin):
    list_display = ('flow', 'phase', 'next_phase', 'sort_no',)
    ordering = ('flow', 'sort_no',)
    list_filter = ('flow',)


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('phase', 'status')
    list_filter = ('phase',)


class ProjectOptionAdmin(admin.ModelAdmin):
    list_display = ('status', 'do', 'opinion',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProjectApprovalAdmin(admin.ModelAdmin):
    list_display = ('project', 'option')



class TaskFlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','flow','pre_status','next_status',)
    ordering = ('flow', 'sort_no',)
    list_filter = ('flow',)

class TaskOptionAdmin(admin.ModelAdmin):
    list_display = ('status', 'do','opinion',)
    list_filter = ('status',)


admin.site.register(Phase, PhaseAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
admin.site.register(TaskOption, TaskOptionAdmin)
admin.site.register(ProjectPhase, ProjectPhaseAdmin)
admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(ProjectOption, ProjectOptionAdmin)
admin.site.register(ProjectFlow, ProjectFlowAdmin)
admin.site.register(TaskFlow, TaskFlowAdmin)
