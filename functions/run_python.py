import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith('.py'):  # Fixed: Added return statement and proper string method
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", target_file]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error executing Python file: {e}"  # Fixed: Removed colon after "Error"

schema_run_python_file = types.FunctionDeclaration(  # Fixed: Renamed to match function name
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to work in.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,  # Fixed: Specified ARRAY type for list of strings
                items=types.Schema(  # Fixed: Added items schema to define array elements
                    type=types.Type.STRING,
                    description="Individual argument string"
                ),
                description="The arguments to add to the file to execute"
            )
        },
        required=["working_directory", "file_path"]  # Added required fields
    ),
)