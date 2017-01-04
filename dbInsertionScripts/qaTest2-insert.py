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
                        'test_service':'heat',
                        'test_scenario':'heat',
                        'test_regex': row
                     }   
            tt = Testcases()
            tt.createEvent(create_data)
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')
qaTestList = ['tempest.api.orchestration.stacks.test_non_empty_stack.StacksTestJSON.test_resource_metadata[id-898070a9-eba5-4fae-b7d6-cf3ffa03090f]','tempest.api.orchestration.stacks.test_non_empty_stack.StacksTestJSON.test_show_event[id-92465723-1673-400a-909d-4773757a3f21]','tempest.api.orchestration.stacks.test_non_empty_stack.StacksTestJSON.test_show_resource[id-2aba03b3-392f-4237-900b-1f5a5e9bd962]', 'tempest.api.orchestration.stacks.test_non_empty_stack.StacksTestJSON.test_stack_list[id-065c652a-720d-4760-9132-06aedeb8e3ab]']
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


