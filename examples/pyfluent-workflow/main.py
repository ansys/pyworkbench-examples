# # Integrating PyFluent with PyWorkbench:
# This example showcases how to use PyFluent workflow together with PyWorkbench - (Python client scripting for Ansys Workbench).
#
# This example sets up and solves a three-dimensional turbulent fluid flow
# and heat transfer problem in a mixing elbow, which is common in piping
# systems in power plants and process industries. Predicting the flow field
# and temperature field in the area of the mixing region is important to
# designing the junction properly.
#
# This example uses Pyfluent settings objects API's.
#
# ## Problem description
#
# A cold fluid at 20 deg C flows into the pipe through a large inlet. It then mixes
# with a warmer fluid at 40 deg C that enters through a smaller inlet located at
# the elbow. The pipe dimensions are in inches, and the fluid properties and
# boundary conditions are given in SI units. Because the Reynolds number for the
# flow at the larger inlet is ``50,800``, a turbulent flow model is required.

# ## Performed required imports
# Performing essential imports for Ansys Workbench, Fluent Pythonic Interface and for downloading examples data.

import os
import pathlib
from ansys.workbench.core import launch_workbench
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples

# ## Specify client and server directories with launch WB service.

workdir = pathlib.Path("__file__").parent


wb = launch_workbench(client_workdir=str(workdir.absolute()))

# ## Download the input file from example data and upload to server directory.

import_filename = examples.download_file("mixing_elbow.msh.h5", "pyfluent/mixing_elbow")
wb.upload_file(import_filename)

# ## Generate a "FLUENT" System using Ansys Workbench Scripting API (used for Journaling) and parse it to the PyWorkbench API.

export_path = "wb_log_file.log"
wb.set_log_file(export_path)
wb.run_script_string('template1 = GetTemplate(TemplateName="FLUENT")', log_level="info")
wb.run_script_string("system1 = template1.CreateSystem()")


# ## Launch Fluent & Connect to Fluent
# Launch Fluent as server with PyWorkbench API and and connect to Pyfluent session

server_info_file = wb.start_fluent_server(system_name="FLU")
fluent_session = pyfluent.connect_to_fluent(server_info_file_name=server_info_file)


# ## Import mesh and perform mesh check

# +
# Import the mesh and perform a mesh check, which lists the minimum and maximum
# x, y, and z values from the mesh in the default SI units of meters. The mesh
# check also reports a number of other mesh features that are checked. Any errors
# in the mesh are reported. Ensure that the minimum volume is not negative because
# Fluent cannot begin a calculation when this is the case.

fluent_session.file.read_mesh(file_name=import_filename)
fluent_session.mesh.check()

# -

# ## Set working units for mesh

# Set the working units for the mesh to inches. Because the default SI units are
# used for everything except length, you do not have to change any other units
# in this example. If you want working units for length to be other than inches
# (for example, millimeters), make the appropriate change.

fluent_session.tui.define.units("length", "in")


# ## Enable heat transfer
# Enable heat transfer by activating the energy equation.

fluent_session.setup.models.energy.enabled = True

# ## Create material
# Create a material named ``"water-liquid"``.

fluent_session.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")

# ## Set up cell zone conditions

# Set up the cell zone conditions for the fluid zone (``elbow-fluid``). Set ``material``
# to ``"water-liquid"``.

fluent_session.setup.cell_zone_conditions.fluid['elbow-fluid'].general.material = "water-liquid"

# ## Set up boundary conditions for CFD analysis

# Set up the boundary conditions for the inlets, outlet, and walls for CFD
# analysis.
# - cold inlet (cold-inlet), Setting: Value:
# - Velocity Specification Method: Magnitude, Normal to Boundary
# - Velocity Magnitude: 0.4 [m/s]
# - Specification Method: Intensity and Hydraulic Diameter
# - Turbulent Intensity: 5 [%]
# - Hydraulic Diameter: 4 [inch]
# - Temperature: 293.15 [K]

