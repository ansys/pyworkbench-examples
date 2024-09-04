# # Transient Electro-Thermal Simulation of Transient Voltage Suppression (TVS) Diodes

# This notebook demonstrates the process of running a Workbench service with Electronic Desktop on a local machine to solve highly non-linear Diode response subjected to high thermal load and mechanical stresses.  
# It includes steps for uploading project files, executing scripts.


import pathlib
import os
from ansys.workbench.core import launch_workbench

# Launch the Workbench service on the local machine using specific options.
# Define the working directory and subdirectories for assets, scripts, and geometry databases (agdb).
# The `launch_workbench` function starts a Workbench session with the specified directories.


workdir = pathlib.Path(__file__).parent

assets = workdir / "assets"
scripts = workdir / "scripts"


wb = launch_workbench(client_workdir=str(workdir.absolute()), server_workdir=str(workdir.absolute()))

# Upload the project files to the server using the `upload_file` method.
# The files uploaded are `TVR14471_V.wbpz`, `10_1000_Pulse.csv`


wb.upload_file_from_example_repo("ansys-aedt-workflow/wbpz/TVR14471_V.wbpz")
wb.upload_file(str(assets / "10_1000_Pulse.csv"))

# Execute a Workbench script (`project.wbjn`) to define the project and load the geometry using the `run_script_file` method. 
# The `set_log_file` method is used to direct the logs to `wb_log_file.log`. 

export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
csv_path = str((assets / "10_1000_Pulse.csv").absolute())
csv_path = csv_path.replace("\\", "/")

wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')

with open(str((workdir / "pulse_data.wbjn").absolute()), "w") as f:
    f.write(f"""csv_file_name=r'{csv_path}' """)

wb.run_script_file(str((workdir / "pulse_data.wbjn").absolute()), log_level='info')

# Start a Mechanical and AEDT client sessions to solve the Transient Electro-Thermal Simulation.
# Both MECHANICAL and AEDT sessions will be started
# Note: Disable the Distribution of the solution in Ansys Mechanical.
wb.run_script_file(str((scripts / "DC_Cond_ThermTransient_VariableTimeStep.py").absolute()), log_level='info')
