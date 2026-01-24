import os
import json

ExtAPI.Application.ScriptByName("jscript").CallJScript("doGraphicsFit")

analysis = Model.Analyses[0]

fixed_support = analysis.AddFixedSupport()
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [19]
fixed_support.Location = selection

force = analysis.AddForce()
selection1 = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection1.Ids = [13]
force.Location = selection1
force.Magnitude.Output.SetDiscreteValue(0, Quantity(800, "N"))

mesh = Model.Mesh
mesh.GenerateMesh()

solution = analysis.Solution
total_deformation = solution.AddTotalDeformation()

solution.Solve(True)

mechdir = analysis.Children[0].SolverFilesDirectory
export_path = os.path.join(mechdir, "deformation.png")
total_deformation.Activate()
Graphics.ExportImage(export_path, GraphicsImageExportFormat.PNG)

results = { "total_deformation": str(total_deformation.Maximum) }
json.dumps(results)
