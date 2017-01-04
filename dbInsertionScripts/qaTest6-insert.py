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
                        'test_service':'cinder',
                        'test_scenario':'cinder',
                        'test_regex': row
                     }   
            tt = Testcases()
            tt.createEvent(create_data)
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')
qaTestList = ['tempest.api.volume.admin.test_qos.QosSpecsV1TestJSON.test_create_delete_qos_with_both_consumer[id-f88d65eb-ea0d-487d-af8d-71f4011575a4]','tempest.api.volume.admin.test_qos.QosSpecsV1TestJSON.test_create_delete_qos_with_front_end_consumer[id-7e15f883-4bef-49a9-95eb-f94209a1ced1]','tempest.api.volume.admin.test_qos.QosSpecsV1TestJSON.test_get_qos[id-7aa214cc-ac1a-4397-931f-3bb2e83bb0fd]','tempest.api.volume.v2.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_details_with_multiple_params[id-2a7064eb-b9c3-429b-b888-33928fc5edd3]','tempest.api.volume.v2.test_volumes_list.VolumesV2ListTestJSON.test_volume_list_pagination[id-af55e775-8e4b-4feb-8719-215c43b0238c]']
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


