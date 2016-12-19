# File Name: tables.py
#
# Package Name: Openstack Horizon [liberity]
#
# Dashboardd: Sidecar
#
# Start Date: Aug 31th, 2016
#
# Copyright: 2016@nephoscale.com
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.http import urlencode
from openstack_dashboard import api
from openstack_dashboard import policy


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request):
        return '?'
        project_info = api.keystone.tenant_get(request, '5a4fb03113d44f7590789f9aa9ff3619' , admin=True)
        return project_info

class Runtest(tables.LinkAction):
    name = "runtests"
    verbose_name = _("Run test ")
    #url = "horizon:identity:projects:update"
    url = "horizon:rally_dashboard:events:update"
    #classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def get_link_url(self, testcase):
        step = 'runtest'
        base_url = reverse(self.url, args=[testcase.id])
        #param = urlencode({"step": step})
        return base_url+step

class TestReport(tables.LinkAction):
    name = "testsreport"
    verbose_name = _("Test Report")
    url = "horizon:rally_dashboard:events:update"
    #classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def get_link_url(self, testcase):
        step = 'testreport'
        base_url = reverse(self.url, args=[testcase.id])
        #param = urlencode({"step": step})
        return base_url+step
	#return "?".join([base_url, step])

class ViewReport(tables.LinkAction):
    name = "viewreport"
    verbose_name = _("View Report")
    url = "horizon:rally_dashboard:events:update"
    classes = ("ajax-model",)
    icon = "pencil"
    policy_rules  = (("identity",  "identity:list_users"),
                     ("identity",  "identity:list_roles"))

class DeleteReport(tables.LinkAction):
    name ="deletereport"
    verbose_name = _("Delete Report")
    url = "horizon:rally_dashboard:events:update"
    classes= ("ajax-model", )
    icon  = "pencil"
    policy_rules  = (("identity",  "identity:list_users"),
                     ("identity",  "identity:list_roles"))

class AllTestReportTable(tables.DataTable):
    """
    #Table for displaying all the past reports after executing All Tests
    """
    test_name     = tables.Column('testlist_id', verbose_name=_('Test Name'), sortable=True)
    test_service  = tables.Column('testlist_id', verbose_name=_('Service'), sortable=True)
    test_time     = tables.Column('testlist_id', verbose_name=_('Time'), sortable=True)
    
    
    class Meta:
        name = "alltests"
        verbose_name  = _("All Tests")
        table_actions = ()
        row_class  = UpdateRow
        row_actions = (ViewReport, DeleteReport)

class BenchmarkingTestReportTable(tables.DataTable):
    """
    #Table for displaying all the past reports after executing Benchmarking Tests
    """
    test_name     = tables.Column('name', verbose_name=_('Test Name'), sortable=True)
    test_service  = tables.Column('name', verbose_name=_('Service'), sortable=True)
    test_time     = tables.Column('name', verbose_name=_('Time'), sortable=True)

    class Meta:
        name = "benchmarkingtests"
        verbose_name  = _("Benchmarking Tests")
        table_actions = ()
        row_class  = UpdateRow
        row_actions = (ViewReport, DeleteReport)

class QATestReportTable(tables.DataTable):
    """
    #Table for displaying all the past reports after executing Benchmarking Tests
    """
    test_name     = tables.Column('name', verbose_name=_('Test Name'), sortable=True)
    test_service  = tables.Column('name', verbose_name=_('Service'), sortable=True)
    test_time     = tables.Column('name', verbose_name=_('Time'), sortable=True)

    class Meta:
        name = "qatestreporttable"
        verbose_name  = _("QA Tests")
        table_actions = ()
        row_class  = UpdateRow
        row_actions = (ViewReport, DeleteReport)

