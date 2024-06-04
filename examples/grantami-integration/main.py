# # Workbench Client

import os
import pathlib

from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical
from matplotlib import image as mpimg
from matplotlib import pyplot as plt

# +
# specify server working directory
workdir = pathlib.Path("__file__").parent

# Creating server working directory, though this examples demonstrate on local
server_workdir = workdir / 'server_workdir'  
server_workdir.mkdir(exist_ok=True)

scripts = workdir / "scripts"
assets = workdir / "assets"

# +
# launch Workbench service on the local machine; using some options
wb = launch_workbench(release="242", server_workdir=str(server_workdir.absolute()), client_workdir=str(workdir.absolute()))

server_dir = str(server_workdir.absolute())
client_dir = str(workdir.absolute())
# -

# **Install Granta Scriptting Toolkit**

### Note: To install Granta Scriptting Toolkit (STK), download the `Granta MI Enterprise Product` from Ansys Customer Portal.
### Granta STK file = "granta_miscriptingtoolkit-3.2.164-py3-none-any.whl"
### Granta STK is part of licensed Granta MI Enterprise Product.

# Upgrade pip with this command: 
# !python.exe -m pip install --upgrade pip

# Install Granta Scriptting Toolkit with this command: 
# !pip install "C:\userpath\granta_miscriptingtoolkit-3.2.164-py3-none-any.whl"

# +
###################################################################################
# Define function to import material from Granta MI Server
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Use matlabplotlib to display the images.
cwd = server_dir

def getMaterial(name,output):

    from GRANTA_MIScriptingToolkit import granta as mpy
    mi = mpy.connect('http://azeww22sim01/mi_servicelayer', autologon=True)
    db = mi.get_db('MaterialUniverse')
    table = db.get_table('MaterialUniverse')

    # Search for material
    rec = table.search_for_records_by_name(name)[0]
    exporter = rec.get_available_exporters(package="Ansys Workbench")[0]
    # Check if any required parameters are needed for export!
    parameters_required = exporter.get_parameters_required_for_export([rec])
    if parameters_required != {}:
        print("Parameters required!   :    ", parameters_required)
        exit()
    material_card = exporter.run_exporter([rec], parameter_defs=parameters_required)

    path_to_save = os.path.join(os.path.join(workdir.absolute()) + '/')
    exporter.save(file_path=path_to_save, file_name=name)
    file_extension = exporter.default_file_extension
    print("Exporter output saved to \"{}{}.{}\"".format(path_to_save, name, file_extension))
# -

# Export required material in xml file format to import in Mechanical
imp_materials = ['Structural steel, ASTM A500 Grade A']
for nmat in imp_materials:
    # Get the material from Granta
    getMaterial(nmat,'gradeA')

# +
# upload input files from example data repo to the server working directory
wb.upload_file_from_example_repo("blade-geometry.pmdb","grantami-integration/pmdb")
wb.upload_file_from_example_repo("results.csv","grantami-integration/csv")
wb.upload_file_from_example_repo("temperature-data.txt","grantami-integration/txt")

# upload input files from client working directory to server working directory
wb.upload_file("Structural steel, ASTM A500 Grade A.xml")
wb.upload_file(str(scripts / "nasa_rotor_67_fan_blade_inverse_solve.py"))
# -

# run a Workbench script to define the project and load geometry
export_path = 'wb_log_file.log'
wb.set_log_file(export_path)
sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')
print(sys_name)

# +
# start PyMechanical server on the system, then create a PyMechanical client session
# to solve Inverse analysis on NASA 67 Fan Blade Model

server_port = wb.start_mechanical_server(system_name=sys_name)
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)
# -

# run a Mechanical python script via PyMechanical to mesh and solve the model
with open (os.path.join(server_dir, "nasa_rotor_67_fan_blade_inverse_solve.py")) as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# +
# Download output file from PyMechanical working directory and print contents

# Specify Mechanical directory 
mechanical.run_python_script(f"solve_dir=ExtAPI.DataModel.AnalysisList[0].WorkingDir")

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

#Specify Mechanical directory path
mechanical.run_python_script(f"image_dir=ExtAPI.DataModel.AnalysisList[0].WorkingDir")

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

image_name = "thermal_strain.png"
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
# Download all the files from the server to the client working directory

import shutil
import glob

current_working_directory = os.getcwd()
destination_dir = server_dir
# Verify the target path to copy the files.
print(f"Download the files from server path to: {destination_dir}")

# Verify the source path for directory.
print(f"All the solver file is stored on the server at: {result_solve_dir_server}")

source_dir = result_solve_dir_server
# Copy all the files
for file in glob.glob(source_dir + '/*'):
    shutil.copy(file, destination_dir)
# -

# shutdown the Workbench client and service
wb.exit()
