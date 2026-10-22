""" .. _ref_example_04_td_013:

Centrifugal Impeller Analysis Using Cyclic Symmetry and Linear Perturbation
---------------------------------------------------------------------------

The impeller blade assembly in this example is a subsystem of a gas turbine
engine used in aerospace applications. The model consists of a shroud and
an impeller blade assembly with a sector angle of 27.692 degrees. The full
model is composed of 13 primary blades and splitters located at a distance
of 1 mm from the rigid wall at the start of the analysis.

Coverage:
Modal, perturbed prestressed modal with linear and nonlinear base static 
solution, full-harmonic are performed on the cyclic-sector model.
Cyclic symmetry is applied.
Pressure, Rotational Velocity and Thermal Condition are applied.

"""

import os
import os.path
import tempfile
import string
import time
import json

from Ansys.ACT.Automation import Mechanical

# Store all main tree nodes as variables
GEOM = ExtAPI.DataModel.Project.Model.Geometry
MSH = ExtAPI.DataModel.Project.Model.Mesh
NS_GRP = ExtAPI.DataModel.Project.Model.NamedSelections
CONN_GRP = ExtAPI.DataModel.Project.Model.Connections
CS_GRP = ExtAPI.DataModel.Project.Model.CoordinateSystems

# Select NMM units add named selections and coordinate system
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

LCS1 = CS_GRP.AddCoordinateSystem()
LCS1.CoordinateSystemType=CoordinateSystemTypeEnum.Cylindrical
LCS1.OriginX = Quantity('0 [mm]')
LCS1.OriginY = Quantity('0 [mm]')
LCS1.OriginZ = Quantity('0 [mm]')
LCS1.SecondaryAxisDefineBy=CoordinateSystemAlignmentType.GlobalZ

NS_LOW = NS_GRP.AddNamedSelection()
NS_LOW.Name="NS_LOW"
NS_LOW.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_LOW.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.GeoFace
CRT1.Criterion=SelectionCriterionType.Size
CRT1.Operator=SelectionOperatorType.Equal
CRT1.Value = Quantity('607.35 [mm^2]')
GEN_CRT.Add(CRT1)

CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active=True
CRT2.Action=SelectionActionType.Filter
CRT2.EntityType=SelectionType.GeoFace
CRT2.Criterion=SelectionCriterionType.LocationZ
CRT2.Operator=SelectionOperatorType.Equal
CRT2.Value = Quantity('46.544 [mm]')
GEN_CRT.Add(CRT2)

CRT3 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT3.Active=True
CRT3.Action=SelectionActionType.Add
CRT3.EntityType=SelectionType.GeoFace
CRT3.Criterion=SelectionCriterionType.Size
CRT3.Operator=SelectionOperatorType.Equal
CRT3.Value = Quantity('997.65 [mm^2]')
GEN_CRT.Add(CRT3)

CRT4 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT4.Active=True
CRT4.Action=SelectionActionType.Filter
CRT4.EntityType=SelectionType.GeoFace
CRT4.Criterion=SelectionCriterionType.LocationZ
CRT4.Operator=SelectionOperatorType.GreaterThan
CRT4.Value = Quantity('21 [mm]')
GEN_CRT.Add(CRT4)
NS_LOW.Activate()
NS_LOW.Generate()


NS_HIGH = NS_GRP.AddNamedSelection()
NS_HIGH.Name="NS_LOW"
NS_HIGH.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_HIGH.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.GeoFace
CRT1.Criterion=SelectionCriterionType.Size
CRT1.Operator=SelectionOperatorType.Equal
CRT1.Value = Quantity('607.35 [mm^2]')
GEN_CRT.Add(CRT1)

CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active=True
CRT2.Action=SelectionActionType.Filter
CRT2.EntityType=SelectionType.GeoFace
CRT2.Criterion=SelectionCriterionType.LocationZ
CRT2.Operator=SelectionOperatorType.Equal
CRT2.Value = Quantity('24.348 [mm]')
GEN_CRT.Add(CRT2)

