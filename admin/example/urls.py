from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/templates/', include('mailing.api.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
]
