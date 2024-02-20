"""
=====================================================
                   Version: 24.1.7 Simple
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

Last update(mm/dd/yyyy): 02/13/2024
=====================================================
Developer: Qun-Gao Chen, John McKain
E-mail: chen2qo@ucmail.uc.mail, mckainjr@mail.uc.edu
=====================================================
"""
import ctypes # Use to transfer syntax from C++ to Python.
import time # Use to delay closing time.

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
Distance_X_Axis = 50.0
Distance_Y_Axis = 0.0
Distance_Z_Axis = 0.0
Move_Speed = 5.0
Move_Acc = 5.0
Move_Dec = 1.0
Move_Mode = ctypes.c_int(2)     #1: Relative motion.    2: Absolute motion.
Stop_Mode = 2                   #1: Decelerate.         2: Stop immediately.
Home_Speed = 50.0
Home_AccDec = 10.0
Home_Dir_Positive = 1
Home_Dir_Negative = 2
Distance_X_Axis_Machine = 0.0
Distance_Y_Axis_Machine = 0.0
Distance_Z_Axis_Machine = 0.0


#1: X axis.   2: Y axis   3: Z axis
move_axis = 1 
#Still need to update Y and Z axis

print("\n"*5, flush = True)
Device_Response_Open_Device = hllApi_Open_Device (Username, ip_addr_c, Port)

while 1 :

    if Device_Response_Open_Device == 0 :
                    
        if move_axis == "1" : #Move X axis
            
            Distance_X_Axis = (20) #Set distance
            Distance_X_Axis_Machine = ctypes.c_float(Distance_X_Axis * 10)

            Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
            print("\n""The x-axis is moving...", flush = True)

            sec = 0
            sec = Distance_X_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
            time.sleep(sec) # Reduce the burden of software running multiple times
            print(f"The x-axis current Position {Distance_X_Axis} mm.", flush = True)
            print("\n", flush = True)


            return_home = 2
            #1. Immediately stop moviing.
            #2. Let the x-axis go back home.
            #3. Continue.", flush = True
            while 1:
                if return_home == "1" :
                    Device_Response_Stop_Single_Axis = hllApi_Stop_Single_Axis (Username, X_Axis, Stop_Mode)
                    print(f"The device response: {Device_Response_Stop_Single_Axis}.", flush = True)
                    break

                elif return_home == "2" :
                    print(f"The x-axis current Position {Distance_X_Axis} mm.\n", flush = True)
                    Device_Response_X = hllApi_Move_Single_Axis (Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Device_Response_X}.", flush = True)
                    print("\n""The x-axis is going to back home...", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times
                    break

                elif return_home == "3" :

                    break
            
                else :

                    print("\n""Please type the correct value.""\n", flush = True)
                    sec_sub_cmd = 2
                    #input("Enter the value: \n#1. Immediately stop moviing.\n#2. Let the x-axis go back home.\n#3. Continue.:  ", flush = True)

                    break
        
        elif move_axis == "2" : #Move Y axis
            
            Distance_Y_Axis = 50
            #float(input("Y-axis move distance(Positive/ Negative ) float number: "))
            Distance_Y_Axis_Machine = ctypes.c_float(Distance_Y_Axis * 10)

            Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, Y_Axis, Distance_Y_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
            print("\n""The y-axis is moving...", flush = True)

            sec = 0
            sec = Distance_Y_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
            time.sleep(sec) # Reduce the burden of software running multiple times

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
            sec_sub_cmd = 2 #input("Enter the value: ")

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
                    sec_sub_cmd = 2 #input("Enter the value: ")

                    break

        
        elif move_axis == "3" : #Move Z axis
            
            Distance_Z_Axis = 20 #float(input("Z-axis move distance(Positive/ Negative ) float number: "))
            Distance_Z_Axis_Machine = ctypes.c_float(Distance_Z_Axis * 10)

            Device_Response_Move_Single_Axis = hllApi_Move_Single_Axis (Username, Z_Axis, Distance_Z_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            print(f"The device response: {Device_Response_Move_Single_Axis}.", flush = True)
            print("\n""The z-axis is moving...", flush = True)

            sec = 0
            sec = Distance_Z_Axis_Machine.value / Move_Speed.value # Calculate the waiting time.
            time.sleep(sec) # Reduce the burden of software running multiple times

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
            sec_sub_cmd = 2 #input("Enter the value: ")

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
                    sec_sub_cmd = 2 #input("Enter the value: ")

                    break
            


        else: #Close Program

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
            print ("-----Closing program-----", flush = True)
            
            break