CRT3 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT3.Active=True
CRT3.Action=SelectionActionType.Add
CRT3.EntityType=SelectionType.GeoFace
CRT3.Criterion=SelectionCriterionType.Size
CRT3.Operator=SelectionOperatorType.Equal
CRT3.Value = Quantity('997.65 [mm^2]')
GEN_CRT.Add(CRT3)

CRT4 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT4.Active=True
CRT4.Action=SelectionActionType.Filter
CRT4.EntityType=SelectionType.GeoFace
CRT4.Criterion=SelectionCriterionType.LocationX
CRT4.Operator=SelectionOperatorType.GreaterThan
CRT4.Value = Quantity('13 [mm]')
GEN_CRT.Add(CRT4)
NS_HIGH.Activate()
NS_HIGH.Generate()

NS_PRES = NS_GRP.AddNamedSelection()
NS_PRES.Name="NS_PRES"
NS_PRES.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_PRES.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.GeoFace
CRT1.Criterion=SelectionCriterionType.Size
CRT1.Operator=SelectionOperatorType.Equal
CRT1.Value = Quantity('2302.1 [mm^2]')
GEN_CRT.Add(CRT1)

CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active=True
CRT2.Action=SelectionActionType.Add
CRT2.EntityType=SelectionType.GeoFace
CRT2.Criterion=SelectionCriterionType.Size
CRT2.Operator=SelectionOperatorType.Equal
CRT2.Value = Quantity('101.11 [mm^2]')
GEN_CRT.Add(CRT2)
NS_PRES.Activate()
NS_PRES.Generate()

NS_BODIES = NS_GRP.AddNamedSelection()
NS_BODIES.Name="NS_BODIES"
NS_BODIES.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_BODIES.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.GeoBody
CRT1.Criterion=SelectionCriterionType.Size
CRT1.Operator=SelectionOperatorType.GreaterThan
CRT1.Value = Quantity('1 [mm^3]')
GEN_CRT.Add(CRT1)
NS_BODIES.Activate()
NS_BODIES.Generate()

NS_RESP_VERTEX = NS_GRP.AddNamedSelection()
NS_RESP_VERTEX.Name="NS_RESP_VERTEX"
NS_RESP_VERTEX.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_RESP_VERTEX.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.GeoVertex
CRT1.Criterion=SelectionCriterionType.LocationX
CRT1.Operator=SelectionOperatorType.Equal
CRT1.Value = Quantity('96.3 [mm]')
GEN_CRT.Add(CRT1)
NS_RESP_VERTEX.Activate()
NS_RESP_VERTEX.Generate()

# Add and define premeshed cyclic region
SYMM = Model.AddSymmetry()
SYMMETRY_REGION = SYMM.AddPreMeshedCyclicRegion()
SYMMETRY_REGION.LowBoundaryLocation=NS_LOW
SYMMETRY_REGION.HighBoundaryLocation=NS_HIGH
SYMMETRY_REGION.CoordinateSystem=LCS1
SYMMETRY_REGION.NumberOfSectors = 13

# Solve first standalone Modal analysis
MODAL01 = Model.Analyses[0]
ANA_SETTING_MODAL01 = Model.Analyses[0].AnalysisSettings
SOLN_MODAL01 = Model.Analyses[0].Solution

ANA_SETTING_MODAL01.MaximumModesToFind = 2
ANA_SETTING_MODAL01.HarmonicIndexRange=CyclicHarmonicIndex.Manual
ANA_SETTING_MODAL01.MaximumHarmonicIndex = 6

TOT_DEF_MODAL01 = SOLN_MODAL01.AddTotalDeformation()

SOLN_MODAL01.Solve(1)

