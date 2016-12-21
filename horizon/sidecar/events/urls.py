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
from openstack_dashboard.dashboards.sidecar.events import views
"""
urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<test_id>[^/]+)/runtest$', views.get_test_detail, name="run_test"),
    url(r'^(?P<test_id>[^/]+)/runtests$', views.get_test_details, name="run_tests"),
    url(r'^get_log$', views.get_log, name="get_log"),
    #url(r'^(?P<test_id>[^/]+)/update/$', views.UpdateProjectView.as_view(), name='update'),
    #url(r'^(?P<event_id>[^/]+)/update/$', views.UpdateView.as_view(), name='update'),
    url(r'^(?P<test_id>[^/]+)/update_list/$', views.UpdateView.as_view(), name='update_list'),
    #url(r'^(?P<event_id>[^/]+)/update_list/$', views.UpdateProjectView.as_view(), name='update_list'),
    url(r'^(?P<test_id>[^/]+)/testreport/$', views.get_test_report, name="test_report"),
    #url(r'^(?P<test_id>[^/]+)/$', views.UpdateProjectView.as_view(), name='update'),
    url(r'^(?P<test_id>[^/]+)/report/$', views.display_report, name="report"),
)
"""
urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<test_id>[^/]+)/runtest$', views.get_test_detail, name="run_test"),
    url(r'^(?P<test_id>[^/]+)/runtests$', views.get_test_details, name="run_tests"),
    url(r'^get_log$', views.get_log, name="get_log"),
    #url(r'^(?P<event_id>[^/]+)/update/$', views.UpdateProjectView.as_view(), name='update'),
    #url(r'^(?P<event_id>[^/]+)/update_list/$', views.UpdateProjectView.as_view(), name='update_list'),
    url(r'^(?P<test_id>[^/]+)/update_list/$', views.UpdateView.as_view(), name='update_list'),
    url(r'^(?P<test_id>[^/]+)/testreport/$', views.get_test_report, name="test_report"),
    url(r'^(?P<event_id>[^/]+)/$', views.UpdateProjectView.as_view(), name='update'),
    url(r'^(?P<project_id>[^/]+)/report/$', views.display_report, name="report"),
    url(r'^project_report/$', views.project_report, name="project_report"),    
)
