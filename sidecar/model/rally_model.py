# -*- coding: utf-8 -*-
# _______________________________________________________
# | File Name: rally_model.py                         |
# |                                                     |
# | Package Name: Python-Sidecar MODEL API              |
# |                                                     |
# | Version: 2.0                                        |
# |                                                     |
# | Sofatware: Openstack                                |
# |_____________________________________________________|
# | Copyright: 2016@nephoscale.com                      |
# |                                                     |
# | Author:  info@nephoscale.com                        |
# |_____________________________________________________|

#importing the packages
from oslo_config        import cfg
from oslo_log           import log
from oslo_db.sqlalchemy import models
from sqlalchemy.ext     import declarative
from sqlalchemy         import *
from sqlalchemy.sql     import select
from sqlalchemy         import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME, Enum
from sidecar            import exception
from sqlalchemy.orm     import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
try:
    import simplejson as json
except ImportError: 
    import json
import sqlalchemy, ConfigParser, enum, uuid, datetime, collections

CONF = cfg.CONF
LOG = log.getLogger(__name__)

# READ THE CONNECTION VARIABLE
try:
    config_file = cfg.CONF.config_file[0]
    config = ConfigParser.ConfigParser()
    config.read(config_file) 
    sql_connection = config.get('database', 'connection', '')   
    LOG.info("Getting the db configuration and ding the connection.)")
except Exception as e:
    LOG.error(str(e))
    sql_connection = ''
    raise exception.ConnectionError("Connection Error with the database")

