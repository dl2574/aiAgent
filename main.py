import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = False

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

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)

print(response.text)

if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
