def read_gcode_file(file_path):
    """
    Opens a G-code file and prints out each command line by line.

    Parameters:
    - file_path: The path to the G-code file.
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove whitespace and newline characters
                if line:  # Check if the line is not empty
                    print(line)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with test file
file_path = "test_files/dog-2.5H.gcode"
read_gcode_file(file_path)
