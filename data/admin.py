# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from .models import CpuData, GlData, GpuData, MachineData, OsData, PlatformData, ScreenData, SDLData


class CpuDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'cores')
    search_fields = ['name', 'id', 'cores']
    list_filter = ('name',)


class GlDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'glVersion', 'glVendor')
    search_fields = ['id', 'glVersion', 'glVendor', 'glewVersion', 'glslVersion']
    list_filter = ('glVersion', 'glVendor')


class GpuDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'gpuVendor', 'gpu', 'gpuMemorySize')
    search_fields = ['id', 'gpuVendor', 'gpu', 'gpuMemorySize']
    list_filter = ('gpuVendor',)


class MachineDataAdmin(admin.ModelAdmin):
    list_display = ('account', 'id', 'cpu', 'os', 'updated')
    search_fields = ['account', 'id', 'cpu__name', 'os__osFamily', 'updated']
    list_filter = ('updated', 'os__osFamily', 'gpu_data__gpuVendor', 'gl_data__glVendor', 'cpu__name')


class OsDataAdmin(admin.ModelAdmin):
    list_display = ('osFamily', 'id', 'osName')
    search_fields = ['osFamily', 'id', 'osName']
    list_filter = ('osFamily', 'osName')


class PlatformDataAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value', 'id')
    search_fields = ['attribute', 'value', 'id']


class ScreenDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'resolution_x', 'resolution_y', 'color_depth', 'refresh_rate', 'windowed')
    search_fields = ['resolution_x', 'id', 'resolution_y', 'color_depth', 'refresh_rate']
    list_filter = ('resolution_x', 'resolution_y', 'color_depth', 'refresh_rate', 'windowed')


class SDLDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'sdlVersionCompiledMajor', 'sdlVersionLinkedMajor')
    search_fields = ['sdlVersionCompiledMajor', 'id', 'sdlVersionLinkedMajor']

admin.site.register(CpuData, CpuDataAdmin)
admin.site.register(GlData, GlDataAdmin)
admin.site.register(GpuData, GpuDataAdmin)
admin.site.register(MachineData, MachineDataAdmin)
admin.site.register(OsData, OsDataAdmin)
admin.site.register(PlatformData, PlatformDataAdmin)
admin.site.register(ScreenData, ScreenDataAdmin)
admin.site.register(SDLData, SDLDataAdmin)
