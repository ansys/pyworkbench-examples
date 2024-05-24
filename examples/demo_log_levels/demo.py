# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # PyWorkbench demo: launcher options; log levels; wild card file names; etc

import os
import json
from ansys.api.workbench.v0.launch_workbench import launch_workbench

# launch Workbench service on the local machine; using some options
server_workdir = 'C:/Users/fli/demo/server_workdir'
client_workdir = 'C:/Users/fli/demo/client_workdir'
alternative_target_dir = 'C:/Users/fli/demo/alternative_target_dir'
release = '241'
wb = launch_workbench(release=release, server_workdir=server_workdir, client_workdir=client_workdir)

# demo downloading files with wildcard
downloaded1 = wb.download_file('server1.*')

# demo downloading whole server directory into an alternative local directory
downloaded2 = wb.download_file('*', target_dir=alternative_target_dir)

# demo uploading files with wildcard
wb.upload_file('*.txt', 'model?.prt')

# demo uploading files in an alternative dir and non-existing files, with progress bar off
wb.upload_file(os.path.join(alternative_target_dir, 'app.py'), 'non_existing_file1', 'non_existing_file2', show_progress=False)

# use a log file for PyWorkbench script execution
wb.set_log_file('C:/Users/fli/demo/wb.log')
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
