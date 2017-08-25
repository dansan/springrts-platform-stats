# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework import serializers
from data.models import CpuData, EngineData, GlData, GpuData, MachineData, OsData, PlatformData, ScreenData, SDLData
from data.serializers import MachineDataSerializer
from .models import Machine
from springrts_platform_stats.logging import logger


class MachineSerializer(serializers.ModelSerializer):
    platformData = serializers.DictField(
        required=False,
        help_text='JSON Object, e.g.: {"glslVersion": "4.50 NVIDIA", "gpu": "GeForce GTX 760/PCIe/SSE2"}'
    )
    result = MachineDataSerializer(
        read_only=True,
        help_text='JSON object representing how the data was saved in the DB.'
    )

    class Meta:
        model = Machine
        fields = ('accountId', 'cpuName', 'osFamily', 'platformData', 'result')
        read_only_fields = ('result',)
        depth = 1

    def create(self, validated_data):
        """
        Save POST data in data.models.* objects instead of an
        api.models.Machine object. (But return a not-saved one to satisfy
        the protocol.)

        :param validated_data: dict with validated POST data
        :return: api.models.Machine object (unsaved)
        """
        logger.debug('validated_data=%r', validated_data)
        accountid = validated_data['accountId']
        accountid_hash = MachineData.mkhash(accountid)
        cpu_name = validated_data['cpuName']
        os_family = validated_data['osFamily']
        platform_data = validated_data.get('platformData', {})
        for field_name in ('accountId', 'cpuName', 'osFamily'):
            # handle data in wrong place
            try:
                del platform_data[field_name]
            except KeyError:
                pass
        ram = platform_data.pop('ram', 0)
        cpu_obj, _ = CpuData.objects.get_or_create(
            name=cpu_name,
            cores=platform_data.pop('cpuCores', '')
        )
        os_obj, _ = OsData.objects.get_or_create(
            osFamily=os_family,
            osName=platform_data.pop('osName', '')
        )

        machine, self.machine_data_created = MachineData.objects.get_or_create(
            account=accountid_hash,
            cpu__name=cpu_name,
            os__osFamily=os_family,
            defaults={
                'account': accountid_hash,
                'cpu': cpu_obj,
                'os': os_obj,
                'ram': ram,
            }
        )
        if not self.machine_data_created:
            machine.ram = ram

        # create objects from classifiable POST data
        old_objs = list()
        for attr_name, kls in (
                ('engine_data', EngineData),
                ('gl_data', GlData),
                ('gpu_data', GpuData),
                ('screen_data', ScreenData),
                ('sdl_data', SDLData),
        ):
            obj = kls.from_api_dict(platform_data)
            if obj:
                old_obj = getattr(machine, attr_name)
                if old_obj != obj:
                    old_objs.append(old_obj)
                setattr(machine, attr_name, obj)
                # remove attributes used in current object from POST data
                for field_name in kls.get_lua_field_names():
                    try:
                        del platform_data[field_name]
                    except KeyError:
                        pass

        # save the remaining POST data in generic key-value objects
        for k, v in platform_data.items():
            platform_data_obj, _c = PlatformData.objects.get_or_create(attribute=k, value=v)
            try:
                associated_attr = machine.platform_data.get(attribute=k)
                if associated_attr.value != v:
                    associated_attr.value = v
                    associated_attr.save()
            except PlatformData.DoesNotExist:
                machine.platform_data.add(platform_data_obj)

        # remove generic data that was associated with machine, but is not in
        # the input data anymore
        for pd in machine.platform_data.exclude(attribute__in=platform_data.keys()):
            machine.platform_data.remove(pd)
            old_objs.append(pd)

        machine.save()

        # remove objects that are not referenced by any machine anymore
        old_objs = [oo for oo in old_objs if oo and not oo.machinedata_set.exists()]
        if old_objs:
            logger.info('Deleting not referenced objects: %r.', old_objs)
        for old_obj in old_objs:
            old_obj.delete()

        # don't actually save the API object (Machine.objects.create(**data))
        # but return a valid object
        return Machine(accountId=accountid, cpuName=cpu_name, osFamily=os_family)