H0_FRQ1_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][0]
H0_FRQ2_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][1]
H1_FRQ1_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][2]
H1_FRQ2_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][3]
H2_FRQ1_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][4]
H2_FRQ2_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][5]
H3_FRQ1_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][6]
H3_FRQ2_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][7]
H4_FRQ1_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][8]
H4_FRQ2_MODAL01 = TOT_DEF_MODAL01.TabularData["Frequency"][9]

# Setup linear Static Structural analysis
STAT_STRUC01 = Model.Analyses[1]
ANA_SETTING_STAT_STRUC01 = Model.Analyses[1].AnalysisSettings
SOLN_STAT_STRUC01 = Model.Analyses[1].Solution

PRES_STAT_STRUC01 = STAT_STRUC01.AddPressure()
PRES_STAT_STRUC01.Location = NS_PRES
PRES_STAT_STRUC01.Magnitude.Output.DiscreteValues = [Quantity('20 [MPa]')]

ROT_VEL_STAT_STRUC01 = STAT_STRUC01.AddRotationalVelocity()
ROT_VEL_STAT_STRUC01.DefineBy=LoadDefineBy.Components
ROT_VEL_STAT_STRUC01.CoordinateSystem=LCS1
ROT_VEL_STAT_STRUC01.ZComponent.Output.DiscreteValues = [Quantity("3000 [rad sec^-1]")]

THERM_COND_STRUC01 = STAT_STRUC01.AddThermalCondition()
THERM_COND_STRUC01.Location = NS_BODIES
THERM_COND_STRUC01.Magnitude.Output.DiscreteValues = [Quantity('50 [C]')]

# Solve prestress modal analysis
MODAL02 = Model.Analyses[2]
ANA_SETTING_MODAL02 = Model.Analyses[2].AnalysisSettings
SOLN_MODAL02 = Model.Analyses[2].Solution

ANA_SETTING_MODAL02.MaximumModesToFind = 2
ANA_SETTING_MODAL02.HarmonicIndexRange=CyclicHarmonicIndex.Manual
ANA_SETTING_MODAL02.MaximumHarmonicIndex = 6

TOT_DEF_MODAL02 = SOLN_MODAL02.AddTotalDeformation()

SOLN_MODAL02.Solve(1)

H0_FRQ1_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][0]
H0_FRQ2_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][1]
H1_FRQ1_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][2]
H1_FRQ2_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][3]
H2_FRQ1_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][4]
H2_FRQ2_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][5]
H3_FRQ1_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][6]
H3_FRQ2_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][7]
H4_FRQ1_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][8]
H4_FRQ2_MODAL02 = TOT_DEF_MODAL02.TabularData["Frequency"][9]

# Setup non-linear Static Structural analysis
STAT_STRUC02 = Model.Analyses[3]
ANA_SETTING_STAT_STRUC02 = Model.Analyses[3].AnalysisSettings
SOLN_STAT_STRUC02 = Model.Analyses[3].Solution

ANA_SETTING_STAT_STRUC02.LargeDeflection = True

PRES_STAT_STRUC02 = STAT_STRUC02.AddPressure()
PRES_STAT_STRUC02.Location = NS_PRES
PRES_STAT_STRUC02.Magnitude.Output.DiscreteValues = [Quantity('20 [MPa]')]

ROT_VEL_STAT_STRUC02 = STAT_STRUC02.AddRotationalVelocity()
ROT_VEL_STAT_STRUC02.DefineBy=LoadDefineBy.Components
ROT_VEL_STAT_STRUC02.CoordinateSystem=LCS1
ROT_VEL_STAT_STRUC02.ZComponent.Output.DiscreteValues = [Quantity("6000 [rad sec^-1]")]

THERM_COND_STRUC02 = STAT_STRUC02.AddThermalCondition()
THERM_COND_STRUC02.Location = NS_BODIES
THERM_COND_STRUC02.Magnitude.Output.DiscreteValues = [Quantity('50 [C]')]

