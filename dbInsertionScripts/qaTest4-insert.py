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
                        'test_service':'neutron',
                        'test_scenario':'neutron',
                        'test_regex': row
                     }   
            tt = Testcases()
            tt.createEvent(create_data)
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')
qaTestList = ['tempest.api.network.test_routers.RoutersTest.test_update_router_admin_state[id-a8902683-c788-4246-95c7-ad9c6d63a4d9]','tempest.api.network.test_routers.RoutersTest.test_update_router_reset_gateway_without_snat[id-f2faf994-97f4-410b-a831-9bc977b64374]','tempest.api.network.test_routers.RoutersTest.test_update_router_set_gateway[id-6cc285d8-46bf-4f36-9b1a-783e3008ba79]']
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


