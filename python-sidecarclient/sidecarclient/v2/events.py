# -*- coding: utf-8 -*-
# ___________________________________________________________________________________
# | File Name: events.py                                                            |
# |                                                                                 |
# | Package Name: Python-Sidecarclient to handel the sidecar REST API               |
# |                                                                                 |
# | Version: 2.0                                                                    |
# |                                                                                 |
# | Sofatware: Openstack                                                            |
# |_________________________________________________________________________________|
# | Copyright: 2016@nephoscale.com                                                  |
# |                                                                                 |
# | Author: Binoy MV <binoymv@poornam.com>, Dinesh Patra<dinesh.p@poornam.com>      |
# |                                                                                 |
# | Author:  info@nephoscale.com                                                    |
# |_________________________________________________________________________________|
from __future__ import print_function
from sidecarclient import exception
import sidecarclient

class Event(object):
    """
    # | Class to provide Event Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | name: Name of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    name = None

    # | vm_uuid_list: List containg instance ids
    # |
    # | Default Value: Empty List
    # |
    # | Type: List
    vm_uuid_list = None
    
    # | node_uuid: Id of the host taking part in evacuates
    # |
    # | Default Value: None
    # |
    # | Type: String
    node_uuid = None

    # | event_status: Status of the event
    # |
    # | Default Value: None
    # | 
    # | Type: String
    # |
    # | Allowed Values: created, running, completed
    event_status = None

    # | extra: Extra value for the event
    # |
    # | Default Value: {}
    # |
    # | Type: dictionary
    extra = None

    # | event_create_time: Event create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    event_create_time = None

    # | event_complete_time: Event create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    event_complete_time = None

    def __init__(self, event):
        """ Initialization Function """
        self.id            = event['id']
        self.name                = event['name']
        self.vm_uuid_list        = event['vm_uuid_list']
        self.node_uuid           = event['node_uuid']
        self.event_status        = event['event_status']
        self.extra               = event['extra']
        self.event_create_time   = event['event_create_time']
        self.event_complete_time = event['event_complete_time']
        self.event_more          = event['moredata']
        self.event_prev          = event['predata']

class ResultGenerator(object):
    """ Result Generator object """

    def __init__(self, event_list):
        # | Intialziation function
        # |
        # | Arguments: event_list
        # |
        # | Returns None        
        self._count = len(event_list['events'])
        self._events = event_list['events']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  Event(self._events[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class EvacuateLogs(object):
    """
    # | Class to provide Logs Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | hypervisor_name: Hypervisor name
    # |
    # | Default Value: None
    # |
    # | Type: String
    hypervisor_name = None
    
    # | down_since: down since the host is gone offline
    # |
    # | Default Value: 0
    # |
    # | Type: Float
    down_since = None

    # | evacuated: Event is evacuated or not 
    # |
    # | Default Value: False
    # | 
    # | Type: String
    evacuated = None

    # | event_id : Event id of the event
    # |
    # | Default Value: None
    # |
    # | Type: Integer
    event_id = None

    # | prev_time: Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    prev_time = None

    # | event_creation_time : Event create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    event_creation_time = None

    def __init__(self, logs):
        """ Initialization Function """
        self.id                  = logs['id']
        self.hypervisor_name     = logs['hypervisor_name']
        self.down_since          = logs['down_since']
        self.evacuated           = logs['evacuated']
        self.event_id            = logs['event_id']
        self.prev_time           = logs['prev_time']
        self.event_creation_time = logs['event_creation_time']

