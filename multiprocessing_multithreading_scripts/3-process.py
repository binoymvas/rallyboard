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
    
    tests_list = ['tempest.api.image.v2.test_images_member.ImagesMemberTest.test_get_image_members_schema', 'tempest.api.identity.admin.v2.test_tenants.TenantsTestJSON.test_tenant_update_name', 'tempest.api.identity.admin.v2.test_roles_negative.RolesNegativeTestJSON.test_remove_user_role_non_existent_role', 'tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_trust_impersonate', 'tempest.api.identity.admin.v3.test_roles.RolesV3TestJSON.test_list_roles','tempest.api.compute.admin.test_services_negative.ServicesAdminNegativeTestJSON.test_get_service_by_invalid_params','neutron.tests.tempest.api.test_trunk.TrunkTestJSON.test_create_trunk_empty_subports_list','tempest.api.compute.floating_ips.test_floating_ips_actions_negative.FloatingIPsNegativeTestJSON.test_associate_ip_to_server_without_passing_floating_ip', 'tempest.api.compute.servers.test_attach_interfaces.AttachInterfacesTestJSON.test_create_list_show_delete_interfaces','tempest.api.compute.servers.test_servers_negative.ServersNegativeTestJSON.test_resize_nonexistent_server','tempest.api.identity.admin.v2.test_tenant_negative.TenantsNegativeTestJSON.test_update_non_existent_tenant','tempest.api.identity.admin.v3.test_trusts.TrustsV3TestJSON.test_trust_expire_invalid','tempest.api.identity.admin.v2.test_users_negative.UsersNegativeTestJSON.test_update_user_for_non_existent_user','tempest.api.volume.test_volumes_snapshots.VolumesV1SnapshotTestJSON.test_snapshot_create_offline_delete_online','tempest.api.volume.admin.test_volume_types_negative.VolumeTypesNegativeV2Test.test_delete_nonexistent_type_id','tempest.api.volume.test_volumes_list.VolumesV1ListTestJSON.test_volume_list_with_detail_param_metadata','tempest.api.volume.test_volumes_snapshots.VolumesV1SnapshotTestJSON.test_snapshot_create_offline_delete_online','tempest.api.network.test_routers.RoutersIpV6Test.test_router_interface_port_update_with_fixed_ip','tempest.api.network.test_routers.RoutersIpV6Test.test_update_delete_extra_route','tempest.api.image.v1.test_images.ListImagesTest.test_index_status_active_detail','tempest.api.image.v2.test_images_member.ImagesMemberTest.test_get_image_members_schema']


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
