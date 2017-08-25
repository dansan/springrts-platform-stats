# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from passlib.hash import pbkdf2_sha256
from django.db import models
from django.conf import settings
from springrts_platform_stats.logging import logger


class FromLuaMixin(object):
    """
    Must be used with a models.Model subclass. All its fields must have set "blank=True".
    """
    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.fields if f.name != 'id']

    @classmethod
    def from_api_dict(cls, api_request_data, **kwargs):
        logger.debug('%s api_request_data=%r kwargs=%r', cls.__name__, api_request_data, kwargs)
        if not api_request_data:
            return None
        for field_name in cls.get_lua_field_names():
            try:
                kwargs[field_name] = api_request_data[field_name]
            except KeyError:
                pass
        if kwargs:
            obj, _ = cls.objects.get_or_create(**kwargs)
            return obj
        else:
            return None

    @classmethod
    def get_lua_field_names(cls):
        return cls.get_field_names()


class CpuData(FromLuaMixin, models.Model):
    name  = models.CharField(max_length=128)
    cores = models.CharField(max_length=32, blank=True)

    def __unicode__(self):
        return "CpuData({!r}, {!r}, {!r})".format(self.pk, self.name, self.cores)

    @classmethod
    def get_lua_field_names(cls):
        return 'cpuName', 'cpuCores'

class Meta:
        unique_together = ('name', 'cores')
        ordering = ('name', 'cores')


class GlData(FromLuaMixin, models.Model):
    glRenderer                = models.CharField(max_length=256, blank=True)
    glVendor                  = models.CharField(max_length=256, blank=True)
    glVersion                 = models.CharField(max_length=256, blank=True)
    glVersionShort            = models.CharField(max_length=128, blank=True)
    glewVersion               = models.CharField(max_length=256, blank=True)
    glslVersion               = models.CharField(max_length=256, blank=True)
    glslVersionShort          = models.CharField(max_length=128, blank=True)
    glSupportNonPowerOfTwoTex = models.NullBooleanField(blank=True, null=True)
    glSupportTextureQueryLOD  = models.NullBooleanField(blank=True, null=True)
    glSupport24bitDepthBuffer = models.NullBooleanField(blank=True, null=True)
    glSupportRestartPrimitive = models.NullBooleanField(blank=True, null=True)
    glSupportClipSpaceControl = models.NullBooleanField(blank=True, null=True)
    glSupportFragDepthLayout  = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return "GlData({!r}, {!r}, {!r})".format(self.pk, self.glRenderer, self.glVersion)

    class Meta:
        # MySQL: #1071 - Specified key was too long; max key length is 767 bytes
        # unique_together = ('glRenderer', 'glVendor', 'glVersion', 'glVersionShort', 'glewVersion', 'glslVersion', 'glslVersionShort', 'glSupportNonPowerOfTwoTex', 'glSupportTextureQueryLOD', 'glSupport24bitDepthBuffer', 'glSupportRestartPrimitive', 'glSupportClipSpaceControl', 'glSupportFragDepthLayout')
        ordering = ('glRenderer', 'glVersion')


class GpuData(FromLuaMixin, models.Model):
    gpu           = models.CharField(max_length=256, blank=True)
    gpuMemorySize = models.PositiveIntegerField(blank=True, null=True)  # size of total GPU memory in MBs; only available for "Nvidia", (rest are 0)
    gpuVendor     = models.CharField(max_length=256, blank=True)  # one of "Nvidia", "Intel", "ATI", "Mesa", "Unknown"

    def __unicode__(self):
        return "GpuData({!r}, {!r}, {!r}, {!r})".format(self.pk, self.gpu, self.gpuMemorySize, self.gpuVendor)

    class Meta:
        # MySQL: #1071 - Specified key was too long; max key length is 767 bytes
        # unique_together = ('gpuVendor', 'gpu', 'gpuMemorySize')
        ordering = ('gpuVendor', 'gpu', 'gpuMemorySize')