class RallyModel():
    """
    # | Evacuate model
    """
    metadata = MetaData()
    engine   = create_engine(sql_connection, pool_recycle=3600)
    conn     = engine.connect()
    
    #Creating the tables
    project_tests_list = Table('project_tests_list', metadata,
                               Column('id', Integer(), primary_key=True, unique=True, nullable=False),
                               Column('name', String(100), default='', unique=True, nullable=False),
                               Column('test_status', Integer(), default='0', nullable=True),
                               Column('test_create_time', DATETIME, default='0000-00-00 00:00:00', nullable=False),
                               Column('extra', Text)
                               )

    #Creating a configuration table
    tests_list   = Table('tests_list', metadata,
                         Column('id', String(100), primary_key=True, unique=True, nullable=False),
                         Column('name', String(200), default='', nullable=False),
                         Column('project_id', Integer, ForeignKey('project_tests_list.id')),
                         Column('test_service', String(200), default='', nullable=False),
                         Column('test_scenario', String(100), default='', nullable=False),
                         Column('test_regex', String(300), default='', nullable=False),
                         Column('test_added', Integer(), default='0', nullable=True),
                         Column('test_verified', String(100), nullable=True),
                         Column('test_create_time', DATETIME, default='0000-00-00 00:00:00', nullable=False),
                         Column('test_uuid', String(200), nullable=True),
                         Column('results', Text(), default='', nullable=False)
                         )

    #Test logs
    test_log = Table('tests_log', metadata,
                     Column('id', String(100), primary_key=True, unique=True, nullable=False),
                     Column('log_data', Text(), default='', nullable=False),
                     Column('project_id', String(100), default='', nullable=False),
                     Column('test_status', Integer(), default='0', nullable=True)
                     )

    #Creating the tables
    metadata.create_all(engine)
    LOG.info("Created the rally tables.)")
    project_tests_name = ['All Tests', 'Benchmark Tests', 'Quick QA Tests']
    for name in  project_tests_name:
        unique_id = uuid.uuid4().hex
        arg = {
            "name": name,
            "test_status": "1",
            "test_create_time": datetime.datetime.now()
        }
        #Inserting the data
        ins = project_tests_list.insert().values(arg)
        #result = conn.execute(ins)
    
    def project_tests_lists(self, args={}):
        """
        # | Method to list the event logs
        # |
        # | Arguments: 
        # |   <args>: Dictionary
        # |
        # | Returns 
        """

        # Okay Bow lets start our query builder
        get_project_test_list = select([self.project_tests_list])
        LOG.info("Created the query to get the list of project tests.")
 
        try:
            result = self.conn.execute(get_project_test_list)
        except Exception as e:
            return []

        #Getting the values are setting it in list
        log_list = []
        for row in result:
            log_data = collections.OrderedDict()
            log_data['id']               = row['id']
            log_data['name']             = row['name']
            log_data['test_status']      = row['test_status']
            log_data['test_create_time'] = row['test_create_time']
            log_data['extra']            = row['extra']
            log_list.append(log_data)
        LOG.info("Created the query to get the list of project tests.")
        return log_list
    
    def list_tests(self, args={}):
        """
        # | Method to list the event logs
        # |
        # | Arguments: 
        # |   <args>: Dictionary
        # |
        # | Returns 
        """

        # Okay Bow lets start our query builder
        get_tests_list = select([self.tests_list])
        LOG.info("Created the query to get the list of tests.")
            
        #Making the search criteria
        if "id" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.id == args['id'])
        if "name" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.name.like('%' + args['name'] + '%'))
        if "project_id" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.project_id == args['project_id'])
        if "test_service" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.test_service.like('%' + args['test_service'] + '%'))
        if "test_scenario" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.test_scenario.like('%' + args['test_scenario'] + '%'))
	if "test_added" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.test_added == args['test_added'])
  
        try:
            result = self.conn.execute(get_tests_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values are setting it in list
        test_list = []
        for row in result:
            test_data = collections.OrderedDict()
            test_data['id']               = row['id']
            test_data['name']             = row['name']
            test_data['project_id']       = row['project_id']
            test_data['test_service']     = row['test_service']
            test_data['test_scenario']    = row['test_scenario']
            test_data['test_regex']       = row['test_regex']
            test_data['test_added']       = row['test_added']
            test_data['test_verified']    = row['test_verified']
            test_data['test_create_time'] = row['test_create_time']
            test_list.append(test_data)
        return test_list

    def update_test(self, test_id, args):
        """
        # | Method to update an tests
        # |
        # | Arguments:
        # |     <uuid>: id
        # |     <args>: Dictionary containg diffrent update sections
        # |
        # | Returns: None
        """
        LOG.info('++++++++Update_test section in Model+++++++++')
        data = {}
        
        #Fetching all individual values and storing it before DB updation
        if "test_verified" in args['test_list']:
	    data['test_verified'] = args['test_list']['test_verified']
	if "test_added" in args['test_list']:
	    data['test_added'] = args['test_list']['test_added']
        if "test_uuid" in args['test_list']:
            data['test_uuid']  = args['test_list']['test_uuid']
        if "results" in args['test_list']:
            data['results']  = args['test_list']['results']
        
        LOG.info('+++++++Entering the sidecar update_test function++++++++')
        #Updating the data
        update = self.tests_list.update().where(self.tests_list.c.id == test_id).values(data)
        LOG.info('Update Query is ')
        LOG.info(update)
        LOG.info('+++++++++++++++++++++++++++')
        self.conn.execute(update)
        LOG.info("Test is updated succesfully.")

    def update_test_log(self, project_id, data):
	"""
        # | Method to update an tests log
        # |
        # | Arguments:
        # |     <uuid>: project_id
        # |     <data>: Dictionary containg diffrent update sections
        # |
        # | Returns: None
        """

        #Getting the details of test log using project id
        #Updating the data
        update = self.test_log.update().where(self.test_log.c.project_id == project_id).values(data)
        self.conn.execute(update)
        LOG.info("Test log is updated succesfully.")	

    def get_test_details(self, test_id):
        """
        # | Function to get the details of a test
        # |
        # | Arguments:
        # |  <id>: Id of thetest
        # |
        # | Returns: 
        """
        #Getting the detail of the test
        get_data_select = select([self.tests_list]).where(and_(self.tests_list.c.test_added == 1, self.tests_list.c.project_id == test_id))
	LOG.info('get_data_select')
	LOG.info(get_data_select)
	LOG.info('get_data_select')

        try:
            result = self.conn.execute(get_data_select)
        except Exception as e:
            return []

        #Getting the values are setting it in list
        log_list = []
        for row in result:
            log_data = collections.OrderedDict()
            log_data['id']                     = row['id']
            log_data['name']                   = row['name']
            log_data['project_id']             = row['project_id']
            log_data['test_service']           = row['test_service']
            log_data['test_scenario']          = row['test_scenario']
            log_data['test_regex']             = row['test_regex']
            log_data['test_added']             = row['test_added']
	    log_data['test_verified']          = row['test_verified']
	    log_data['test_create_time']       = row['test_create_time']
	    log_data['test_uuid']              = row['test_uuid']
            log_data['results']                = row['results']
            log_list.append(log_data)
        
	#Retunrning the log list
	LOG.info("Created the query to get the list of project tests.")
        return log_list

    def test_report(self, args={}):
        """
        # | Method to list the event logs
        # |
        # | Arguments: 
        # |   <args>: Dictionary
        # |
        # | Returns 
        """

        # Okay Bow lets start our query builder
        get_tests_list = select([self.tests_list])
        LOG.info("Created the query to get the list of tests for the report.")

        #Making the search criteria
        if "project_id" in args:
            get_tests_list = get_tests_list.where(self.tests_list.c.project_id == args['project_id'])
        try:
            result = self.conn.execute(get_tests_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values are setting it in list
        test_list = []
        for row in result:
            reports = self.conn.execute("select * from verification_results where verification_uuid='" + str(row['test_uuid']) + "'")
	    for report in reports:
		report_data = collections.OrderedDict()
		report_data['updated_at'] = report['updated_at']
		report_data['created_at'] = report['created_at']
		report_data['id'] = report['id']
		report_data['data'] = report['data']
		report_data['verification_uuid'] = report['verification_uuid']
	    	test_list.append(report_data)
        return test_list

    def get_test_log(self, project_id=None):
	"""
        # | Method to get logs
        # |
        # | Arguments: 
        # |   <args>: Dictionary
        # |
        # | Returns 
        """
	# Okay Bow lets start our query builder
        get_test_log = select([self.test_log])
        LOG.info("Created the query to get the log of project.")
	LOG.info(project_id)
        #Making the search criteria
        if project_id != None:
            get_test_log = get_test_log.where(self.test_log.c.project_id == project_id)
	    LOG.info(get_test_log)
        try:
            result = self.conn.execute(get_test_log)
        except Exception as e:
            LOG.error(str(e))
            return []


	row = result.fetchone()
        log_data = collections.OrderedDict()
	log_data['id'] = row['id']
        log_data['log_data'] = row['log_data']
        log_data['project_id'] = row ['project_id']
        log_data['test_status'] = row ['test_status']
        return log_data

	"""
        result["id"]                  = uuid
        result["name"]                = data["name"]
        result["event_status"]        = data["event_status"]
        result["event_create_time"]   = data["event_create_time"]
        result["event_complete_time"] = data["event_complete_time"]
        result["node_uuid"]           = data["node_uuid"]
        result["vm_uuid_list"]        = None
        result['extra']               = None
        result['moredata']            = None
        result['predata']             = None
    
        # If the proper data is there 
        # then convert them into json
        if data["vm_uuid_list"]:
            result["vm_uuid_list"] = json.loads(data["vm_uuid_list"])
        if data['extra']:
            result['extra'] = json.loads(data['extra'])
 
        return result


        #Getting the values are setting it in list
        test_logs = []
        for row in result:
	    log_data = collections.OrderedDict()
	    log_data['id'] = row['id']
   	    log_data['log_data'] = row['log_data']
	    log_data['project_id'] = row ['project_id']
	    log_data['test_status'] = row ['test_status']
  	    test_logs.append(log_data)
	LOG.info('test_logs')
        LOG.info(test_logs)
	LOG.info('test_logs')
	return test_logs
	"""
