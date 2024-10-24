# # Ansys Fluent workflow
#
# In this example, the application of PyWorkbench, a Python client scripting tool for Ansys Workbench, is demonstrated in a use case for Ansys Fluent Workflow. The Ansys Fluent TUI (Text User Interface) journal files are utilized to set up and solve the simulation. For meshing Ansys Fluent Meshing WTM (Water Tight Meshing Workflow)is employed through recorded journaling capabilites of Ansys Fluent. As aware, Workbench offers the ability to record actions performed in the user interface, also known as journaling. These recorded actions are saved as Python scripts, which allow for extending functionality, automating repetitive analyses, and running analyses in batch mode. This example demonstrates how to use such a journal file with PyWorkbench for Ansys Fluent Workflow.

# This example sets up and solves a three-dimensional turbulent fluid flow and heat transfer problem in a mixing elbow, which is common in piping systems in power plants and process industries. Predicting the flow field and temperature field in the area of the mixing region is important to designing the junction properly.
#
# # Problem description
# A cold fluid at 20 deg C flows into the pipe through a large inlet. It then mixes with a warmer fluid at 40 deg C that enters through a smaller inlet located at the elbow. The pipe dimensions are in inches, and the fluid properties and boundary conditions are given in SI units. Because the Reynolds number for the flow at the larger inlet is ``50,800``, a turbulent flow model is required.

# # What this tutorial covers
#
# This use case that demonstrates following PyWorkbench API capabilities such as:
# - Initiating the Ansys Workbench server locally and establishing a connection with a local client.
# - Uploading the required input data from client working directory to server working directory.
# - Executing the Ansys Workbench journal (.wbjn) script on the server, which will execute the Fluent simulation using setup.jou and solve.jou TUI scripts. refer assets for simulation input data.
# - Downloading the results from the server to client.
# - Shutting down the server.

# ## Performed required imports
# Performing essential imports for Ansys Workbench, pathlib to handle filesystems path.

import pathlib
from ansys.workbench.core import launch_workbench

# ## Setting up server Working directory and asset paths

# +
workdir = pathlib.Path("__file__").parent

server_workdir = workdir / 'server_workdir'
server_workdir.mkdir(exist_ok=True)

assets = workdir / "assets"
scdoc = assets /"scdoc"
jou = assets / "jou"
# -

# ## Launch the workbench session with specified server and client working directories

wb = launch_workbench(server_workdir=str(server_workdir.absolute()), client_workdir=str(workdir.absolute()))

# ## Uploading the input data
# Upload several input files (Geometry, Ansys Fluent simulation setup and solve journal files ), which will be transferred to the host.

wb.upload_file(str(scdoc / "mixing_elbow.scdoc"))
wb.upload_file(str(jou / "setup.jou"))
wb.upload_file(str(jou / "solve.jou"))

# ## Executing a workbench script
# This will configure the workbench project schematic. This file is Ansys Workbench recorded journal file (Python Script). This can be easily configured as per requirement.
# >Note: For a better understanding of how meshing, setup, and solve workflows are being utilized, please refer to the project.wbjn file.

sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()))

# ## Downloading output files to the client-side working directory
# Here, only the contour saved during the simulation data post-processing is being downloaded. But one can download all the output as required.

wb.download_file("temperature_contour.jpeg")

# ## Shutdown the Ansys Workbench server session

wb.exit()


