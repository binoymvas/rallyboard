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

#Importing the required packages
from openstack_dashboard.dashboards.rallyboard.test_reports import tabs as history_tabs
from django.utils.translation import ugettext_lazy as _
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from horizon import tabs
from horizon import exceptions
from horizon.utils import memoized
from horizon import workflows
from openstack_dashboard.dashboards.rallyboard.tasks import setting

#Setting the connections
sidecar_conn = setting.sidecar_conn()
default_value = setting.ConfigSetter()

class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing ticket list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = history_tabs.ReportDisplayTab
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

    #Getting the history using the id
    test_report =  sidecar_conn.events.get_test_history(id=kwargs['history_id'])
    test_results = ''
    if test_report.results != None:
        test_results = test_report.results

    #Displaying the report
    context = {
        "page_title": _("Test Report"),
        "test_report": test_results
    }
    return render(request, 'rally_dashboard/test_reports/view_report.html', context)