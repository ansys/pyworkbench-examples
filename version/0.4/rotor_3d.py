""" .. _ref_example_03_td_014:

Rotordynamics of a shaft assembly based on a representative model of Nelson-Vaugh rotor
---------------------------------------------------------------------------------------

UNIT System: NMM TON and RPM

Coverage:
Modal analyses of the 3D solid model with and without gyroscopic 
effects are solved.
Campbell diagram analyses are performed for the 3D solid model.
Unbalance response analyses are solved for the 3D solid model.

Validation:
Frequency response and total deformation results are compared 
between the general axisymmetric model and 3D solid model.

"""

import json
import os
import os.path
import string

from Ansys.ACT.Automation import Mechanical

###################################################################################
# Configure graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ExtAPI.Graphics.Camera.SetSpecificViewOrientation(
    Ansys.Mechanical.DataModel.Enums.ViewOrientationType.Iso
)
ExtAPI.Graphics.Camera.SetFit()
image_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = (
    Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType.EnhancedResolution
)
settings_720p.Background = Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType.White
settings_720p.Width = 1280
#settings_720p.Capture = Ansys.Mechanical.DataModel.Enums.GraphicsCaptureType.ImageOnly
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# Set NMM_TON Unit System
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMMton
ExtAPI.Application.ActiveAngularVelocityUnit=AngularVelocityUnitType.RPM

# Define variables
GEOM = ExtAPI.DataModel.Project.Model.Geometry
MSH = ExtAPI.DataModel.Project.Model.Mesh
NS_GRP = ExtAPI.DataModel.Project.Model.NamedSelections
CONN_GRP = ExtAPI.DataModel.Project.Model.Connections
MODAL1 = Model.Analyses[0]
MODAL1.Name ="Modal omega=0"

# Define variables for named selection objects
NS_GRP.Activate()
NS_PointMass_RemotePoint = [i for i in NS_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if i.Name == 'NS_PointMass_RemotePoint'][0]
NS_RemotePoint_Bearing1 = [i for i in NS_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if i.Name == 'NS_RemotePoint_Bearing1'][0]
NS_RemotePoint_Bearing2 = [i for i in NS_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if i.Name == 'NS_RemotePoint_Bearing2'][0]
NS_PointMass_RemotePoint2 = [i for i in NS_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if i.Name == 'NS_PointMass_RemotePoint2'][0]
NS_All_Bodies = [i for i in NS_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True) if i.Name == 'NS_All_Bodies'][0]

# Mesh the model
MSH.Activate()
MSH.Resolution=4
MSH.TransitionOption=1

MSH_SIZING1 = MSH.AddSizing()
MSH_SIZING1.Activate()
MSH_SIZING1.Location = NS_All_Bodies
MSH_SIZING1.ElementSize=Quantity("7.5 [mm]")

MSH_METHOD = MSH.AddAutomaticMethod()
MSH_METHOD.Location=NS_All_Bodies
MSH_METHOD.Method=MethodType.AllTriAllTet

MSH.Activate()
MSH.GenerateMesh()

# Create new mesh based named selection objects
NS_Freq_resp_1= Model.AddNamedSelection()
NS_Freq_resp_1.Activate()
NS_Freq_resp_1.Name = "NS_Freq_resp_1"
NS_Freq_resp_1.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_Freq_resp_1.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.MeshNode
CRT1.Criterion=SelectionCriterionType.LocationX
CRT1.Operator=SelectionOperatorType.Equal
CRT1.Operator=SelectionOperatorType.RangeInclude
CRT1.LowerBound=Quantity('88.5 [mm]')
CRT1.UpperBound=Quantity('89.5 [mm]')
GEN_CRT.Add(CRT1)

GEN_CRT = NS_Freq_resp_1.GenerationCriteria
CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active=True
CRT2.Action=SelectionActionType.Filter
CRT2.EntityType=SelectionType.MeshNode
CRT2.Criterion=SelectionCriterionType.LocationY
CRT2.Operator=SelectionOperatorType.Equal
CRT2.Value=Quantity("20.3 [mm]")
GEN_CRT.Add(CRT2)

