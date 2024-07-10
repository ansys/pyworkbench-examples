import pathlib
import os
from ansys.workbench.core import launch_workbench


workdir = pathlib.Path(__file__).parent

server = workdir / "server"
client = workdir / "client"

# path_name = os.path.dirname(__file__)
assets = workdir / "assets"
scripts = workdir / "scripts"
wbpz = workdir / "wbpz"

# # Specify client and server directories and launch WB service (This example launches WB locally)
wb = launch_workbench(release="241", server_workdir=str(server.absolute()), client_workdir=str(client.absolute()))

wb.upload_file(str(assets / "project.wbjn"))
wb.upload_file(str(wbpz / "TVR14471_V.wbpz"))
wb.upload_file(str(assets / "10_1000_Pulse.csv"))
wb.upload_file(str(scripts / "DC_Cond_ThermTransient_VariableTimeStep.py"))

# Execute a Workbench script (`project.wbjn`) to define the project and load the geometry using the `run_script_file` method. 
# The `set_log_file` method is used to direct the logs to `wb_log_file.log`. 
# The name of the system created is stored in `sys_name` and printed.

export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
csv_path = str((assets / "10_1000_Pulse.csv").absolute())
csv_path = csv_path.replace("\\", "/")

wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')
# wb.run_script_file(f""" 'csv_path'={csv_path}""")
with open(str((assets / "pulse_data.wbjn").absolute()), "w") as f:
    f.write(f"""csv_path=r'{csv_path}' """)

wb.run_script_file(str((assets / "pulse_data.wbjn").absolute()), log_level='info')
wb.run_script_file(str((scripts / "DC_Cond_ThermTransient_VariableTimeStep.py").absolute()), log_level='info')






# script_file = "DC_Cond_ThermTransient_VariableTimeStep.py"

# pulse_file = "10_1000_Pulse.csv"
# wb_script_open = os.path.join(path_name,"assets", wbjn_file)
# wb_script_run = os.path.join(path_name, script_file)  #ath_name +'\\'+ script_file

# # launch script to open the workbench project
# wb.run_script_file(wb_script_open,log_level="info")
# # launch script to start the workflow
# wb.run_script_file(wb_script_run,log_level="info")

