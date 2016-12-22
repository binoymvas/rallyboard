# File Name: panel.py
#
# Software: Openstack Horizon [liberity]
#
# Dashboard Name: Rally board
#
# Panel Name: Test Report
#
# Start Date: 2016@nephoscale.com

from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.rallyboard import dashboard
import horizon

class TestReports(horizon.Panel):
    name = _("Test Reports")
    slug = "test_reports"
dashboard.RallyDashboard.register(TestReports)
