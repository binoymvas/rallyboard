import subprocess
from prettytable import PrettyTable
from  model import * 

x = PrettyTable(["File"])
x.align = 'l'
#chk = Testcases()

def executeCommands(qaTestList):
    for row in qaTestList:
            create_data = {
                        'name' : row, 
                        'project_id': 3,
                        'test_service':'swift',
                        'test_scenario':'swift',
                        'test_regex': row
                     }   
            tt = Testcases()
            tt.createEvent(create_data)
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')
qaTestList = ['tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_create_agent[id-1fc6bdc8-0b6d-4cc7-9f30-9b04fabe5b90]', 'tempest.api.compute.admin.test_agents.AgentsAdminTestJSON.test_delete_agent[id-470e0b89-386f-407b-91fd-819737d0b335]']
executeCommands(qaTestList)
#test_lists = chk.list_events()

"""
for test in test_lists:
    names = test['name']   
    if 'tempest_sidecar_plugin.tests.api.test_sidecar.TestTempestSidecar.test_pecan_is_running' in names:
        print names
        test_command = 'rally verify start --system-wide --regex ' + names
        p = subprocess.Popen(test_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            x.add_row([line])
        print x
"""    


