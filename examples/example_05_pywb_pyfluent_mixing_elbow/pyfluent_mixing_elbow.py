# # Fluent setup and solution using PyFluent APIs
# ------------------------------------------------
# This example sets up and solves a three-dimensional turbulent fluid flow
# and heat transfer problem in a mixing elbow, which is common in piping
# systems in power plants and process industries. Predicting the flow field
# and temperature field in the area of the mixing region is important to
# designing the junction properly.
#
# This example uses settings objects.
#
# **Problem description**
#
# A cold fluid at 20 deg C flows into the pipe through a large inlet. It then mixes
# with a warmer fluid at 40 deg C that enters through a smaller inlet located at
# the elbow. The pipe dimensions are in inches, and the fluid properties and
# boundary conditions are given in SI units. Because the Reynolds number for the
# flow at the larger inlet is ``50, 800``, a turbulent flow model is required.

# ###############################################################################
# # Perform required imports
# # ~~~~~~~~~~~~~~~~~~~~~~~~

import os
from ansys.workbench.core import launch_workbench

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization.pyvista import Graphics

# # Specify client and server directories and launch WB service (This example launches WB locally)

# +
client_dir = r'D:\users\mvani\PyWB\PyWB-examples\pyfluent_mixing_elbow\client_work_dir'
server_dir = r'D:\users\mvani\PyWB\PyWB-examples\pyfluent_mixing_elbow\server_work_dir'

host = 'localhost'
release = '241'

wb = launch_workbench(release=release, server_workdir=server_dir, client_workdir=client_dir)
# -

# # Get the input file from example data and upload to server directory

import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
wb.upload_file(import_filename)

# +
# run a Workbench script to define the project and load geometry

export_path = os.path.join(client_dir, 'wb_log_file.log')
wb.set_log_file(export_path)
wb.run_script_string('template1 = GetTemplate(TemplateName="FLUENT")', log_level='info')
wb.run_script_string('system1 = template1.CreateSystem()')

# -

# ###############################################################################
# # Launch Fluent
# # ~~~~~~~~~~~~~
# # Launch Fluent as a service in meshing mode with double precision running on
# # two processors.

server_info_file = wb.start_fluent_server(system_name= "FLU")
fluent_session = pyfluent.connect_to_fluent(server_info_filepath= server_info_file)

# ###############################################################################
# # Import mesh and perform mesh check
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Import the mesh and perform a mesh check, which lists the minimum and maximum
# # x, y, and z values from the mesh in the default SI units of meters. The mesh
# # check also reports a number of other mesh features that are checked. Any errors
# # in the mesh are reported. Ensure that the minimum volume is not negative because
# # Fluent cannot begin a calculation when this is the case.

import_filename = os.path.join(server_dir, 'mixing_elbow.msh.h5')
fluent_session.file.read(file_type="case", file_name= import_filename)

# ###############################################################################
# # Set working units for mesh
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Set the working units for the mesh to inches. Because the default SI units are
# # used for everything except length, you do not have to change any other units
# # in this example. If you want working units for length to be other than inches
# # (for example, millimeters), make the appropriate change.

fluent_session.tui.define.units("length", "in")

# ###############################################################################
# # Enable heat transfer
# # ~~~~~~~~~~~~~~~~~~~~
# # Enable heat transfer by activating the energy equation.

fluent_session.setup.models.energy.enabled = True

# ###############################################################################
# # Create material
# # ~~~~~~~~~~~~~~~
# # Create a material named ``"water-liquid"``.

fluent_session.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

# ###############################################################################
# # Set up cell zone conditions
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Set up the cell zone conditions for the fluid zone (``elbow-fluid``). Set ``material``
# # to ``"water-liquid"``.

fluent_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "water-liquid"

