# # Axisymmetric rotor

# This notebook demonstrates the process of running a Workbench service on a local machine to solve both 2D general axisymmetric rotor and 3D rotor models using PyMechanical. 
# It includes steps for uploading project files, executing scripts, downloading results, and displaying output images.

import os
import pathlib

from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical

# Launch the Workbench service on the local machine using specific options.
# Define the working directory and subdirectories for assets, scripts, and geometry databases (agdb).
# The `launch_workbench` function starts a Workbench session with the specified directory.

workdir = pathlib.Path("__file__").parent

assets = workdir / "assets"
scripts = workdir / "scripts"

wb = launch_workbench(client_workdir=str(workdir.absolute()))

# Upload the project files to the server using the `upload_file_from_example_repo` method. 
# The files uploaded are `axisymmetric_model.agdb`, `rotor_3d_model.agdb`. 

wb.upload_file_from_example_repo("axisymmetric-rotor/agdb/axisymmetric_model.agdb")
wb.upload_file_from_example_repo("axisymmetric-rotor/agdb/rotor_3d_model.agdb")

# Execute a Workbench script (`project.wbjn`) to define the project and load the geometry.
# The log file is set to `wb_log_file.log` and the name of the system created is stored in `sys_name` and printed.

export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')
print(sys_name)

# Start a PyMechanical server for the system and create a PyMechanical client session to solve the 2D general axisymmetric rotor model.
# The project directory is printed to verify the connection.

server_port = wb.start_mechanical_server(system_name=sys_name[1])
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)

# Read and execute the script `axisymmetric_rotor.py` via the PyMechanical client to mesh and solve the 2D general axisymmetric rotor model.
# The output of the script is printed.

with open(scripts / "axisymmetric_rotor.py") as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# Specify the Mechanical directory for the Modal Campbell Analysis and fetch the working directory path.
# Download the solver output file (`solve.out`) from the server to the client's current working directory and print its contents.

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

# Specify the Mechanical directory path for the Modal Campbell Analysis and fetch the image directory path.
# Download an image file (`tot_deform_2D.png`) from the server to the client's current working directory and display it using `matplotlib`.

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")
result_image_dir_server = mechanical.run_python_script(f"image_dir")
print(f"Images are stored on the server at: {result_image_dir_server}")

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

# Specify the Mechanical directory for the Unbalance Response Analysis and fetch the working directory path.
# Download the solver output file (`solve.out`) from the server to the client's current working directory and print its contents.

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

# Start a PyMechanical server for the 3D rotor model system and create a PyMechanical client session.
# The project directory is printed to verify the connection.

server_port = wb.start_mechanical_server(system_name=sys_name[0])
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)

# Read and execute the script `rotor_3d.py` via the PyMechanical client to mesh and solve the 3D rotor model.
# The output of the script is printed.

with open(scripts / "rotor_3d.py") as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# Specify the Mechanical directory for the Modal Campbell Analysis and fetch the working directory path.
# Download the solver output file (`solve.out`) from the server to the client's current working directory and print its contents.

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

# Specify the Mechanical directory path for the Modal Campbell Analysis and fetch the image directory path.
# Download an image file (`tot_deform_3D.png`) from the server to the client's current working directory and display it using `matplotlib`.

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[2].WorkingDir")
result_image_dir_server = mechanical.run_python_script(f"image_dir")
print(f"Images are stored on the server at: {result_image_dir_server}")

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

# Specify the Mechanical directory for the Unbalance Response Analysis and fetch the working directory path.
# Download the solver output file (`solve.out`) from the server to the client's current working directory and print its contents.

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

# Download all the files from the server to the current working directory for the 3D rotor model.
# Verify the source path for the directory and copy all files from the server to the client.

import shutil
import glob

current_working_directory = os.getcwd()
target_dir2 = current_working_directory
print(f"Files to be copied from server path at: {target_dir2}")
print(f"All the solver files are stored on the server at: {result_solve_dir_server}")

source_dir = result_solve_dir_server
destination_dir = target_dir2

for file in glob.glob(source_dir + '/*'):
    shutil.copy(file, destination_dir)

# Finally, call the `exit` method on both the PyMechanical and Workbench clients to gracefully shut down the services.

mechanical.exit()
wb.exit()
