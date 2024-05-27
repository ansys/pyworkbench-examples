# # PyWorkbench - Fluent Use Case - Mixing Elbow
#
# #### This is a Ansys Fluent use case to demonstrates PyWorkbench features like:
# - Launch the Workbench server locally and connect a local client to the server
# - Update the required input data
# - Run the wbjn script on the server which will run the Fluent simulation using setup.jou & solve.jou tui scripts
# - Download the results from the server
# - Disconnect the client from the server and shutdown the server
#

# ### Import necessary libraries

from ansys.workbench.core import launch_workbench as lw

# ### Define the working directory

workdir = "D:\Research\pyworkbench\example"

# ### Launch the workbench session

# launch Workbench service
client = lw(client_workdir = workdir)


# ### Upload the CAD model

# upload a couple of input files, This files get uploaded to the host
client.upload_file("mixing_elbow.scdoc")
client.upload_file("setup.jou")
client.upload_file("solve.jou")

# ### Run the script

# run a Workbench script to define the Workbench Project Schematic
output = client.run_script_file('wb_setup.wbjn')
print(output)

# ### Download the simulation data

# download a output files in working directory at client side working directory
client.download_file("contour_1.jpeg")

# ### Shutdown the service

# shutdown the server and client
client.exit()