NS_Freq_resp_1.Activate()
NS_Freq_resp_1.Generate()

NS_Freq_resp_2= Model.AddNamedSelection()
NS_Freq_resp_2.Activate()
NS_Freq_resp_2.Name = "NS_Freq_resp_2"
NS_Freq_resp_2.ScopingMethod=GeometryDefineByType.Worksheet

GEN_CRT = NS_Freq_resp_2.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active=True
CRT1.Action=SelectionActionType.Add
CRT1.EntityType=SelectionType.MeshNode
CRT1.Criterion=SelectionCriterionType.LocationX
CRT1.Operator=SelectionOperatorType.RangeInclude
CRT1.LowerBound=Quantity('249.5 [mm]')
CRT1.UpperBound=Quantity('250.5 [mm]')
GEN_CRT.Add(CRT1)

GEN_CRT = NS_Freq_resp_2.GenerationCriteria
CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active=True
CRT2.Action=SelectionActionType.Filter
CRT2.EntityType=SelectionType.MeshNode
CRT2.Criterion=SelectionCriterionType.LocationY
CRT2.Operator=SelectionOperatorType.Equal
CRT2.Value=Quantity("15.2 [mm]")
GEN_CRT.Add(CRT2)

NS_Freq_resp_2.Activate()
NS_Freq_resp_2.Generate()

NS_Freq_resp_2.Activate()
NS_Freq_resp_2.Generate()

# Define Remote Points
Model.Activate()
RMPT1 = Model.AddRemotePoint()
RMPT1.Location = NS_PointMass_RemotePoint
RMPT1.Name = "PointMass_RemotePoint"

Model.Activate()
RMPT2 = Model.AddRemotePoint()
RMPT2.Location = NS_RemotePoint_Bearing1
RMPT2.Name = "RemotePoint_Bearing1"

Model.Activate()
RMPT3 = Model.AddRemotePoint()
RMPT3.Location = NS_RemotePoint_Bearing2
RMPT3.Name = "RemotePoint_Bearing2"
RMPT3.XCoordinate = Quantity("287 [mm]")
RMPT3.YCoordinate = Quantity("0 [mm]")

Model.Activate()
RMPT4 = Model.AddRemotePoint()
RMPT4.ScopingMethod=GeometryDefineByType.FreeStanding
RMPT4.XCoordinate = RMPT2.XCoordinate
RMPT4.YCoordinate = Quantity("30 [mm]")
RMPT4.Name = "RemotePoint_FreeStanding1"

Model.Activate()
RMPT5 = Model.AddRemotePoint()
RMPT5.ScopingMethod=GeometryDefineByType.FreeStanding
RMPT5.XCoordinate = Quantity("287 [mm]")
RMPT5.YCoordinate = Quantity("30 [mm]")
RMPT5.Name = "RemotePoint_FreeStanding2"

Model.Activate()
RMPT6 = Model.AddRemotePoint()
RMPT6.Location = NS_PointMass_RemotePoint2
RMPT6.Name = "PointMass_RemotePoint2"
RMPT6.YCoordinate = Quantity("0.5 [mm]")

# Add bearing supports under connections folder
CONN_GRP.Activate()
BEARNG01=CONN_GRP.AddBearing()
BEARNG01.ConnectionType=ConnectionScopingType.BodyToBody
BEARNG01.MobileLocation=RMPT2
BEARNG01.ReferenceLocation=RMPT4
BEARNG01.ReferenceRotationPlane=RotationPlane.YZ
BEARNG01.StiffnessK11.Output.SetDiscreteValue(0, Quantity("35030 [N/mm]"))
BEARNG01.StiffnessK22.Output.SetDiscreteValue(0, Quantity("35030 [N/mm]"))
BEARNG01.StiffnessK12.Output.SetDiscreteValue(0, Quantity("-8756 [N/mm]"))
BEARNG01.StiffnessK21.Output.SetDiscreteValue(0, Quantity("-8756 [N/mm]"))