class LogResultGenerator(object):
    """ Result Generator object """

    def __init__(self, log_list):
        # | Intialziation function
        # |
        # | Arguments: log_list
        # |
        # | Returns None       
        self._count = len(log_list['logs'])
        self._logs = log_list['logs']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  EvacuateLogs(self._logs[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class ProjectTests(object):
    """
    # | Class to provide Logs Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | hypervisor_name: Hypervisor name
    # |
    # | Default Value: None
    # |
    # | Type: String
    name = None
    
    # | event_id : Event id of the event
    # |
    # | Default Value: None
    # |
    # | Type: Integer
    test_status = None

    # | prev_time: Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    test_create_time  = None

    # | extra: Extra value for the event
    # |
    # | Default Value: {}
    # |
    # | Type: dictionary
    extra = None


    def __init__(self, logs):
        """ Initialization Function """
        self.id                  = logs['id']
        self.name     = logs['name']
        self.test_status          = logs['test_status']
        self.extra           = logs['extra']
        self.test_create_time = logs['test_create_time']

class ProjectTestsGenerator(object):
    """ Project Generator object """

    def __init__(self, log_list):
        # | Intialziation function
        # |
        # | Arguments: log_list
        # |
        # | Returns None       
        self._count = len(log_list['project_tests'])
        self._logs = log_list['project_tests']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  ProjectTests(self._logs[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class TestResults(object):
    """
    # | Class to provide Logs Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | name: Name of the test
    # |
    # | Default Value: None
    # |
    # | Type: String
    name = None
    
    # | tet_type : Type of the test 
    # |
    # | Default Value: None
    # |
    # | Type: Integer
    project_id = None

    # | test_service: Service name of the test 
    # |
    # | Default Value: None
    # |
    # | Type: string
    test_service  = None

    # | test_scenario: Scenario name of the test
    # |
    # | Default Value: None
    # |
    # | Type: String
    test_scenario = None

    # | test_added: Value  to show the test added to the list
    # |
    # | Default Value: None
    # |
    # | Type: String 
    test_added = None

    # | test_verified: Regex value for the test
    # |
    # | Default Value: None
    # |
    # | Type: String 
    test_verified = None

    # | test_regex: Regex value for the test
    # |
    # | Default Value: None
    # |
    # | Type: String 
    test_regex = None

    # | test_create_time:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    test_create_time = None
    
    # | test_create_time:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    test_uuid = None

    # | test_create_time:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    results = None

    def __init__(self, logs):
        """ Initialization Function """
        self.id               = logs['id']
        self.name             = logs['name']
        self.project_id       = logs['project_id']
        self.test_service     = logs['test_service']
        self.test_scenario    = logs['test_scenario']
        self.test_regex       = logs['test_regex']
        self.test_added       = logs['test_added']
        self.test_verified    = logs['test_verified']
        self.test_create_time = logs['test_create_time']
        self.test_uuid        = logs['test_uuid']
        self.results          = logs['results']

class TestResultsGenerator(object):
    """ Project Generator object """

    def __init__(self, log_list):
        # | Intialziation function
        # |
        # | Arguments: log_list
        # |
        # | Returns None       
        self._count = len(log_list['tests_list'])
        self._logs = log_list['tests_list']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  TestResults(self._logs[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class TestReports(object):
    """
    # | Class to provide Logs Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | test_create_time:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    created_at = None

    # | test_create_time:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    updated_at = None

    # | verification_uuid:  Log create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    verification_uuid = None

    # | data:  data in json format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    data = None

    def __init__(self, logs):
        """ Initialization Function """
        self.id              = logs['id']
        self.created_at      = logs['created_at']
        self.updated_at = logs['updated_at']
        self.verification_uuid = logs['verification_uuid']
        self.data  = logs['data']


class TestReportsGenerator(object):
    """ Project Generator object """

    def __init__(self, log_list):
        # | Intialziation function
        # |
        # | Arguments: log_list
        # |
        # | Returns None       
        self._count = len(log_list['tests_list'])
        self._logs = log_list['tests_list']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj = TestReports(self._logs[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()


class TestLogs(object):
    """
    # | Class to provide Logs Object
    """

    # | id: id of the event
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | log_data:  Log data
    # |
    # | Default Value: None
    # |
    # | Type: text
    log_data = None

    # | results:  HTML Results
    # |
    # | Default Value: None
    # |
    # | Type: Longtext
    results = None

    # | project_id :  project_id in json format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    project_id = None

    # | test_status : test_status in json format
    # |
    # | Default Value: None
    # |
    # | Type: date 
    test_status = None

    def __init__(self, logs):
        """ Initialization Function """
        self.id              = logs['id']
 	self.log_data      = logs['log_data']
        self.project_id = logs['project_id']
        self.test_status = logs['test_status']
	self.results = logs['results']

class TestLogGenerator(object):
    """ Log Generator object """

    def __init__(self, log_list):
        # | Intialziation function
        # |
        # | Arguments: log_list
        # |
        # | Returns None       
        self._count = len(log_list['tests_logs'])
        self._logs = log_list['tests_logs']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj = TestLogs(self._logs[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class TestConfig(object):
    """
    # | Class related to TestConfig entries
    # | 
    """

    # | id :  config id
    # |
    # | Default Value: None
    # |
    id     = None

    # | option :  option name in string format
    # |
    # | Default Value: None
    # |
    option = None

    # | value :  value corresponding to the option
    # |
    # | Default Value: None
    # |
    value  = None

    def __init__(self, test_config):

        """ Initialization Function """
        self.id             = test_config['id']
        self.option         = test_config['option']
        self.value          = test_config['value']


class TestConfigGenerator(object):
    """ Result Generator object """

    def __init__(self, test_config_list):
        # | Intialziation function
        # |
        # | Arguments: test_config_list
        # |
        # | Returns None        
        self._count = len(test_config_list['test_config'])
        self._config = test_config_list['test_config']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  TestConfig(self._config[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class TestHistory(object):
    """
    # | Class to provide History Object
    """

    # | id: id of the test history
    # |
    # | Default Value: None
    # |
    # | Type: String
    id = None

    # | testlist_id: Id of the test list
    # |
    # | Default Value: None
    # |
    # | Type: String
    testlist_id = None

    # | project_id: Project ID
    # |
    # | Default Value: None
    # |
    # | Type: List
    project_id = None
    
    # | history_create_time: History create time in yyy-mm-dd HH:ii:ss format
    # |
    # | Default Value: None
    # |
    # | Type: string
    history_create_time = None

    # | result: Result string
    # |
    # | Default Value: None
    # |
    # | Type: string
    results = None

    # | test_regex: Test regex name
    # | 
    # | Default Value: None
    # | 
    # | Type: string
    # |
    #test_regex = None

    # | test_service: Name of the service
    # |
    # | Default Value: None
    # |
    # | Type: String
    # |
    #test_service = None

    def __init__(self, test_history):
        """ Initialization Function """
        self.id           	 = test_history['id']
        self.testlist_id         = test_history['testlist_id']
        self.project_id          = test_history['project_id']
        self.history_create_time = test_history['history_create_time']
        self.results 		 = test_history['results']
        self.event_more          = test_history['moredata']
        self.event_prev          = test_history['predata']
	#self.test_regex          = test_history['test_regex']
        #self.test_service        = test_history['test_service']

class TestHistoryGenerator(object):
    """ Result Generator object """

    def __init__(self, test_history_list):
        # | Intialziation function
        # |
        # | Arguments: test_history_list
        # |
        # | Returns None        
	self._count = len(test_history_list['test_history'])
        self._history = test_history_list['test_history']
        self._position = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self._count

    def __next__(self):
        return self.next()

    def next(self):
        if self._position < self._count:
            # | IF POSITION IS LESS THAN TOTAL ELEMT
            # | Continue the looping
            obj =  TestHistory(self._history[self._position])
            self._position = self._position + 1
            return obj
        raise StopIteration()

class EventsHttp(object):
    """
    # | Class to make api request
    """
    def __init__(self, obj):
        """ 
        # | Initialization function
        # |
        # | Arguments: 
        # | <obj>: Instabnce of the v2.client
        """
        if type(obj) != sidecarclient.v2.client.Client:
            raise exception.NotSupported("Not an instance of sidecarclient.")
        self._obj = obj

        
    def list(self, id=None, name=None, node_uuid=None, event_create_time=None,
        min_event_create_time=None, max_event_create_time=None, marker=None, limit=None, event_status=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :node_uuid   <string>: Host id
        # |     :event_create_time <string in yyyy-mm-dd HH:ii::ss format>: Event create time
        # |     :min_event_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Minimum time when the event was created
        # |     :max_event_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Maximum time when the event was created
        # |     :marker <last event id>: Minimum time when the event was created
        # |     :limit  <integer>: Minimum time when the event was created
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/events?'
                
        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if name:
            url = url + "name=%s&" % (name)
        if event_status:
            url = url + "event_status=%s&" % (event_status)
        if node_uuid:
            url = url + "node_uuid=%s&" % (node_uuid)
        if event_create_time:
            url = url + "event_create_time=%s&" % (event_create_time)
        if min_event_create_time:
            url = url + "min_event_create_time=%s&" % (min_event_create_time)
        if max_event_create_time:
            url = url + "max_event_create_time=%s&" % (max_event_create_time)
        if marker:
            url = url + "marker=%s&" % (marker)
        if limit:
            url = url + "limit=%s&" % (limit)

        # | Make http request
        data = self._obj.http.get(url, headers)
        return ResultGenerator(data['body'])

    def create(self, vm_uuid_list=[], name=None, node_uuid=None):
        """
        # | Function to create a new event
        # |
        # | Arguments: filter options
        # |     :name         <string>:        name of the event
        # |     :node_uuid    <string>:        Host id
        # |     :vm_uuid_list <list of strings>list containg instance ids
        # |
        # | Returns: Event object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events'        
        data = {
            "event": {
                "name": name,
                "vm_uuid_list": vm_uuid_list,
                "node_uuid": node_uuid
            }
        }
        data = self._obj.http.post(url,  data, headers)
        return Event(data['body']['event'])

    def detail(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> Event id
        # |
        # | Returns: Event Object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = self._obj.http.get(url, headers)
        return Event(data['body']['event'])

    def edit(self, id = None, name=None, event_status=None, node_uuid=None, vm_uuid_list=[]):
        """
        # | Function to edit the event
        # |
        # | Arguments:
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :node_uuid   <string>: Host id
        # |     :event_create_time <string in yyyy-mm-dd HH:ii::ss format>: Event create time
        # |     :event_status <string, either running, completed>
        # |
        # | Returns:
        # |   None
        """
        event_id = id
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = {}
        data["event"] = {}

        # | Creating event list
        if name:
            data["event"]["name"] =  name
        if event_status:
            data["event"]["event_status"] = event_status
        if node_uuid:
            data["event"]["node_uuid"] = node_uuid
        if vm_uuid_list:
            data["event"]["vm_uuid_list"] = vm_uuid_list
        data = self._obj.http.put(url, data, headers)
    
    def delete(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> Event id
        # |
        # | Returns: Event Object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/events/%s' %(id)
        data = self._obj.http.delete(url, headers)

    def evacuate_runEvent(self, id = None):
        """
        # | Function to run a evacuate event
        # | 
        # | Arguments
        # |   :id  <string>: event id
        # | Returns:
        # |   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/hostevacuate'
        data = {"event": {"id": id}}
        data = self._obj.http.post(url,  data, headers)

    def evacuate_healthcheck(self):
        """
        # | Function to execute and fetch the healthcheck details for all events
        # |
        # | Arguments
        # |   :id <string>: event_id
        # | Returns:
        #|   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/hostevacuate'
        data = {"event": {"name": 'name',"vm_uuid_list": 'vm_uuid_list',"node_uuid": 'node_uuid'}}
        data = self._obj.http.post(url,  data, headers)

    def get_test_config(self, id=None, option=None, value=None):
        """
        # | Function to fetch the test config values
        # | Arguments:
        # | 
        # | Return:
        # |
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally/testconfig?'
        data    = self._obj.http.get(url, headers)
        return TestConfigGenerator(data['body'])

    def evacuate_healthcheck_status(self):
        """
        # | Function to execute and fetch the healthcheck details for all events
        # |
        # | Arguments
        # |   :id <string>: event_id
        # | Returns:
        #|   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/hostevacuate'
        data = self._obj.http.get(url, headers)
        return LogResultGenerator(data['body'])

    def project_test_list(self, id=None, name=None, test_status=None, marker=None, limit=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :test_status   <string>: Host id
        # |     :marker <last event id>: Minimum time when the event was created
        # |     :limit  <integer>: Minimum time when the event was created
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally?'
                
        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if name:
            url = url + "name=%s&" % (name)
        if test_status:
            url = url + "test_status=%s&" % (test_status)
        if marker:
            url = url + "marker=%s&" % (marker)
        if limit:
            url = url + "limit=%s&" % (limit)

        # | Make http request
        data = self._obj.http.get(url, headers)
	print('++++++++++++++++++++++++++++++++++++++++++Client Side+++++++++++++++++++++++')
	print(data)
        return ProjectTestsGenerator(data['body'])

    def tests_list(self, id=None, name=None, project_id=None, test_service=None, test_scenario=None, test_regex=None, test_added=None, marker=None, limit=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :name        <string>: name of the event
        # |     :project_id <string>: Type of the test
        # |     :test_service <string>: Type of the test service
        # |     :test_scenario <string>: Test scenario
        # |     :test_regex   <string>: Test regex
        # |     :marker <last event id>: Minimum time when the event was created
        # |     :limit  <integer>: Minimum time when the event was created
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally/testlist?'

        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if name:
            url = url + "name=%s&" % (name)
        if project_id:
            url = url + "project_id=%s&" % (project_id)
        if test_service:
            url = url + "test_service=%s&" % (test_service)
        if test_scenario:
            url = url + "test_scenario=%s&" % (test_scenario)
        if test_regex:
            url = url + "test_regex=%s&" % (test_regex)
	if test_added:
	    url = url + "test_added=%s&" % (test_added)
        if marker:
            url = url + "marker=%s&" % (marker)
        if limit:
            url = url + "limit=%s&" % (limit)

        # | Make http request
        data = self._obj.http.get(url, headers)
        return TestResultsGenerator(data['body'])

    def update_test(self, id=None, name=None, test_added=None, test_verified=None, test_uuid=None, results=None, update_null=None):
        """
        # | Function to edit the event
        # |
        # | Arguments:
        # |     :id            <string>: test id
        # |     :name          <string>: name of the test
        # |     :test_uuid     <string>: UUID obtained after executing the test
        # |     :test_added    <string>: whether the test is enabled or not
        # |     :test_verified <string>: whether the test has been executed or not
        # |     :results       <string>: the output obtained after test execution
	# |     :update_null   <string>: to update 0 in test_added
        # | Returns:
        # |   None
        """
        test_id = id
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/sidecarrally/testlist/%s' %(id)
        data = {}
        data["test_list"] = {}

        # | Creating test list
        if name:
            data["test_list"]["name"] =  name
        if test_added:
            data["test_list"]["test_added"] = test_added
        if test_verified:
            data["test_list"]["test_verified"] = test_verified
        if test_uuid:
            data["test_list"]["test_uuid"] = test_uuid
        if results:
            data["test_list"]["results"]   = results
	if update_null:
	    data["test_list"]["update_null"] = update_null
        data = self._obj.http.put(url, data, headers)

    def test_report(self, id=None, project_id=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :project_id <string>: Type of the test
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally/testlist?'

        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if project_id:
            url = url + "project_id=%s&" % (project_id)
            url = url + "report=1"

        # | Make http request
        data = self._obj.http.get(url, headers)
        return TestReportsGenerator(data['body'])


    def test_logs(self, project_id=None):
        """
        # | Function to list the logs
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :project_id <string>: Type of the test
        # |
        # | Returns: Events generator object
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally/testlog/'

        # | Createing filter options
        if project_id:
            url = url + "%s" % (project_id)

        # | Make http request
        data = self._obj.http.get(url, headers)
	return TestLogs(data['body']['tests_logs'])

    def run_command(self, id=None):
        """
        # | Function to run a evacuate event
        # | 
        # | Arguments
        # |   :id  <string>: event id
        # | Returns:
        # |   None
        """
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/sidecarrally'
        data = {"project": {"id": id}}
	print('data', data)
        data = self._obj.http.post(url,  data, headers)
	print('data', data)
	return data

    def list_test_history(self, id=None, testlist_id=None, project_id=None, history_create_time=None,
        min_history_create_time=None, max_history_create_time=None, marker=None, limit=None):
        """
        # | Function to list the evenets
        # |
        # | Arguments: filter options
        # |     :id          <string>: event id
        # |     :testlist_id        <string>: name of the event
        # |     :project_id   <string>: Host id
        # |     :history_create_time <string in yyyy-mm-dd HH:ii::ss format>: Event create time
        # |     :min_history_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Minimum time when the event was created
        # |     :max_history_create_time <strimg in yyyy-mm-dd HH:ii::ss format>: Maximum time when the event was created
        # |     :marker <last event id>: Minimum time when the event was created
        # |     :limit  <integer>: Minimum time when the event was created
        # |
        # | Returns: Events generator object
        """
	print('++++++++++++++++++++++++List Test History++++++++++++++++++++++++++')
	print(project_id)
	print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url     = self._obj.sidecar_url + '/evacuates/sidecarrally/testhistory?'
                
        # | Createing filter options
        if id:
            url = url + "id=%s&" % (id)
        if testlist_id:
            url = url + "testlist_id=%s&" % (testlist_id)
        if project_id:
            url = url + "project_id=%s&" % (project_id)
        if history_create_time:
            url = url + "history_create_time=%s&" % (history_create_time)
        if min_history_create_time:
            url = url + "min_history_create_time=%s&" % (min_history_create_time)
        if max_history_create_time:
            url = url + "max_history_create_time=%s&" % (max_history_create_time)
        if marker:
            url = url + "marker=%s&" % (marker)
        if limit:
            url = url + "limit=%s&" % (limit)

        # | Make http request
        data = self._obj.http.get(url, headers)
	print(data)
	print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return TestHistoryGenerator(data['body'])

    def create_test_history(self, testlist_id=None, project_id=None, results=None):
        """
        # | Function to create a new event
        # |
        # | Arguments: filter options
        # |     :testlist_id <string>: testlist_id
        # |     :project_id  <string>: project_id
        # |     :results <strings> containg result html
        # |
        # | Returns: Event object
        """

	#Authenticating the post
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/sidecarrally/testhistory'

	#Making the data to post
        data = {
            "history": {
                "testlist_id": testlist_id,
                "project_id": project_id,
                "results": results
            }
        }
        data = self._obj.http.post(url,  data, headers)
        return TestHistory(data['body']['test_history'])

    def get_test_history(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> test history id
        # |
        # | Returns: history Object
        """

	#Authenticating and sending the get request
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/sidecarrally/testhistory/%s' %(id)
        data = self._obj.http.get(url, headers)
        return TestHistory(data['body']['test_history'])
     
    def delete_test_history(self, id):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  :id <string> history id
        # |
        # | Returns: history Object
        """

	#Authenticating and sending the delete request
        self._obj.authenticate()
        headers = {"X-Auth-Token":self._obj.authenticated_token}
        url = self._obj.sidecar_url + '/evacuates/sidecarrally/testhistory/%s' %(id)
        data = self._obj.http.delete(url, headers) 
