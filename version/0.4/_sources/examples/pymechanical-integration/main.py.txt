# # PyMechanical integration

# This example demonstrates how to use PyWorkbench and PyMechanical together to upload geometry, run simulations, and visualize results. 
# It covers launching services, running scripts, and handling files between the client and server.

# First, import the necessary modules. We import `pathlib` for handling filesystem paths, `os` for interacting with the operating system, and `pyvista` for visualization. 
# The `launch_workbench` function from `ansys.workbench.core` is imported to start a Workbench session, and `launch_mechanical` from `ansys.mechanical.core` to start a Mechanical session.

import os
import pathlib
import pyvista as pv
from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical

# Define several directories that will be used during the session. 
# `workdir` is set to the parent directory of the current file. 
# `assets`, `scripts`, and `agdb` are subdirectories within the working directory. 
# The `launch_workbench` function is called to start a Workbench session with specified directories.

workdir = pathlib.Path("__file__").parent
assets = workdir / "assets"
scripts = workdir / "scripts"
agdb = workdir / "agdb"
wb = launch_workbench(release="241", server_workdir=str(workdir.absolute()), client_workdir=str(workdir.absolute()))

# Upload a geometry file (`two_pipes.agdb`) from the client to the server using the `upload_file` method.

wb.upload_file(str(agdb / "two_pipes.agdb"))

# Execute a Workbench script (`project.wbjn`) to create a mechanical system and load the geometry using the `run_script_file` method. 
# The name of the system created is stored in `system_name`.

system_name = wb.run_script_file(str((assets / "project.wbjn").absolute()))

# Start a PyMechanical service for the specified system using the `start_mechanical_server` method. 
# Create a PyMechanical client connected to this service using `launch_mechanical`. 
# The project directory is printed to verify the connection.

pymech_port = wb.start_mechanical_server(system_name=system_name)
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=pymech_port)
print(mechanical.project_directory)

# Read and execute the script `solve.py` via the PyMechanical client using `run_python_script`. 
# This script typically contains commands to mesh and solve the model. 
# The output of the script is printed.

with open(scripts / "solve.py") as sf:
    mech_script = sf.read()
print(mechanical.run_python_script(mech_script))

# Fetch output files (`*solve.out` and `*deformation.png`) from the solver directory to the client's working directory using the `download` method.

mechanical.download("*solve.out", target_dir=str(workdir.absolute()))
mechanical.download("*deformation.png", target_dir=str(workdir.absolute()))

# Read and print the content of the solver output file (`solve.out`) to the console.

with open(os.path.join(str(workdir.absolute()), "solve.out"), "r") as f:
    print(f.read())

# Plot the deformation result (`deformation.png`) using `pyvista`. 
# A `Plotter` object is created, and the image is added as a background. 
# The plot is then displayed.

pl = pv.Plotter()
pl.add_background_image(os.path.join(str(workdir.absolute()), "deformation.png"))
pl.show()

# Finally, the `exit` method is called on both the PyMechanical and Workbench clients to gracefully shut down the services, ensuring that all resources are properly released.

mechanical.exit()
wb.exit()
