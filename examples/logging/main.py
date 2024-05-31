# # PyWorkbench demo: launcher options; log levels; wild card file names; etc

import pathlib
import os
from ansys.api.workbench.v0.launch_workbench import launch_workbench

# launch Workbench service on the local machine; using some options
workdir = pathlib.Path("__file__").parent
server_workdir = workdir / "server_workdir"
client_workdir = workdir / "client_workdir"
alternative_target_dir = workdir / "alternative_target_dir"

wb = launch_workbench(release="241", server_workdir=str(server_workdir.absolute()), client_workdir=str(client_workdir.absolute()))

# demo downloading files with wildcard
downloaded1 = wb.download_file('server1.*')

# demo downloading whole server directory into an alternative local directory
downloaded2 = wb.download_file('*', target_dir=alternative_target_dir)

# demo uploading files with wildcard
wb.upload_file('*.txt', 'model?.prt')

# demo uploading files in an alternative dir and non-existing files, with progress bar off
wb.upload_file(os.path.join(alternative_target_dir, 'app.py'), 'non_existing_file1', 'non_existing_file2', show_progress=False)

# use a log file for PyWorkbench script execution
export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
print(wb.run_script_file('wb.wbjn', log_level='info'))

# disable the log file; make console log verbose
wb.reset_log_file()
wb.set_console_log_level('info')
print(wb.run_script_file('wb.wbjn', log_level='info'))

# run the same workflow with more restricted console log level
wb.set_console_log_level('error')
print(wb.run_script_file('wb.wbjn', log_level='info'))

# shutdown the Workbench client and service
wb.exit()
