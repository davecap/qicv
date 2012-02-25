# -*- coding: utf-8 -*-
from django.contrib import admin
from cv.models import CV, CVViewPermission


class CVViewPermissionInline(admin.StackedInline):
    model = CVViewPermission


class CVAdmin(admin.ModelAdmin):
    inlines = [CVViewPermissionInline, ]


admin.site.register(CV, CVAdmin)
admin.site.register(CVViewPermission)
