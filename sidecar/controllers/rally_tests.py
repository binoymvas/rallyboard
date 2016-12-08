# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: RootController.py                        |
# |                                                     |
# | Package Name: Python-Sidecar REST API               |
# |                                                     |
# | Version: 2.0                                        |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

from pecan         import expose
from pecan.rest    import RestController
from sidecar       import rbac
from sidecar.model import rally_model as rally_sql
from sidecar       import exception, rbac
from oslo_log      import log
from oslo_config   import cfg
import pecan, sidecar.validation as validation, ConfigParser, collections
import subprocess
import re

try:
    import simplejson as json
except ImportError: 
    import json
import datetime
CONF = cfg.CONF
LOG = log.getLogger(__name__)

class TestLogController(RestController):
    LOG.error("In  the getting all the project tests. TestListController")
    
    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """

        # Getting the configuartion file and its details
        LOG.info("Getting the configuration file(/etc/sidecar/sidecar.conf")
	LOG.info("In TestLogController")
        config_file = cfg.CONF.config_file[0]
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        #Making the database connection
        LOG.info("Making the database connection.")
        self.rally_tests = rally_sql.RallyModel()

    @expose(generic=True, template='json')
    def get_all(self, **kw):
        """
        # | Function to list the events
        # |
        # | @Arguments:
        # |     <kw>: Url query parameters
        # |
        # | @Returns: Json response
        """
	LOG.info("getting the list of logssss..")
        try:
            rbac.enforce('list_events', pecan.request)
            if 'report' in kw.keys():
                tests = self.rally_tests.test_report(kw)
            else:
                tests = self.rally_tests.list_tests(kw)
            return {"tests_list": tests}
        except Exception as err:
            LOG.error("Error in getting all the tests. get all")
            return exception_handle(err)

    @expose(generic=True, template='json')
    def get(self, project_id):
	LOG.info("getting the logssss..")
	try:
            logs = self.rally_tests.get_test_log(project_id)
  	    return {"tests_logs": logs}
	except Exception as err:
            LOG.error("Error in getting all the tests. get")
            return exception_handle(err)

    @expose(generic=True, template='json', content_type="application/json")
    def put(self, test_id):
        """
        # | Function to handel the edit part of an event
        # |
        # | Arguments:
        # | <event_id>: The event id which will be edited
        # | 
        # | Returns: Dictionary
        """
        try:
            rbac.enforce('edit_event', pecan.request)
            #valid = validation.Validation()
            #valid.json_header()
            #json_data = valid.json_data('edit_event', pecan.request.body_file.read())
            kw = {}
            kw['test_added'] = '1'
            self.rally_tests.update_test(test_id, kw)
            pecan.response.status = 204
        except Exception as e:
            print e.message
            return exception_handle(e)

class TestListController(RestController):
    LOG.error("In  the getting all the project tests. TestListController")
    
    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """

        # Getting the configuartion file and its details
        LOG.info("Getting the configuration file(/etc/sidecar/sidecar.conf")
        config_file = cfg.CONF.config_file[0]
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        #Making the database connection
        LOG.info("Making the database connection.")
        self.rally_tests = rally_sql.RallyModel()

    @expose(generic=True, template='json')
    def get_all(self, **kw):
        """
        # | Function to list the events
        # |
        # | @Arguments:
        # |     <kw>: Url query parameters
        # |
        # | @Returns: Json response
        """
        try:
            rbac.enforce('list_events', pecan.request)
	    if 'report' in kw.keys():
	        tests = self.rally_tests.test_report(kw)
	    else:
                tests = self.rally_tests.list_tests(kw)
            return {"tests_list": tests}
        except Exception as err:
            LOG.error("Error in getting all the tests. get lla 2")
            return exception_handle(err)


    @expose(generic=True, template='json', content_type="application/json")
    def put(self, test_id):
        """
        # | Function to handel the edit part of an event
        # |
        # | Arguments:
        # | <event_id>: The event id which will be edited
        # | 
        # | Returns: Dictionary
        """
        try:
            rbac.enforce('edit_event', pecan.request)
            #valid = validation.Validation()
            #valid.json_header()
            #json_data = valid.json_data('edit_event', pecan.request.body_file.read())
            kw = {}
            kw['test_added'] = '1'
            self.rally_tests.update_test(test_id, kw)
            pecan.response.status = 204
        except Exception as e:
            print e.message
            return exception_handle(e)

