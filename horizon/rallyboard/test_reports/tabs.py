# ______________________________________________________________________
# | File Name: tabs.py                                                  |
# |                                                                     |
# | This file is for handling the views of Rally tasks display          |
# |_____________________________________________________________________|
# | Start Date: Aug 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
from django.utils.translation import ugettext_lazy as _
from horizon import tabs, exceptions
from openstack_dashboard.dashboards.rallyboard.test_reports import tables
from django.core.urlresolvers import reverse_lazy, reverse
from horizon.utils import memoized
from django.conf import settings
from sidecarclient import client
from django.conf import settings
import requests
import json
from openstack_dashboard.dashboards.rallyboard.tasks import setting

#Making the connection to sidecar client
default_value = setting.ConfigSetter()
sidecar_conn = setting.sidecar_conn()

class AllTestReportTab(tabs.TableTab):
    """
    Class to Display the reports after executing All tests
    """
    name = _("All Test Reports")
    slug = "all_test_report_listing"
    table_classes = (tables.AllTestReportTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    _has_prev = True
    _has_more = True

    def has_more_data(self, table):
        return False
   
    def has_prev_data(self, table):
        return False

    def get_alltests_data(self):
        """
        # | Function to get the data for All Report Listing
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:
            
            #Fetching the reports of All Test Execution and returning it
            all_report  = sidecar_conn.events.list_test_history(project_id = 1)
            self.event_data = all_report
            return list(all_report)
        except Exception, e:
            exceptions.handle(self.request, "Unable to fetch the reports.")
            return []

class BenchmarkingTestReportTab(tabs.TableTab):
    """
    Class to Display the reports after executing Benchmarking Tests
    """
    name = _("Benchmark Test Reports")
    slug = "benchmark_test_report_listing"
    table_classes = (tables.BenchmarkingTestReportTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    _has_prev = True
    _has_more = True

    def has_more_data(self, table):
        return False

    def has_prev_data(self, table):
        return False

    def get_benchmarkingtests_data(self):
        """
        # | Function to get the data for All Report Listing
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:
            
            #Fetching the reports of Benchmark Test Execution and returning it
            benchmark_history  = sidecar_conn.events.list_test_history(project_id = 2)
            self.event_data = benchmark_history
            return list(benchmark_history)
        except Exception, e:
            exceptions.handle(self.request, "Unable to fetch the reports.")
            return []

class QATestReportTab(tabs.TableTab):
    """
    Class to Display the reports after executing Benchmarking Tests
    """
    name = _("QA Test Reports")
    slug = "qa_test_report_listing"
    table_classes = (tables.QATestReportTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    _has_prev = True
    _has_more = True

    def has_more_data(self, table):
        return False

    def has_prev_data(self, table):
        return False

    def get_qatestreporttable_data(self):
        """
        # | Function to get the data for QA test report listing
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:
            
            #Fetching th reports of QA Test Execution and returning it
            qa_report = sidecar_conn.events.project_test_list()
            self.event_data = qa_report
            events = []
            return qa_report
        except Exception, e:
            exceptions.handle(self.request, "Unable to fetch the reports.")
            return []

class ReportDisplayTab(tabs.TabGroup):
    slug = "report_display_tab"
    tabs = (AllTestReportTab, BenchmarkingTestReportTab, QATestReportTab)
    sticky = True