CONN_GRP.Activate()
BEARNG01=CONN_GRP.AddBearing()
BEARNG01.ConnectionType=ConnectionScopingType.BodyToBody
BEARNG01.MobileLocation=RMPT3
BEARNG01.ReferenceLocation=RMPT5
BEARNG01.ReferenceRotationPlane=RotationPlane.YZ
BEARNG01.StiffnessK11.Output.SetDiscreteValue(0, Quantity("35030 [N/mm]"))
BEARNG01.StiffnessK22.Output.SetDiscreteValue(0, Quantity("35030 [N/mm]"))
BEARNG01.StiffnessK12.Output.SetDiscreteValue(0, Quantity("-8756 [N/mm]"))
BEARNG01.StiffnessK21.Output.SetDiscreteValue(0, Quantity("-8756 [N/mm]"))

# Add Point Mass
GEOM.Activate()
PT_MASS = GEOM.AddPointMass()
PT_MASS.Location = RMPT1
PT_MASS.Mass = Quantity('0.001401 [tonne]')
PT_MASS.MassMomentOfInertiaX=Quantity("2 [tonne mm mm]")
PT_MASS.MassMomentOfInertiaY=Quantity("13.6 [tonne mm mm]")
PT_MASS.MassMomentOfInertiaZ=Quantity("13.6 [tonne mm mm]")

# Set Number of Processors to 6 using DANSYS
#testval2 = MODAL1.SolveConfiguration.SolveProcessSettings.MaxNumberOfCores
#MODAL1.SolveConfiguration.SolveProcessSettings.MaxNumberOfCores=6

# The natural frequencies of the 3-D solid model without rotation
ANA_SETTINGS_MODAL1 = MODAL1.AnalysisSettings
ANA_SETTINGS_MODAL1.Activate()
ANA_SETTINGS_MODAL1.MaximumModesToFind=12

MODAL1.Activate()
REM_DISP = MODAL1.AddRemoteDisplacement()
REM_DISP.Location = RMPT4
REM_DISP.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP2 = MODAL1.AddRemoteDisplacement()
REM_DISP2.Location = RMPT5
REM_DISP2.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP3 = MODAL1.AddRemoteDisplacement()
REM_DISP3.Location = RMPT2
REM_DISP3.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP3.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP4 = MODAL1.AddRemoteDisplacement()
REM_DISP4.Location = RMPT3
REM_DISP4.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP4.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

SOLN1 = MODAL1.Solution
SOLN1.Activate()

SOLN1.Activate()
TOT_DEF1=SOLN1.AddTotalDeformation()
TOT_DEF1.Mode=1
TOT_DEF1.CreateParameter("ReportedFrequency")
TOT_DEF2=SOLN1.AddTotalDeformation()
TOT_DEF2.Mode=2
TOT_DEF2.CreateParameter("ReportedFrequency")
TOT_DEF3=SOLN1.AddTotalDeformation()
TOT_DEF3.Mode=3
TOT_DEF3.CreateParameter("ReportedFrequency")
TOT_DEF4=SOLN1.AddTotalDeformation()
TOT_DEF4.Mode=4
TOT_DEF4.CreateParameter("ReportedFrequency")
TOT_DEF5=SOLN1.AddTotalDeformation()
TOT_DEF5.Mode=5
TOT_DEF5.CreateParameter("ReportedFrequency")
TOT_DEF6=SOLN1.AddTotalDeformation()
TOT_DEF6.Mode=6
TOT_DEF6.CreateParameter("ReportedFrequency")
TOT_DEF7=SOLN1.AddTotalDeformation()
TOT_DEF7.Mode=7
TOT_DEF7.CreateParameter("ReportedFrequency")
TOT_DEF8=SOLN1.AddTotalDeformation()
TOT_DEF8.Mode=8
TOT_DEF8.CreateParameter("ReportedFrequency")
TOT_DEF9=SOLN1.AddTotalDeformation()
TOT_DEF9.Mode=9
TOT_DEF9.CreateParameter("ReportedFrequency")
TOT_DEF10=SOLN1.AddTotalDeformation()
TOT_DEF10.Mode=10
TOT_DEF10.CreateParameter("ReportedFrequency")
TOT_DEF11=SOLN1.AddTotalDeformation()
TOT_DEF11.Mode=11
TOT_DEF11.CreateParameter("ReportedFrequency")
TOT_DEF12=SOLN1.AddTotalDeformation()
TOT_DEF12.Mode=12
TOT_DEF12.CreateParameter("ReportedFrequency")