class RallyTestController(RestController):
    """
    # | Class to handel the REST API part of events in Evacuate 
    # | During post and put, we need a 307 redirection, which is
    # | Difficult if we handel it with index_GET, index_POST, etc.
    # | So AS per the doc http://pecan.readthedocs.io/en/latest/rest.html#url-mapping
    # | We have inherited this class from RestController    
    """

    testlist = TestListController()
    testlog  = TestLogController()

    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """

        # Getting the configuartion file and its details
        LOG.info("Getting the configuration file(/etc/sidecar/sidecar.conf")
        config_file = cfg.CONF.config_file[0]
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        
        #Making the database connection
        LOG.info("Making the database connection.")
        self.rally_tests = rally_sql.RallyModel()

    @expose(generic=True, template='json', content_type="application/json")
    def post(self, **kw):
        """
        # | Method to post detail of a test
        # |
        # | Arguments: id
        # |
        # | Returns: Dictonary
        """
        try:
  	    
            #Getting the id of the project and getting the test details	   
	    LOG.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
	    LOG.info(kw)
  	    LOG.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")

	    if 'id' in kw['project']:
		project_id = kw['project']['id']
		#rbac.enforce('get_test_details', pecan.request)
		
		#Getting the test details
                result = self.rally_tests.get_test_details(project_id)
	
		#Callign the execution methods
        	if str(project_id) == '1':
		    test_output = self.executeAllTests(result)
		    LOG.info('nooooooooooooooooooooooo---------------------')
		    print(test_output)
		    LOG.info('nooooooooooooooooooooooo*************************')

                elif str(project_id) == '2':
                    test_output = self.executeBenchmarkTests(result)
                else:
                    LOG.info('nooooooooooooooooooooooo')
		    LOG.info(project_id)
            LOG.info('Executon of the test is completed. Updated the test uuid.')
        except Exception as e:
            LOG.error(e)
       
    @expose(generic=True, template='json')
    def get_all(self, **kw):
        """
        # | Function to list the events
        # |
        # | @Arguments:
        # |     <kw>: Url query parameters
        # |
        # | @Returns: Json response
        """
        try:
            rbac.enforce('list_events', pecan.request)
            tests = self.rally_tests.project_tests_lists(kw)
            return {"project_tests": tests}
        except Exception as err:
            LOG.error("Error in getting all the project tests.")
            return exception_handle(err)

    """
    def executeAllTests(self, test_list):

	for row in test_list:
            test_id  = row['id']
            regex    = row['test_regex']
            LOG.info('Entering the loop for All Tests section')
            #output = subprocess.call('rally verify start --system-wide --regex ' + regex, shell=True)
            cmd = 'rally verify start --system-wide --regex ' + regex + ' &'


	    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
	    for stdout_line in iter(popen.stdout.readline, ""):
        	yield stdout_line

	    popen.stdout.close()
	    return_code = popen.wait()
	    if return_code:
        	raise subprocess.CalledProcessError(return_code, cmd)

	    # Example
	    #for path in execute(["locate", "a"]):
	    #    print(path, end="")
    """

    def executeAllTests(self, test_list):
        """
        # | Function to execute all tests
        # | 
        # | @Arguments:
        # |   
        # | @Return
        """
        #execute All tests
        for row in test_list:
            test_id  = row['id']
            regex    = row['test_regex']
	    project_id = row['project_id']
            LOG.info('Entering the loop for All Tests section')
            #output = subprocess.call('rally verify start --system-wide --regex ' + regex, shell=True)
            cmd = 'rally verify start --system-wide --regex ' + regex 
	    LOG.info(cmd)
            res = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
            output, err = res.communicate()
	    LOG.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2 ")
	    LOG.info(output)
	    self.update_testlog(project_id, output, 0)
	    LOG.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2---------------------------------")
            LOG.info('Going to extract the UUID corresponding to the test id ' + test_id)
            uuid = self.extractVerificationUUID(output)
            LOG.info('Updating the test uuid in the Database')
  	    kw = {}
  	    kw['test_uuid'] = uuid
            exec_test = self.rally_tests.update_test(test_id, kw)
	return True

    def update_testlog(self, project_id, output, status):
	kw = {}


	previous_data = self.rally_tests.get_test_log(project_id)
	LOG.info("###############################################################################")
	#LOG.info(previous_data)
	LOG.info(previous_data['log_data'])
	LOG.info("###############################################################################")

	newout = str(previous_data['log_data'] + str(output))
	kw['log_data'] = newout
	kw['test_status'] = status
	self.rally_tests.update_test_log(project_id, kw)

    def executeBenchmarkTests(self, service_list):
        """
        # | Function to execute Benchmarking Tests
        # | 
        # | @Arguments:
        # |
        # | @Return:    
        """
        #execute Benchmark tests
        yaml_path       = '/home/qaTest/'
        task_file       = 'task.yaml'
        scenario        = yaml_path + task_file
        LOG.info(scenario)
        LOG.info('Going to execute the command - rally task start '+ scenario +' --task-args \'{"service_list": ["hosts", "images"]}\'')
        #output       = subprocess.call('rally task start '+ scenario +' --task-args \'{"service_list": ["hosts", "images"]}\'', shell=True)
        cmd = 'rally task start '+ scenario +' --task-args \'{"service_list": ["hosts", "images"]}\''
        res = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
        output, err = res.communicate()
        LOG.info(output)
        LOG.info('Going to extract the UUID corresponding to the test id ' + test_id)
        uuid = self.extractTestUUID(output)
        LOG.info(uuid)
        LOG.info('Updating the test uuid in the Database')
        #update_uuid = sidecar.events.update_test(id = test_id, test_uuid = uuid)
	kw = {}
	kw['test_uuid'] = uuid
	exec_test = self.rally_tests.update_test(test_id, kw)
	return True

    def extractVerificationUUID(self, output):
        """
        # |
        # |
        # |
        # |
        # |
        """
        #extract the Verification UUID from the output
        replaced_output = output.replace('\n', ' ')
        LOG.info('+++++++++Replaced Output+++++++++')
        LOG.info(replaced_output)
        match = re.findall('Verification UUID: (.*?) ', replaced_output)
        LOG.info(match)
        return match

    def extractTestUUID(self, output):
        """
        # | Extract the UUID of the test
        # |
        # |
        # |
        # |
        """
        #extract the test UUID from the output
        replaced_output = output.replace('\n', ' ')
        LOG.info('+++++++++Replaced Output+++++++++')
        LOG.info(replaced_output)
        match = re.findall('rally task results (.*?) ', replaced_output)
        LOG.info(match)
        return match

def exception_handle(e):
    """
    # | Function to handle the exception
    # |
    # | Arguments: None
    # |
    # | Returns: error
    """
    LOG.error(e.message)
    if hasattr(e, 'code') and hasattr(e, 'title'):
        # If code is present, then it is a cutom exception
        # made by us
        return send_error(e.code, e.title, e.message)
    return send_error(500, 'Internal Server Error', 'Unknown error occured')

def send_error(code, title, message):
    """
    # | Functon to retun the exception
    # |
    # | Arguments: 
    # | <code>: Error code  
    # | <title>: Http tile
    # | <message>: Exception message
    # |
    # | Returns: Dictionary
    """
    pecan.response.status = code
    error =  collections.OrderedDict()
    error["code"]    = code
    error["title"]   = title
    error["message"] = message
    return { "error": error }

