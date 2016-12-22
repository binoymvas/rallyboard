# File Name: dashboard.py
#
# Software: Openstack Horizon [liberity]
#
# Start Date: 31th Aug 2016
#
# Copyright: 2016@nephoscale.com

from django.utils.translation import ugettext_lazy as _
import horizon
class SidecarDashboard(horizon.Dashboard):
    """ 
    Class to register the Customer Support dashboard to horizon
    """
    name   = _("Rally Tests")
    slug   = "rally_dashboard"
    panels = ('events', 'test_reports', ) 
    default_panel = 'events'
    permissions = ('openstack.roles.admin',)

horizon.register(SidecarDashboard)