cold_inlet = fluent_session.setup.boundary_conditions.velocity_inlet["cold-inlet"]
cold_inlet.get_state()
cold_inlet.momentum.velocity.value = 0.4
cold_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
cold_inlet.turbulence.turbulent_intensity = 0.05
cold_inlet.turbulence.hydraulic_diameter = "4 [in]"
cold_inlet.thermal.t.value = 293.15

# - hot inlet (hot-inlet), Setting: Value:
# - Velocity Specification Method: Magnitude, Normal to Boundary
# - Velocity Magnitude: 1.2 [m/s]
# - Specification Method: Intensity and Hydraulic Diameter
# - Turbulent Intensity: 5 [%]
# - Hydraulic Diameter: 1 [inch]
# - Temperature: 313.15 [K]

hot_inlet = fluent_session.setup.boundary_conditions.velocity_inlet["hot-inlet"]
hot_inlet.momentum.velocity.value = 1.2
hot_inlet.turbulence.turbulent_specification = "Intensity and Hydraulic Diameter"
hot_inlet.turbulence.turbulent_intensity = 0.05
hot_inlet.turbulence.hydraulic_diameter = "1 [in]"
hot_inlet.thermal.t.value = 313.15

# - pressure outlet (outlet), Setting: Value:
# - Backflow Turbulent Intensity: 5 [%]
# - Backflow Turbulent Viscosity Ratio: 4

fluent_session.setup.boundary_conditions.pressure_outlet[
    "outlet"
].turbulence.backflow_turbulent_viscosity_ratio = 4

# ## Initialize flow field

fluent_session.solution.initialization.hybrid_initialize()

# ## Solve for 150 iterations
# Setting iteration count to 150 to solve the model.

fluent_session.solution.run_calculation.iter_count = 100


# ## Update Solution using Workbench Journal Commands

script_string = """
solutionComponent1 = system1.GetComponent(Name="Solution")
system1 = GetSystem(Name="FLU")
solutionComponent1 = system1.GetComponent(Name="Solution")
solutionComponent1.Update(AllDependencies=True)
"""

wb.run_script_string(script_string)


# ## Postprocessing
# Create and display velocity vectors on the ``symmetry-xyplane`` plane.

# ## Configure graphics picture export
# Since Fluent is being run without the GUI, you must to export plots as picture files. Edit the picture settings to use a custom resolution so that the images are large enough.

graphics = fluent_session.results.graphics
if graphics.picture.use_window_resolution.is_active():
    graphics.picture.use_window_resolution = False
graphics.picture.x_resolution = 1920
graphics.picture.y_resolution = 1440

# ## Create velocity vectors
# Create and display velocity vectors on the ``symmetry-xyplane`` plane. Then, export the image for inspection.

graphics = fluent_session.results.graphics

graphics.vector["velocity_vector_symmetry"] = {}
velocity_symmetry = fluent_session.results.graphics.vector["velocity_vector_symmetry"]
velocity_symmetry.print_state()
velocity_symmetry.field = "velocity-magnitude"
velocity_symmetry.surfaces_list = [
    "symmetry-xyplane",
]
velocity_symmetry.scale.scale_f = 4
velocity_symmetry.style = "arrow"
velocity_symmetry.display()

graphics.views.restore_view(view_name="front")
graphics.views.auto_scale()
graphics.picture.save_picture(file_name="velocity_vector_symmetry.png")

# ## Compute mass flow rate
# Compute the mass flow rate.

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

# ## Exit Fluent Session

fluent_session.exit()

# ## Save project

save_string = """import os
workdir = GetServerWorkingDirectory()
path = os.path.join(workdir, "mixing_elbow.wbpj")
Save(FilePath=path , Overwrite=True)"""  
wb.run_script_string(save_string)

# ## Archive Project

archive_string ="""import os
workdir = GetServerWorkingDirectory()
path = os.path.join(workdir, "mixing_elbow.wbpz")
Archive(FilePath=path , IncludeExternalImportedFiles=True)"""  
wb.run_script_string(archive_string)

# ## Download the archived project which has all simulation data and results.

wb.download_file("mixing_elbow.wbpz")

# ## Exit Workbench Session.

wb.exit()
