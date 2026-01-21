# # Transient Electro-Thermal Simulation of Transient Voltage Suppression (TVS) Diodes

# This notebook demonstrates the process of running a Workbench service with Electronic Desktop on a local machine to solve highly non-linear Diode response subjected to high thermal load and mechanical stresses.
# It includes steps for uploading project files, executing scripts.


import pathlib
import os
from ansys.workbench.core import launch_workbench

# Launch the Workbench service on the local machine using specific options.
# Define the working directory and subdirectories for assets, scripts, and geometry databases (agdb).
# The `launch_workbench` function starts a Workbench session with the specified directories.


workdir = pathlib.Path("__file__").parent

assets = workdir / "assets"
scripts = workdir / "scripts"


wb = launch_workbench(client_workdir=str(workdir.absolute()), use_insecure_connection=True)

# Upload the project files to the server using the `upload_file` method.
# The files uploaded are `TVR14471_V_short.wbpz`, `10_1000_Pulse_short.csv`
#
# **Note**: use 10_1000_Pulse.csv for fullscale simulation


wb.upload_file_from_example_repo("ansys-aedt-workflow/wbpz/TVR14471_V_short.wbpz")
wb.upload_file(str(assets / "10_1000_Pulse_short.csv"))

# Execute a Workbench script (`project.wbjn`) to define the project and load the geometry using the `run_script_file` method.
# The `set_log_file` method is used to direct the logs to `wb_log_file.log`.
#
# **Note**: For full-scale simulation use `TVR14471_V.wbpz` in line 7 of `project.wbjn`

log_path = 'wblog.txt'
wb.set_log_file(log_path)
wb.run_script_file(str(assets / "project.wbjn"), log_level='info')

# Start a Mechanical and AEDT client sessions to solve the Transient Electro-Thermal Simulation.
# Both MECHANICAL and AEDT sessions will be started
#
# **Note**: Disable the Distribution of the solution in Ansys Mechanical. For Full scale simulation use `10_1000_Pulse.csv` in line 232 of `DC_Cond_ThermTransient_VariableTimeStep.py`
#

wb.run_script_file(str(scripts / "DC_Cond_ThermTransient_VariableTimeStep.py"), log_level='info')

# Shutdown the Ansys Workbench server session

wb.exit()


