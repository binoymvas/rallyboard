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

from openstack_dashboard.dashboards.sidecar.events import tabs as event_tabs
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.sidecar.events import tables
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
from openstack_dashboard.dashboards.sidecar.events import workflows as project_workflows
from openstack_dashboard.dashboards.sidecar.events import setting
import subprocess
import os

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
"""#############################################"""
class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing ticket list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = event_tabs.EvacuationEventsTab
    template_name   = "rally_dashboard/events/index.html"
    page_title      = "Rally Tests"

def get_test_detail(request, **kwargs):
    """
    # | Function to get the test details
    # |
    # | Arguments: Kwargs: test id
    # |
    # | Returns: Template 
    """

    #Getting the test detaisl
    test_list = sidecar.events.tests_list(project_id=kwargs['test_id'], test_added=1)
    report_list = []
	
    #Creating the test details dictionary	
    for tests in test_list._logs:
	tests['report_url'] = ''
        if tests['results'].strip() != '':
            tests['report_url'] = tests['id']+'/report'
        report_list.append(tests)
	
    #Making the context for the template	
    context = {
        "page_title": _("Test Details"),
        "test_lists": report_list, #tests_listi
	"test_id": kwargs['test_id']
    }
    return render(request, 'rally_dashboard/events/test_lists.html', context)

def get_test_details(request, **kwargs):
    """
    # | Function to get the list
    # |
    # | Arguments: Kwargs: prpoject id
    # |
    # | Returns: Json object
    """
	
    #Values are taken from settings.py file
    test_list = sidecar.events.run_command(id=1)
    """"
    #Creating the command for the logs
    command = 'sudo cat /tmp/rally_dashboard.log'
    try:
        outputStr = subprocess.check_output(command, shell=True)
    except Exception, e:
    	print("Error in the command", e)
	outputStr = "Error in the command" + command
    """
    #Making the output
    #outputStr = " <br>".join(outputStr.split("\n"))
    context = {
        "page_title": _("Test Details"),
        "test_lists": 'report_list', #tests_list
	"log_data": 'outputStr'
    }
    
    return render(request, 'rally_dashboard/events/test_logs.html', context)

def get_log(request, **kwargs):
    """
    # | Function to get the logs
    # |
    # | Arguments: Kwargs: prpoject id
    # |
    # | Returns: Json object
    """

    #Creating the command for the logs 
    try:
	print(kwargs)
	print(request.GET['project_id'])
	outputStr = sidecar.events.test_logs(project_id=request.GET['project_id'])
	log_data = outputStr.log_data
	outputStr = " <br>".join(log_data.split("\n"))
    except Exception, e:
        outputStr = "Error while fetching the details from logs"	
    #Making the output
    context = {
        "page_title": _("Test Details"),
        "test_lists": 'report_list', #tests_list
        "log_data": outputStr
    }
    return render(request, 'rally_dashboard/events/test_logs.html', context)
    #return render(request, 'rally_dashboard/events/a.html', context)
    #return render(request, 'rally_dashboard/events/b.html', context)

def get_test_report(request, **kwargs):

    #Fetching the details of the selected event
    test_list = sidecar.events.test_report(project_id=kwargs['test_id'])
    report_list = []
    for tests in test_list._logs:
	json_test = json.loads(tests['data'])
	tests['success'] = json_test['success'] 
	tests['time'] = json_test['time']
	tests['test_cases'] = json_test['test_cases']
	report_list.append(tests)
    context = {
        "page_title": _("Test Results"),
        "tests": report_list
    }
    return render(request, 'rally_dashboard/events/test_detail.html', context)

def display_report(request, **kwargs):

    test_report = sidecar.events.test_report(id = kwargs['test_id'])
    test_result = ''
    for row in test_report._logs:
        test_result  =  row['results']

    print('+++++++++++++++++++++++') 
    print test_result
 
    #Displaying the report
    context = {
        "page_title": _("Test Report"),
        "test_report": test_result
    }
   
    return render(request, 'rally_dashboard/events/view_report.html', context)


def execute_testiii(request):
    print("hai")



class UpdateProjectView(workflows.WorkflowView):
    workflow_class = project_workflows.UpdateProject

    def get_initial(self):
        initial = super(UpdateProjectView, self).get_initial()
        default_value = setting.ConfigSetter()                
        #path = '/etc/tempest/tempest.conf'
        image_ref = default_value.get_setting('compute', 'image_ref')    
        flavor_ref = default_value.get_setting('compute', 'flavor_ref')
        initial["flavor_ref"] = flavor_ref
        initial['image_ref'] = image_ref
        initial['enabled'] = self.kwargs['event_id']
        self.event_id = self.kwargs['event_id']
        return initial
