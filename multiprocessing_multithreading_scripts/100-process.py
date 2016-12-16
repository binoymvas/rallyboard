from Queue import Empty
import time
from multiprocessing import Process, Queue
import subprocess

def executeTest(item):
    try:
        print('+++++++++++++++++++++')
	print item
        print('+++++++++++++++++++++')
        p = subprocess.Popen('rally verify start --system-wide --regex '+item, stderr=subprocess.STDOUT, shell=True, stdout=subprocess.PIPE)
        output, err = p.communicate()
	return output
    except Exception as details:
        print('Error')
        print details

def do_work(q):
    while not q.empty():
    #while True:
        try:
            x = q.get(block=False)
            print executeTest(x)
        except Empty:
            break

if __name__ == '__main__':
    start_time = time.time()
    work_queue = Queue()
    
    tests_list = ['tempest.api.image.v2.test_images_member.ImagesMemberTest.test_get_image_members_schema', 'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_name', 'tempest.api.identity.admin.v2.test_roles_negative.RolesNegativeTestJSON.test_remove_user_role_non_existent_role', 'tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_trust_impersonate', 'tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_list_roles','tempest.api.compute.admin.test_services_negative.ServicesAdminNegativeTestJSON.test_get_service_by_invalid_params','neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_trunk_empty_subports_list','tempest.api.compute.floating_ips.test_floating_ips_actions_negative.FloatingIPsNegativeTestJSON.test_associate_ip_to_server_without_passing_floating_ip', 'tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_create_list_show_delete_interfaces','tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_nonexistent_server','tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_update_non_existent_tenant','tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_trust_expire_invalid','tempest.api.identity.admin.v2.test_users_negative.UsersNegativeTestJSON.test_update_user_for_non_existent_user','tempest.api.volume.test_volumes_snapshots.VolumesV1SnapshotTestJSON.test_snapshot_create_offline_delete_online','tempest.api.volume.admin.test_volume_types_negative.VolumeTypesNegativeV2Test.test_delete_nonexistent_type_id','tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list_with_detail_param_metadata','tempest.api.volume.test_volumes_snapshots.VolumesV1SnapshotTestJSON.test_snapshot_create_offline_delete_online','tempest.api.network.test_routers.RoutersIpV6Test.test_router_interface_port_update_with_fixed_ip','tempest.api.network.test_routers.RoutersIpV6Test.test_update_delete_extra_route','tempest.api.image.v1.test_images.ListImagesTest.test_index_status_active_detail','tempest.api.image.v2.test_images_member.ImagesMemberTest.test_get_image_members_schema',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_add_host_create_server_with_az',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_add_host_get_details',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_add_host_list',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_add_remove_host',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_create_delete',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_create_delete_with_az',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_create_update_metadata_get_details',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_create_update_with_az',
'tempest.api.compute.admin.test_aggregates.AggregatesAdminTestJSON.test_aggregate_create_verify_entry_in_list',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_add_existent_host',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_add_host_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_add_non_exist_host',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_create_aggregate_name_length_exceeds_255',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_create_aggregate_name_length_less_than_1',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_create_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_create_with_existent_aggregate_name',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_delete_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_delete_with_invalid_id',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_get_details_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_get_details_with_invalid_id',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_list_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_remove_host_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_list_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_remove_host_as_user',
'tempest.api.compute.admin.test_aggregates_negative.AggregatesAdminNegativeTestJSON.test_aggregate_remove_nonexistent_host',
'tempest.api.compute.admin.test_auto_allocate_network.AutoAllocateNetworkTest.test_server_create_no_allocate',
'tempest.api.compute.admin.test_auto_allocate_network.AutoAllocateNetworkTest.test_server_multi_create_auto_allocate',
'tempest.api.compute.admin.test_availability_zone.AZAdminV2TestJSON.test_get_availability_zone_list',
'tempest.api.compute.admin.test_availability_zone.AZAdminV2TestJSON.test_get_availability_zone_list_detail',
'tempest.api.compute.admin.test_fixed_ips_negative.FixedIPsNegativeTestJson.test_set_unreserve_with_non_admin_user',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_flavor_using_string_ram',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_flavor_verify_entry_in_list_details',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_flavor_with_int_id',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_flavor_with_none_id',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_flavor_with_uuid_id',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_list_flavor_without_extra_data',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_create_server_with_non_public_flavor',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_is_public_string_variations',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_list_non_public_flavor',
'tempest.api.compute.admin.test_flavors.FlavorsAdminTestJSON.test_list_public_flavor_with_other_user',
'tempest.api.compute.admin.test_flavors_access.FlavorsAccessTestJSON.test_flavor_access_add_remove',
'tempest.api.compute.admin.test_flavors_access.FlavorsAccessTestJSON.test_flavor_access_list_with_private_flavor',
'tempest.api.compute.admin.test_flavors_access_negative.FlavorsAccessNegativeTestJSON.test_add_flavor_access_duplicate',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_non_admin_set_keys',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_non_admin_unset_keys',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_non_admin_update_specific_key',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_unset_nonexistent_key',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_update_mismatch_key',
'tempest.api.compute.admin.test_flavors_extra_specs_negative.FlavorsExtraSpecsNegativeTestJSON.test_flavor_update_more_key',
'tempest.api.compute.floating_ips.test_floating_ips_actions.FloatingIPsTestJSON.test_associate_disassociate_floating_ip',
'tempest.api.compute.floating_ips.test_floating_ips_actions.FloatingIPsTestJSON.test_delete_floating_ip',
'tempest.api.compute.floating_ips.test_floating_ips_actions_negative.FloatingIPsNegativeTestJSON.test_allocate_floating_ip_from_nonexistent_pool',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_create_tenant_with_empty_name',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_create_tenants_name_length_over_64',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_delete_non_existent_tenant',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_list_tenant_request_without_token',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_list_tenants_by_unauthorized_user',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_tenant_create_duplicate',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_tenant_delete_by_unauthorized_user',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_tenant_delete_request_without_token',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_tenant_update_by_unauthorized_user',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_tenant_update_request_without_token',
'tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_update_non_existent_tenant',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_create_enabled',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_create_not_enabled',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_create_with_description',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_list_delete',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_desc',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_enable',
'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_name',
'tempest.api.identity.admin.v2.test_tokens.TokensTestJSON.test_create_get_delete_token',
'tempest.api.identity.admin.v2.test_tokens.TokensTestJSON.test_rescope_token',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_authentication_request_without_token',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_create_user_with_enabled',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_delete_user',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_get_users',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_list_users_for_tenant',
'tempest.api.identity.admin.v2.test_users.UsersTestJSON.test_list_users_with_roles_for_tenant',
'tempest.api.identity.admin.v3.test_list_projects.ListProjectsTestJSON.test_list_projects',
'tempest.api.identity.admin.v3.test_list_projects.ListProjectsTestJSON.test_list_projects_with_domains',
'tempest.api.identity.admin.v3.test_list_projects.ListProjectsTestJSON.test_list_projects_with_enabled',
'tempest.api.identity.admin.v3.test_list_projects.ListProjectsTestJSON.test_list_projects_with_name',
'tempest.api.identity.admin.v3.test_list_projects.ListProjectsTestJSON.test_list_projects_with_parent',
'tempest.api.identity.admin.v3.test_list_users.UsersV3TestJSON.test_get_user',
'tempest.api.identity.admin.v3.test_list_users.UsersV3TestJSON.test_list_user_domains',
'tempest.api.identity.admin.v3.test_list_users.UsersV3TestJSON.test_list_users',
'tempest.api.identity.admin.v3.test_list_users.UsersV3TestJSON.test_list_users_with_name',
'tempest.api.identity.admin.v3.test_list_users.UsersV3TestJSON.test_list_users_with_not_enabled',
'tempest.api.identity.admin.v3.test_policies.PoliciesTestJSON.test_create_update_delete_policy',
'tempest.api.volume.admin.test_volume_hosts.VolumeHostsAdminV1TestsJSON.test_list_hosts',
'tempest.api.volume.admin.test_volume_hosts.VolumeHostsAdminV2TestsJSON.test_list_hosts',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_delete_quota',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_list_default_quotas',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_list_quotas',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_quota_usage',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_quota_usage_after_volume_transfer',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_show_quota_usage',
'tempest.api.volume.admin.test_volume_quotas.BaseVolumeQuotasAdminV2TestJSON.test_update_all_quota_resources_for_tenant',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_delete_quota',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_list_default_quotas',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_list_quotas',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_quota_usage',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_quota_usage_after_volume_transfer',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_show_quota_usage',
'tempest.api.volume.admin.test_volume_quotas.VolumeQuotasAdminV1TestJSON.test_update_all_quota_resources_for_tenant',
'tempest.api.volume.admin.test_volume_quotas_negative.BaseVolumeQuotasNegativeV2TestJSON.test_quota_volume_gigabytes',
'tempest.api.volume.admin.test_volume_quotas_negative.BaseVolumeQuotasNegativeV2TestJSON.test_quota_volumes',
'tempest.api.volume.admin.test_volume_quotas_negative.VolumeQuotasNegativeV1TestJSON.test_quota_volume_gigabytes',
'tempest.api.volume.admin.test_volume_quotas_negative.VolumeQuotasNegativeV1TestJSON.test_quota_volumes',
'tempest.scenario.test_shelve_instance.TestShelveInstance.test_shelve_volume_backed_instance',
'tempest.scenario.test_snapshot_pattern.TestSnapshotPattern.test_snapshot_pattern',
'tempest.scenario.test_stamp_pattern.TestStampPattern.test_stamp_pattern',
'tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_create_ebs_image_and_check_boot',
'tempest.scenario.test_volume_boot_pattern.TestVolumeBootPattern.test_volume_boot_pattern']


    #tests_list = ['tempest.api.image.v2.test_images_member.ImagesMemberTest.test_get_image_members_schema', 'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_name']
    for item in tests_list:
        work_queue.put(item)

    #processes = [Process(target=do_work, args=(work_queue,)) for i in range(2)]
    processes = [Process(target=do_work, args=(work_queue,)) for i in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print('++++++++++++++++++++++++++++++++')
    print time.time() - start_time
    print('++++++++++++++++++++++++++++++++')
