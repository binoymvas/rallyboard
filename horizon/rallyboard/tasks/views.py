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

from openstack_dashboard.dashboards.rallyboard.tasks import tabs as event_tabs
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.rallyboard.tasks import tables
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
from openstack_dashboard.dashboards.rallyboard.tasks import workflows as project_workflows
from openstack_dashboard.dashboards.rallyboard.tasks import setting
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
    tab_group_class = event_tabs.EvacuationEventsTab
    template_name   = "rally_dashboard/tasks/index.html"
    page_title      = "Rally Tests"

def get_test_detail(request, **kwargs):

    test_list = sidecar.events.tests_list(project_id=kwargs['test_id'], test_added=1)
    report_list = []
    for tests in test_list._logs:
	tests['report_url'] = ''
        if tests['results'].strip() != '':
            tests['report_url'] = tests['id']+'/report'
        report_list.append(tests)

    context = {
        "page_title": _("Test Details"),
        "test_lists": report_list, #tests_listi
	"test_id": kwargs['test_id'],
	"report_url": '../'+kwargs['test_id']+'/report'
    }
    return render(request, 'rally_dashboard/tasks/test_lists.html', context)

def get_test_details(request, **kwargs):
    """
    # | Function to get the list
    # |
    # | Arguments: Kwargs: prpoject id
    # |
    # | Returns: Json object
    """
	
    #Values are taken from settings.py file
    print("______________________________________________________________________")
    print(kwargs)
    print("______________________________________________________________________")
    test_list = sidecar.events.run_command(id=kwargs['test_id'])
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
    
    return render(request, 'rally_dashboard/tasks/test_logs.html', context)

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
        outputStr = "Updating the logs..."	
    #Making the output
    context = {
        "page_title": _("Test Details"),
        "test_lists": 'report_list', #tests_list
        "log_data": outputStr
    }
    return render(request, 'rally_dashboard/tasks/test_logs.html', context)

def project_report(request, **kwargs):
    """
    # | Function to get the logs
    # |
    # | Arguments: Kwargs: prpoject id
    # |
    # | Returns: Json object
    """

    #Creating the command for the logs 
    print("in the project_report ...........................................")
    outputStr = "Updating the logs..."
    #Making the output
    context = {
        "page_title": _("Test Details"),
        "test_lists": 'report_list', #tests_list
        "log_data": outputStr
    }
    return render(request, 'rally_dashboard/tasks/test_logs.html', context)


def get_test_report(request, **kwargs):
    """
    # | Function to display the report to the user
    # |
    # | Arguments: Kwargs: project id
    # | 
    # | Returns: Json object
    """ 
	
    #Fetching the details of the selected event
    test_list = sidecar.events.test_report(project_id=kwargs['test_id'])
    report_list = []
	
    #Creating the list for the report
    for tests in test_list._logs:
	json_test = json.loads(tests['data'])
	tests['success'] = json_test['success'] 
	tests['time'] = json_test['time']
	tests['test_cases'] = json_test['test_cases']
	report_list.append(tests)

    #Making the context and sending to template
    context = {
        "page_title": _("Test Results"),
        "tests": report_list
    }
    return render(request, 'rally_dashboard/tasks/test_detail.html', context)

def display_report(request, **kwargs):
    """
    # | Function to display the report to the user
    # |
    # | Arguments: Kwargs: project id
    # |
    # | Returns: Json object
    """

    #Getting the report of the tests 
    try:
        outputStr = sidecar.events.test_logs(project_id=kwargs['project_id'])
        outputStr = outputStr.results
    except Exception, e:
        outputStr = "Updating the logs..."
    
    #Making the output
    context = {
        "page_title": _("Test Report"),
        "test_report": outputStr
    }
    return render(request, 'rally_dashboard/tasks/view_report.html', context)

class UpdateProjectView(workflows.WorkflowView):
    #workflow_class = project_workflows.UpdateProject
    workflow_class = project_workflows.UpdateConfig

    def get_initial(self):
        initial = super(UpdateProjectView, self).get_initial()
        #default_value = setting.ConfigSetter()                
        #path = '/etc/tempest/tempest.conf'
        image_ref = default_value.get_setting('compute', 'image_ref')    
        flavor_ref = default_value.get_setting('compute', 'flavor_ref')
        initial["flavor_ref"] = flavor_ref
        initial['image_ref'] = image_ref
        initial['enabled'] = self.kwargs['event_id']
        self.event_id = self.kwargs['event_id']
        return initial

class UpdateView(workflows.WorkflowView):
    workflow_class = project_workflows.UpdateTest
    success_url = reverse_lazy("horizon:rally_dashboard:tasks:index")

    def get_context_data(self, **kwargs):
	"""
	# | Function to get the context data
   	# |
    	# | Arguments: Kwargs: test_id
    	# |
    	# | Returns: Json object
    	"""

	#Getting the context data
        context = super(UpdateView, self).get_context_data(**kwargs)
	print("in get_context_data end")
        context["test_id"] = kwargs['test_id'] 
        return context

    @memoized.memoized_method
    def get_object(self, *args, **kwargs):
	"""
        # | Function to get the object
        # |
        # | Arguments: Kwargs, args
        # |
        # | Returns: Json object
        """
	
        #Setting the test_id
	test_id = self.kwargs['test_id']
        try:
            return api.nova.server_get(self.request, test_id)
        except Exception:
            redirect = reverse("horizon:rally_dashboard:tasks:index")
            msg = _('Unable to retrieve instance details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
	"""
        # | Function to get the initial  data
        # |
        # | Arguments: Self
        # |
        # | Returns: Json object
        """
	
	#Getting the initial data and setting it
        initial = super(UpdateView, self).get_initial()
	image_ref = default_value.get_setting('compute', 'image_ref')    
        flavor_ref = default_value.get_setting('compute', 'flavor_ref')
        initial.update({'test_id': self.kwargs['test_id'], 'image_ref': image_ref, 'flavor_ref': flavor_ref})
        return initial

