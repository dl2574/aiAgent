import os

def get_file_content(working_directory, file_path):
    working_abs = os.path.abspath(working_directory)

    file_abs = os.path.abspath(os.path.join(working_abs, file_path))

    if not file_abs.startswith(working_abs.rstrip(os.sep) + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    try:
        with open(file_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string = f"{file_content_string}[...File \"{file_path}\" truncated at 10000 characters]"
            
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    