import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_abs = os.path.abspath(working_directory)
    
    if directory is None or directory == ".":
        directory = ""

    dir_abs = os.path.abspath(os.path.join(working_abs, directory)).rstrip(os.sep) + os.sep

    display_dir = "." if directory in [None, ""] else directory
    if not dir_abs.startswith(working_abs.rstrip(os.sep) + os.sep):
        return f'Error: Cannot list "{display_dir}" as it is outside the permitted working directory'
    
    if not os.path.isdir(dir_abs):
        return f'Error: "{display_dir}" is not a directory'
    
    dir_contents_list = os.listdir(dir_abs)

    lines = []

    for item in dir_contents_list:
        item_path = os.path.join(dir_abs, item)
        try:
            lines.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        except Exception as e:
            return f"Error: {e}"
    
    return "\n".join(lines)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
