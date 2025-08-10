import os
from config import MAX_IMPORT

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        # Open the file in read mode ('r') using a 'with' statement
        # The 'with' statement ensures the file is properly closed even if errors occur
        with open(target_file, 'r', encoding='utf-8') as file:
            file_content = file.read()  # Read the entire content into a string
    except FileNotFoundError:
        return f"Error: The file '{target_file}' was not found."
    except Exception as e:
        return f"Error: An error occurred: {e}"
    if len(file_content)>MAX_IMPORT:
        file_content=file_content[1:10000]
        file_content=f'{file_content}[...File "{target_file}" truncated at 10000 characters]'
    return file_content