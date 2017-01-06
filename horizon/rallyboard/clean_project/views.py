# _______________________________________________________________________
# | File Name: views.py                                                 |
# |                                                                     |
# | This file is for handling the views of support ticket display       |
# |_____________________________________________________________________|
# | Start Date: Aug 31th, 2016                                          |
# |                                                                     |
# | Package: Openstack Horizon Dashboard [liberity]                     |
# |                                                                     |
# | Copy Right: 2016@nephoscale                                         |
# |_____________________________________________________________________|

#Importing the required packages
from django.utils.translation import ugettext_lazy as _
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from horizon import exceptions
from horizon.utils import memoized
import subprocess
import shlex
import os
from django.conf import settings
from django.contrib import messages

#Making the credential for the command
username = getattr(settings, "SC_USERNAME")
password = getattr(settings, "SC_PASSWORD")
auth_url = getattr(settings, "SC_AUTH_URL")
tenant_name = getattr(settings, "SC_TENANT_NAME")
cmd = '--username '+username + ' --password '+ password +' --auth-url '+ auth_url +' --admin-project '+ tenant_name

def IndexView(request):
    """
    # | Method to show the resources
    # |
    # | Arguments: 
    # |   <request>: request
    # |
    # | Returns: NA
    """

    #Making the command
    global cmd
    command = 'ospurge --dry-run --cleanup-project rallyTestProject ' + cmd
    res = subprocess.Popen(command, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
    resources, err = res.communicate()
    resources = " <br>".join(resources.split("\n"))
    
    #Displaying the report
    context = {
        "page_title": _("Clean Following Resources"),
        "resources": resources
    }
    return render(request, 'rally_dashboard/clean_project/list_resource.html', context)

def clean_project(request, **kwargs):
    """
    # | Method to run the os purge 
    # |
    # | Arguments: 
    # |   <kwargs>: Dictionary
    # |
    # | Returns: NA
    """

    #Making the command for the test execution
    global cmd
    command = 'ospurge --verbose --dont-delete-project --cleanup-project rallyTestProject '+ cmd
    res = subprocess.Popen(command, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
    output, err = res.communicate()
    
    #If there is no error then showing the success message	
    if err == None:
        messages.add_message(request, messages.SUCCESS, 'Project cleaning is successfully completed.')
    else:
	messages.add_message(request, messages.ERROR, 'Project cleaning is failed.')

    #Showing the cleaned resources 
    command = 'ospurge --dry-run --cleanup-project rallyTestProject ' + cmd
    res = subprocess.Popen(command, stderr=subprocess.STDOUT, shell = True, stdout=subprocess.PIPE)
    output, err = res.communicate()
    cleaned_output = " <br>".join(output.split("\n"))
    print('cleaned_output')
    print(cleaned_output)
    print('cleaned_outputnnn')

    #Displaying the report
    context = {
        "page_title": _("Cleaned Resources"),
        "resource_list": cleaned_output
    }
    return render(request, 'rally_dashboard/clean_project/purged_resource.html', context)
