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
                        'test_service':'glance',
                        'test_scenario':'glance',
                        'test_regex': row
                     }   
            tt = Testcases()
            tt.createEvent(create_data)
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')
qaTestList = ['tempest.api.image.v1.test_images.ListImagesTest.test_index_disk_format[id-f1755589-63d6-4468-b098-589820eb4031]','tempest.api.image.v1.test_images.ListImagesTest.test_index_max_size[id-feb32ac6-22bb-4a16-afd8-9454bb714b14]','tempest.api.image.v1.test_images.ListImagesTest.test_index_min_size[id-6ffc16d0-4cbf-4401-95c8-4ac63eac3]']
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


