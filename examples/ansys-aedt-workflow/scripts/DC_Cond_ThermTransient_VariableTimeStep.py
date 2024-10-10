# Author: Davide Frigerio (ANSYS IT) - based on original script by Tomoya Horiuchi and Paul Larsen - encoding: utf-8
# Reviewed by Tiziana Bertoncelli (Ansys Germany) on July 13, adapted to 2023R1, tested for 2023R2 on August 02, adapt for DC Conduction 2023R2 on November 23, 2023
# Added Variable Time-Step in December 2023

# Varistor Workflow (2 way coupling Maxwell - Mechanical Thermal Transient):
# Pre-requisites:
# 1.	Maxwell: setup in the chosen solver (DC conduction) with current excitation defined by means of a design variable
# 2.	Maxwell project coupled to a Mechanical Thermal Transient in Workbench
# 3.	Current input vs. time (current pulses) information is contained a *csv file with a given formatting (strict)
# Workflow Steps:
# 1.	Read the pulse data from*. csv file
# 2.	Define time steps transient setup according to time points defined in the *.csv file
# 3.	For each time point from the *.csv file:
#       •	Update the value of current in the Maxwell design
#       •	Run Maxwell Design
#       •	Pass power Loss Density to Mechanical 
#       •	Run a time step in Mechanical
# 4.	For each time step in Mechanical transient, the temperature from the precious time step must be preserved and the fields saved (restart)

# Definitions

import os
import time
import datetime
import shutil
import glob
import sys
import clr
import System
import math
import threading
import logging
import csv

from System.IO import File

class ProjectSetting:
	def __init__(self):
		self.PrjPath = ""
		self.PrjName = ""
		self.ThermSystemDir = ""
		self.UserDir = ""
		self.LogFileName = ""
		self.LogFileName_phy = ""

Setting=ProjectSetting()

threads = []

global Setting, stopped, progress

def RefreshReport(step):

	global Setting

	PrjFullName = GetProjectFile()
	Setting.PrjPath=os.path.dirname(PrjFullName)
	Setting.UserDir=Project.GetUserFilesDirectory()
	
	shutil.copyfile(step.Extension.InstallDir+'\\help\\report.html', Setting.UserDir+'\\report.html')
	report = step.UserInterface.GetComponent("Report")
	report.SetHtmlContent(Setting.UserDir+'\\report.html')
	report.Refresh()
    
def EmptyReset(step):
    pass

# Subroutines

def Init_Step(ThermCompSetup, StepEndTime, MinTimeStep, MaxTimeStep):
	global Setting
	fTempFile = open(os.path.join(Setting.UserDir, "temp.js"),"w")
	fTempFile.write('''
		var endTime =''' + str(StepEndTime) + ''';
		var minSubStep =''' + str(MinTimeStep) + ''';
		var maxSubStep =''' + str(MaxTimeStep) + ''';
		ds=DS;
		wb=WB;
		var model = DS.Tree.FirstActiveModel;
		var myenvironments = model.Environments;
		var myEnvTherm = myenvironments.Item(1);
		var myAnalysis = myEnvTherm.AnalysisSettings;
		myAnalysis.EndTime = endTime;
		myAnalysis.CleanupOptionalANSYSFiles=false;
		myAnalysis.UseAutoTimeStepping = 1;
		myAnalysis.TimeStepDefineby = 1;
		myAnalysis.InitialTimeStep = minSubStep;
		myAnalysis.MinimumTimeStep = minSubStep;
		myAnalysis.MaximumTimeStep = maxSubStep;
		var myExternalGroup = myEnvTherm.ExternalLoadGroups;
		var myExternalGroupItem = myExternalGroup.Item(1);
		var myExternalGroupChildren = myExternalGroupItem.Children;
		var myImportedTemperature = myExternalGroupChildren.Item(1);
		scriptcode.changeActiveObject(myImportedTemperature.ID);
		var heatGenObj = DS.Tree.FirstActiveObject;
		var myAnalysis = myEnvTherm.AnalysisSettings;
		heatGenObj.SequenceInfoCollAnalysisTimeByIndex(0) = endTime;
		var commandText=\"\";
		commandText+=\"thopt,full\\n\";
		commandText+=\"rescontrol,define,last,last\\n\";
		commandText+=\"save,file,db\\n\";
		var command = myEnvTherm.AddCommandEditor();
		command.Text = commandText;
		ds.Script.fillTree();
		''')
	fTempFile.close()
	s2 = os.path.join(Setting.UserDir, "temp.js").replace("\\","\\\\")
	ThermCompSetup.SendCommand(Command="WB.AppletList.Applet(\"DSApplet\").App.Script.doToolsRunMacro(\""+s2+"\")")

