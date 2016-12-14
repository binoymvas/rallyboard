from sidecarclient import client

sidecar = client.Client(
    username = "admin",
    password = "stack123",
    auth_url = "http://198.100.181.68:35357/v2",
    region_name = "RegionOne",
    tenant_name = "admin",
    timeout = 10,
    insecure = False
)
"""
print "###############################################################"
print "# LISTING EVENTS                                              #"
print "###############################################################"

logs = sidecar.events.list_test_history(project_id='45')
for history in logs:
    print(history.id)

print "###############################################################"
print "# Detail                                                      #"
print "###############################################################"


logs = sidecar.events.get_test_history(id='asd1f')
print(logs.__dict__)
print(logs.history_create_time)
"""
print "###############################################################"
print "# Create                                                      #"
print "###############################################################"

logs = sidecar.events.create_test_history(testlist_id="fff5293c11cc4844b84e6754d7e1d855",
    project_id="8978",
    results = "gvjhsdgvjs7678bcjhdhgbskjch786768"
)


