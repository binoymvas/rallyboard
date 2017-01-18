## Table of content

- [Description](#description)
    - [Rally-Horizon Integration Plugin](#rally-horizon-integration-plugin)
    - [Tasks Panel](#tasks-panel)
    - [Tests History Panel](#test-history-panel)
    - [Clean Project Panel](#clean-project-panel)
- [Pre-Requisites](#pre-requisites)
- [Installation and Configuration Steps:](#install-configure-steps)
- [Important Notes](#important-notes)

## Description

### Rally-Horizon Integration Plugin

This repository contains the files related to the integration of Rally test suite with Horizon Dashboard.
On successful installation, a "Rally Dashboard" plugin will be displayed in the left side of the Horizon dashboard.

http://i.imgur.com/4p8fcy2.png

Rally Dashboard will have the following 3 Panels:

* Tasks - Listing of all Testing options - All Tests, Benchmark Tests and QA Tests
* Test History - Contains a history of all tests that have been executed till now. Test Reports have been categorized and will be available under their respective tabs itself (All Test Reports, Benchmark Test Reports and QA Test Reports).
* Clean Project - This corresponds to the Ospurge test suite integration. On opening this panel, a dry run will be executed to list all the resources that are present under the project. On user confirmation, these resources will be deleted.

http://i.imgur.com/oVuAdoL.png

### Tasks Panel

2 tabs are present inside this panel. They are - Rally Tests and Test Configuration.

1) Rally Tests
All the available Testing options will be listed in this panel. Following actions are also available:

a) Run Tests - Clicking this button, will display all the active tests that would be executed. Tests can be executed from that page.
b) Edit Test Details - Opens up the form to edit the test config details and add/remove tests

(Screenshot)

The form will have 2 sections:

i) Configuration Information
- Config details like image name and flavor name can be set from this section.

(Screenshot)
ii) Assign Tests
- Users can select the tests which they want to execute from this section.
(Screenshot)

c) View Report - Displays the latest test report

(Screenshot)

2) Test Configuration

This is just a listing of config values from all the available projects.
(Screenshot)

### Tests History

All available Test Reports from the past will be displayed in this panel. Test Reports will be displayed under their corresponding tabs.
a) All Test Reports
b) Benchmark Test Reports
c) QA Test Reports

(Screenshot)

Following actions are available here:

a) View Report
- To view the test report via frontend
b) Delete Report
- To delete any report

### Clean Project:

This panel links ospurge to our project.
OSpurge is used for cleaning up all the resources left over after testing.
On opening the panel, it will display the results of a 'dry-run'. .ie- a plain listing of all resources that would get deleted on executing the cleanup. These resources will get cleaned up only if user clicks on the 'Confirm' button available in the page.

(Screenshot)

## Pre-Requisites

1) Sidecar client module must be already installed.
Ref: https://github.com/nephoscale/python-sidecarclient.git

2) Sidecar api must be already installed.
Ref: https://github.com/nephoscale/sidecar.git

3) Sidecar service and it's endpoints must be created and configured correctly.

4) The environment variables must be correctly setup.

_Example_
############
export OS_USERNAME="admin"
export OS_PASSWORD="openstack"
export OS_TENANT_NAME="admin"
export OS_ENDPOINT="http://198.100.181.74:9090/v2"
export OS_ENDPOINT_TYPE='publicURL'
export OS_REGION_NAME='RegionOne'
export OS_AUTH_URL="http://198.100.181.74:35357/v2.0"
############



