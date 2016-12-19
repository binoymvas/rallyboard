# _______________________________________________________________
# |  File Name: urls.py                                         |
# |                                                             |
# | Software: Openstack Horizon Dashboard ['liberity']          |
# |_____________________________________________________________|
# |                                                             |
# | Dashboard Name: Sidecar                                     |
# |                                                             |
# | Copyright: 2016@nephoscale.com                              |
# |_____________________________________________________________|
from django.conf.urls import patterns
from django.conf.urls import url
from openstack_dashboard.dashboards.sidecar.test_reports import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
)
