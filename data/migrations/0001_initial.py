# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 06:52
from __future__ import unicode_literals

import data.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CpuData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('cores', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'ordering': ('name', 'cores'),
            },
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EngineData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildFlags', models.CharField(blank=True, max_length=1024)),
                ('version', models.CharField(blank=True, max_length=64)),
                ('versionFull', models.CharField(blank=True, max_length=128)),
                ('versionPatchSet', models.CharField(blank=True, max_length=32)),
                ('wordSize', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ('versionFull', 'versionPatchSet'),
            },
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GlData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('glRenderer', models.CharField(blank=True, max_length=256)),
                ('glVendor', models.CharField(blank=True, max_length=256)),
                ('glVersion', models.CharField(blank=True, max_length=256)),
                ('glVersionShort', models.CharField(blank=True, max_length=128)),
                ('glewVersion', models.CharField(blank=True, max_length=256)),
                ('glslVersion', models.CharField(blank=True, max_length=256)),
                ('glslVersionShort', models.CharField(blank=True, max_length=128)),
                ('glSupportNonPowerOfTwoTex', models.NullBooleanField()),
                ('glSupportTextureQueryLOD', models.NullBooleanField()),
                ('glSupport24bitDepthBuffer', models.NullBooleanField()),
                ('glSupportRestartPrimitive', models.NullBooleanField()),
                ('glSupportClipSpaceControl', models.NullBooleanField()),
                ('glSupportFragDepthLayout', models.NullBooleanField()),
            ],
            options={
                'ordering': ('glRenderer', 'glVersion'),
            },
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GpuData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpu', models.CharField(blank=True, max_length=256)),
                ('gpuMemorySize', models.PositiveIntegerField(blank=True, null=True)),
                ('gpuVendor', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'ordering': ('gpuVendor', 'gpu', 'gpuMemorySize'),
            },
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MachineData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=128)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('ram', models.PositiveIntegerField(blank=True)),
                ('cpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.CpuData')),
                ('engine_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.EngineData')),
                ('gl_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.GlData')),
                ('gpu_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.GpuData')),
            ],
            options={
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='OsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osFamily', models.CharField(max_length=32)),
                ('osName', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'ordering': ('osFamily', 'osName'),
            },
        ),
        migrations.CreateModel(
            name='PlatformData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ('attribute',),
            },
        ),
        migrations.CreateModel(
            name='ScreenData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolution_x', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('resolution_y', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('color_depth', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('refresh_rate', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('windowed', models.NullBooleanField()),
            ],
            options={
                'ordering': ('resolution_x', 'resolution_y', 'color_depth'),
            },
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SDLData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdlVersionCompiledMajor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sdlVersionCompiledMinor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sdlVersionCompiledPatch', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sdlVersionLinkedMajor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sdlVersionLinkedMinor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('sdlVersionLinkedPatch', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            bases=(data.models.FromLuaMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='sdldata',
            unique_together=set([('sdlVersionCompiledMajor', 'sdlVersionCompiledMinor', 'sdlVersionCompiledPatch', 'sdlVersionLinkedMajor', 'sdlVersionLinkedMinor', 'sdlVersionLinkedPatch')]),
        ),
        migrations.AlterUniqueTogether(
            name='screendata',
            unique_together=set([('resolution_x', 'resolution_y', 'color_depth', 'refresh_rate', 'windowed')]),
        ),
        migrations.AddField(
            model_name='machinedata',
            name='os',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.OsData'),
        ),
        migrations.AddField(
            model_name='machinedata',
            name='platform_data',
            field=models.ManyToManyField(to='data.PlatformData'),
        ),
        migrations.AddField(
            model_name='machinedata',
            name='screen_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.ScreenData'),
        ),
        migrations.AddField(
            model_name='machinedata',
            name='sdl_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.SDLData'),
        ),
        migrations.AlterUniqueTogether(
            name='cpudata',
            unique_together=set([('name', 'cores')]),
        ),
        migrations.AlterUniqueTogether(
            name='machinedata',
            unique_together=set([('account', 'cpu', 'os')]),
        ),
    ]
