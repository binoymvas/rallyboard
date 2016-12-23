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
from openstack_dashboard.dashboards.rallyboard.tasks import tables
from django.core.urlresolvers import reverse_lazy, reverse
from horizon.utils import memoized
from openstack_dashboard.dashboards.rallyboard.tasks import setting
default_value = setting.ConfigSetter()
sidecar_conn = setting.sidecar_conn()

class RallyConfig:
    """ 
    # | Class to handle the Configuration values
    """
    
    def __init__(self, info):
        self.id = info['id']
        self.name = info['name']
        self.value = info['value']

class HistoryListingTab(tabs.TableTab):
    """ 
    # | Class to handle the log listing
    """
    name = _("Test configuration")
    slug = "evacuate_logs"
    table_classes = (tables.TestConfigTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = True
    _has_more_data = False
    _has_prev_data = False

    def get_logs_data(self):
        """
        # | Function to get the evacuate log list 
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:
            rally_data = self.process_dict_and_display('test')
            return rally_data
        except Exception, e:
            return []

    # Process invoice dict and display
    def process_dict_and_display(self, values):
        """
        # | Method: Method to create the dictionary with the data available
        # | @Arguments: list of objects. 
        #| 
        # | @Return Type: dictionary
        """
        
        # Converting an Invoice Unicode to Dict
        image_ref = default_value.get_setting('compute', 'image_ref')
        flavor_ref = default_value.get_setting('compute', 'flavor_ref')
        rally_config = [{'id':'1', 'name': 'image_ref', 'value': image_ref}, {'id': 2, 'name': 'flavor_ref', 'value':flavor_ref}]
        rally_config_full = rally_config
        content = [] 
        
        # tenant based processing in invoicedata
        for rally_data in rally_config_full:
            
            # Assigned necessary values for reusing the same
            info = {}
            info['id'] = rally_data['id']
            info['name'] = rally_data['name']
            info['value'] = rally_data['value']
            content.append(RallyConfig(info))
        return content

class RallyTestTab(tabs.TableTab):
    """ 
    Class to Display the Evacuation Events
    """
    name = _("Rally Tests")
    slug = "evacuation_events_listing"
    table_classes = (tables.TasksListTable, )
    template_name = ("horizon/common/_detail_table.html")
    preload = False
    _has_more = True
    _has_prev = True

    def has_more_data(self, table):
        """
        # | Function to show the more link
        """
        return False

    def has_prev_data(self, table):
        """
        # | function to show the previous link
        """
        return False
 
    def get_events_data(self):
        """
        # | Function to get the ticket list for the given user
        # |
        # | @Arguments: None
        # |
        # | @Return Type: Dictionary
        """
        try:
            
            #Fetching the event list and returning it
            events = sidecar_conn.events.project_test_list()
            self.event_data = events
            return list(events)
        except Exception, e:
            exceptions.handle(self.request, "Unable to fetch events.")
            return []

class RallyTab(tabs.TabGroup):
    slug = "evacuation_events_tab"
    tabs = (RallyTestTab, HistoryListingTab)
    sticky = True