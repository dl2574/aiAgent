import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = False
model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Do not explain your steps or return a text response until the task has been completed and you have a final answer to the user prompt.
"""

args = sys.argv[1:]

if args == []:
    print("Error: You must include a prompt...")

prompt = args[0]

if "--verbose" in args:
    verbose = True

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_run_python,
        schema_write_file
    ]
)
for i in range(20):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
        )
    except Exception as e:
        print(e)

    if response.text:
        print(response.text)
        break

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    for function in response.function_calls:
        try:
            function_result = call_function(function, verbose=verbose)
            function_response = {'result': function_result}
        except Exception as e:
            function_response = {'error': str(e)}

        plain_response = function_result.parts[0].function_response.response
        if not plain_response:
            raise Exception("Error: The function did not have a vailid response")
        elif verbose:
            print(f"-> {plain_response}")

        function_response_part = types.Part.from_function_response(
            name=function.name,
            response=function_response,
        )
        function_response_content = types.Content(
            role='tool', parts=[function_response_part]
        )
        messages.append(function_response_content)

if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


