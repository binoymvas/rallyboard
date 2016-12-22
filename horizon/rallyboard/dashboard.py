# File Name: dashboard.py
#
# Software: Openstack Horizon [liberity]
#
# Start Date: 31th Aug 2016
#
# Copyright: 2016@nephoscale.com

from django.utils.translation import ugettext_lazy as _
import horizon
class RallyDashboard(horizon.Dashboard):
    """ 
    Class to register the Customer Support dashboard to horizon
    """
    name   = _("Rally Tests")
    slug   = "rally_dashboard"
    panels = ('tasks', 'test_reports', ) 
    default_panel = 'tasks'
    permissions = ('openstack.roles.admin',)

horizon.register(RallyDashboard)
