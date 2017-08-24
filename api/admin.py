# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from .models import Machine


class MachineAdmin(admin.ModelAdmin):
    list_display = ('accountId', 'id', 'cpuName', 'osFamily')
    search_fields = ['accountId', 'id', 'cpuName', 'osFamily']


admin.site.register(Machine, MachineAdmin)