def ChangeStep(ThermCompSetup, StepEndTime, MinTimeStep, MaxTimeStep, counter,Nsubsteps):
	global Setting
	fTempFile = open(os.path.join(Setting.UserDir, "temp.js"),"w")
	fTempFile.write('''
		ds=DS;
		wb=WB;
		var endTime =''' + str(StepEndTime) + ''';
		var minSubStep =''' + str(MinTimeStep) + ''';
		var maxSubStep =''' + str(MaxTimeStep) + ''';
		var model = DS.Tree.FirstActiveModel;
		var myenvironments = model.Environments;
		var myEnvTherm = myenvironments.Item(1);
		var mysolution = myEnvTherm.AnswerSet;
		var myAnalysis = myEnvTherm.AnalysisSettings;
		myAnalysis.EndTime = endTime;
		myAnalysis.UseAutoTimeStepping = 1;
        myAnalysis.TimeStepDefineby = 1;
		myAnalysis.InitialTimeStep = minSubStep;
		myAnalysis.MinimumTimeStep = minSubStep;
		myAnalysis.MaximumTimeStep = maxSubStep;
		var userDir = "''' + Setting.PrjName + '''_files";
		var myExternalGroup = myEnvTherm.ExternalLoadGroups;
		var myExternalGroupItem = myExternalGroup.Item(1);
		var myExternalGroupChildren = myExternalGroupItem.Children;
		var myImportedTemperature = myExternalGroupChildren.Item(1);
		scriptcode.changeActiveObject(myImportedTemperature.ID);
		var heatGenObj = DS.Tree.FirstActiveObject;
		var myAnalysis = myEnvTherm.AnalysisSettings;
		heatGenObj.SequenceInfoCollAnalysisTimeByIndex(0) = endTime;
		var commandText=\"\";
		commandText+=\"fini\\n\";
		commandText+=\"/clear\\n\";
		commandText+=\"/copy,file,rdb,..\\\\..\\\\\";
		commandText+=userDir;
		commandText+=\"\\\\user_files,file,rdb\\n\";
		commandText+=\"/copy,file,LDHI,..\\\\..\\\\\";
		commandText+=userDir;
		commandText+=\"\\\\user_files,file,LDHI\\n\";
		commandText+=\"/copy,file,rth,..\\\\..\\\\\";
        commandText+=userDir;
		commandText+=\"\\\\user_files,file,rth\\n\";
        commandText+=\"/copy,file,r'''+ str(counter).zfill(3) +''',..\\\\..\\\\\";
		commandText+=userDir;
		commandText+=\"\\\\user_files,file,r'''+ str(counter).zfill(3) +'''\\n\";
		commandText+=userDir;
		commandText+=\"\\\\user_files,file,rth\\n\";
		commandText+=\"resume,file,rdb\\n\";
		commandText+=\"/solu\\n\";
		commandText+=\"antype,transient,rest\\n\";
		commandText+=\"rescontrol,define,last,last\\n\";
		commandText+=\"thopt,full\\n\";
        commandText+=\"nsubst,'''+str(Nsubsteps)+'''\\n\";        
		commandText+=\"time,\"+endTime.toString()+\"\\n\";
		commandText+=\"/input,loss,dat\\n\";
		commandText+=\"save\\n\";
		var command = myEnvTherm.AddCommandEditor();
		command.Text = commandText;
		ds.Script.fillTree();
		''')
	fTempFile.close()
	s2 = os.path.join(Setting.UserDir, "temp.js").replace("\\","\\\\")
	ThermCompSetup.SendCommand(Command="WB.AppletList.Applet(\"DSApplet\").App.Script.doToolsRunMacro(\""+s2+"\")")
  
