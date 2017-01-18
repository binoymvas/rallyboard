import subprocess
from prettytable import PrettyTable
from  model import * 

x = PrettyTable(["File"])
x.align = 'l'
#chk = Testcases()
def executeCommand(command, shellFlag = True, debug = False):
    '''
    function to execute chef command
    command - Command to execute
    shellFlag - execute in shell or not[default - True]
    debug -The debug option
    Return - outputStr output of the command
    '''
            
    # execute command
    try:
        outputStr = subprocess.check_output(command, shell = shellFlag)
    except Exception, e:
        print("Error in the command ===================================", e)
        print("command is " + command)
        outputStr = ""
        
        # if debug print commands
        if debug:
            print "\n=++++++++++++++++++++++++++++++++++++++++++++++Command: " + command + "\n"
            print "\nException: "
            print e
            print "\n"
   
    print('outputStr', outputStr) 
    return outputStr

def executeCommands(command, shellFlag = True, debug = False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        #x.add_row([line])
        #test_case = line.split("[") 
	test_case = line 
	print(test_case)
        create_data = {'name' : test_case}        
        chk = test_case.split(".")

        if len(chk) > 2:
            #x.add_row('test_case') 
            create_data = {
                        'name' : chk[-2], 
                        'project_id': 1,
                        'test_service':chk[0],
                        'test_scenario':chk[-2],
                        'test_regex':  test_case
                     }  
           
	    #print(test_case[0])
	    #print(create_data) 
            tt = Testcases()
            tt.createEvent(create_data)
	    
    #print x

#executeCommand('rally verify start --system-wide --regex tempest.api.baremetal.admin.test_api_discovery.TestApiDiscovery.test_api_versions')

#executeCommands('rally verify discover  --system-wide')
executeCommands('rally verify list-verifier-tests')
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


