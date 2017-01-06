# _______________________________________________________________________
# | File Name: panel.py                                                 |
# |                                                                     |
# | This file is for handling the clean up of the projects created by rally|
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

class CleanProject(horizon.Panel):
    name = _("Clean Project")
    slug = "clean_project"
    
#Registering the class
dashboard.RallyDashboard.register(CleanProject)