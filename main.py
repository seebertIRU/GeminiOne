import sys
import os
from dotenv import load_dotenv
from google import genai
from sys import argv
from google.genai import types



def main():
    if len(sys.argv)<2:
        raise Exception("no prompt seen")
    blnverbose=len(sys.argv)==3
    user_prompt=sys.argv[1]
    if blnverbose:
        blnverbose=sys.argv[2]=="--verbose"
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    load_dotenv()
    api_key=os.environ.get("GEMINI_API_KEY")
    client=genai.Client(api_key=api_key)
    response = client.models.generate_content(model='gemini-1.5-flash', contents=messages,)
    print(response.text)
    if blnverbose:
        print(f"User prompt:  {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Hello from geminione!")


if __name__ == "__main__":
    main()
