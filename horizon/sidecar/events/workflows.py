# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import memoized
from horizon import workflows
from openstack_dashboard import api
from openstack_dashboard.api import base
from openstack_dashboard.dashboards.sidecar.events import setting
from sidecarclient import client

sidecar = client.Client(
        username = getattr(settings, "SC_USERNAME"),
        password = getattr(settings, "SC_PASSWORD"),
        auth_url = getattr(settings, "SC_AUTH_URL"),
        region_name = getattr(settings, "SC_REGION_NAME"),
        tenant_name = getattr(settings, "SC_TENANT_NAME"),
        timeout = getattr(settings, "SC_TIMEOUT"),
        insecure = getattr(settings, "SC_INSECURE")
    )

default_setting = setting.ConfigSetter()
INSTANCE_SEC_GROUP_SLUG = "update_security_groups"

class UpdateTestListAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(UpdateTestListAction, self).__init__(request, *args, **kwargs)
        err_msg = _('Unable to retrieve security group list. Please try again later.')
        context = args[0]
        test_id = context.get('test_id', '')

        default_role_name = self.get_default_role_field_name()
        self.fields[default_role_name] = forms.CharField(required=False)
        self.fields[default_role_name].initial = 'member'

        # Get list of available security groups
        all_groups = []
	try:
	    print("+++++++++++++++++++++++++++++++++++++++++")
	    print(args)
	    print(kwargs)
	    print(args[0]['test_id'])
	    print("+++++++++++++++++++++++++++++++++++++++++")

            test_list = sidecar.events.tests_list(project_id=args[0]['test_id'])
        except Exception:
            exceptions.handle(request, err_msg)
        tests_list = [(tests['id'], tests['test_scenario']) for tests in test_list._logs]

        field_name = self.get_member_field_name('member')
        self.fields[field_name] = forms.MultipleChoiceField(required=False)
        self.fields[field_name].choices = tests_list #groups_list
	self.fields[field_name].initial = []
	for tests in test_list._logs:
	    if tests['test_added'] == 1:
      	        self.fields[field_name].initial.append(tests['id']) 

    def handle(self, request, data):
        test_id = data['test_id']
        return True

    class Meta(object):
        name = _("Assign tests *")
        slug = INSTANCE_SEC_GROUP_SLUG

class UpdateTestList(workflows.UpdateMembersStep):
    action_class = UpdateTestListAction
    help_text = _("Add/remove test to this list.")
    available_list_title = _("All Tests")
    members_list_title = _("Added tests")
    no_available_text = _("No tests found.")
    no_members_text = _("No tests enabled.")
    show_roles = False
    depends_on = ("test_id",)
    contributes = ("wanted_tests",)

    def contribute(self, data, context):
        request = self.workflow.request
        if data:
            field_name = self.get_member_field_name('member')
            context["wanted_tests"] = request.POST.getlist(field_name)
        return context


class UpdateConfigAction(workflows.Action):
    image_ref = forms.CharField(label=_("Image Ref"), max_length=255)
    flavor_ref = forms.CharField(label=_("Flavor Ref"), max_length=255)    

    def handle(self, request, data):
        try:
	    default_setting.update_setting('compute', 'image_ref', data['image_ref'])
            default_setting.update_setting('compute', 'flavor_ref', data['flavor_ref'])
	    sidecar.events.update_test(id=data['test_id'], update_null='1')
	    for tests_id in data['wanted_tests']:
                try:
                    sidecar.events.update_test(id=tests_id, test_added='1')
                except exceptions.Conflict:
                    msg = _('Test with id "%s" is already used.') % tests_id
                    self.failure_message = msg
                    return False
        except Exception:
            exceptions.handle(request, ignore=True)
            return False
        return True

    class Meta(object):
        name = _("Configuration Information")
        slug = 'instance_info'
        help_text = _("Edit the test conf details.")

class UpdateConfig(workflows.Step):
    action_class = UpdateConfigAction
    depends_on = ("test_id",)
    contributes = ("image_ref", "flavor_ref",)

class UpdateTest(workflows.Workflow):
    slug = "update_instance"
    name = _("Edit Test list")
    finalize_button_name = _("Save")
    success_message = _('Modified Test list "%s".')
    failure_message = _('Unable to modify test list "%s".')
    success_url = "horizon:rally_dashboard:events:index"
    default_steps = (UpdateConfig,
                     UpdateTestList)

    def format_status_message(self, message):
        return message % self.context.get('image_ref', 'unknown test')

class AdminUpdateInstance(UpdateTest):
    success_url = "horizon:rally_dashboard:events:index"
    default_steps = (UpdateConfig,)
