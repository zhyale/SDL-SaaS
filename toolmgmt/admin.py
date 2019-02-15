from django.contrib import admin

# Register your models here.
from models import IpSegment


class IpSegmentAdmin(admin.ModelAdmin):
    list_display = ('ip_start', 'ip_end', 'address')


admin.site.register(IpSegment, IpSegmentAdmin)