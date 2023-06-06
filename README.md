# pyworkbench-examples
This repo stores PyWorkbench examples.

To add a new example:
1. A new subdirectory should be created under the "examples" directory, to store the files.
2. Only script files (PyANSYS scripts, Jupyter Notebook scripts, etc) can be stored in this repo. 
3. All data files(geometry files, engineering data, application databases, solution configurations, etc) used by the scripts should be uploaded to [the ANSYS example-data repo](https://github.com/ansys/example-data) under pyworkbench directory, and accessed in the scripts using `upload_file_from_example_repo` API.
4. Update [the CODEOWNERS file](https://github.com/ansys-internal/pyworkbench-examples/blob/main/CODEOWNERS).
