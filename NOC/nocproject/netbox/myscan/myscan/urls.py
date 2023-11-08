

from django.urls import path
from .views import Add_Device_View

urlpatterns = [
    path('fast_add_device/', Add_Device_View.as_view(), name='fast_add_device'),
]
