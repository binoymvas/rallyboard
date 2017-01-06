# _______________________________________________________________
# |  File Name: urls.py                                         |
# |                                                             |
# | Software: Openstack Horizon Dashboard ['liberity']          |
# |_____________________________________________________________|
# |                                                             |
# | Dashboard Name: RAlly Board                                 |
# |                                                             |
# | Copyright: 2016@nephoscale.com                              |
# |_____________________________________________________________|

#Importing the required packages
from django.conf.urls import patterns
from django.conf.urls import url
from openstack_dashboard.dashboards.rallyboard.test_reports import views

#Setting the url patterns
urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<history_id>[^/]+)/cleanproject/$', views.clean_all_project, name="cleanproject"),
)