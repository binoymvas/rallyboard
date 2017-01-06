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
from django.utils.translation import ungettext_lazy
from horizon import tables
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.http import urlencode
from openstack_dashboard import api
from openstack_dashboard import policy
from sidecarclient import client
from django.conf import settings
from openstack_dashboard.dashboards.rallyboard.tasks import setting
import datetime

#Setting the connections
sidecar_conn = setting.sidecar_conn()

class UpdateRow(tables.Row):
    """
    # | Class to handle the row actions
    """
    ajax = True

    def get_data(self, request):
        return '?'

class ViewReport(tables.LinkAction):
    """
    # | Class to handle the View Report
    """
    name = "viewreport"
    verbose_name = _("View Report")
    url = "horizon:rally_dashboard:test_reports:testhistory"
    classes = ("ajax-model",)
    icon = "pencil"
    policy_rules  = (("identity",  "identity:list_users"),
                     ("identity",  "identity:list_roles"))


class DeleteReport(tables.DeleteAction):
    """
    # | Class to handle the Delete Report
    """
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete History",
            u"Delete History",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted History",
            u"Deleted History",
            count
        )
    policy_rules = (("identity", "identity:delete_role"),)
    
    def allowed(self, request, role):
        return True

    def delete(self, request, obj_id):
        try: 
            sidecar_conn.events.delete_test_history(id=obj_id)
            return True
        except Exception, e:
            return False

def get_test_regex(tests_list):
    """
    # | Function to fetch the test_regex value from tests_list table
    # | 
    # | Tests_list object
    # |
    # | Returns string
    """
    
    #Setting the display values
    time = tests_list.history_create_time
    date_str = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    date_in_words = date_str.strftime('%B %d, %Y')
    return 'Test of '+ date_in_words

def get_test_service(tests_list):
    """
    # | Function to fetch the tests_service value from the tests_list table
    # | 
    # | Tests_list object
    # |
    # | Returns string
    """
    
    #Setting the service display value
    if not tests_list.test_service:
        return '-'
    return str(tests_list.test_service)

class AllTestReportTable(tables.DataTable):
    """
    # | Table for displaying all the past reports after executing All Tests
    """

    #Columns which are to be displayed in the table
    test_regex = tables.Column(get_test_regex, verbose_name=_('Test Details'), sortable=False)
    history_create_time = tables.Column('history_create_time', verbose_name=_('Time'), sortable=True)
   
    class Meta:
        name = "alltests"
        verbose_name  = _("All Tests")
        table_actions = ()
        row_class  = UpdateRow
        row_actions = (ViewReport, DeleteReport)

class BenchmarkingTestReportTable(tables.DataTable):
    """
    # | Table for displaying all the past reports after executing Benchmarking Tests
    """

    #Columns which are to be displayed in the table
    test_regex = tables.Column(get_test_regex, verbose_name=_('Test Details'), sortable=False)
    history_create_time = tables.Column('history_create_time', verbose_name=_('Time'), sortable=True)

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

    #Columns which are to be displayed in the table
    #test_name     = tables.Column('name', verbose_name=_('Test Name'), sortable=True)
    #test_service  = tables.Column('name', verbose_name=_('Service'), sortable=True)
    #test_time     = tables.Column('name', verbose_name=_('Time'), sortable=True)
   
    #Columns which are to be displayed in the table
    test_regex = tables.Column(get_test_regex, verbose_name=_('Test Details'), sortable=False)
    history_create_time = tables.Column('history_create_time', verbose_name=_('Time'), sortable=True)

    class Meta:
        name = "qatestreporttable"
        verbose_name  = _("QA Tests")
        table_actions = ()
        row_class  = UpdateRow
        row_actions = (ViewReport, DeleteReport)
