## Table of content

- [Description](#description)
    - [Rally-Horizon Integration Plugin](#rally-horizon-integration-plugin)
    - [Tasks Panel](#tasks-panel)
    - [Tests History Panel](#test-history-panel)
    - [Clean Project Panel](#clean-project-panel)
- [Pre-Requisites](#pre-requisites)
- [Installation and Configuration Steps:](#install-configure-steps)
    - [Sidecar Related Steps](#sidecar-related-steps)
    - [Tenant and User Creation](#tenant-user-creation)
    - [Rally Installation](#rally-installation)
    - [Rally Deployment Creation](#rally-deployment-creation)
    - [Add Tempest as a verifier to Rally](#add-tempest-verifier-rally)
    - [Deployment Verification](#deployment-verification)
    - [Create new tables](#create-tables)
    - [Insert data into these tables](#insert-data-tables)
    - [Script execution to add tests to the DB](#script-insert-test-to-DB)
    - [Configuring the Benchmark Test Files](#configure-benchmark-test-files)
    - [Configuring the Rally Dashboard](#configure-rally-dashboard)
    - [Ospurge installation](#ospurge-installtion)
- [Important Notes](#important-notes)

## Description

### Rally-Horizon Integration Plugin

This repository contains the files related to the integration of Rally test suite with Horizon Dashboard.
On successful installation, a "Rally Dashboard" plugin will be displayed in the left side of the Horizon dashboard.


![Rally Dashboard listing](http://i.imgur.com/4p8fcy2.png "Rally Dashboard listing")


**Rally Dashboard will have the following 3 Panels:**

* Tasks - Listing of all Testing options - All Tests, Benchmark Tests and QA Tests
* Test History - Contains a history of all tests that have been executed till now. Test Reports have been categorized and will be available under their respective tabs itself (All Test Reports, Benchmark Test Reports and QA Test Reports).
* Clean Project - This corresponds to the Ospurge test suite integration. On opening this panel, a dry run will be executed to list all the resources that are present under the project. On user confirmation, these resources will be deleted.

![Panel listing](http://i.imgur.com/oVuAdoL.png "Panel listing")

### Tasks Panel

2 tabs are present inside this panel. They are - Rally Tests and Test Configuration.

**1) Rally Tests**
All the available Testing options will be listed in this panel. Following actions are also available:

  - **Run Tests:-**
       - Clicking this button, will display all the active tests that would be executed. Tests can be executed from that page.
  - **Edit Test Details:**
       - Opens up the form to edit the test config details and add/remove tests

         (Screenshot)

         The form will have 2 sections:

            i) Configuration Information*
                - Config details like image name and flavor name can be set from this section.

                http://i.imgur.com/MGF6VsW.png
                
            ii) Assign Tests
                - Users can select the tests which they want to execute from this section.
                 http://i.imgur.com/CO9wG6A.png

  - **View Report - Displays the latest test report**]
  
    ![Actions](http://i.imgur.com/zQ3UtZx.png "Actions")
        

**2) Test Configuration**

This is just a listing of config values from all the available projects.


### Tests History

All available Test Reports from the past will be displayed in this panel. Test Reports will be displayed under their corresponding tabs.
 - All Test Reports
 - Benchmark Test Reports
 - QA Test Reports

![Test History](http://i.imgur.com/YdGPSfV.png "Test History")

Following actions are available here:

 - View Report
    - To view the test report via frontend
 - Delete Report
    - To delete any report

### Clean Project:

This panel links ospurge to our project.
OSpurge is used for cleaning up all the resources left over after testing.
On opening the panel, it will display the results of a 'dry-run'. .ie- a plain listing of all resources that would get deleted on executing the cleanup. These resources will get cleaned up only if user clicks on the 'Confirm' button available in the page.

![Resource Cleanup](http://i.imgur.com/EHHuuni.png "Resource Cleanup")

## Pre-Requisites

1) Sidecar client module must be already installed.
Ref: https://github.com/nephoscale/python-sidecarclient.git

2) Sidecar api must be already installed.
Ref: https://github.com/nephoscale/sidecar.git

3) Sidecar service and it's endpoints must be created and configured correctly.

4) The environment variables must be correctly setup.

_Example_

<pre>
export OS_USERNAME="admin"
export OS_PASSWORD="openstack"
export OS_TENANT_NAME="admin"
export OS_ENDPOINT="http://198.100.181.74:9090/v2"
export OS_ENDPOINT_TYPE='publicURL'
export OS_REGION_NAME='RegionOne'
export OS_AUTH_URL="http://198.100.181.74:35357/v2.0"
</pre>

## Installation and Configuration Steps

### Sidecar Related Steps

1) Install the latest version of Sidecar client and sidecar api.
2) Ensure that the sidecar.conf file (/etc/sidecar/sidecar.conf) is updated correctly.

### Tenant and User Creation

1) Need to create a project/tenant. All the tests wil be done inside this project.

<pre>
openstack project create --description 'Rally Test Project' rallyTestProject
</pre>

_(If environment variables are not set, then there will be errors related to 'authurl'.)_

2) Need to create test users inside this project.

<pre>
openstack user create --project rallyTestProject --password rallyTest rallyUser
openstack user create --project rallyTestProject --password rallyTest rallyUser1
</pre>

### Rally Installation

1) Clone the Rally Project
<pre>
git clone https://github.com/openstack/rally.git
</pre>

2) Execute Rally Installation script by passing the correct db access details
(We use the sidecar database itself)
<pre>
cd rally/
./install_rally.sh --system --dbtype mysql --db-user db-username --db-password db-password --db-host db-host> --db-name db-name
</pre>

**Ex - ./install_rally.sh --system --dbtype mysql --db-user root --db-password openstack --db-host 198.100.181.74 --db-name sidecar**

### Rally Deployment Creation

1) Create a file 'existing_users.json'. Through this file, we are registering the details of newly created users in rally
Ref: http://rally.readthedocs.io/en/latest/quick_start/tutorial/step_3_benchmarking_with_existing_users.html

2) Add the following details into the above json file and change the config values based on each installation.
<pre>
{
    "type": "ExistingCloud",
    "auth_url": "http://198.100.181.74:35357/v2.0",
    "region_name": "RegionOne",
    "endpoint_type": "public",
    "admin": {
        "username": "admin",
        "password": "openstack",
        "tenant_name": "demo"
    },
    "users": [
        {
            "username": "rallyUser",
            "password": "rallyTest",
            "tenant_name": "rallyTestProject"
        },
        {
            "username": "rallyUser1",
            "password": "rallyTest",
            "tenant_name": "rallyTestProject"
        }
    ]
}
</pre>

3) Create a new Rally Deployment by passing the above file.
<pre>
rally deployment create --filename existing_users.json  --name name of the deployment
</pre>

**Ex- rally deployment create --filename existing_users.json  --name sampleDeployment***

### Add Tempest as a verifier to Rally

1) Add tempest as a Rally verifier via the following command:

<pre>
rally verify create-verifier --source https://github.com/openstack/tempest.git --system-wide --name Tempest --type tempest
</pre>

### Deployment Verification

1) Verify the newly created deployment via the following command:
<pre>
rally deployment list
</pre>

2) Verify the newly added tempest verifier via the following command:
<pre>
rally verify list-verifiers
</pre>

### Create new tables

1) Create new tables into the sidecar database. These are our custom tables used for storing rally task history, reports, log, config data, etc.

**Table Name - project_tests_list**

<pre>
CREATE TABLE `project_tests_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  `test_create_time` datetime NOT NULL,
  `extra` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
</pre>

**Table Name - test_config**

<pre>

CREATE TABLE `test_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option_name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `project_id` int(11) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
</pre>

**Table Name - tests_list**

<pre>
CREATE TABLE `tests_list` (
  `id` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `test_service` varchar(200) NOT NULL,
  `test_scenario` varchar(100) NOT NULL,
  `test_regex` varchar(300) NOT NULL,
  `test_added` int(11) DEFAULT NULL,
  `test_verified` varchar(100) DEFAULT NULL,
  `test_create_time` datetime NOT NULL,
  `test_uuid` varchar(200) DEFAULT NULL,
  `results` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1
</pre>

**Table Name - tests_log**
<pre>
CREATE TABLE `tests_log` (
  `id` varchar(100) NOT NULL,
  `log_data` longtext NOT NULL,
  `results` longtext NOT NULL,
  `project_id` varchar(100) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
</pre>

### Insert data into these tables

1)  Execute the following queries to store data in these tables.

<pre>
INSERT into project_tests_list VALUES(1, 'All Tests', 1, '2016-12-05 20:47:47', 'NULL');
INSERT into project_tests_list VALUES(2, 'Benchmark Tests', 1, '2016-12-05 20:47:47', 'NULL');
INSERT into project_tests_list VALUES(3, 'Quick QA', 1, '2016-12-05 20:47:47', 'NULL');
INSERT INTO `test_config` VALUES (1,'image_name','cirros',1,1),(2,'flavor_name','m1.tiny',1,1);
INSERT INTO `test_config` VALUES (3,'image_name','cirros',2,1),(4,'flavor_name','m1.tiny',2,1);
INSERT INTO `test_config` VALUES (5,'image_name','cirros',3,1),(6,'flavor_name','m1.tiny',3,1);
INSERT INTO `tests_log` VALUES (1,'test-log','test-result',1,1),(2,'test-log','test-result',2,1), (3,'test-log','test-result',3,1);
</pre>

### Script execution to add tests to the DB

Next, we execute the queries to add tests into the tests_list table.
<pre>

a) cd dbInsertionScripts/
b) Open model.py file and modify the db access config details in that file.
c) Execute the following scripts

python allTests-insert.py
python benchmarktests-insert.py  
python qaTest1-insert.py
python qaTest3-insert.py
python qaTest5-insert.py
python qaTest2-insert.py
python qaTest4-insert.py
python qaTest6-insert.py
</pre>

### Configuring the Benchmark Test Files

1) All the benchmarking test files are stored in 'benchmarkTests' folder.

