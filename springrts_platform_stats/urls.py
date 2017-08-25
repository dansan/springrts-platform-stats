from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('api.urls')),
    url(r'^schema/$', get_schema_view(title='SpringRTS Platform Statistics API')),
    url(r'^docs/', include_docs_urls(title='My API service')),
]
