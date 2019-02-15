from django.contrib import admin
from models import *


class AppTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IPAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MiddleWareTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DatabaseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class OsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ServerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StorageTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class NetworkDeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CIAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','category',)
    list_filter = ('category','company',)


class IntegrationRelationAdmin(admin.ModelAdmin):
    list_display = ('source','destination',)


class APPAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)
    list_filter = ('company',)


class MIDDLEWAREAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)


class DBAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)

class SERVICEAdmin(admin.ModelAdmin):
    list_display = ('name','service_name',)
    list_filter = ('company',)


class OSAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)


class SERVERAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)


class STORAGEAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)


class NETDEVAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('company',)


class ROOMAdmin(admin.ModelAdmin):
    list_display = ('name','city',)
    list_filter = ('company',)

admin.site.register(AppType, AppTypeAdmin)
admin.site.register(MiddleWareType, MiddleWareTypeAdmin)
admin.site.register(DatabaseType, DatabaseTypeAdmin)
admin.site.register(OsType, OsTypeAdmin)
admin.site.register(ServerType, ServerTypeAdmin)
admin.site.register(StorageType, StorageTypeAdmin)
admin.site.register(NetworkDeviceType, NetworkDeviceTypeAdmin)
admin.site.register(CI, CIAdmin)
admin.site.register(IntegrationRelation, IntegrationRelationAdmin)
admin.site.register(APP, APPAdmin)
admin.site.register(IP, IPAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(MIDDLEWARE, MIDDLEWAREAdmin)
admin.site.register(DB, DBAdmin)
admin.site.register(SERVICE, SERVICEAdmin)
admin.site.register(OS, OSAdmin)
admin.site.register(SERVER, SERVERAdmin)
admin.site.register(STORAGE, STORAGEAdmin)
admin.site.register(NETDEV, NETDEVAdmin)
admin.site.register(ROOM, ROOMAdmin)
