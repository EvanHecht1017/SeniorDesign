"""
=====================================================
                   Version: 24.1.7
=====================================================

1. Loading function from FMC4030-Dll.dll
2. This version include (Open-device, Close-device, Check-axis-is-stop, 
Move-single-axis, Home-single-axis, Stop-single-axis, 
Get-axis-current-position, Get-axis-current-speed, Get-machine-status )
3. This version have "logical operator" and "while loop".
4. This version adds that the All-axis always auto-goes back home before the closing program runs.
5. This version solves some bugs that cause the program to freeze.
6. This version separate the parameter setting about axis distance and move (speed/ acc/ dec). That is gonna help the axis-moving more convenient.
7. This version found the problem between program and device. The unit 10 mm (In Program) equal to 1 mm (In Device), so we add the equation to fix it.

Last update(mm/dd/yyyy): 01/27/2024
=====================================================
Developer: Qun-Gao Chen
E-mail: chen2qo@ucmail.uc.mail
=====================================================
"""
import ctypes # Use to transfer syntax from C++ to Python.
import time # Use to delay closing time.
import math 
# Call the DLL file from the laptop
hllDll = ctypes.WinDLL ("C:\\FMC4030\\FMC4030-Dll.dll")

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

"""
=============================
Define all control parameter.
Line. 161 - 183
=============================
"""

# Set-up all parameter
Username = 1
ip_addr = "192.168.0.30"
ip_addr_c = ctypes.c_char_p(ip_addr.encode("utf-8"))
Port = 8088
X_Axis = 0
Y_Axis = 1
Z_Axis = 2
Distance_X_Axis = 0.0
Distance_Y_Axis = 0.0
Distance_Z_Axis = 0.0
Move_Speed = 5.0
Move_Acc = 2.0
Move_Dec = 1.0
Move_Mode = ctypes.c_int(2) # Operating Mode 1. Relative motion. 2. Absolute motion.
Stop_Mode = 2 # Stopping Mode 1. Decelerate to stop. 2. Stop immediately.
Home_Speed = 50.0
Home_AccDec = 10.0
Home_Dir_Positive = 1
Home_Dir_Negative = 2
Distance_X_Axis_Machine = 0.0
Distance_Y_Axis_Machine = 0.0
Distance_Z_Axis_Machine = 0.0

"""
# Parameter for the function (Get_Axis_Current_Pos).
Current_Position_X_Axis = ctypes.c_float(Distance_X_Axis) 
Current_Position_Y_Axis = ctypes.c_float(Distance_Y_Axis)
Current_Position_Z_Axis = ctypes.c_float(Distance_Z_Axis)
"""
"""
# This section has some unknow problem.
# I tried to call the function, but I didn't get the correct return value.

Device_Response_Get_Machine_Status = hllpi_Get_Machine_Status (Username, machineData_buffer)
received_data = machineData_buffer.raw[:Device_Response_Get_Machine_Status]
print(received_data)
print(f"The device response: {Device_Response_Get_Machine_Status}")
print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
"""

print("\n"*5, flush = True)
Device_Response_Open_Device = hllApi_Open_Device (Username, ip_addr_c, Port)

