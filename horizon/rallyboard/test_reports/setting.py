# _______________________________________________________________________
# | File Name: setting.py                                               |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Nov 16th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
import ConfigParser
import os
import subprocess

class ConfigSetter():

    def __init__(self):
        self.path = '/etc/tempest/tempest.conf'

    def create_config(self):
        """
        Name: create_config
        Desc: Create a config file
        Params: NA
        retrun: NA
        """

        #Setting the configuration values
        config = ConfigParser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "font", "Courier")
        
        #Writing into the configuration file
        with open(self.ath, "wb") as config_file:
            config.write(config_file)

    def get_config(self):
        """
        Name: get_config
        Desc: Returns the config object
        Params: NA
        retrun: configuration values
        """

        #Creating it if not exists
        if not os.path.exists(self.path):
            self.create_config(self.path)

        #Getting the details
        config = ConfigParser.ConfigParser()
        config.read(self.path)
        return config

    def get_setting(self, section, setting):
        """
        Name: get_setting
        Desc: Print out a setting
        Params: NA
        retrun: Getting the details
        """

        #Getting the confguration details
        config = self.get_config()
        value = config.get(section, setting)
        print "{section} {setting} is {value}".format(section=section, setting=setting, value=value)
        return value

    def update_setting(self, section, setting, value):
        """
        Name: update_setting
        Desc: Writing setting into the file
        Params: NA
        retrun: NA
        """

        #Getting the confguration details
        config = self.get_config()
        config.set(section, setting, value)

        #Updating the details
        with open(self.path, "wb") as config_file:
            config.write(config_file)

    def delete_setting(self, section, setting):
        """
        Name: update_setting
        Desc: Delete setting from the file
        Params: NA
        retrun: NA
        """
        
        #Deleting the configuration values
        config = self.get_config()
        config.remove_option(section, setting)

        #Deleting the details
        with open(self.path, "wb") as config_file:
            config.write(config_file)

def executeCommands(command, shellFlag = True, debug = False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print ('line', line)
