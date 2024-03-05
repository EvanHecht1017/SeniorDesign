import ctypes
import time
import sys
# Call the DLL file from the laptop
hllDll = ctypes.WinDLL("C:\\FMC4030\\FMC4030-Dll.dll")

"""
====================================
Define all function parameter types.
Line. 34 - 124
====================================
"""

# Define the Open Device parameter
hllApiProto_Open_Device = ctypes.WINFUNCTYPE (  
    
    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_char_p, # Ipv4address
    ctypes.c_int, # Port
)

# Define the Check Axis parameter
hllApiProto_Check_Axis_Is_Stop = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single axis   
)

# Define the Moving Z Axis parameter
hllApiProto_Move_Single_Axis = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single axis 0. X-axis. 1. Y-axis. 2. Z-axis
    ctypes.c_float, # Distance (unit: mm)
    ctypes.c_float, # Speed (unit: mm/s)
    ctypes.c_float, # Acceleration (unit: mm/s^2)
    ctypes.c_float, # Deceleration (unit: mm/s^2)
    ctypes.c_int, # Mode 1. Relative motion. 2. Absolute motion
)

# After starting the axis, it can stop motion
hllApiProto_Stop_Single_Axis = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single axis
    ctypes.c_int, # Mode 1. Decelerate to stop. 2. Stop immediately.
)

# Control a certain axis to execute zero return
hllApiProto_Home_Single_Axis = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single axis
    ctypes.c_float, # HomeSpeed: Return to zero speed, positive number (unit: mm/s)
    ctypes.c_float, # HomeAccDec: Homing acceleration and deceleration, positive number, (unit: mm/s^2)
    ctypes.c_float, # HomeFallStep: Return to zero falling distance, postive number (unit: mm)
    ctypes.c_int, # HomeDirection: 1. Positive limit return to zero, 2. Negative limit return to zero.
)

# Get the current actual position of an axis.
hllApiProto_Get_Axis_Current_Position = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single axis
    ctypes.POINTER(ctypes.c_float), # Updated current Position (unit: mm)
)

# Get the current running speed of axis
hllApiProto_Get_Axis_Current_Speed = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_float, # Updated current speed (unit: mm/s)
)

# Get equipment status and operating parameters.
buffer_size = 6
machineData_buffer = ctypes.create_string_buffer(buffer_size)
hllApiProto_Get_Machine_Status = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_char_p, # The device data in the structure will be updated after the call
)

# Stop interpolation movement at all.
hllApiProto_Stop_Run = ctypes.WINFUNCTYPE (
    
    ctypes.c_int, # Return value
    ctypes.c_int, # Username
)

# Define the Close Device parameter
hllApiProto_Close_Device = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Reture value
    ctypes.c_int, # Username
)

"""
===================================
Define all function name in Python.
Line. 133 - 152
===================================
"""

# Set-up the function in program
hllApi_Open_Device = hllApiProto_Open_Device (("FMC4030_Open_Device", hllDll),)
hllApi_Check_Axis_Is_Stop = hllApiProto_Check_Axis_Is_Stop (("FMC4030_Check_Axis_Is_Stop", hllDll),)
hllApi_Home_Single_Axis = hllApiProto_Home_Single_Axis (("FMC4030_Home_Single_Axis", hllDll),) # We didn't use it. Using Move_Single_Axis to control go back home.
hllApi_Move_Single_Axis = hllApiProto_Move_Single_Axis (("FMC4030_Jog_Single_Axis", hllDll),)
hllApi_Stop_Single_Axis = hllApiProto_Stop_Single_Axis (("FMC4030_Stop_Single_Axis", hllDll),)
hllApi_Stop_Run = hllApiProto_Stop_Run (("FMC4030_Stop_Run", hllDll),) # We didn't use.
hllApi_Get_Axis_Current_Position = hllApiProto_Get_Axis_Current_Position (("FMC4030_Get_Axis_Current_Pos", hllDll),) # We didn't use it.
hllApi_Get_Axis_Current_Speed = hllApiProto_Get_Axis_Current_Speed (("FMC4030_Get_Axis_Current_Speed", hllDll),) # We didn't use it.
hllpi_Get_Machine_Status = hllApiProto_Get_Machine_Status (("FMC4030_Get_Machine_Status", hllDll),) # Received the machineData have a unknow problem.
hllApi_Close_Device = hllApiProto_Close_Device (("FMC4030_Close_Device", hllDll),)

# Your setup parameters
Username = 1
ip_addr = "192.168.0.30"
ip_addr_c = ctypes.c_char_p(ip_addr.encode("utf-8"))
Port = 8088
X_Axis = 0
Y_Axis = 1
Z_Axis = 2
Move_Speed = ctypes.c_float(100.0)
Move_Acc = ctypes.c_float(100.0)
Move_Dec = ctypes.c_float(50.0)
Move_Mode = ctypes.c_int(1)     #1: Relative motion.    2: Absolute motion.
Stop_Mode = 2                   #1: Decelerate.         2: Stop immediately.
Move_Distance = 20
current_position = {'X': 0, 'Y': 0, 'Z': 0}
# Open Device
Device_Response_Open_Device = hllApi_Open_Device(Username, ip_addr_c, Port)
if Device_Response_Open_Device != 0:
    print("Failed to open device")
    exit(1)

def move_x_axis(distance):
    Distance_X_Axis = ctypes.c_float(distance)
    hllApi_Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
    print("Moving X Axis")

def move_y_axis(distance):
    Distance_Y_Axis = ctypes.c_float(distance)
    hllApi_Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
    print("Moving Y Axis")

def move_z_axis(distance):
    Distance_Z_Axis = ctypes.c_float(distance)
    hllApi_Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
    print("Moving Z Axis")

# Define a function to move the machine head to a specified location at cutting speed
def move_to(x, y, z):

    global current_position

    # Calculate the required movement for each axis
    movement_x = x - current_position['X']
    movement_y = y - current_position['Y']
    movement_z = z - current_position['Z']

    current_position['X'] += movement_x
    current_position['Y'] += movement_y
    current_position['Z'] += movement_z


    move_x_axis(movement_x)
    move_y_axis(movement_y)
    move_z_axis(movement_z)
    print(f"Moving to X={x}, Y={y}, Z={z} ")

def interpret_gcode(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('G'):
                # Split the line into components (command and parameters)
                components = line.split()
                command = components[0]
                params = {component[0]: float(component[1:]) for component in components[1:] if component[0] in {'X', 'Y', 'Z'}}
                
                # Default to the current position if a coordinate is not provided in the G-code
                x = params.get('X', 0)  # Replace 0 with current X if tracking
                y = params.get('Y', 0)  # Replace 0 with current Y if tracking
                z = params.get('Z', 0)  # Replace 0 with current Z if tracking

                if command == 'G0':
                    move_to(x, y, z)
                elif command == 'G1':
                    move_to(x, y, z)
# Run with Test File
                    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gcode.py <path_to_gcode_file>")
        sys.exit(1)

    gcode_file_path = sys.argv[1]
    interpret_gcode(gcode_file_path)                   