while 1 :

    if Device_Response_Open_Device == 0 :
        
        print("Connecting..."
            "\n"f"Connecting device response: {Device_Response_Open_Device}"
            "\n""Please open FMC4030-SDK.pdf to see return value definition."
            "\n""Welcome to control the 3-D printer."
            "\n""Hope your experiment goes well."
            "\n""*********************"
            "\n""*        Menu       *"
            "\n""*********************"
            "\n""1. Get the axis current Position."
            "\n""2. Move the single axis."
            "\n""3. Home the single axis."
            "\n""4. Close the program."
            "\n", flush = True
            )
        
        cmd = input("Enter the value: ")

        if cmd == "1" :
            while 1 :
                """
                # The function can work (Get the correct return value).
                # When I am moving the axis, the "Current_Position_X_Axis" always show 0.0, the number never change.
                # So I try to use the way which is default and set-up the distance parameter to show the current position.
                
                Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                """
                
                print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)

                time.sleep(0.5) # Reduce the burden of software running multiple times

                print(
                    "\n""1. Double check again."
                    "\n""2. Back."
                    "\n""3. Close the program."
                    "\n", flush = True
                    )
                
                sub_cmd = 0
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "1" :
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    print(f"The device response: X-axis -> {Device_Response_X_Axis_Position}, Y-axis -> {Device_Response_Y_Axis_Position}, Z-axis -> {Device_Response_Z_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    
                    time.sleep(1) # Reduce the burden of software running multiple times

                elif sub_cmd == "2" :

                    print("About to back to the previous page.""\n", flush = True)

                    break

                elif sub_cmd == "3" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print("\n""The all axis are going to back home...""\n", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    Device_Response_Close_Device = hllApi_Close_Device (Username)
                    print(f"Closing device response: {Device_Response_Close_Device}", flush = True)
                    print ("The program will close in 3 sec.", flush = True)
                    print ("3", flush = True)
                    time.sleep(1)
                    print ("2", flush = True)
                    time.sleep(1)
                    print ("1", flush = True)
                    print ("Have a good day !", flush = True)
                    print("\n"*5, flush = True)
                    
                    break#exit()

                else :

                    print ("Please type the correct value.""\n", flush = True)
                    sub_cmd = input("Enter the value: ")

        elif cmd == "2" :
            while 1 :
                
                print(
                    "\n""Which axis do you wanna move ?"
                    "\n""1. Set-up the parameters for moving."
                    "\n""2. Setting and Moving the x-axis."
                    "\n""3. Setting and Moving the y-axis."
                    "\n""4. Setting and Moving the z-axis."
                    "\n""5. Back."
                    "\n""6. Close the program.", flush = True
                    )

                print("\n"f"Now the operating mode is {Move_Mode.value}.""\n", flush = True)
                sub_cmd = 0
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "1" :
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    print(f"The device response: X-axis -> {Device_Response_X_Axis_Position}, Y-axis -> {Device_Response_Y_Axis_Position}, Z-axis -> {Device_Response_Z_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    Move_Speed = ctypes.c_float(float(input("Moving speed (Positive) float number: ")))
                    Move_Acc = ctypes.c_float(float(input("Moving acceleration (Positive) float number: ")))
                    Move_Dec = ctypes.c_float(float(input("Moving deceleration (Positive) float number: ")))
                    Move_Mode= ctypes.c_int(int(input("Moving mode (1. Relative motion. 2. Absolute motion.): ")))
                    
                elif sub_cmd == "2" :
                    
                    Distance_X_Axis = float(input("X-axis move distance(Positive/ Negative ) float number: "))
                    Distance_X_Axis_Machine = ctypes.c_float(Distance_X_Axis * 10)

                    Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
                    print("\n""The x-axis is moving...", flush = True)

                    sec = 0
                    sec = Distance_X_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
                    
                    #time.sleep(sec1) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print("\n", flush = True)

                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the x-axis go back home."
                        "\n""3. Continue.", flush = True
                        )
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while 1:
                        if sec_sub_cmd == "1" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, X_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :
                            print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                            print("\n", flush = True)

                            Distance_X_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)

                            Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            print(f"The device response: {Device_Response_X}.", flush = True)
                            print("\n""The x-axis is going to back home...", flush = True)

                            time.sleep(0.5) # Reduce the burden of software running multiple times
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Enter the value: ")

                            break
                
                elif sub_cmd == "3" :
                    
                    Distance_Y_Axis = float(input("Y-axis move distance(Positive/ Negative ) float number: "))
                    Distance_Y_Axis_Machine = ctypes.c_float(Distance_Y_Axis * 10)

                    Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
                    print("\n""The y-axis is moving...", flush = True)

                    sec = 0
                    sec = Distance_Y_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
                    #time.sleep(sec) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    """
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print("\n", flush = True)
                        
                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the y-axis go back home."
                        "\n""3. Continue.", flush = True
                        )
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while 1:
                        if sec_sub_cmd == "1" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, Y_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :
                            print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                            print("\n", flush = True)

                            Distance_Y_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)

                            Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            print(f"The device response: {Device_Response_Y}.", flush = True)
                            print("\n""The y-axis is going to back home...", flush = True)

                            time.sleep(0.5) # Reduce the burden of software running multiple times
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Enter the value: ")

                            break

                
                elif sub_cmd == "4" :
                    
                    Distance_Z_Axis = float(input("Z-axis move distance(Positive/ Negative ) float number: "))
                    Distance_Z_Axis_Machine = ctypes.c_float(Distance_Z_Axis * 10)

                    Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
                    print("\n""The z-axis is moving...", flush = True)

                    sec = 0
                    sec = Distance_Z_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
                    #time.sleep(sec) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    """
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n", flush = True)
                        
                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the z-axis go back home."
                        "\n""3. Continue.", flush = True
                        )
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while 1:
                        if sec_sub_cmd == "1" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, Z_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :
                            print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                            print("\n", flush = True)

                            Distance_Z_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)

                            Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            print(f"The device response: {Device_Response_Z}.", flush = True)
                            print("\n""The z-axis is going to back home...", flush = True)

                            time.sleep(0.5) # Reduce the burden of software running multiple times
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Enter the value: ")

                            break
                    
                elif sub_cmd == "5" :

                    break

                elif sub_cmd == "6" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Device_Response_X}, Y-axis -> {Device_Response_Y}, Z-axis -> {Device_Response_Z}.", flush = True)
                    print("\n""The all axis are going to back home...""\n", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    Device_Response_Close_Device = hllApi_Close_Device (Username)
                    print(f"Closing device response: {Device_Response_Close_Device}", flush = True)
                    print ("The program will close in 3 sec.", flush = True)
                    print ("3", flush = True)
                    time.sleep(1)
                    print ("2", flush = True)
                    time.sleep(1)
                    print ("1", flush = True)    
                    print ("Have a good day !", flush = True)
                    print("\n"*5, flush = True)
                    
                    break#exit()

                else :

                    print ("\n""Please type the correct value.""\n", flush = True)
                    sub_cmd = input("Enter the value: ")

        elif cmd == "3" : # Calling the hllApi_Move_Single_Axis function to go back to a home point is safer.
            while 1:
                """
                Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                print(f"The device response: X-axis -> {Device_Response_X_Axis_Position}, Y-axis -> {Device_Response_Y_Axis_Position}, Z-axis -> {Device_Response_Z_Axis_Position}")
                print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                """
                print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                
                time.sleep(0.5)

                print(
                    "\n""1. Move all axis go back to home."
                    "\n""2. Move X-axis go back to home."
                    "\n""3. Move Y-axis go back to home."
                    "\n""4. Move Z-axis go back to home."
                    "\n""5. Back."
                    "\n""6. Close the program."
                    "\n", flush = True
                    )

                sub_cmd = 0
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "1" :

                    print("\n""\n""\n", flush = True)
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    
                    print(f"The device response: X-axis -> {Device_Response_X_Axis_Position}, Y-axis -> {Device_Response_Y_Axis_Position}, Z-axis -> {Device_Response_Z_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n")

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Device_Response_X}, Y-axis -> {Device_Response_Y}, Z-axis -> {Device_Response_Z}.", flush = True)
                    print("\n""The all axis are going to back home...", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    """
                    
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n")
                    
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Stop moving immediately (y/n): ")
                    

                    while 1:
                        if sec_sub_cmd == "y" :

                            Device_Response_Stop_Single_Axis_X = hllApi_Stop_Single_Axis (Username, X_Axis, Stop_Mode)
                            Device_Response_Stop_Single_Axis_Y = hllApi_Stop_Single_Axis (Username, Y_Axis, Stop_Mode)
                            Device_Response_Stop_Single_Axis_Z = hllApi_Stop_Single_Axis (Username, Z_Axis, Stop_Mode)
                            print(f"The device response: X-axis -> {Device_Response_Stop_Single_Axis_X}, Y-axis -> {Device_Response_Stop_Single_Axis_Y}, Z-axis -> {Device_Response_Stop_Single_Axis_Z}.", flush = True)

                            break

                        elif sec_sub_cmd == "n" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Stop moving immediately (y/n): ")

                elif sub_cmd == "2" :
                    
                    print("\n""\n""\n", flush = True)
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    print(f"The device response: {Device_Response_X_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print("\n", flush = True)

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_X}.", flush = True)
                    print("\n""The x-axis is going to back home...", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_X_Axis_Position = hllApi_Get_Axis_Current_Position (Username, X_Axis, ctypes.byref(Current_Position_X_Axis))
                    """
                    print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
                    print("\n", flush = True)
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Stop moving immediately (y/n): ")

                    while 1:
                        if sec_sub_cmd == "y" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, X_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "n" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Stop moving immediately (y/n): ")

                elif sub_cmd == "3" :

                    print("\n""\n""\n", flush = True)
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    print(f"The device response: {Device_Response_Y_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print("\n", flush = True)

                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_Y}.", flush = True)
                    print("\n""The y-axis is going to back home...", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Y_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Y_Axis, ctypes.byref(Current_Position_Y_Axis))
                    """
                    print(f"The y-axis current Position {Distance_Y_Axis} mm.", flush = True)
                    print("\n", flush = True)
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Stop moving immediately (y/n): ")

                    while 1:
                        if sec_sub_cmd == "y" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, Y_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "n" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Stop moving immediately (y/n): ")

                elif sub_cmd == "4" :

                    print("\n""\n""\n", flush = True)
                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    print(f"The device response: {Device_Response_Z_Axis_Position}")
                    print("Return 0 is execution succeed. If other values are returned, please open FMC4030-SDK.pdf to see return value definition")
                    """
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n", flush = True)

                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_Z}.", flush = True)
                    print("\n""The z-axis is going to back home...", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    """
                    Why this section is the multi-line comment, you can look up the Line. 225 - 233.
                    Device_Response_Z_Axis_Position = hllApi_Get_Axis_Current_Position (Username, Z_Axis, ctypes.byref(Current_Position_Z_Axis))
                    """
                    print(f"The z-axis current Position {Distance_Z_Axis} mm.", flush = True)
                    print("\n", flush = True)
                        
                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Stop moving immediately (y/n): ")

                    while 1:
                        if sec_sub_cmd == "y" :

                            Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, Z_Axis, Stop_Mode)
                            print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "n" :

                            break
                    
                        else :

                            print("\n""Please type the correct value.""\n", flush = True)
                            sec_sub_cmd = input("Stop moving immediately (y/n): ")

                elif sub_cmd == "5" :
                                        
                    break

                elif sub_cmd == "6" :
                    
                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode= ctypes.c_int(2)

                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Device_Response_X}, Y-axis -> {Device_Response_Y}, Z-axis -> {Device_Response_Z}.", flush = True)
                    print("\n""The all axis are going to back home...""\n")

                    time.sleep(0.5) # Reduce the burden of software running multiple times
                    
                    Device_Response_Close_Device = hllApi_Close_Device (Username)
                    print(f"Closing device response: {Device_Response_Close_Device}", flush = True)
                    print ("The program will close in 3 sec.", flush = True)
                    print ("3", flush = True)
                    time.sleep(1)
                    print ("2", flush = True)
                    time.sleep(1)
                    print ("1", flush = True)
                    print ("Have a good day !", flush = True)
                    print("\n"*5, flush = True)
                    
                    break#exit()

                else :

                    print ("Please type the correct value.""\n", flush = True)
                    sub_cmd = input("Enter the value: ")

        elif cmd == "4" :
            
            Distance_X_Axis = ctypes.c_float(0.0)
            Distance_Y_Axis = ctypes.c_float(0.0)
            Distance_Z_Axis = ctypes.c_float(0.0)
            Move_Speed = ctypes.c_float(50.0)
            Move_Acc = ctypes.c_float(20.0)
            Move_Dec = ctypes.c_float(20.0)
            Move_Mode= ctypes.c_int(2)

            Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            Device_Response_Y = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            Device_Response_Z = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            print(f"The device response: X-axis -> {Device_Response_X}, Y-axis -> {Device_Response_Y}, Z-axis -> {Device_Response_Z}.", flush = True)
            print("\n""The all axis are going to back home...""\n")

            time.sleep(0.5) # Reduce the burden of software running multiple times

            Device_Response_Close_Device = hllApi_Close_Device (Username)
            print(f"Closing device response: {Device_Response_Close_Device}", flush = True)
            print ("The program will close in 3 sec.", flush = True)
            print ("3", flush = True)
            time.sleep(1)
            print ("2", flush = True)
            time.sleep(1)
            print ("1", flush = True)
            print ("Have a good day !", flush = True)
            print("\n"*5, flush = True)
            
            break#exit()
            
        else :

            print ("\n""Please type the correct value.""\n", flush = True)
            cmd = input("Enter the value: ")

    elif Device_Response_Open_Device < 0 :
        
        Device_Response_Close_Device = hllApi_Close_Device (Username)
        print(f"Closing device response: {Device_Response_Close_Device}", flush = True)
        print ("The program will close in 3 sec.", flush = True)
        print ("3", flush = True)
        time.sleep(1)
        print ("2", flush = True)
        time.sleep(1)
        print ("1", flush = True)
        print ("Have a good day !", flush = True)
        print("\n"*5, flush = True)
        
        break