def Remove_APDL_Command(ThermCompSetup):
	global Setting
	fTempFile = open(os.path.join(Setting.UserDir, "temp.js"),"w")
	fTempFile.write('''
		var EnvironmentObj = DS.Tree.FirstActiveBranch.Environment;
		var commandObjs = EnvironmentObj.CommandEditors
		try{\n
			var commandObj = commandObjs.Item(1);
			scriptcode.changeActiveObject(commandObj.ID);
			DS.Tree.DeleteObject(commandObj.ID);
		    }\n
		catch(e)\n
		    {\n
		    }\n
		''')
	fTempFile.close()
	s2 = os.path.join(Setting.UserDir, "temp.js").replace("\\","\\\\")
	ThermCompSetup.SendCommand(Command="WB.AppletList.Applet(\"DSApplet\").App.Script.doToolsRunMacro(\""+s2+"\")")

def CopyFiles(counter):
	global Setting
	string = str(counter).zfill(3)
	string_prev = str(counter-1).zfill(3)
	if File.Exists(Setting.UserDir+'\\file.rdb'):
		os.remove(Setting.UserDir+'\\file.rdb')
	if File.Exists(Setting.UserDir+'\\file.LDHI'):
		os.remove(Setting.UserDir+'\\file.LDHI')
	if File.Exists(Setting.UserDir+'\\file.rth'):
		os.remove(Setting.UserDir+'\\file.rth')
	if File.Exists(Setting.UserDir+'\\file.r'+string_prev):
		os.remove(Setting.UserDir+'\\file.r'+string_prev)

	shutil.copyfile(Setting.ThermSystemDir+'\\file.rdb', Setting.UserDir+'\\file.rdb')
	shutil.copyfile(Setting.ThermSystemDir+'\\file.LDHI', Setting.UserDir+'\\file.LDHI')
	shutil.copyfile(Setting.ThermSystemDir+'\\file.rth', Setting.UserDir+'\\file.rth')
	shutil.copyfile(Setting.ThermSystemDir+'\\file.r'+string, Setting.UserDir+'\\file.r'+string)
	
def ClearUserDir(counter):
	global Setting
	string_prev = str(counter-1).zfill(3)
	if File.Exists(Setting.UserDir+'\\file.rdb'):
		os.remove(Setting.UserDir+'\\file.rdb')
	if File.Exists(Setting.UserDir+'\\file.LDHI'):
		os.remove(Setting.UserDir+'\\file.LDHI')
	if File.Exists(Setting.UserDir+'\\file.rth'):
		os.remove(Setting.UserDir+'\\file.rth')
	if File.Exists(Setting.UserDir+'\\file.r'+string_prev):
		os.remove(Setting.UserDir+'\\file.r'+string_prev)
	if File.Exists(Setting.UserDir+'\\temp.js'):
		os.remove(Setting.UserDir+'\\temp.js')	

# Variables Initialization

mxwl_project_name = 'TVR14471_V'
mxwl_design_name  = 'Maxwell3DDesign1'
mxwl_design_var_name = 'I_pulse'

# read the CSV file path # write a wbjn file to read the csv file path
work_dir = GetServerWorkingDirectory()
csv_file = os.path.join(work_dir, "10_1000_Pulse_Short.csv") 
input_values = csv.reader(open(csv_file))

pulse_list_row = []
for row in input_values:
    pulse_list_row.append(row)
