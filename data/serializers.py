# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from rest_framework import serializers
from .models import MachineData


class MachineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineData
        exclude = ('account', 'id')
        depth = 1
