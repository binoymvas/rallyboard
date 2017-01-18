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
from sqlalchemy.dialects.mysql import LONGTEXT

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
    tests_list = Table('tests_list', metadata,
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
                         Column('results', LONGTEXT(), default='', nullable=False)
                         )

    #Test logs
    test_log = Table('tests_log', metadata,
                     Column('id', String(100), primary_key=True, unique=True, nullable=False),
                     Column('log_data', LONGTEXT(), default='', nullable=False),
                     Column('results', LONGTEXT(), default='', nullable=False),
		     Column('project_id', String(100), default='', nullable=False),
                     Column('test_status', Integer(), default='0', nullable=True)
                     )

    #Test history
    test_history = Table('test_history', metadata,
			Column('id', String(100), primary_key=True, unique=True, nullable=False),
 			Column('testlist_id', String(100), ForeignKey('tests_list.id')),
			Column('project_id', Integer(), default='0', nullable=False),		
 			Column('history_create_time', DATETIME, default='0000-00-00 00:00:00', nullable=False),
			Column('results', LONGTEXT(), default='', nullable=False)
			)

    #Test Config table
    test_config = Table('test_config', metadata,
                       Column('id', Integer, primary_key=True, nullable=False),
                       Column('option_name', String(255), default='', nullable=False),
                       Column('value', String(255), default='', nullable=False),
                       Column('project_id', Integer(), default='0', nullable=False),
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
	    test_data['test_uuid']        = row['test_uuid']
	    test_data['results']          = row['results']
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
        if "update_null" in args['test_list']:
	    data['test_added'] = '0'
	    update = self.tests_list.update().where(self.tests_list.c.project_id == test_id).values(data)	
	else:
            #Updating the data
            update = self.tests_list.update().where(self.tests_list.c.id == test_id).values(data)
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
        #Making the search criteria
        if project_id != None:
            get_test_log = get_test_log.where(self.test_log.c.project_id == project_id)
        try:
            result = self.conn.execute(get_test_log)
        except Exception as e:
            LOG.error(str(e))
            return []

	#Fetching the details from the result
	row = result.fetchone()
        log_data = collections.OrderedDict()
	log_data['id'] = row['id']
        log_data['log_data'] = row['log_data']
        log_data['results'] = row['results']
	log_data['project_id'] = row ['project_id']
        log_data['test_status'] = row ['test_status']
        return log_data

    """*****************************Test Config******************************************"""
    def create_test_config(self, kw):
        """
        # | Adding new configuration values
        # | <Arguments>:
        # |  
        # | <Return>:
        # | 
        """
        args = {
                "option": kw['option'],
                "value":  kw['value']
               }
        LOG.info(args)
        #Inserting the data
        ins = self.test_config.insert().values(args)
        LOG.info(ins)
        result = self.conn.execute(ins)
        LOG.info("A new config option has been added to the DB")
        return True

    def get_test_config_value(self, option_name, project_id):
        """
        # | Function to fetch the config value corresponding to an option
        # | <Arguments>:
        # |     option_name : The name of the option for which we need to fetch the value from DB
        # | <Return>:
        # |     result:Value corresponding to the option from the DB
        """
        LOG.info('Entering the function - get_test_config_value')
        LOG.info('Fetching the option value from the DB')
	get_test_config_value = select([self.test_config]).where(and_(self.test_config.c.option_name == option_name, self.test_config.c.project_id == project_id))

	LOG.info('Select query is ')
	LOG.info(get_test_config_value)
        result = self.conn.execute(get_test_config_value)
        for row in result:
            config_value = row['value']
        LOG.info('The value corresponding to this option name is ')
        return config_value

    def get_all_test_configs(self):
        """
        # | Function to fetch the config value corresponding to an option
        # | <Arguments>:
        # |     
        # | <Return>:
        # |     
        """
        get_test_configs = select([self.test_config]).order_by(asc(self.test_config.c.id))
        try:
            result = self.conn.execute(get_test_configs)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values and storing it in a list
        config_list = []
        for row in result:
            config_data = collections.OrderedDict()
            config_data['id']                  = row['id']
            config_data['option_name']         = row['option_name']
            config_data['value']               = row['value']
            config_list.append(config_data)
        LOG.info('Sending back the result')
        return config_list

    def list_test_configs(self, args = {}):
       """
       # |  Function to list down all the config values from the DB
       # |  <Arguments>:
       # |     
       # |  <Return>:
       # |     
       """
       LOG.info('entering the function - list_test_configs')
       get_config_list = select([self.test_config])

       #Adding search criteria
       if "option_name" in args:
           get_config_list = get_config_list.where(self.test_config.c.option_name == args['option_name'])
       if "project_id" in args:
           get_config_list = get_config_list.where(self.test_config.c.project_id  == args['project_id'])
       if "test_status" in args:
           get_config_list = get_config_list.where(self.test_config.c.test_status == args['test_status'])
       LOG.info(get_config_list)
       try:
           result = self.conn.execute(get_config_list)
       except Exception as e:
           LOG.error(str(e))
           return []

       #Getting the values are storing it in list
       config_list = []
       for row in result:
            config_data                     = collections.OrderedDict()
            config_data['id']               = row['id']
            config_data['option_name']      = row['option_name']
            config_data['value']            = row['value']
            config_data['project_id']       = row['project_id']
	    config_data['test_status']      = row['test_status']
            config_list.append(config_data)

       LOG.info('Returning the data -config list')
       LOG.info(config_list)
       return config_list

    def edit_test_config(self, args):
        """"
	# | Function to edit the test config data from the edit form
        # | <Arguments>:
        # |    args - values to be used for DB updation
        # | <Return>:
        # |    Save the updated data in DB
        """
        data = {}
        data1 = {}
	data={}

	LOG.info(args['test_config']['conf_values'])
        LOG.info(args['test_config']['conf_values'].iterkeys())	
	LOG.info('Checking if flavor_ref is present')
        if 'flavor_ref' in args['test_config']['conf_values'].iterkeys():
    	    data['value']  = args['test_config']['conf_values']['flavor_ref']
            LOG.info(data['value'])
	    LOG.info('*************')
	    option = 'flavor_name'

	    test_list = []
	    data1['flavor_name'] = 'testflavor'
	    LOG.info('Going to do the update query for flavor')
	    update = self.test_config.update().where(and_(self.test_config.c.option_name == option, self.test_config.c.project_id == args['project_id'])).values(data)
	    LOG.info(update)
	    self.conn.execute(update)
	    LOG.info('updating the flavor value in db')

	LOG.info('Checking if image_ref is present')
	if 'image_ref' in args['test_config']['conf_values'].iterkeys():
	    data['value']  = args['test_config']['conf_values']['image_ref']
	    LOG.info(data['value'])
	    LOG.info('Going to do the update query for image')
	    update = self.test_config.update().where(and_(self.test_config.c.option_name == 'image_name', self.test_config.c.project_id == args['project_id'])).values(data)
	    LOG.info(update)
	    self.conn.execute(update)
	    LOG.info('Updating image value in DB')

    """***************************** Test Config Ends Here ******************************"""

    """***************************** history ********************************************"""
    def create_test_history(self, kw):
        """
        name createTestHistory
        Params: event data
        Return : Json data
        """

        #Setting the parameters for the event creation
        unique_id = uuid.uuid4().hex
	#LOG.info("History created with id 1111")
	LOG.info(kw)
        arg = {
            "id": unique_id,
            "testlist_id": kw['testlist_id'],
            "project_id":  kw['project_id'],
            "history_create_time": datetime.datetime.now(),
            "results": kw['results']
        }
	
        #Inserting the data
        ins = self.test_history.insert().values(arg)
	LOG.info(ins)
        result = self.conn.execute(ins)
        #LOG.info("History created with id " + str(unique_id))
        return unique_id
    
    def list_test_history(self, args={}):
        """
        # | Method to list the test history
        # |
        # | Arguments: Distionary containg the flter values
        # |
        # | Returns Distionary
        """

        #Setting the allowed args for the serach
        allowed_args = [
            'id',
            'testlist_id',
            'project_id',
            'results', 
            'history_create_time', 
            'min_history_create_time',
            'max_history_create_time', 
            'marker',
            'limit'
        ]
        valid_args = {}
        for arg in args:
            # | For each given argument
            # | If it matches with allowed argument
            # | Then treat it as valid arg
            if arg in allowed_args:
                valid_args[arg] = args[arg]

        # Okay Bow lets start our query builder
	get_history_list = select([self.test_history, self.tests_list.c.test_regex, self.tests_list.c.test_service], self.tests_list.c.id == self.test_history.c.testlist_id)
           
	#Iterating through each key
        for key in valid_args:
            if type(valid_args[key])==bool:
                val = valid_args[key]
            else:
                val = valid_args[key].strip()
       
            if not val:
                continue;
            if key == "id":
                get_history_list = get_history_list.where(self.test_history.c.id == val)
            if key == "testlist_id":
                get_history_list = get_history_list.where(self.test_history.c.testlist_id.like('%' + val + '%'))
            if key == "project_id":
                get_history_list = get_history_list.where(self.test_history.c.project_id.like('%' + val + '%'))
            if key == 'results':
                get_history_list = get_history_list.where(self.test_history.c.results.like('%' + val + '%'))
            if key == 'history_create_time':
                get_history_list = get_history_list.where(self.test_history.c.history_create_time == val)
            if key == 'min_history_create_time':
                get_history_list = get_history_list.where(self.test_history.c.history_create_time >= val)
            if key == 'max_history_create_time':
                get_history_list = get_history_list.where(self.test_history.c.history_create_time <= val)
        
        LOG.info("Created the query with filter options.")
        get_history_list = get_history_list.order_by(desc(self.test_history.c.history_create_time))
        # As per the documentaion in
        # https://specs.openstack.org/openstack/api-wg/guidelines/pagination_filter_sort.html
        # we need to add pagination  only after the filtering. So lets just filter out it.
        #
        # Point to be noted, though it is a bad idea to fetch all the data from db (in worst case when
        # there is no filter option), for time being we have done this way. Later we need to use sqlAlchemy
	LOG.error(get_history_list)
        try:
            result = self.conn.execute(get_history_list)
        except Exception as e:
            LOG.error(str(e))
            return []

        #Getting the values are setting it in list
        history_list = []
        for row in result:
            history_data = collections.OrderedDict()
            history_data['id']                  = row['id']
            history_data['testlist_id']         = row['testlist_id']
            history_data['project_id']          = row['project_id']
            history_data['history_create_time'] = row['history_create_time']
            history_data['results']             = row['results']
            history_data['test_regex']          = row['test_regex']
            history_data['test_service']        = row['test_service']
            history_data['moredata']            = False
            history_data['predata']             = True
            history_list.append(history_data)
 
        first_index = 0
        if 'marker' in valid_args:
            marker = valid_args['marker']
            if marker is not None:
                for (marker_index, history) in enumerate(history_list):
                    if history['id'] == marker:
                        # we start pagination after the marker
                        first_index = marker_index + 1
                        break        
        limit = 10 

        # Checking for the limit. If the given
        # Limit is not positive then, return emepty result
        if "limit" in valid_args:
            if not valid_args["limit"].isnumeric():
                return []
            if not valid_args["limit"] > 0:
                return []
            limit = valid_args["limit"].strip()
        limit = int(float(limit))
        catch_limit = int(first_index) + int(limit)

        #Adding the conditions to show previous or next links   
        if limit > len(history_list):
            #no need to display the next link and previous link
            next_val = False
            prev_val = False
           
        elif first_index > limit:
            #need to display the previous link
            prev_val = True
           
            #Case in each individual page other tahn the first page
            if catch_limit < len(history_list):
                #need to display the next link
                next_val = True
            else:
                next_val = False
        else:
            #need to display the previous link as well as the next link
            next_val = True

            #No need to display the previous link in the first page
            if first_index != 0:
                prev_val = True
            else:
                prev_val = False

        #Getting the event list with limit
        history_list = history_list[first_index: catch_limit]

        #Updating the moredata and predata with values
        for i in range(0, len(history_list)):
            history_list[i]['moredata'] = next_val
            history_list[i]['predata'] = prev_val

        LOG.info("Sending back the result.")
        return history_list
    
    def get_test_history(self, history_id=None):
        """
        # | Function to get the detail of an event
        # |
        # | Arguments:
        # |  <uuid>: Id of the event
        # |
        # | Returns: Json
        """

        #Getting the detail of the event
	LOG.info(history_id)
        get_history_select = select([self.test_history]).where(self.test_history.c.id.like('%' + history_id + '%'))
	get_data = self.conn.execute(get_history_select)
        LOG.info("Getting the history details")
	LOG.info(get_history_select)
	LOG.info(history_id)
        
	#Raise exception if no event is present else fetching the one
        if not get_data.rowcount:
            LOG.error("No history with id " + history_id + " found.")
            raise exception.NotFound("No history with id " + history_id + " found.")
        data = get_data.fetchone()
        result = collections.OrderedDict()
        result["id"]                  = history_id
        result["testlist_id"]         = data["testlist_id"]
        result["project_id"]          = data["project_id"]
        result["history_create_time"] = data["history_create_time"]
        result["results"]             = data["results"]
        result['moredata']            = None
        result['predata']             = None
    
        # If the proper data is there 
        # then convert them into json
        return result
    
    def delete_test_history(self, id):
        """
        # | Function to delete an test_history
        # |
        # | Arguments:
        # |     <id>: id of the testlist_history
        # |
        # | Returns: None
        """

        # | Deleting the history using the id 
        query = self.test_history.delete().where(self.test_history.c.id == id)
        self.conn.execute(query)
        LOG.info("Test list history is deleted succesfully.")

    
"""***************************** history ********************************************"""
