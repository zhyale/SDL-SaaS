from django.contrib import admin
from models import *
from django.forms import TextInput, Textarea


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('top_domain_name','name',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','company',)


class UserAdmin(admin.ModelAdmin):
    #resize the input control in HTML
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'200'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':80})},
    }
    list_display = ('username','salt','hashpwd','last_login_time',)
    list_filter = ('company',)


class DayStatAdmin(admin.ModelAdmin):
    list_display = ('date', 'pv', 'uv',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(DayStat, DayStatAdmin)
