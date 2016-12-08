from sidecarclient import client

sidecar = client.Client(
    auth_version = 2,
    username = "admin",
    password = "stack123",
    endpoint = "http://198.100.181.74:9090/v2",
    auth_url = "http://198.100.181.74:35357/v2.0",
    endpoint_type="publicURL",
    region_name = "RegionOne",
    tenant_name = "admin",
    timeout = 10,
    insecure = True
)
print "###############################################################"
print "# HealthCheck for Events                                      #"
print "###############################################################"
events = sidecar.events.evacuate_healthcheck()
