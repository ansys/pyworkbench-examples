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

import pathlib

from ansys.workbench.core import launch_workbench

# ### Define the working directory

workdir = pathlib.Path("__file__").parent

# Creating server working directory, though this examples demonstrate on local
server_workdir = workdir / 'server_workdir'  
server_workdir.mkdir(exist_ok=True)  

assets = workdir / "assets"
scdoc = assets /"scdoc"
jou = assets / "jou"

# ### Launch the workbench session

# launch Workbench service
wb = launch_workbench(release="241", server_workdir=str(server_workdir.absolute()), client_workdir=str(workdir.absolute()))

# ### Upload the CAD model
# upload a couple of input files, This files get uploaded to the host
wb.upload_file(str(scdoc / "mixing_elbow.scdoc"))
wb.upload_file(str(jou / "setup.jou"))
wb.upload_file(str(jou / "solve.jou"))

# ### Run the script

# run a Workbench script to define the Workbench Project Schematic
sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()))
print(sys_name)

# ### Download the simulation data

# download a output files in working directory at client side working directory
wb.download_file("contour_1.jpeg")

# ### Shutdown the service

# shutdown the server and client
wb.exit()
