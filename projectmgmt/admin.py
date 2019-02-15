from django.contrib import admin
from models import *

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('no','name','manager',)

class ProjectApprovalAdmin(admin.ModelAdmin):
    list_display = ('handle_time','handler','project')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectApproval, ProjectApprovalAdmin)

