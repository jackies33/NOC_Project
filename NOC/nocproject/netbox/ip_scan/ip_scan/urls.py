


from django.urls import path
from .views import ip_address

urlpatterns = [
    path('ip_address_scan/', ip_address, name='ip_address'),
    path('ip_address_scan/network.png' , ip_address, name='ip_address')
]

"""
urlpatterns = [
    path('devices/ipscan', views.IpScan.as_view(), name='random_animal'),
]
"""



