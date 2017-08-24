# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework import mixins, status as http_status, viewsets
from rest_framework.response import Response
from .models import Machine
from .serializers import MachineSerializer
from data.serializers import MachineDataSerializer


class Machines(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Create or update Machine data (POST-only).

    * `accountId`: integer (The users lobby account ID, e.g. 521734.)
    * `cpuName`: string (CPU Family, e.g. "Intel i7-7700K CPU @ 4.20GHz".)
    * `osFamily`: string (The installed OS family, one of "Windows", "Linux",
    "MacOSX", "FreeBSD", "Unknown".)
    * `platformData`: JSON Object (e.g.: {"ram": 1024, "glslVersion": "4.50
    NVIDIA", "gpu": "GeForce GTX
    760/PCIe/SSE2"})

    `accountId`, `cpuName` and `osFamily` are required and together define a
    unique machine entry.

    If the request succeeded, `HTTP 200 OK` will be returned, if an existing
    machine object was updated or `HTTP 201 Created` if a new object was
    created.

    An additional field `result` will be added to the returned resource,
    showing how the transmitted data was saved to the database.

    In the HTML API view, the "HTML form" tab does not support transmitting
    `platformData`. Use the "Raw data" tab.
    """
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    @classmethod
    def _remove_ids(cls, resource):
        try:
            del resource['id']
        except KeyError:
            pass
        for k, v in resource.items():
            if isinstance(v, list):
                resource[k] = [cls._remove_ids(val) for val in v]
            elif isinstance(v, dict):
                resource[k] = cls._remove_ids(v)
        return resource

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        headers = self.get_success_headers(data)
        machine_data = serializer.instance.get_machine_data_object()
        serialized_machine_data = MachineDataSerializer(machine_data).data
        data['result'] = self._remove_ids(serialized_machine_data)
        if getattr(serializer, 'machine_data_created', True):
            status = http_status.HTTP_201_CREATED
        else:
            status = http_status.HTTP_200_OK
        return Response(data, status=status, headers=headers)
