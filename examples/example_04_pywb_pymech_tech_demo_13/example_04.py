# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# # Workbench Client

from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical
import os
import pyvista as pv

# +
# launch Workbench service on the remote host machine; specify remote host machine name and user login credentials

client_dir = r'D:\GPS_Team\Engagements_2023\PyAnsys\PyWorkbench\Examples\Tech_Demo_13\client_dir'
server_dir = r'C:\Users\vnamdeo\Project_Data\PyWorkbench_demo\server_dir'

host = 'PUNVDHPG01023.win.ansys.com'
release = '241'

usrname = "vnamdeo"
key = os.getenv('PRIVATE_KEY')
passwrd = key

wb = launch_workbench(release=release, server_workdir=server_dir, client_workdir=client_dir,host=host,username=usrname,password=passwrd)

# +
# upload a couple of input files from example-data repo
wb.upload_file_from_example_repo("example_04_sector_model.cdb", "example_04")

# upload a input file from client directory to server working directory
wb.upload_file("example_04_cyclic_symm_analyses.py")

# +
# run a Workbench script to define the project and load geometry
log_path = os.path.join(client_dir, 'wb_log_file.log')
wb.set_log_file(log_path)
sys_nam = wb.run_script_file('example_04_geom_prep.wbjn', log_level='info')

print(sys_nam)

# +
# start PyMechanical server on the system, then create a PyMechanical client session
# to solve turbine blade Model

server_port = wb.start_mechanical_server(system_name=sys_nam)
mechanical = launch_mechanical(start_instance=False, ip=host, port=server_port)

print(mechanical.project_directory)
# -

# run a Mechanical python script via PyMechanical to mesh/solve the model
with open (os.path.join(client_dir, "example_04_cyclic_symm_analyses.py")) as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# +
# Download output file from PyMechanical working directory and print contents
# Specify Mechanical directory 
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[5].WorkingDir")
result_solve_dir_server = mechanical.run_python_script(f"solve_dir")
print(f"All solver files are stored on the server at: {result_solve_dir_server}")

solve_out_path = os.path.join(result_solve_dir_server, "solve.out")

def write_file_contents_to_console(path):
    """Write file contents to console."""
    with open(path, "rt") as file:
        for line in file:
            print(line, end="")

current_working_directory = os.getcwd()
mechanical.download(solve_out_path, target_dir=current_working_directory)
solve_out_local_path = os.path.join(current_working_directory, "solve.out")
write_file_contents_to_console(solve_out_local_path)
os.remove(solve_out_local_path)

# +
# Download postprocess/output images from PyMechanical working directory and display

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

#Specify Mechanical directory path
mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[5].WorkingDir")

# Verify the path for image directory.
result_image_dir_server = mechanical.run_python_script(f"image_dir")
print(f"Images are stored on the server at: {result_image_dir_server}")

# Download one image file from the server to the current working directory and plot
# using matplotlib.

def get_image_path(image_name):
    return os.path.join(result_image_dir_server, image_name)

def display_image(path):
    print(f"Printing {path} using matplotlib")
    image1 = mpimg.imread(path)
    plt.figure(figsize=(15, 15))
    plt.axis("off")
    plt.imshow(image1)
    plt.show()

image_name = "deformation.png"
image_path_server = get_image_path(image_name)

if image_path_server != "":
    current_working_directory = os.getcwd()

    local_file_path_list = mechanical.download(
        image_path_server, target_dir=current_working_directory
    )
    image_local_path = local_file_path_list[0]
    print(f"Local image path : {image_local_path}")
    
    display_image(image_local_path)

# +
# Download all the files from the server to the current working directory

# Specify Mechanical directory 
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[5].WorkingDir")
result_solve_dir_server = mechanical.run_python_script(f"solve_dir")
print(f"All solver files are stored on the server at: {result_solve_dir_server}")

solve_out_path = os.path.join(result_solve_dir_server, "*.*")

current_working_directory = os.getcwd()
mechanical.download(solve_out_path, target_dir=current_working_directory)
# -

# shutdown the Workbench client and service
wb.exit()
