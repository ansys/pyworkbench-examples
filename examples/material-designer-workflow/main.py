# # Material Designer

# This notebook demonstrates the process of sending user-defined parameter values to a parameterized analysis and receive the corresponding simulation output via a Workbench service on a local machine. 

import os
import pathlib

from ansys.workbench.core import launch_workbench

# Launch the Workbench service on the local machine, using some options. 
# Define several directories that will be used during the session. 
# `workdir` is set to the parent directory of the current file. 
# `assets`, `scripts`, and `wbpz` are subdirectories within the working directory. 
# The `launch_workbench` function is called to start a Workbench session with specified directory.

workdir = pathlib.Path("__file__").parent

assets = workdir / "assets"

wb = launch_workbench(show_gui=True, client_workdir=str(workdir.absolute()))

# Upload the project files to the server using the `upload_file_from_example_repo` method. 
# The file to upload is `MatDesigner.wbpz`.

wb.upload_file_from_example_repo("material-designer/wbpz/MatDesigner.wbpz")

# Execute a Workbench script (`project.wbjn`) to define the project and load the geometry using the `run_script_file` method. 
# The `set_log_file` method is used to direct the logs to `wb_log_file.log`.

export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')

# Prepare the Workbench command template to make modifications to the material property, in this case the Young's modulus of the material

wbjn_template = """designPoint1 = Parameters.GetDesignPoint(Name="0")
parameter1 = Parameters.GetParameter(Name="P1")
designPoint1.SetParameterExpression(
    Parameter=parameter1,
    Expression="{} [Pa]")
backgroundSession1 = UpdateAllDesignPoints(DesignPoints=[designPoint1])
"""

# Update the project with a new value for the Young's modulus

my_command = wbjn_template.format( 1.6e10 )
wb.run_script_string( my_command )

# Extract output values. First, we prepare the Workbench script to quiry output parameter values

extract_output = '''import json
p = Parameters.GetParameter(Name="P{}")
my_tag = p.DisplayText
wb_script_result =json.dumps( my_tag + ',' + str(p.Value) )
'''

# Get updated output values

outputs = {}
for p in range( 2 , 12 ):
    return_val = wb.run_script_string( extract_output.format( p ) ).split(',')
    name = return_val[0]
    parameter_val = float(return_val[1])
    outputs[ name ] = parameter_val
print( outputs )

# Finally, call the `exit` method on the Workbench client to gracefully shut down the service.

wb.exit()