pulse_list_row.pop(0)
t_list = [pulse_list_row[n_row][0]+'.'+pulse_list_row[n_row][1].partition(';')[0] for n_row in range(len(pulse_list_row))]
i_list = []
for n_row in range(len(pulse_list_row)):
    if len(pulse_list_row[n_row])==2: #integer only
        i_list.append(pulse_list_row[n_row][1].partition(';')[2])
    if len(pulse_list_row[n_row])==3: #float
        i_list.append(pulse_list_row[n_row][1].partition(';')[2]+'.'+pulse_list_row[n_row][2]) 

my_input_I = str(i_list[0])+"A"

for system in GetAllSystems():
    if "SYS" in system.Name:
        MechSys=system
    if "Max" in system.Name:
        MaxwSys=system

MechDir=MechSys.Name
if " " in MechDir:
    MechDir=MechDir.replace(" ","-")

MaxwComponents=MaxwSys.Components
MaxwSolution=MaxwSys.Components[2]
MechSetup=MechSys.GetComponent(Name="Setup")
MechSolution=MechSys.GetComponent(Name="Results")
ThermCompSetup=MechSys.GetContainer(ComponentName="Setup")
containerTherm=MechSys.GetContainer(ComponentName='Setup')

PrjFullName = GetProjectFile()
Setting.PrjPath=os.path.dirname(PrjFullName)
Setting.UserDir=Project.GetUserFilesDirectory()
Setting.PrjName, temp=os.path.splitext(os.path.basename(PrjFullName))
Setting.ThermSystemDir=os.path.join(Setting.PrjPath, Setting.PrjName) + "_files\\dp0\\" + MechDir + "\\MECH"
Setting.LogFileName=os.path.join(Setting.PrjPath , Setting.PrjName + "_2way_log.txt")

if File.Exists(Setting.LogFileName):
    os.remove(Setting.LogFileName)
    
# Check analysis type (2D/3D)

if "2D" in str(MaxwSolution):
    an_dim=2
    
if "3D" in str(MaxwSolution):
    an_dim=3

# Logger startup

logging.basicConfig(filename=Setting.LogFileName, level=logging.DEBUG, filemode='w', format='%(asctime)s %(levelname)s : %(message)s' )

# Workflow start
# Project reset

logging.info("Coupled simulation start - Analysis type:" + " " + str(an_dim) + "D")
logging.info("Project cleanup")
ThermCompSetup.Edit()

if an_dim == 3:

    MaxwSys.SendAnsoftCommand(PyCommand="""oDesktop.SetActiveProject(\""""+mxwl_project_name+ """\").SetActiveDesign(\""""+mxwl_design_name+"""\").GetModule("AnalysisSetup").RevertSetupToInitial("Setup1")""")

if an_dim == 2:

    MaxwSys.SendAnsoftCommand(Command='oDesktop.GetActiveProject.GetActiveDesign.GetModule("AnalysisSetup").RevertSetupToInitial "Setup1"')#to be checked

MechSolution.Clean()
Remove_APDL_Command(ThermCompSetup)

# First Coupling Step
# Retrieve parameters from lists	
StepEndTime = t_list[0]
MinTimeStep = StepEndTime
MaxTimeStep = StepEndTime #no substeps in mechanical
Nsubsteps = 1 # defined by the user

logging.info("Step n. 1 - Maxwell solution start")
MaxwSys.SendAnsoftCommand(PyCommand="""oDesktop.SetActiveProject(\""""+mxwl_project_name+ """\").SetActiveDesign(\""""+mxwl_design_name+"""\").ChangeProperty(
	[
		\"NAME:AllTabs\",
		[
			\"NAME:LocalVariableTab\",
			[
				\"NAME:PropServers\", 
				\"LocalVariables\"
			],
			[
				\"NAME:ChangedProps\",
				[
					\"NAME:"""+mxwl_design_var_name+"""\",
					\"Value:=\"		, \""""+my_input_I+"""\"
				]
			]
		]
	])""")
