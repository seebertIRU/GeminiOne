import os
from config import MAX_IMPORT

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    # if not os.path.isfile(target_file):
    #    return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        # Open the file in read mode ('r') using a 'with' statement
        # The 'with' statement ensures the file is properly closed even if errors occur
        with open(target_file, 'w', encoding='utf-8') as file:
            file.write(content) # Read the entire content into a string
    except FileNotFoundError:
        return f"Error: The file '{target_file}' was not found."
    except Exception as e:
        return f"Error: An error occurred: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'