# File Name: panel.py
#
# Software: Openstack Horizon [liberity]
#
# Dashboard Name: Sidecar
#
# Panel Name: events
#
# Start Date: 2016@nephoscale.com

from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.sidecar import dashboard
import horizon

class TestReports(horizon.Panel):
    name = _("Test Reports")
    slug = "test_reports"

dashboard.SidecarDashboard.register(TestReports)
