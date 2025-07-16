import os
from google.genai import types

from functions import get_files_info
from functions import get_file_content
from functions  import run_python
from functions import write_file


def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    working_directory = "./calculator"
    function_name_dict = {
        get_files_info.schema_get_files_info.name: get_files_info.get_files_info,
        get_file_content.schema_get_files_content.name: get_file_content.get_file_content,
        run_python.schema_run_python.name: run_python.run_python_file,
        write_file.schema_write_file.name: write_file.write_file,
    }

    if not function_name:
        return print("Error: FunctionCall must have a name part.")
    else:
        if function_name not in function_name_dict.keys():
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        else:
            function_args["working_directory"] = working_directory
            function_call = function_name_dict[function_name]

            if verbose:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            else:
                print(f" - Calling function: {function_call_part.name}")
            
            function_result = function_call(**function_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result},
                    )
                ],
            )


            

