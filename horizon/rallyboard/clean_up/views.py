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
from openstack_dashboard.dashboards.rallyboard.clean_up import tabs as history_tabs
from django.utils.translation import ugettext_lazy as _
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from horizon import tabs
from horizon import exceptions
from horizon.utils import memoized
from horizon import workflows
import subprocess
import shlex

class IndexView(tabs.TabbedTableView):
    """
    # | IndexView for showing ticket list 
    # |
    # | Code is in tabs.py 
    """
    tab_group_class = history_tabs.ReportDisplayTab
    template_name   = "rally_dashboard/clean_up/index.html"
    page_title      = "Rally Tests History"

def cleanproject(request, **kwargs):
    """
    # | Method to show the report 
    # |
    # | Arguments: 
    # |   <kwargs>: Dictionary
    # |
    # | Returns: NA
    """

    #Getting the history using the id
    #Making the command for the test execution
    cmd = 'ospurge --dry-run --cleanup-project rallyTestProject'
    res = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
    output, err = res.communicate()
    print(output)

    #Displaying the report
    context = {
        "page_title": _("Resources Clean"),
        "test_report": output
    }
    return render(request, 'rally_dashboard/clean_up/list_resource.html', context)