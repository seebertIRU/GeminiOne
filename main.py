import sys
import os
import time
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types
from config import system_prompt, model_name, model2_name
from call_function import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def main():
    
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)



    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def call_function(function_call_part, verbose=False):    
    result=""
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # Import and call the actual function
    
    if function_call_part.name == "get_files_info":
        # Extract arguments (directory is optional)
        directory = function_call_part.args.get("directory", ".")
        
        # Call the function with the working directory (current directory)
        result = get_files_info("./calculator", directory)
        
        
    if function_call_part.name == "get_file_content":
        print(f"{function_call_part.args}")
        file_path=function_call_part.args.get("file_path", ".")
        result=get_file_content("./calculator",file_path)
        

    if function_call_part.name == "write_file":
        print(f"{function_call_part.args}")
        file_path=function_call_part.args.get("file_path", ".")
        content=function_call_part.args.get("content")
        result=write_file("./calculator",file_path, content)

    if function_call_part.name == "run_python_file":
        result=run_python_file("./calculator",function_call_part.args.get("file_path"), function_call_part.args.get("args"))

    if len(result)>0:
        function_call_result= types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )
    else:
        function_call_result= types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )



    if verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")        
            
    return function_call_result


def generate_content(client, messages, verbose):
    limit=20
    while True:
        limit-=1
        modeln=model2_name
        response = client.models.generate_content(
            model=modeln,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if (not response.function_calls) or limit<1:
            print("Response:")
            print(response.text)
            # Get the AI's final response after processing the function result
            final_response = client.models.generate_content(
                model=modeln,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            print(f"Final Response:  {final_response.text}")    
            break
        
        print(response.text)
    
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
    
        # Handle function calls
        for function_call_part in response.function_calls:
            result=call_function(function_call_part, verbose)
            if verbose:
               print(f"-> {result.parts[0].function_response.response}")

                # Add the function result to the conversation
            messages.append(types.Content(
                role="model", 
                parts=[types.Part(function_call=function_call_part)]
            ))
            messages.append(types.Content(
                role="function", 
                parts=[types.Part(function_response=types.FunctionResponse(
                    name=function_call_part.name,
                    response={"result": result}
                ))]
            ))
        
        #handle candidates
        for candidate in response.candidates:
            messages.append(candidate.content)



        


if __name__ == "__main__":
    main()
