from django.conf.urls import url
from dlc import views

urlpatterns = [
    url(r'^dlc/$', views.dlc_list),
    url(r'^dlc/(?P<pk>[0-9]+)/$', views.dlc_detail),
]