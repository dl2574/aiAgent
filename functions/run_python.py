import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_abs = os.path.abspath(working_directory)

    file_abs = os.path.abspath(os.path.join(working_abs, file_path))

    if not file_abs.startswith(working_abs.rstrip(os.sep) + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_abs):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python3", file_abs], capture_output=True, cwd=working_abs, timeout=30, text=True)

        stdout_output = result.stdout if result.stdout else ""
        stderr_output = result.stderr if result.stderr else ""
    
        if not stdout_output and not stderr_output:
            return "No output produced."
        
        output_parts = []
        if stdout_output:
            output_parts.append(f"STDOUT: {stdout_output}")
        if stderr_output:
            output_parts.append(f"STDERR: {stderr_output}")
    
        output_str = "\n".join(output_parts)
    
        if result.returncode != 0:
            output_str += f"\nProcess exited with code {result.returncode}"
    
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified python file and return the STDOUT and STDERR if they exsist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file to be run. This parameter is required.",
            ),
        },
    ),
)