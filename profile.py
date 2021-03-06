"""
This script creates a 4 node cluster of virtual computers on CloudLab

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
# Create local topology
link = request.LAN("lan")

# Add four XenVMs to the request.
for i in range(1, 5):    
    node = request.XenVM("node-" + str(i)) 
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
    
    iface = node.addInterface("if" + str(i))
    iface.component_id = "eth" + str(i)
    
    # assign unique IPs
    iface.addAddress(rspec.IPv4Address("192.168.1." + str(i), "255.255.255.0"))        
    link.addInterface(iface)
    

    # if node-1, give it a public interface
    if i == 1:
        node.routable_control_ip = True
        # install and run Apache server on public-facing machine
        node.addService(rspec.Execute(shell="sh", command="/local/repository/silly.sh"))
        

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
