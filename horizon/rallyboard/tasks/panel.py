# File Name: panel.py
#
# Software: Openstack Horizon [liberity]
#
# Dashboard Name: Rally Borad
#
# Panel Name: tasks
#
# Start Date: 2016@nephoscale.com

from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.rallyboard import dashboard
import horizon

class Tasks(horizon.Panel):
    name = _("Tasks")
    slug = "tasks"	
dashboard.RallyDashboard.register(Tasks)
