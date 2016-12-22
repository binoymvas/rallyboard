# File Name: tables.py
#
# Package Name: Openstack Horizon [liberity]
#
# Dashboardd: Rally Board
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

class EventFilterAction(tables.FilterAction):
    """
    # | Class to filtering the events
    """
    name = "eventfilter"
    filter_type = "server"
    verbose_name = _("Filter Events")
    needs_preloading = True
    filter_choices = (("id", _("ID"), True),
                     ("name", _("Name"), True),
                     ("event_status", _("Event Status"), True),
                     ("node_uuid", _("Node UUID"), True),
                     ('event_create_time', _("Create Time >="), True),
                     ('vm_uuid_list', _("VM UUID"), True))

def transform_status(event):
    """
    # | Function to transform the status to uppercase
    # | 
    # | Event object
    # |
    # | Returns string
    """

    if not event.event_status:
        return '-'
    return str(event.event_status).upper()


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request):
        return '?'
        project_info = api.keystone.tenant_get(request, '5a4fb03113d44f7590789f9aa9ff3619' , admin=True)
        return project_info

class Runtest(tables.LinkAction):
    name = "runtests"
    verbose_name = _("Run test ")
    url = "horizon:rally_dashboard:tasks:update"
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def get_link_url(self, testcase):
        step = 'runtest'
        base_url = reverse(self.url, args=[testcase.id])
        return base_url+step

class TestReport(tables.LinkAction):
    name = "report"
    verbose_name = _("View Report")
    url = "horizon:rally_dashboard:tasks:update"
    #classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def allowed(self, request, testcase=None):
        return True

    def get_link_url(self, testcase):
        step = 'report'
        base_url = reverse(self.url, args=[testcase.id])
        return base_url+step

class Edittestlist(tables.LinkAction):
    name = "edittestslist"
    verbose_name = _("Edit Test List")
    url = "horizon:rally_dashboard:tasks:update"
    classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def get_link_url(self, testcase):
        step = 'update_list'
        base_url = reverse(self.url, args=[testcase.id])
        param = urlencode({"step": step})
        return base_url+step

class EditConf(tables.LinkAction):
    name = "editconf"
    verbose_name = _("Edit Conf")
    url = "horizon:rally_dashboard:tasks:update"
    classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:list_users"),
                    ("identity", "identity:list_roles"))

    def get_link_url(self, testcase):
        step = 'update'
        base_url = reverse(self.url, args=[testcase.id])
        param = urlencode({"step": step})
        return base_url+step

class EventListTable(tables.DataTable):
    """ 
    TABLE TO LIST THE EVENTS
    """
    name = tables.Column('name', verbose_name=_('Name'), sortable=True, link='horizon:rally_dashboard:tasks:event_detail')
     
    class Meta:
        name = "events"
        verbose_name = _("Rally Tests")
        table_actions = ()
        table_actions = ( )#EventFilterAction,)
        row_class = UpdateRow
        row_actions = (Runtest, Edittestlist, TestReport) 

class LogListTable(tables.DataTable):
    """ 
    TABLE TO LIST THE LOGS
    """
    id = tables.Column('id', verbose_name=_('ID'), sortable=True)
    name = tables.Column('name',  verbose_name=_("Name"), sortable=True)
    value = tables.Column('value', verbose_name=_('Value'), sortable=True)

    class Meta:
        name = "logs"
        verbose_name = _("Test configuration")
        table_actions = ()
        row_class = UpdateRow
        row_actions = () #(EditConf,)
