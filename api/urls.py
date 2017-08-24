# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'machine', views.Machines)
urlpatterns = router.urls