class OsData(models.Model):
    osFamily = models.CharField(max_length=32)  # one of "Windows", "Linux", "MacOSX", "FreeBSD", "Unknown"
    osName   = models.CharField(max_length=256, blank=True)  # full name of the OS

    def __unicode__(self):
        return "OsData({!r}, {!r}, {!r})".format(self.pk, self.osFamily, self.osName)

    class Meta:
        # MySQL: #1071 - Specified key was too long; max key length is 767 bytes
        # unique_together = ('osFamily', 'osName')
        ordering = ('osFamily', 'osName')


class PlatformData(models.Model):
    attribute = models.CharField(max_length=128)
    value     = models.CharField(max_length=1024)

    def __unicode__(self):
        return "PlatformData({!r}, {!r}, {!r})".format(self.pk, self.attribute, self.value)

    class Meta:
        # MySQL: #1071 - Specified key was too long; max key length is 767 bytes
        # unique_together = ('attribute', 'value')
        ordering = ('attribute',)


class ScreenData(FromLuaMixin, models.Model):
    resolution_x = models.PositiveSmallIntegerField(blank=True, null=True)
    resolution_y = models.PositiveSmallIntegerField(blank=True, null=True)
    color_depth  = models.PositiveSmallIntegerField(blank=True, null=True)
    refresh_rate = models.PositiveSmallIntegerField(blank=True, null=True)
    windowed     = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return "ScreenData({!r}): {!r}x{!r}:{!r}bit @{!r}Hz ({!r})".format(
            self.pk, self.resolution_x, self.resolution_y, self.color_depth, self.refresh_rate,
            'windowed' if self.windowed else 'fullscreen')

    class Meta:
        unique_together = ('resolution_x', 'resolution_y', 'color_depth', 'refresh_rate', 'windowed')
        ordering = ('resolution_x', 'resolution_y', 'color_depth')


class SDLData(FromLuaMixin, models.Model):
    sdlVersionCompiledMajor = models.PositiveSmallIntegerField(blank=True, null=True)
    sdlVersionCompiledMinor = models.PositiveSmallIntegerField(blank=True, null=True)
    sdlVersionCompiledPatch = models.PositiveSmallIntegerField(blank=True, null=True)
    sdlVersionLinkedMajor   = models.PositiveSmallIntegerField(blank=True, null=True)
    sdlVersionLinkedMinor   = models.PositiveSmallIntegerField(blank=True, null=True)
    sdlVersionLinkedPatch   = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('sdlVersionCompiledMajor', 'sdlVersionCompiledMinor', 'sdlVersionCompiledPatch', 'sdlVersionLinkedMajor', 'sdlVersionLinkedMinor', 'sdlVersionLinkedPatch')

    def __unicode__(self):
        return "SDLData({!r}, sdlVersionCompiledMajor={!r}, .., .., sdlVersionLinkedMajor={!r}, .., ..)".format(
            self.pk, self.sdlVersionCompiledMajor, self.sdlVersionLinkedMajor)


class MachineData(models.Model):
    account       = models.CharField(max_length=128)
    updated       = models.DateTimeField(auto_now=True)
    cpu           = models.ForeignKey(CpuData)
    os            = models.ForeignKey(OsData)
    ram           = models.PositiveIntegerField(blank=True)
    gl_data       = models.ForeignKey(GlData, blank=True, null=True)
    gpu_data      = models.ForeignKey(GpuData, blank=True, null=True)
    screen_data   = models.ForeignKey(ScreenData, blank=True, null=True)
    sdl_data      = models.ForeignKey(SDLData, blank=True, null=True)
    platform_data = models.ManyToManyField(PlatformData)

    def __unicode__(self):
        return "MachineData({!r}, {!r}, {!r}, {!r})".format(
            self.pk, self.account, self.cpu.name, self.os.osFamily)

    class Meta:
        unique_together = ('account', 'cpu', 'os')
        ordering = ('-updated',)

    @staticmethod
    def mkhash(value):
        return pbkdf2_sha256.using(salt=settings.ACCOUNT_SALT, rounds=100000).hash(str(value))


def purge_not_associated():
    for kls in (CpuData, OsData, GlData, GpuData, ScreenData, SDLData, PlatformData):
        objs = kls.objects.exclude(id__in=MachineData.objects.values_list('platform_data__id', flat=True))
        if objs.exists():
            logger.warn('Deleting: %s', '\n'.join(objs))
            objs.delete()
