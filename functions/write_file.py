import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_abs = os.path.abspath(working_directory)

    file_abs = os.path.abspath(os.path.join(working_abs, file_path))

    if not file_abs.startswith(working_abs.rstrip(os.sep) + os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(os.path.dirname(file_abs)):
            os.makedirs(os.path.dirname(file_abs))
        
        with open(file_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes contents provided to the content parameter to a specified file path. Returns a sucess message and how many characters were written or an error.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to be written. This parameter is required. If the path does not exsist, it will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file path. This parameter is required."
            )
        },
    ),
)
