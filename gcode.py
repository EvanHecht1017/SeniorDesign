# Adjust the parsing function to correctly extract XYZ coordinates from the identified G-code commands

file_path1 = "/Users/evanhecht/Downloads/dog-2.5H.gcode"

def parse_gcode_for_xyz(file_path):
    """
    Parses the G-code file to extract XYZ coordinates from the identified G-code movement commands.

    Args:
    file_path (str): Path to the G-code file.

    Returns:
    list of tuples: A list containing tuples of XYZ coordinates.
    """
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip comments and empty lines
            if line.startswith(';') or not line.strip():
                continue

            # Filter for movement command G1
            if line.startswith('G1'):
                parts = line.split(' ')
                coord = {'X': None, 'Y': None, 'Z': None}
                for part in parts:
                    if part.startswith('X'):
                        coord['X'] = float(part[1:])
                    elif part.startswith('Y'):
                        coord['Y'] = float(part[1:])
                    elif part.startswith('Z'):
                        coord['Z'] = float(part[1:])

                # Check if any XYZ coordinate is present
                if any(coord.values()):
                    coordinates.append((coord['X'], coord['Y'], coord['Z']))
    return coordinates
    
coordinates = parse_gcode_for_xyz(file_path1)
total = len(coordinates)
for i in range(1, total):
    print(coordinates[i])

