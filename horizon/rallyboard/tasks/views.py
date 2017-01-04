# _______________________________________________________________________
# | File Name: views.py                                                 |
# |                                                                     |
# | This file is for handling the views of Rally tasks display          |
# |_____________________________________________________________________|
# | Start Date: Aug 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
from openstack_dashboard.dashboards.rallyboard.tasks import tabs as tasks_tabs
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
import json
from horizon import workflows
from openstack_dashboard.dashboards.rallyboard.tasks import workflows as project_workflows
from openstack_dashboard.dashboards.rallyboard.tasks import setting
from openstack_dashboard import api

#Setting the connections
sidecar_conn = setting.sidecar_conn()
default_value = setting.ConfigSetter()

class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing Tasks list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = tasks_tabs.RallyTab
    template_name   = "rally_dashboard/tasks/index.html"
    page_title      = "Rally Tests"

def get_test_detail(request, **kwargs):
    """
    # | Function to get the list of test added
    # |
    # | Arguments: Kwargs: project id and the test added
    # |
    # | Returns: Json object
    """
    
    #Getting the list of test added to the project
    test_list = sidecar_conn.events.tests_list(project_id=kwargs['test_id'], test_added=1)
    test_lists = []
    for tests in test_list._logs:
        test_lists.append(tests)

    #Sending the list to the template
    context = {
        "page_title": _("Approved Test List"),
        "test_lists": test_lists,
        "test_id": kwargs['test_id'],
        "report_url": '../'+kwargs['test_id']+'/report'
    }
    return render(request, 'rally_dashboard/tasks/test_lists.html', context)

def run_tests(request, **kwargs):
    """
    # | Function to get the list
    # |
    # | Arguments: Kwargs: project id
    # |
    # | Returns: Json object
    """

    #Making the run list and startign the execution
    test_list = sidecar_conn.events.run_command(id=kwargs['test_id'])
    
    #Sending the details to the template
    context = {
        "page_title": _("Test Details"),
        "test_lists": 'report_list',
        "log_data": 'Starting the execution of the tests added...'
    }
    return render(request, 'rally_dashboard/tasks/test_logs.html', context)

def get_log(request, **kwargs):
    """
    # | Function to get the logs
    # |
    # | Arguments: Kwargs: project id
    # |
    # | Returns: Json object
    """
     
    try:
        
        #Getting the logs using the project id 
        output_str = sidecar_conn.events.test_logs(project_id=request.GET['project_id'])
        log_data = output_str.log_data
        output_str = " <br>".join(log_data.split("\n"))
    except Exception, e:
        output_str = "Updating the logs..."
    
    #Making the output and sending to template
    context = {
        "log_data": output_str
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

    #Fetching the details of the selected test using the project id
    test_list = sidecar_conn.events.test_report(project_id=kwargs['test_id'])
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
     
    try:
        
        #Getting the report of the tests using the project id
        outputStr = sidecar_conn.events.test_logs(project_id=kwargs['project_id'])
        outputStr = outputStr.results
    except Exception, e:
        outputStr = "Updating the logs..."
    
    #Making the output and sending to the template
    context = {
        "page_title": _("Test Report"),
        "test_report": outputStr
    }
    return render(request, 'rally_dashboard/tasks/view_report.html', context)

class UpdateProjectConfig(workflows.WorkflowView):
    """
    # | IndexView for showing configuration details 
    """
    workflow_class = project_workflows.UpdateConfig

    def get_initial(self):
        """
        # | Function to get the initial values of the configuration
        # |
        # | Arguments: Self
        # |
        # | Returns: initial values
        """
        
        #Getting and setting the initial values
        initial = super(UpdateProjectConfig, self).get_initial()
        image_ref = default_value.get_setting('compute', 'image_ref')    
        flavor_ref = default_value.get_setting('compute', 'flavor_ref')
        initial["flavor_ref"] = flavor_ref
        initial['image_ref'] = image_ref
        initial['enabled'] = self.kwargs['project_id']
        self.event_id = self.kwargs['project_id']
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
            msg = _('Unable to retrieve tasks details.')
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
        #image_ref = default_value.get_setting('compute', 'image_ref')    
        #flavor_ref = default_value.get_setting('compute', 'flavor_ref')

        image_ref  = sidecar_conn.events.get_test_config_value(option_name='image_name')
        flavor_ref  = sidecar_conn.events.get_test_config_value(option_name='flavor_name')
	
        initial.update({'test_id': self.kwargs['test_id'], 'image_ref': image_ref, 'flavor_ref': flavor_ref})
        return initial
