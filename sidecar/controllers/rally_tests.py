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
import shlex
import re
import os

try:
    import simplejson as json
except ImportError: 
    import json
import datetime
CONF = cfg.CONF
LOG = log.getLogger(__name__)

class TestConfigController(RestController):
    """
    # Class to handle the TestConfig settings
    #
    #
    #
    """
    def __init__(self, data=None):
        """
        # | Initialization function
        # | <Arguments>:
        # |             None
        # | Return Type: Void
        # | 
        """
        self.rally_tests = rally_sql.RallyModel()

    @expose(generic=True, template='json')
    def get(self, option_name):
        """
        # | Method to get the Test Config details
        # | Argument:
        # |   <testconfig_id>: id from test config table
        # | Return:
        """
        try:
            LOG.info('Get function')
            rbac.enforce('get_detail', pecan.request)
            result = self.rally_tests.get_test_config_value(option_name)
            return { "test_history": result }
        except Exception as e:
            return exception_handle(e)

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
            LOG.info('get all function')
            test_configs = self.rally_tests.get_all_test_configs(kw)
            return {"test_history": test_configs}
        except Exception as err:
            return exception_handle(err)

class TestHistoryController(RestController):
    """
    # | Class to handel the REST API part of events in Evacuate 
    # | During post and put, we need a 307 redirection, which is
    # | Difficult if we handel it with index_GET, index_POST, etc.
    # | So AS per the doc http://pecan.readthedocs.io/en/latest/rest.html#url-mapping
    # | We have inherited this class from RestController    
    """
    def __init__(self, data=None):
        """
        # | Constructor function
        # | 
        # | Arguments: None
        # |
        # | Return Ttype: Void
        """
        self.rally_tests = rally_sql.RallyModel()

    @expose(generic=True, template='json')
    def get(self, testhistory_id):
        """
        # | Method to get get detail of an event
        # |
        # | Arguments: testhistory id
        # |
        # | Returns: Dictonary
        """
        try:
            LOG.info('Get function')
            rbac.enforce('get_detail', pecan.request) 
            result = self.rally_tests.get_test_history(testhistory_id)
            return { "test_history": result }
        except Exception as e:
            return exception_handle(e)
     
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
            LOG.info('get all function')
            rbac.enforce('list_events', pecan.request)
            test_histories = self.rally_tests.list_test_history(kw)
            return {"test_history": test_histories}
        except Exception as err:
            return exception_handle(err)
       
    @expose(generic=True, template='json', content_type="application/json")
    def post(self,  **kw):
        """
        # | Function to create a new history
        # |
        # | Arguments: None
        # |
        # | Returns: Json object
        """
        try:
  	    LOG.info("In the create of the history..................")
            rbac.enforce('create_event', pecan.request)
	    LOG.info(kw)
	    #valid = validation.Validation()
            #valid.json_header()
	    #json_data = valid.json_data('create_event', pecan.request.body_file.read())
	    #print(json_data)
	    LOG.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")    
            data = kw['history']
            LOG.info('creating test history with data')
	    LOG.info(data)
	    LOG.info('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            new_id = self.rally_tests.create_test_history(data)
            pecan.response.status = 201
            return { "test_history": self.rally_tests.get_test_history(new_id)}
        except Exception as e:
            return exception_handle(e)
              
    @expose(generic=True, template='json',  content_type="application/json")
    def delete(self, testhistory_id):
        """
        # | Function to handle the delete test history via REST API call
        # |
        # | Arguments:
        # |     <testhistory_id>: id of the test history
        # |
        # | Returns: Null
        """
        try:
            rbac.enforce('delete_event', pecan.request)
            self.rally_tests.delete_test_history(testhistory_id)
            pecan.response.status = 204
            return {}
        except Exception as e:
            return exception_handle(e)

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
    def put(self, test_id, **kw):
        """
        # | Function to handel the edit part of an event
        # |
        # | Arguments:
        # | <event_id>: The event id which will be edited
        # | 
        # | Returns: Dictionary
        """
	LOG.error('kw start')
	LOG.error(kw)
	LOG.error('kw end ')
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
    def put(self, test_id, **kw):
        """
        # | Function to handel the edit part of an event
        # |
        # | Arguments:
        # | <event_id>: The event id which will be edited
        # | 
        # | Returns: Dictionary
        """
        try:
            LOG.info('PUT SECTION............................')
            rbac.enforce('edit_event', pecan.request)
            #valid = validation.Validation()
            #valid.json_header()
            #json_data = valid.json_data('edit_event', pecan.request.body_file.read())
            #kw = {}
            #kw['test_added'] = '1'
            LOG.info('++++++++++++++++++++++++++++++')
            LOG.info(kw)
            LOG.info('++++++++++++++++++++++++++++++')
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
    testhistory = TestHistoryController()

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
	    if 'id' in kw['project']:
		project_id = kw['project']['id']
		#rbac.enforce('get_test_details', pecan.request)
                LOG.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
	        #Getting the test details
                result = self.rally_tests.get_test_details(project_id)
                LOG.info("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
		
		#Calling the execution methods
        	if str(project_id) == '1':
 		    self.update_testlog(project_id, '', 0)
		    test_output = self.executeAllTests(result)

                elif str(project_id) == '2':
                    LOG.info('Project id is 2')
	            self.update_testlog(project_id, '', 0)
                    LOG.info('Result is ')
		    LOG.info(result)
                    test_output = self.executeBenchmarkTests(result, project_id)
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

    def executeAllTests(self, test_list):
        """
        # | Function to execute all tests
        # | 
        # | @Arguments:
        # |   
        # | @Return
        """
        #execute All tests
        LOG.info("Creating the file to save the list")
        file_path = "/tmp/test_list.txt"
        fp = open(file_path,"w")
        os.chmod(file_path, 0777)

        #Adding the test to the file
        for row in test_list:
            test_id    = row['id']
            regex      = row['test_regex']
            project_id = row['project_id']
            fp.write(regex + '\n')
            LOG.info("Adding test %s to the list", row['test_regex'])
        fp.close
        fp.flush()

        #Entering to the loop and making the file execution
        if os.path.isfile(file_path):
            LOG.info('Entering the loop for All Tests section')

            #Making the command for the test execution
            cmd = 'rally verify start --system-wide --tests-file ' + file_path
            LOG.info(cmd)
            res = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
            output, err = res.communicate()
            LOG.info(output)
            #self.update_testlog(project_id, output, 0)
            LOG.info('Going to extract the UUID corresponding to the test id ' + test_id)
            uuid = self.extractVerificationUUID(output)
            LOG.info('Test UUID is ')
            LOG.info(uuid)
            LOG.info('Executing the function for generating the report')
            test_report = self.generateTestReport(test_id, uuid)

            LOG.info('Updating the test log with the log and the result.')
	    self.update_testlog(project_id, output, 0, test_report)

            #Making the dictionary for the history creation
            history = {}
            history['testlist_id'] = test_id
            history['project_id'] = project_id
            history['results'] = test_report
            self.rally_tests.create_test_history(history)
            LOG.info("Created the history for test reporti")
        return True

    def update_testlog(self, project_id, output, status, results=None):
        kw = {}
        LOG.info("###############################################################################")
        if output != None:
            kw['log_data'] = output
        kw['test_status'] = status
        if results != None:
            kw['results']     = results
        self.rally_tests.update_test_log(project_id, kw)

    def execute_command(self, command, project_id, search_text):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        uuid = ''
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                LOG.info("#####################################")
                LOG.info(output.strip())
                previous_data = self.rally_tests.get_test_log(project_id)
                newout = str(previous_data['log_data'] + str(output))
                self.update_testlog(project_id, newout, 0)
                replaced_output = output.replace('\n', ' ')
                LOG.info('+++++++++Replaced Output+++++++++')
                match = re.findall('rally task results (.*?) ', replaced_output)
                if len(match) > 0:
                    uuid = match[0]
                    LOG.info("uuid")
                    LOG.info(uuid)
                    LOG.info("uuid end ")

                LOG.info("#####################################")
        rc = process.poll()
        return uuid

    def executeBenchmarkTests(self, service_list, project_id):
        """
        # | Function to execute Benchmarking Tests
        # | 
        # | @Arguments:
        # |
        # | @Return:    
        """
        services = []
        for row in service_list:
            services.append(row['test_regex'])

        LOG.info('Service list is ')
	LOG.info(services)
	self.update_testlog(project_id, '', 0, '')
      
        LOG.info('Entering the config data check')

        #Fetching the config values from DB
        image_value   = self.rally_tests.get_test_config_value('image_name')
        flavor_value  = self.rally_tests.get_test_config_value('flavor_name')

        #config_data = self.rally_tests.get_all_test_configs()
        LOG.info('################################################')
        LOG.info(image_value)
	LOG.info(flavor_value)
        LOG.info('################################################')

        #execute Benchmark tests
        #LOG.info(service_list)
        LOG.info('service list printed above+++++++++++++++++++++++++')
        LOG.info(project_id)
        LOG.info('=========================================')
        yaml_path       = '/home/benchmarkTests/'
        task_file       = 'task.yaml'
        scenario        = yaml_path + task_file
        LOG.info(scenario)
        
	#cmd = 'rally task start '+ scenario +' --task-args \'{"service_list": ' + str(services) + '}\''
        cmd = 'rally task start '+ scenario +' --task-args \'{"service_list": ' + str(services) + ', "image_name": ' + image_value + ', "flavor_name": '+ flavor_value + '}\''

        LOG.info('Command is ')
        LOG.info(cmd)
        LOG.info("~~~~~~~~~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@~~~~~~~~~~~~~~~")
        uuid = self.execute_command(cmd, project_id, 'rally task results (.*?) ')
        LOG.info(uuid)
        LOG.info("~~~~~~~~~@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@~~~~~~~~~~~~~~~end")
        """
        LOG.info(cmd)
        res = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
        output, err = res.communicate()
        
        LOG.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2 ")
        LOG.info(output)
        LOG.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2---------------------------------")
        uuid = self.extractTestUUID(output)
        """
        LOG.info('Test UUID is ')
        LOG.info(uuid)
        LOG.info('Executing the function for generating the report')
        test_report = self.generateBenchmarkTestReport(uuid)
        LOG.info('Updating the test details in the Database')

        LOG.info('Inserting the details into test log table')
        self.update_testlog(project_id, None, 0, test_report)

        #Making the dictionary for the history creation
        history = {}
        history['testlist_id'] = '48381965508b4b1494b48d67f727dc91'
        history['project_id'] = project_id
        history['results'] = test_report
        self.rally_tests.create_test_history(history)
        LOG.info(history)
        LOG.info("Created the history for test report")
        LOG.info('Completed')
        return True
    
    def extractVerificationUUID(self, output):
        """
        # | Function to extract the Verification UUID from the output after running the Tempests Tests
        # | 
        # | <Arguments>
        # |     output: the output obtained after running the test
        # | <Return>
        # |     match[0] : the UUID obtained after regex check
        """
        #extract the Verification UUID from the output
        replaced_output = output.replace('\n', ' ')
        LOG.info('+++++++++Replaced Output+++++++++')
        #LOG.info(replaced_output)
        match = re.findall('Verification UUID: (.*?) ', replaced_output)
        LOG.info(match[0])
        return match[0]

    def extractTestUUID(self, output):
        """
        # | Extract the UUID from the output obtained after running the benchmark tests
        # |
        # | <Arguments>
        # |     output: the output obtained after running the test
        # | <Return>
        # |     match[0]: the UUID obtained after the regex check   
        """
        #extract the test UUID from the output
        replaced_output = output.replace('\n', ' ')
        LOG.info('+++++++++Replaced Output+++++++++')
        #LOG.info(replaced_output)
        match = re.findall('rally task results (.*?) ', replaced_output)
        LOG.info(match[0])
        return match[0]

    def generateTestReport(self, test_id, test_uuid):
        """
        # | Generate the Test Report using test uuid
        # | <Arguments>:
        # |    test_id: The id of the test which is to be executed
        # |    test_uuid: UUID obtained after running the test
        # | <Return>:
        # |    test_report: a test report in html format
        # |
        """
        LOG.info('Going to generate the test report')
        report_cmd = 'rally verify results --uuid '+ test_uuid +' --html'
        LOG.info('Report command is '+ report_cmd)
        p = subprocess.Popen(report_cmd, stderr=subprocess.STDOUT, shell=True, stdout=subprocess.PIPE)
        output, err = p.communicate()
        return output

    def generateBenchmarkTestReport(self, test_uuid):
        """
        # | Generate the Test Report of Benchmark Tests using test uuid
        # | <Arguments>:
        # |    test_id: The id of the test which is to be executed
        # |    test_uuid: UUID obtained after running the test
        # | <Return>:
        # |    test_report: a test report in html format
        # |
        """
        LOG.info('Going to generate the test report')
 	LOG.info('@@@@@@@@@@@@@@@@@@@@@@')
 	LOG.info('Task UUID is ')
 	LOG.info(test_uuid)
 	LOG.info('@@@@@@@@@@@@@@@@@@@@@@')
        report_cmd = 'rally task report '+ test_uuid +' --html'
        LOG.info('Report command is '+ report_cmd)
        p = subprocess.Popen(report_cmd, stderr=subprocess.STDOUT, shell=True, stdout=subprocess.PIPE)
        output, err = p.communicate()
 	LOG.info('Benchmarking test Report Has been Generated successfully')
	return output

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