MaxwSys.SendAnsoftCommand(PyCommand="""oDesktop.AddMessage("""+"\""""+mxwl_project_name+"""","""+"\""""+mxwl_design_name+"""",0,"My Current is: """+my_input_I+"""")""")
MaxwSolution.Update(AllDependencies=True)
logging.info("Step n. 1 - Maxwell solution end")
Init_Step(ThermCompSetup, StepEndTime, MinTimeStep, MaxTimeStep)
logging.info("Step n. 1 - Thermal solution start")
MechSolution.Update(AllDependencies=True)
logging.info("Step n. 1 - Thermal solution end")

# Additional Coupling Steps
nSteps = len(t_list) #number of steps
counter = 1
while counter < nSteps:

    step_n = counter + 1
    StepEndTime= t_list[counter]
    MaxTimeStep = str(float(t_list[counter])-float(t_list[counter-1]))
    MinTimeStep = str(1*(float(t_list[counter])-float(t_list[counter-1])))
    logging.info("Step n." + " " + str(step_n) + " " + "- Copy files for new step")
    CopyFiles(counter)
    logging.info("Step n." + " " + str(step_n) + " " + "- Maxwell solution start")
    
    my_input_I = str(i_list[counter])+"A"
    MaxwSys.SendAnsoftCommand(PyCommand="""oDesktop.SetActiveProject(\""""+mxwl_project_name+ """\").SetActiveDesign(\""""+mxwl_design_name+"""\").ChangeProperty(
	[
		\"NAME:AllTabs\",
		[
			\"NAME:LocalVariableTab\",
			[
				\"NAME:PropServers\", 
				\"LocalVariables\"
			],
			[
				\"NAME:ChangedProps\",
				[
					\"NAME:"""+mxwl_design_var_name+"""\",
					\"Value:=\"		, \""""+my_input_I+"""\"
				]
			]
		]
	])""")
    MaxwSys.SendAnsoftCommand(PyCommand="""oDesktop.AddMessage("""+"\""""+mxwl_project_name+"""","""+"\""""+mxwl_design_name+"""",0,"My Current is: """+my_input_I+"""")""")  
    
    Ansoft.ForceSolutionIntoUpdateRequiredState(System=MaxwSys)
    MaxwSolution.Update(AllDependencies=True)
    logging.info("Step n." + " " + str(step_n) + " " + "- Maxwell solution end")
    Remove_APDL_Command(ThermCompSetup)
    ChangeStep(ThermCompSetup, StepEndTime, MinTimeStep, MaxTimeStep, counter,Nsubsteps)

    time.sleep(2)
    MechSetup.Update(AllDependencies=True)
    fdsdat = open(Setting.ThermSystemDir+'\\ds.dat',"r")
    fLoss = open(Setting.ThermSystemDir+'\\loss.dat',"w")

    copy = False
    for line in fdsdat:
        if line.find('bfeblock') != -1:
            fLoss.write(line)
            copy = True
            continue
        elif line.find('bfe,') != -1:
            fLoss.write(line)
            copy = False
            continue
        elif copy:
            fLoss.write(line)         
            
    fdsdat.close()
    fLoss.close()
    logging.info("Step n." + " " + str(step_n) + " " + "- Thermal solution start")
    time.sleep(2)
    MechSolution.Update(AllDependencies=True)
    logging.info("Step n." + " " + str(step_n) + " " + "- Thermal solution end")
    
    counter = counter + 1

logging.info("Coupled simulation end")

# Temperature plot extraction (last step)

logging.info("Temperature plot extraction start")

cmd="""temp_2=ExtAPI.DataModel.Project.Model.Analyses[0].Solution.AddTemperature()
temp_2.EvaluateAllResults()
temp_view=ExtAPI.Graphics.ModelViewManager.CreateView()
ExtAPI.Graphics.ModelViewManager.CaptureModelView("temp_view","PNG")
temp_2.Delete()"""

ThermCompSetup.SendCommand(Language="Python", Command=cmd)

logging.info("Temperature plot extraction end")

# Final cleanup and logger shutdown

ClearUserDir(counter)
logging.shutdown()
	
