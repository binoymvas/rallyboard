 _______________________________________________________________________
# | File Name: dashboard.py                                             |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Nov 16th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
from django.utils.translation import ugettext_lazy as _
import horizon
class RallyDashboard(horizon.Dashboard):
    """ 
    Class to register the Customer dashboard to horizon
    """
    name   = _("Rally Tests")
    slug   = "rally_dashboard"
    panels = ('tasks', 'test_reports', ) 
    default_panel = 'tasks'
    permissions = ('openstack.roles.admin',)
horizon.register(RallyDashboard)