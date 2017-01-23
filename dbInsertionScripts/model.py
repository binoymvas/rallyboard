#importing the packages
from oslo_config        import cfg
from oslo_log           import log
from oslo_db.sqlalchemy import models
from sqlalchemy.ext     import declarative
from sqlalchemy         import *
from sqlalchemy.sql     import select
from sqlalchemy         import Table, Column, Integer, String, MetaData, ForeignKey, DATETIME, Enum

from sqlalchemy.orm     import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import UUID
try:   
    import simplejson as json
except ImportError: 
    import json
import sqlalchemy, ConfigParser, enum, uuid, datetime, collections


LOG = log.getLogger(__name__)

# READ THE CONNECTION VARIABLE
try:
    sql_connection = 'mysql+pymysql://root:openstack@198.100.181.77/sidecar'    
    LOG.info("Getting the db configuration and ding the connection.)")
except Exception as e:
    LOG.error(str(e))
    sql_connection = ''
    raise exception.ConnectionError("Connection Error with the database")

class Testcases():
    """
    # | Evacuate model
    """
    metadata = MetaData()
    engine   = create_engine(sql_connection, pool_recycle=3600)
    conn     = engine.connect()
    
    #Creating the tables
    #Creating a configuration table
    #Creating a configuration table

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
                         Column('results', LONGTEXT(), default='', nullable=False)
                         )


    metadata.create_all(engine)
    LOG.info("Created the tables.)")
    
    def createEvent(self, kw):
        """
        name createEvent
        Params: event data
        Return : Json data
        """

        #Setting the parameters for the event creation
        unique_id = uuid.uuid4().hex
        arg = {
            "id": unique_id,
            "name": kw['name'],
            "project_id": kw['project_id'],
            'test_service': kw['test_service'],
            'test_scenario': kw['test_scenario'],
            'test_regex': kw['test_regex'],
            'test_added': 1,
            'test_verified': '',
            "test_create_time": datetime.datetime.now(),
            "test_uuid": '',
            "results":''
        }
        #Inserting the data
        ins = self.tests_list.insert().values(arg)
        result = self.conn.execute(ins)
        LOG.info("Event created with id " + str(unique_id))
        return unique_id

    def list_events(self, args={}):
        """
        # | Method to list the events
        # |
        # | Arguments: Distionary containg the flter values
        # |
        # | Returns Distionary
        """
        get_event_list = select([self.tests_list])
        try:
            result = self.conn.execute(get_event_list)
        except Exception as e:
            LOG.error(str(e))
            return []
        event_list = []
        for row in result:
            event_data = {}
            event_data['name'] = row['name']
            event_data['id'] = row['id']
            event_list.append(event_data)
        return event_list