2) Copy this folder to '/home/' or '/etc/' and update the corresponding location in 'sidecar.conf' file ( /etc/sidecar/sidecar.conf)

### Configuring the Rally Dashboard

1) Copy the rally dashboard folder - "rallyboard" into it's corresponding folder (/openstack_dashboard/dashboard/)

2) Check the dashboard settings file and ensure that a section similar to the following is present there:

<pre>
#####Settings Corresponding to Sidecar#####
SC_AUTH_VERSION  = 2
SC_USERNAME      = 'admin'
SC_PASSWORD      = 'openstack'
SC_ENDPOINT      = 'http://198.100.181.74:9090/v2'
SC_AUTH_URL      = 'http://198.100.181.74:35357/v2.0'
SC_ENDPOINT_TYPE = 'publicURL'
SC_REGION_NAME   = 'RegionOne'
SC_TENANT_NAME   = 'admin'
SC_TIMEOUT       = 10
SC_INSECURE      = True

SIDECAR_ENABLED  = True
</pre>

### Ospurge installation

1) Final step is related to the Ospurge installation. Execute the following command to install OSpurge.

<pre>
pip install git+https://git.openstack.org/openstack/ospurge@328f6
</pre>

## Important Notes

1) One thing which we have noted is that the Rally commands have changes multiple times in their recent versions. We had made the required modifications and had tested till Rally version '0.7.1~dev269'.
 ( the version available as on Jan 18, 2017).
_Please cross check the version. Sometimes commands might again change in the latest version. If so, the corresponding changes need to be made in the 'controller(rally_tests.py)' file._

2) Second one is related to OSpurge. Current version of ospurge (available as on Jan 18, 2017) works only with a limited number of openstack installations. It's not working in latest Openstack version as it's pointing to incorrect/deprecated module paths. Need to cross check this.