SOLN1.Activate()
SOLN1.ClearGeneratedData()
SOLN1.Solve(True)
	
FREQ_1_MODAL1 = SOLN1.TabularData.Values[1][0]
FREQ_2_MODAL1 = SOLN1.TabularData.Values[1][1]
FREQ_3_MODAL1 = SOLN1.TabularData.Values[1][2]
FREQ_4_MODAL1 = SOLN1.TabularData.Values[1][3]
FREQ_5_MODAL1 = SOLN1.TabularData.Values[1][4]
FREQ_6_MODAL1 = SOLN1.TabularData.Values[1][5]
FREQ_7_MODAL1 = SOLN1.TabularData.Values[1][6]
FREQ_8_MODAL1 = SOLN1.TabularData.Values[1][7]
FREQ_9_MODAL1 = SOLN1.TabularData.Values[1][8]
FREQ_10_MODAL1 = SOLN1.TabularData.Values[1][9]
FREQ_11_MODAL1 = SOLN1.TabularData.Values[1][10]
FREQ_12_MODAL1 = SOLN1.TabularData.Values[1][11]

# The natural frequencies of the 3-D solid model with rotation of 50000 rpm
MODAL2 = Model.Analyses[1]
MODAL2.Name = "Modal omega"

ANA_SETTINGS_MODAL2 = MODAL2.AnalysisSettings
ANA_SETTINGS_MODAL2.Activate()
ANA_SETTINGS_MODAL2.MaximumModesToFind=12
ANA_SETTINGS_MODAL2.Damped=True
ANA_SETTINGS_MODAL2.SolverType=SolverType.ReducedDamped
ANA_SETTINGS_MODAL2.CoriolisEffect=True

MODAL2.Activate()
ROT_VEL01 = MODAL2.AddRotationalVelocity()
ROT_VEL01.DefineBy=LoadDefineBy.Components
ROT_VEL01.XComponent.Output.DiscreteValues = [Quantity("50000 [rev min^-1]")]

MODAL2.Activate()
REM_DISP = MODAL2.AddRemoteDisplacement()
REM_DISP.Location = RMPT4
REM_DISP.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP2 = MODAL2.AddRemoteDisplacement()
REM_DISP2.Location = RMPT5
REM_DISP2.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP3 = MODAL2.AddRemoteDisplacement()
REM_DISP3.Location = RMPT2
REM_DISP3.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP3.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP4 = MODAL2.AddRemoteDisplacement()
REM_DISP4.Location = RMPT3
REM_DISP4.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP4.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

SOLN2 = MODAL2.Solution
SOLN2.Activate()

