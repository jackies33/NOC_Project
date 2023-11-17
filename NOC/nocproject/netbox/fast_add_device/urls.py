

from django.urls import path
from .views import Add_Device_View

urlpatterns = [
    path('add_device/', Add_Device_View.as_view(), name='add_device'),
]
