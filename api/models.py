# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from data.models import MachineData


class Machine(models.Model):
    """
    Machine model that will be exposed through the HTTP API.

    No objects of this model will ever be saved. The models in data.models.*
    will be used by the serializer instead.
    """
    accountId = models.IntegerField(help_text='The users lobby account ID, e.g. 521734.')
    cpuName = models.CharField(max_length=128, help_text='CPU Family, e.g. "Intel i7-7700K CPU @ 4.20GHz".')
    osFamily = models.CharField(max_length=32, help_text='The installed OS family, e.g. "Linux", "Mac OS", "Windows".')

    def __unicode__(self):
        return "Machine(accountid={!r}, cpu={!r}, os={!r})".format(self.accountId, self.cpuName, self.osFamily)

    def get_machine_data_object(self):
        return MachineData.objects.get(
            account=MachineData.mkhash(self.accountId),
            cpu__name=self.cpuName,
            os__osFamily=self.osFamily
        )
