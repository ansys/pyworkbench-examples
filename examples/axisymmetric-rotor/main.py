# # Workbench Client

import os
import pathlib

from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical

# +
# launch Workbench service on the local machine; using some options

workdir = pathlib.Path("__file__").parent
assets = workdir / "assets"
scripts = workdir / "scripts"
agdb = workdir / "agdb"

wb = launch_workbench(release="241", server_workdir=str(workdir), client_workdir=str(workdir))
# -

# upload a couple of input files from example data repo
wb.upload_file(str(agdb / "axisymmetric_model.agdb"))
wb.upload_file(str(agdb / "rotor_3d_model.agdb"))
wb.upload_file(str(scripts / "axisymmetric_rotor.py"))
wb.upload_file(str(scripts / "rotor_3d.py"))

# run a Workbench script to define the project and load geometry. Export workbench log to a file w2.log.
export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
sys_name = wb.run_script_file(str(assets / "project.wbjn"), log_level='info')
print(sys_name)

# +
# start PyMechanical server on the system, then create a PyMechanical client session
# to solve 2D General Axisymmetric Rotor Model

server_port = wb.start_mechanical_server(system_name=sys_name[1])
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)
# -

# run a Mechanical python script via PyMechanical to mesh and solve the 2D general axisymmetric rotor model
with open (scripts / "axisymmetric_rotor.py") as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# +
# Download output file from PyMechanical working directory and print contents of 2D general axisymmetric rotor model

# Specify Mechanical directory of Modal Campbell Analysis
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")

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
# Download postprocess/output images from PyMechanical working directory and display of 2D general axisymmetric rotor model

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

#Specify Mechanical directory path of Modal Campbell Analysis
mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")

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

image_name = "tot_deform_2D.png"
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
# Download output file from PyMechanical working directory and print contents of 2D general axisymmetric rotor model

# Specify Mechanical directory of Unbalance response Analysis
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[3].WorkingDir")

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
# start PyMechanical server on the system, then create a PyMechanical client session
# Reference solution: to solve 3D Rotor Model

server_port = wb.start_mechanical_server(system_name=sys_name[0])
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)
# -

# run a Mechanical python script via PyMechanical to mesh and solve the 3D rotor model
with open (r"scripts\rotor_3d.py") as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# +
# Download output file from PyMechanical working directory and print contents of 3D Rotor Model

# Specify Mechanical directory of Modal Campbell Analysis
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")

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
# Download postprocess/output images from PyMechanical working directory and display of 3D rotor model

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

#Specify Mechanical directory path of Modal Campbell Analysis
mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")

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

image_name = "tot_deform_3D.png"
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
# Download output file from PyMechanical working directory and print contents of 3D Rotor Model

# Specify Mechanical directory of Unbalance Response Analysis
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[3].WorkingDir")

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
# Download all the files from the server to the current working directory of 3D Rotor Model
# set working directory accordingly

import shutil
import glob

current_working_directory = os.getcwd()
target_dir2 = current_working_directory
# Verify the target path to copy the files.
print(f"Files to be copied from server path at: {target_dir2}")

# Verify the source path for directory.
print(f"All the solver file is stored on the server at: {result_solve_dir_server}")

source_dir = result_solve_dir_server
destination_dir = target_dir2
# Copy all the files
for file in glob.glob(source_dir + '/*'):
    shutil.copy(file, destination_dir)
# -

# shutdown the Workbench client and service
wb.exit()