# Solve Modal with prestress from non linear Static analysis
MODAL03 = Model.Analyses[4]
ANA_SETTING_MODAL03 = Model.Analyses[4].AnalysisSettings
SOLN_MODAL03 = Model.Analyses[4].Solution

ANA_SETTING_MODAL03.MaximumModesToFind = 2
ANA_SETTING_MODAL03.HarmonicIndexRange=CyclicHarmonicIndex.Manual
ANA_SETTING_MODAL03.MaximumHarmonicIndex = 6

TOT_DEF_MODAL03 = SOLN_MODAL03.AddTotalDeformation()

SOLN_MODAL03.Solve(1)

H0_FRQ1_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][0]
H0_FRQ2_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][1]
H1_FRQ1_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][2]
H1_FRQ2_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][3]
H2_FRQ1_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][4]
H2_FRQ2_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][5]
H3_FRQ1_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][6]
H3_FRQ2_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][7]
H4_FRQ1_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][8]
H4_FRQ2_MODAL03 = TOT_DEF_MODAL03.TabularData["Frequency"][9]

# Setup standalone FULL Harmonic analysis
HARM_RESP01 = Model.Analyses[5]
ANA_SETTING_HARM_RESP01 = Model.Analyses[5].AnalysisSettings
SOLN_HARM_RESP01 = Model.Analyses[5].Solution

ANA_SETTING_HARM_RESP01.RangeMinimum = Quantity('1200 [Hz]')
ANA_SETTING_HARM_RESP01.RangeMaximum = Quantity('5500 [Hz]')
ANA_SETTING_HARM_RESP01.SolutionIntervals = 20

ANA_SETTING_HARM_RESP01.SolutionMethod = HarmonicMethod.Full

ANA_SETTING_HARM_RESP01.StructuralDampingCoefficient = 0.02

PRES_HARM_RESP01 = HARM_RESP01.AddPressure()
PRES_HARM_RESP01.Location = NS_PRES
PRES_HARM_RESP01.Magnitude.Output.DiscreteValues = [Quantity('20 [MPa]')]

FRQ_RES_DEF_HARM_RESP01 = SOLN_HARM_RESP01.AddDeformationFrequencyResponse()
FRQ_RES_DEF_HARM_RESP01.Location = NS_RESP_VERTEX
FRQ_RES_DEF_HARM_RESP01.NormalOrientation = NormalOrientationType.YAxis

SOLN_HARM_RESP01.Activate()
TOT_DEF4_1=SOLN_HARM_RESP01.AddTotalDeformation()
TOT_DEF4_1.Frequency = Quantity(3000, "Hz")
TOT_DEF4_1.Amplitude=True
TOT_DEF4_1.Name = "Total Deformation"
TOT_DEF4_1.CreateParameter("Maximum")

SOLN_HARM_RESP01.Activate()
TOT_DEF4_2=SOLN_HARM_RESP01.AddTotalDeformation()
TOT_DEF4_2.Frequency = Quantity(2500, "Hz")
TOT_DEF4_2.Amplitude=True
TOT_DEF4_2.Name = "Total Deformation 2"
TOT_DEF4_2.CreateParameter("Maximum")

SOLN_HARM_RESP01.Solve(1)

TOT_DEF4_1.Activate()
TOT_DEF4_2.Activate()

# Set isometric view and zoom to fit
cam = Graphics.Camera
cam.SetSpecificViewOrientation(ViewOrientationType.Iso)
cam.SetFit()

mechdir = HARM_RESP01.Children[1].SolverFilesDirectory
export_path = os.path.join(mechdir, "deformation.png")
TOT_DEF4_1.Activate()
Graphics.ExportImage(export_path, GraphicsImageExportFormat.PNG)

results = { "Total Deformation": str(TOT_DEF4_1.Maximum), 
            "Total Deformation 2": str(TOT_DEF4_2.Maximum)}
json.dumps(results)