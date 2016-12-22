# _______________________________________________________________________
# | File Name: views.py                                                 |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Aug 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

from openstack_dashboard.dashboards.rallyboard.test_reports import tabs as event_tabs
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.rallyboard.test_reports import tables
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from horizon import views
from horizon import tabs
from horizon import exceptions
from horizon.utils import memoized
from django.conf import settings
from sidecarclient import client
import requests
import json
from horizon import workflows
from openstack_dashboard.dashboards.rallyboard.test_reports import workflows as project_workflows
from openstack_dashboard.dashboards.rallyboard.test_reports import setting
import subprocess
import os
from openstack_dashboard import api


"""##################Setting the sidecar client##########################"""
sidecar = client.Client(
        username = getattr(settings, "SC_USERNAME"),
        password = getattr(settings, "SC_PASSWORD"),
        auth_url = getattr(settings, "SC_AUTH_URL"),
        region_name = getattr(settings, "SC_REGION_NAME"),
        tenant_name = getattr(settings, "SC_TENANT_NAME"),
        timeout = getattr(settings, "SC_TIMEOUT"),
        insecure = getattr(settings, "SC_INSECURE")
    )
default_value = setting.ConfigSetter()
"""#############################################"""
class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing ticket list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = event_tabs.ReportDisplayTab
    template_name   = "rally_dashboard/test_reports/index.html"
    page_title      = "Rally Tests"


def display_history_report(request, **kwargs):
    """
    # | Method to show the report 
    # |
    # | Arguments: 
    # |   <kwargs>: Dictionary
    # |
    # | Returns: NA
    """
    print("in the report")
    test_report =  sidecar.events.get_test_history(id=kwargs['history_id'])
    test_result = ''
    print('have result')
    print(test_report)
    print(test_report.__dict__)
    print(test_report.results)	
    test_result = ''
    if test_report.results != None:
        test_result = test_report.results

    #Displaying the report
    context = {
        "page_title": _("Test Report"),
        "test_report": test_result
    }
    return render(request, 'rally_dashboard/test_reports/view_report.html', context)


#def delete_history_report(request, **kwargs):
    """
    # | Method to show the report 
    # |
    # | Arguments: 
    # |   <kwargs>: Dictionary
    # |
    # | Returns: NA
    """
    """
    print("in the report")
    test_report =  sidecar.events.delete_test_history(id=kwargs['history_id'])
    print('have result')
    #Displaying the report
    context = {
        "page_title": _("Test Report"),
        "test_report": 'test_result'
    }
    return render(request, 'rally_dashboard/test_reports/view_report.html', context)
"""
