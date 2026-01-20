# # PyWorkbench: PyMechanical-Granta MI STK Example (NASA Rotor67 Fan Blade Model - Inverse Solve)
#
# This is a Ansys Mechanical use case to demonstrates PyWorkbench features and its connection with PyMechanical-Granta MI STK like:
#
# - Launch the Workbench server locally and connect a local client to the server
# - Connect to the Granta MI server using STK and download required material data to consume in the simulation setup.
# - Update the required input data
# - Run the wbjn script on the server which will run the Mechanical simulation using project.wbjn & python scripts.
# - Download the results from the server
# - Disconnect the client from the server and shutdown the server
#
# Mechanical Use Case: Inverse-Solving Analysis of a Rotor Fan Blade with Disk
#
# Description: The NASA Rotor 67 fan bladed disk is a subsystem of a turbo fan compressor set used
# in aerospace engine applications. This sector model, representing a challenging industrial
# example for which the detailed geometry and flow information is available in the public
# domain, consists of a disk and a fan blade with a sector angle of 16.364 degrees.
# The sector model represents the running condition or hot geometry of the blade. It is
# already optimized at the running condition under loading. The primary objective is to
# obtain the cold geometry (for manufacturing) from the given hot geometry using inverse solving.

# ### Import necessary libraries

import os
import pathlib

from ansys.workbench.core import launch_workbench
from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import delete_downloads, download_file
from matplotlib import image as mpimg
from matplotlib import pyplot as plt

# ### Specify working directory

# +
workdir = pathlib.Path("__file__").parent
scripts = workdir / "scripts"
assets = workdir / "assets"
# -

# ### Launch Workbench as a service; using some options

# +
wb = launch_workbench(client_workdir=str(workdir.absolute()))
current_directory = os.getcwd()

# -

# ## Install Granta Scriptting Toolkit

# ### Note: To install Granta Scriptting Toolkit (STK), download the `Granta MI Enterprise Product` from Ansys Customer Portal.
# ### Granta STK file = "granta_miscriptingtoolkit-3.2.164-py3-none-any.whl"
# ### Granta STK is part of licensed Granta MI Enterprise Product.

# ### Upgrade pip with this command:

# +
# python -m pip install --upgrade pip
# -

# ### Install Granta Scriptting Toolkit with this command:

# +
#python -m pip install granta_miscriptingtoolkit-3.2.164-py3-none-any.whl
# -

# ### Granta MI STK Workflow
# ### Define function to import material from Granta MI Server
#
# ### Connect to Granta MI Service Layer
#
# ### Write a material card specific to selected Solver
#
# ### In this case exporting the material data in Ansys Mechanical Specific format in .xml file, which will get read by Ansys Mechanical Solver using PyMechnical API's.
#
# ### Note: In order to access the Granta service layer instance deployed for ACE, you must have the necessary permissions. Additionally, this instance can only be accessed through a VPN in case of remote access. Ensure that your VPN is active before proceeding.

GRANTAMI_ENDPOINT = os.getenv('GRANTA_ENDPOINT', None)
if not GRANTAMI_ENDPOINT:
    raise ValueError("GRANTA_ENDPOINT environment variable not set")

# Use matlabplotlib to display the images.
cwd = os.path.join(os.getcwd(), "out")

# Use matlabplotlib to display the images.
def getMaterial(name,output):

    from GRANTA_MIScriptingToolkit import granta as mpy
    mi = mpy.connect(GRANTAMI_ENDPOINT, autologon=True)
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

# ### Export the required material in xml file format from Granta MI to import it into Mechanical

imp_materials = ['Structural steel, ASTM A500 Grade A']
for nmat in imp_materials:
    # Get the material from Granta
    getMaterial(nmat,'gradeA')

# ### Upload input files from example data repo to the server working directory

# +
#wb.upload_file_from_example_repo("blade-geometry.pmdb","grantami-integration/pmdb")
#wb.upload_file_from_example_repo("results.csv","grantami-integration/csv")
#wb.upload_file_from_example_repo("temperature-data.txt","grantami-integration/txt")
# -

# ### Upload input files from client working directory to server working directory

wb.upload_file("Structural steel, ASTM A500 Grade A.xml")
wb.upload_file(str(scripts / "nasa_rotor_67_fan_blade_inverse_solve.py"))

# ### Run a Workbench script to define the project workflow and reads material data exported from Granta MI

log_path = 'wblog.txt'
wb.set_log_file(log_path)
sys_name = wb.run_script_file(str((assets / "project.wbjn").absolute()), log_level='info')
print(sys_name)

# ### Start PyMechanical server on the system, then create a PyMechanical client session to solve Inverse analysis on NASA 67 Fan Blade Model

# +
server_port = wb.start_mechanical_server(system_name=sys_name)
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)

print(mechanical.project_directory)
# -

# ### Download required files from the PyMechanical embedding example data repo

# +
# Download the geometry file
geometry_path = download_file("example_10_td_055_Rotor_Blade_Geom.pmdb", "pymechanical", "embedding")

# Download the CFX pressure data
cfx_data_path = download_file("example_10_CFX_ExportResults_FT_10P_EO2.csv", "pymechanical", "embedding")

# Download the temperature data
temp_data_path = download_file("example_10_Temperature_Data.txt", "pymechanical", "embedding")
# -

# ### File path corrections

geometry_path = geometry_path.replace("\\",r"/")
cfx_data_path = cfx_data_path.replace("\\",r"/")
temp_data_path = temp_data_path.replace("\\",r"/")

# ### Pass this vairable info to the PyMechanical instance

mech_output = mechanical.run_python_script(f"""
geometry_path='{geometry_path}'
cfx_data_path='{cfx_data_path}'
temp_data_path='{temp_data_path}'
""")

# ### Run a Mechanical python script using PyMechanical to mesh and solve the model

with open (scripts / "nasa_rotor_67_fan_blade_inverse_solve.py") as sf:
    mech_script = sf.read()
mech_output = mechanical.run_python_script(mech_script)
print(mech_output)

# ### Download output files from PyMechanical working directory and print contents

# +
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

mechanical.download(solve_out_path, target_dir=current_directory)
solve_out_local_path = os.path.join(current_directory, "solve.out")
write_file_contents_to_console(solve_out_local_path)
os.remove(solve_out_local_path)
# -

# ### Download postprocess/output images from PyMechanical working directory and display

# +
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
    local_file_path_list = mechanical.download(
        image_path_server, target_dir=current_directory
    )
    image_local_path = local_file_path_list[0]
    print(f"Local image path : {image_local_path}")

    display_image(image_local_path)
# -

# ### Download all the files from the server to the client working directory

# +
import shutil
import glob

destination_dir = current_directory
# Verify the target path to copy the files.
print(f"Download the files from server path to: {destination_dir}")

# Verify the source path for directory.
print(f"All the solver file is stored on the server at: {result_solve_dir_server}")

source_dir = result_solve_dir_server
# Copy all the files
for file in glob.glob(source_dir + '/*'):
    shutil.copy(file, destination_dir)
# -

# ### Shutdown the Workbench client and service

mechanical.exit()
wb.exit()
