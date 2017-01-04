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
qaTestList = ['tempest.api.object_storage.test_account_services.AccountTest.test_list_containers_with_prefix[id-365e6fc7-1cfe-463b-a37c-8bd08d47b6aa]','tempest.api.object_storage.test_account_services.AccountTest.test_list_extensions[id-6eb04a6a-4860-4e31-ba91-ea3347d76b58]']
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


