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
from openstack_dashboard.dashboards.rallyboard.clean_project import views

#Setting the url patterns
urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView, name='index'),
    url(r'^cleanproject$', views.clean_project, name="cleanproject"),
)
