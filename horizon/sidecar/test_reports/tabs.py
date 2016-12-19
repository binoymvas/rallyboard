# File Name: tabs.py
#
# @Software: Openstack Horizon
#
# @version: Liberity
#
# @Package: Sidecar 
#
# Start Date: 31th Aug 2016
from django.utils.translation import ugettext_lazy as _
from horizon import tabs, exceptions
from openstack_dashboard.dashboards.sidecar.test_reports import tables
from django.core.urlresolvers import reverse_lazy, reverse
from horizon.utils import memoized
from django.conf import settings
from sidecarclient import client
from django.conf import settings
from pprint import pprint
import requests
import json
from openstack_dashboard.dashboards.sidecar.test_reports import setting
default_value = setting.ConfigSetter()

#Making the connection to sidecar client
_sidecar_ = None
def sidecar_conn():
    
    #Making the sidecar connection
    global _sidecar_
    if not _sidecar_:
        _sidecar_ = client.Client(
                  username = getattr(settings, "SC_USERNAME"),
                  password = getattr(settings, "SC_PASSWORD"),
                  auth_url = getattr(settings, "SC_AUTH_URL"),
                  region_name = getattr(settings, "SC_REGION_NAME"),
                  tenant_name = getattr(settings, "SC_TENANT_NAME"),
                  timeout = getattr(settings, "SC_TIMEOUT"),
                  insecure = getattr(settings, "SC_INSECURE"))
    return _sidecar_


class AllTestReportTab(tabs.TableTab):
    """
    Class to Display the reports after executing All tests
    """
    name = _("All Test Reports")
    slug = "all_test_report_listing"
    table_classes = (tables.AllTestReportTable, )
    template_name = ("horizon/common/_detail_table.html")
    #template_name = ("horizon/openstack_dashboard/dashboard/sidecar/events/templates/events/test_reports.html")
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
            print('++++++++++++++++++++tabs.py file+++++++++++++++++++++++++')
            #Fetching th reports of All Test Execution and returning it
            #events = sidecar_conn().events.project_test_list()
	    print("E1")
	    events  = sidecar_conn().events.list_test_history()
	    print('Enter 1')
            print('++++++++++++++++++++++++++++++++++')
	    #print(events)
	    #print "".join([str(x) for x in events] )
            #print '\n'.join(events)
	    print('++++++++++++++++++++++++++++++++++')
            self.event_data = events
	    print('enter 2')
            return list(events)
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
            #Fetching th reports of All Test Execution and returning it
            events = sidecar_conn().events.project_test_list()
            self.event_data = events
            self.event_data = events
            return list(events)
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
            events = sidecar_conn().events.project_test_list()
            self.event_data = events
            events = []
            return events
            #return "testttt"
        except Exception, e:
            exceptions.handle(self.request, "Unable to fetch the reports.")
            return []

class ReportDisplayTab(tabs.TabGroup):
    slug = "report_display_tab"
    tabs = (AllTestReportTab, BenchmarkingTestReportTab, QATestReportTab)
    sticky = True