# ###############################################################################
# # Set up boundary conditions for CFD analysis
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Set up the boundary conditions for the inlets, outlet, and walls for CFD
# # analysis.
#
# # cold inlet (cold-inlet), Setting: Value:
# # Velocity Specification Method: Magnitude, Normal to Boundary
# # Velocity Magnitude: 0.4 [m/s]
# # Specification Method: Intensity and Hydraulic Diameter
# # Turbulent Intensity: 5 [%]
# # Hydraulic Diameter: 4 [inch]
# # Temperature: 293.15 [K]

cold_inlet = fluent_session.setup.boundary_conditions.velocity_inlet["cold-inlet"]

cold_inlet.get_state()


cold_inlet.momentum.velocity.value = 0.4
cold_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
cold_inlet.turbulence.turbulent_intensity = 0.05
cold_inlet.turbulence. hydraulic_diameter = "4 [in]"
cold_inlet.thermal.t.value = 293.15

# # hot inlet (hot-inlet), Setting: Value:
# # Velocity Specification Method: Magnitude, Normal to Boundary
# # Velocity Magnitude: 1.2 [m/s]
# # Specification Method: Intensity and Hydraulic Diameter
# # Turbulent Intensity: 5 [%]
# # Hydraulic Diameter: 1 [inch]
# # Temperature: 313.15 [K]

# +
hot_inlet = fluent_session.setup.boundary_conditions.velocity_inlet["hot-inlet"]

hot_inlet.momentum.velocity.value = 1.2
hot_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
hot_inlet.turbulence.turbulent_intensity = 0.05
hot_inlet.turbulence. hydraulic_diameter = "1 [in]"
hot_inlet.thermal.t.value = 313.15
# -

# # pressure outlet (outlet), Setting: Value:
# # Backflow Turbulent Intensity: 5 [%]
# # Backflow Turbulent Viscosity Ratio: 4

fluent_session.setup.boundary_conditions.pressure_outlet["outlet"].turbulence.turbulent_viscosity_ratio_real = 4

# # Set 150 iterations for solution

fluent_session.solution.run_calculation.iter_count = 150

# # Update Solution using WB Journal Command

wb.run_script_string("system1 = GetSystem(Name=\"FLU\")")
wb.run_script_string("solutionComponent1 = system1.GetComponent(Name=\"Solution\")")
wb.run_script_string("solutionComponent1.Update(AllDependencies=True)")

# ###############################################################################
# # Create velocity vectors
# # ~~~~~~~~~~~~~~~~~~~~~~~
# # Create and display velocity vectors on the ``symmetry-xyplane`` plane

# ###############################################
# # Post processing with PyVista (3D visualization)
# # =============================================

graphics_session_vec = Graphics(fluent_session)
velocity_vector = graphics_session_vec.Vectors["velocity-vector"]
velocity_vector.field = "temperature"
velocity_vector.surfaces_list = ["symmetry-xyplane"]
velocity_vector.scale = 2
velocity_vector.display()

# ###############################################################################
# # Compute mass flow rate
# # ~~~~~~~~~~~~~~~~~~~~~~
# # Compute the mass flow rate.

# +
fluent_session.solution.report_definitions.flux["mass_flow_rate"] = {}

mass_flow_rate = fluent_session.solution.report_definitions.flux["mass_flow_rate"]
mass_flow_rate.boundaries = [
    "cold-inlet",
    "hot-inlet",
    "outlet",
]
mass_flow_rate.print_state()
fluent_session.solution.report_definitions.compute(report_defs=["mass_flow_rate"])
# -

# # Save project

file_path = os.path.join(server_dir, "mixing_elbow.wbpj")
save_string = "Save(FilePath=\"" + file_path + "\"," + "Overwrite=True)"
# wb.run_script_string('Save(FilePath="mixing_elbow1.wbpj", Overwrite=True)')
wb.run_script_string(save_string)


file_path = os.path.join(server_dir, "mixing_elbow.wbpz")
archive_string = "Archive(FilePath=\"" + file_path + "\")"
wb.run_script_string(archive_string)

# # Download the WB archived project

wb.download_file("mixing_elbow.wbpz")

fluent_session.exit()

wb.exit()
