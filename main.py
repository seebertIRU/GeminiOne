import sys
import os
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types
from config import system_prompt, model_name, model2_name
from call_function import available_functions

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


def generate_content(client, messages, verbose):
    while True:
        modeln=model_name
        response = client.models.generate_content(
            model=modeln,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        
        if not response.function_calls:
            print("Response:")
            print(response.text)
            break

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # If no function calls, just return the text response
        if not response.function_calls:
            print("Response:")
            print(response.text)
            return

        # Handle function calls
        for function_call_part in response.function_calls:
            if verbose:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            
            # Import and call the actual function
            from functions.get_files_info import get_files_info
            
            if function_call_part.name == "get_files_info":
                # Extract arguments (directory is optional)
                directory = function_call_part.args.get("directory", ".")
                
                # Call the function with the working directory (current directory)
                result = get_files_info(".", directory)
                
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

            response = client.models.generate_content(
                model=modeln,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            
        # Get the AI's final response after processing the function result
        final_response = client.models.generate_content(
            model=modeln,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        print(f"Final Response:  {final_response.text}")    


if __name__ == "__main__":
    main()