SOLN2.Activate()
TOT_DEF2_1=SOLN2.AddTotalDeformation()
TOT_DEF2_1.Mode=1
TOT_DEF2_1.CreateParameter("ReportedFrequency")
TOT_DEF2_2=SOLN2.AddTotalDeformation()
TOT_DEF2_2.Mode=2
TOT_DEF2_2.CreateParameter("ReportedFrequency")
TOT_DEF2_3=SOLN2.AddTotalDeformation()
TOT_DEF2_3.Mode=3
TOT_DEF2_3.CreateParameter("ReportedFrequency")
TOT_DEF2_4=SOLN2.AddTotalDeformation()
TOT_DEF2_4.Mode=4
TOT_DEF2_4.CreateParameter("ReportedFrequency")
TOT_DEF2_5=SOLN2.AddTotalDeformation()
TOT_DEF2_5.Mode=5
TOT_DEF2_5.CreateParameter("ReportedFrequency")
TOT_DEF2_6=SOLN2.AddTotalDeformation()
TOT_DEF2_6.Mode=6
TOT_DEF2_6.CreateParameter("ReportedFrequency")
TOT_DEF2_7=SOLN2.AddTotalDeformation()
TOT_DEF2_7.Mode=7
TOT_DEF2_7.CreateParameter("ReportedFrequency")
TOT_DEF2_8=SOLN2.AddTotalDeformation()
TOT_DEF2_8.Mode=8
TOT_DEF2_8.CreateParameter("ReportedFrequency")
TOT_DEF2_9=SOLN2.AddTotalDeformation()
TOT_DEF2_9.Mode=9
TOT_DEF2_9.CreateParameter("ReportedFrequency")
TOT_DEF2_10=SOLN2.AddTotalDeformation()
TOT_DEF2_10.Mode=10
TOT_DEF2_10.CreateParameter("ReportedFrequency")
TOT_DEF2_11=SOLN2.AddTotalDeformation()
TOT_DEF2_11.Mode=11
TOT_DEF2_11.CreateParameter("ReportedFrequency")
TOT_DEF2_12=SOLN2.AddTotalDeformation()
TOT_DEF2_12.Mode=12
TOT_DEF2_12.CreateParameter("ReportedFrequency")

SOLN2.Activate()
SOLN2.ClearGeneratedData()
SOLN2.Solve(True)
	
FREQ_1_MODAL2 = SOLN2.TabularData.Values[1][0]
FREQ_2_MODAL2 = SOLN2.TabularData.Values[1][1]
FREQ_3_MODAL2 = SOLN2.TabularData.Values[1][2]
FREQ_4_MODAL2 = SOLN2.TabularData.Values[1][3]
FREQ_5_MODAL2 = SOLN2.TabularData.Values[1][4]
FREQ_6_MODAL2 = SOLN2.TabularData.Values[1][5]
FREQ_7_MODAL2 = SOLN2.TabularData.Values[1][6]
FREQ_8_MODAL2 = SOLN2.TabularData.Values[1][7]
FREQ_9_MODAL2 = SOLN2.TabularData.Values[1][8]
FREQ_10_MODAL2 = SOLN2.TabularData.Values[1][9]
FREQ_11_MODAL2 = SOLN2.TabularData.Values[1][10]
FREQ_12_MODAL2 = SOLN2.TabularData.Values[1][11]

# Campbell diagram analysis of the 3-D solid model
MODAL3 = Model.Analyses[2]
MODAL3.Name = "Modal Campbell"

ANA_SETTINGS_MODAL3 = MODAL3.AnalysisSettings
ANA_SETTINGS_MODAL3.Activate()
ANA_SETTINGS_MODAL3.MaximumModesToFind=9
ANA_SETTINGS_MODAL3.Damped=True
ANA_SETTINGS_MODAL3.SolverType=SolverType.ReducedDamped
ANA_SETTINGS_MODAL3.CoriolisEffect=True
ANA_SETTINGS_MODAL3.CampbellDiagram=True
ANA_SETTINGS_MODAL3.ModalNumberOfPoints=3

MODAL3.Activate()
ROT_VEL02 = MODAL3.AddRotationalVelocity()
ROT_VEL02.DefineBy=LoadDefineBy.Components
ROT_VEL02.XComponent.Output.DiscreteValues = [Quantity("1e-14 [rev min^-1]"), Quantity("50000 [rev min^-1]"), Quantity("1e5 [rev min^-1]")]

MODAL3.Activate()
REM_DISP = MODAL3.AddRemoteDisplacement()
REM_DISP.Location = RMPT4
REM_DISP.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP2 = MODAL3.AddRemoteDisplacement()
REM_DISP2.Location = RMPT5
REM_DISP2.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP3 = MODAL3.AddRemoteDisplacement()
REM_DISP3.Location = RMPT2
REM_DISP3.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP3.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP4 = MODAL3.AddRemoteDisplacement()
REM_DISP4.Location = RMPT3
REM_DISP4.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP4.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

