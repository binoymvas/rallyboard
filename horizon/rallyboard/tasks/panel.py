# _______________________________________________________________________
# | File Name: panel.py                                                 |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Nov 16th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the packages
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.rallyboard import dashboard
import horizon

class Tasks(horizon.Panel):
    name = _("Test Suites")
    slug = "tasks"
    
#Registering the class
dashboard.RallyDashboard.register(Tasks)
