# _______________________________________________________________________
# | File Name: tables.py                                                |
# |                                                                     |
# | This file is for handling the table support Test tasks display      |
# |_____________________________________________________________________|
# | Start Date: Nov 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
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

class TasksListTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Name'), sortable=True, link='horizon:rally_dashboard:tasks:event_detail')
     
    class Meta:
        name = "events"
        verbose_name = _("Rally Tests")
        table_actions = ()
        table_actions = ( )
        row_class = UpdateRow
        row_actions = (Runtest, Edittestlist, TestReport) 

class TestConfigTable(tables.DataTable):
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
        row_actions = ()