SOLN3 = MODAL3.Solution

SOLN3.Activate()
TOT_DEF3_1=SOLN3.AddTotalDeformation()
TOT_DEF3_1.Mode=19
TOT_DEF3_1.CreateParameter("ReportedFrequency")
TOT_DEF3_2=SOLN3.AddTotalDeformation()
TOT_DEF3_2.Mode=20
TOT_DEF3_2.CreateParameter("ReportedFrequency")
TOT_DEF3_3=SOLN3.AddTotalDeformation()
TOT_DEF3_3.Mode=21
TOT_DEF3_3.CreateParameter("ReportedFrequency")
TOT_DEF3_4=SOLN3.AddTotalDeformation()
TOT_DEF3_4.Mode=22
TOT_DEF3_4.CreateParameter("ReportedFrequency")
TOT_DEF3_5=SOLN3.AddTotalDeformation()
TOT_DEF3_5.Mode=23
TOT_DEF3_5.CreateParameter("ReportedFrequency")
TOT_DEF3_6=SOLN3.AddTotalDeformation()
TOT_DEF3_6.Mode=24
TOT_DEF3_6.CreateParameter("ReportedFrequency")
TOT_DEF3_7=SOLN3.AddTotalDeformation()
TOT_DEF3_7.Mode=25
TOT_DEF3_7.CreateParameter("ReportedFrequency")
TOT_DEF3_8=SOLN3.AddTotalDeformation()
TOT_DEF3_8.Mode=26
TOT_DEF3_8.CreateParameter("ReportedFrequency")
TOT_DEF3_9=SOLN3.AddTotalDeformation()
TOT_DEF3_9.Mode=27
TOT_DEF3_9.CreateParameter("ReportedFrequency")

SOLN3.Activate()
CMPBL_DIAG = SOLN3.AddCampbellDiagram()

SOLN3.Activate()
SOLN3.Solve(True)

mechdir = ExtAPI.DataModel.AnalysisList[2].WorkingDir
export_path = os.path.join(mechdir, "tot_deform_3D.png")
Tree.Activate([TOT_DEF3_1])
ExtAPI.Graphics.ViewOptions.ResultPreference.ExtraModelDisplay=Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ExtraModelDisplay.NoWireframe
ExtAPI.Graphics.ExportImage(export_path, image_export_format, settings_720p)
	
FREQ_1_MODAL3 = SOLN3.TabularData.Values[3][18]
FREQ_2_MODAL3 = SOLN3.TabularData.Values[3][19]
FREQ_3_MODAL3 = SOLN3.TabularData.Values[3][20]
FREQ_4_MODAL3 = SOLN3.TabularData.Values[3][21]
FREQ_5_MODAL3 = SOLN3.TabularData.Values[3][22]
FREQ_6_MODAL3 = SOLN3.TabularData.Values[3][23]
FREQ_7_MODAL3 = SOLN3.TabularData.Values[3][24]
FREQ_8_MODAL3 = SOLN3.TabularData.Values[3][25]
FREQ_9_MODAL3 = SOLN3.TabularData.Values[3][26]

CMPBL_DIAG.Activate()

# Unbalance Response of the 3-D solid model
HARM_RESP = Model.Analyses[3]
HARM_RESP.Name = "Unbalance Response"

ANA_SETTINGS_HARM_RESP = HARM_RESP.AnalysisSettings
ANA_SETTINGS_HARM_RESP.Activate()
ANA_SETTINGS_HARM_RESP.RangeMinimum = Quantity("0 [Hz]")
ANA_SETTINGS_HARM_RESP.RangeMaximum = Quantity("1666.7 [Hz]")
ANA_SETTINGS_HARM_RESP.SolutionIntervals=200
ANA_SETTINGS_HARM_RESP.SolutionMethod=HarmonicMethod.Full
ANA_SETTINGS_HARM_RESP.CoriolisEffect=True
ANA_SETTINGS_HARM_RESP.StructuralDampingCoefficient=0.02

