from django.urls import path
from .views import TemplateDataView

urlpatterns = [
    path(r'<q>', TemplateDataView.as_view())
]
