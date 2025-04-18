# # Logging
#
# This example showcases the logging capabilities of PyWorkbench.

import pathlib
import os
from ansys.workbench.core import launch_workbench

# First, import the necessary modules. We import `pathlib` for handling filesystem paths and `os` for interacting with the operating system. The `launch_workbench` function from `ansys.workbench.core` is imported to start a Workbench session.

# Next, launch a Workbench session using PyWorkbench. Different directories are declared, including the client and server working directories, which should NOT be the same.

workdir = pathlib.Path("__file__").parent
server_workdir = workdir / "server_workdir"
client_workdir = workdir / "client_workdir"
alternative_target_dir = workdir / "alternative_target_dir"

# Here, we define several directories that will be used during the session.
# `workdir` is set to the directory containing the current file.
# `server_workdir`, `client_workdir`, and `alternative_target_dir` are subdirectories within the working directory.

# Launch Workbench using previous directories:

wb = launch_workbench(server_workdir=str(server_workdir.absolute()), client_workdir=str(client_workdir.absolute()))

# The `launch_workbench` function is called to start a Workbench session.
# `server_workdir` and `client_workdir` are set to their absolute paths to avoid any ambiguity in directory locations.

downloaded1 = wb.download_file('server1.*')

# This command demonstrates how to download files from the server using a wildcard.
# The `download_file` method is used to fetch all files matching the pattern `server1.*` from the server to the client.

downloaded2 = wb.download_file('*', target_dir=alternative_target_dir)

# This command downloads the entire contents of the server directory to an alternative local directory specified by `alternative_target_dir`.

wb.upload_file('*.txt', 'model?.prt')

# This command shows how to upload files to the server using wildcards.
# All `.txt` files and files matching the pattern `model?.prt` in the client directory are uploaded to the server.

wb.upload_file(os.path.join(alternative_target_dir, 'app.py'), 'non_existing_file1', 'non_existing_file2', show_progress=False)

# Here, files are uploaded from an alternative directory, and non-existing files are specified.
# The `show_progress` parameter is set to `False` to disable the progress bar during the upload.

export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
print(wb.run_script_file('wb.wbjn', log_level='info'))

# This segment sets up a log file for the script execution.
# The `set_log_file` method directs the logs to `wb_log_file.log`, and `run_script_file` executes a script with `info` log level.
# The output of the script is printed to the console.

wb.reset_log_file()
wb.set_console_log_level('info')
print(wb.run_script_file('wb.wbjn', log_level='info'))

# To change the logging configuration, we first disable the log file using `reset_log_file`.
# The console log level is then set to `info` using `set_console_log_level`.
# The script is run again with the same log level, and the output is printed.

wb.set_console_log_level('error')
print(wb.run_script_file('wb.wbjn', log_level='info'))

# In this step, the console log level is set to `error`, making the logging more restrictive.
# The script is executed again, and only error-level logs are shown.

wb.exit()