HARM_RESP.Activate()
ROT_FRC = HARM_RESP.AddRotatingForce()
ROT_FRC.Axis = Ansys.Mechanical.Math.BoundVector(Point((89.01,0,0),'mm'), Vector3D(1,0,0))
ROT_FRC.DefineBy=GeometryDefineByType.RemotePoint
ROT_FRC.RemotePointSelection=RMPT6
ROT_FRC.Mass=Quantity('0.0038 [tonne]')
ROT_FRC.HitPointSelection=False
ROT_FRC.HitPointRemotePointSelection=RMPT1

HARM_RESP.Activate()
REM_DISP = HARM_RESP.AddRemoteDisplacement()
REM_DISP.Location = RMPT4
REM_DISP.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP2 = HARM_RESP.AddRemoteDisplacement()
REM_DISP2.Location = RMPT5
REM_DISP2.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.YComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.ZComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP2.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationY.Output.DiscreteValues=[Quantity("0 [deg]")]
REM_DISP2.RotationZ.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP3 = HARM_RESP.AddRemoteDisplacement()
REM_DISP3.Location = RMPT2
REM_DISP3.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP3.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

REM_DISP4 = HARM_RESP.AddRemoteDisplacement()
REM_DISP4.Location = RMPT3
REM_DISP4.XComponent.Output.DiscreteValues=[Quantity("0 [m]")]
REM_DISP4.RotationX.Output.DiscreteValues=[Quantity("0 [deg]")]

SOLN4 = HARM_RESP.Solution
SOLN4.Activate()

SOLN4.Activate()
TOT_DEF4_1=SOLN4.AddTotalDeformation()
TOT_DEF4_1.Location = NS_Freq_resp_1
TOT_DEF4_1.Amplitude=True
TOT_DEF4_1.Name = "Total Deformation1@1666.7Hz"
TOT_DEF4_1.CreateParameter("Maximum")

SOLN4.Activate()
TOT_DEF4_2=SOLN4.AddTotalDeformation()
TOT_DEF4_2.Location = NS_Freq_resp_2
TOT_DEF4_2.Amplitude=True
TOT_DEF4_2.Name = "Total Deformation2@1666.7Hz"
TOT_DEF4_2.CreateParameter("Maximum")

FRQ_RESP_DEF1=SOLN4.AddDeformationFrequencyResponse()
FRQ_RESP_DEF1.Location=NS_Freq_resp_1
FRQ_RESP_DEF1.NormalOrientation =NormalOrientationType.YAxis
FRQ_RESP_DEF1.CreateParameter("FrequencyAtMaximumAmplitude")

FRQ_RESP_DEF2=SOLN4.AddDeformationFrequencyResponse()
FRQ_RESP_DEF2.Location=NS_Freq_resp_1
FRQ_RESP_DEF2.NormalOrientation =NormalOrientationType.ZAxis
FRQ_RESP_DEF2.CreateParameter("FrequencyAtMaximumAmplitude")

FRQ_RESP_DEF3=SOLN4.AddDeformationFrequencyResponse()
FRQ_RESP_DEF3.Location=NS_Freq_resp_2
FRQ_RESP_DEF3.NormalOrientation =NormalOrientationType.YAxis
FRQ_RESP_DEF3.CreateParameter("FrequencyAtMaximumAmplitude")

FRQ_RESP_DEF4=SOLN4.AddDeformationFrequencyResponse()
FRQ_RESP_DEF4.Location=NS_Freq_resp_2
FRQ_RESP_DEF4.NormalOrientation =NormalOrientationType.ZAxis
FRQ_RESP_DEF4.CreateParameter("FrequencyAtMaximumAmplitude")

SOLN4.Activate()
SOLN4.Solve(True)

TOT_DEF4_1.Activate()
TOT_DEF4_2.Activate()

# Reset Number of Processors
# MODAL1.SolveConfiguration.SolveProcessSettings.MaxNumberOfCores=testval2

results = { "Total Deformation": str(TOT_DEF4_1.Maximum), 
            "Total Deformation 2": str(TOT_DEF4_2.Maximum)}
json.dumps(results)