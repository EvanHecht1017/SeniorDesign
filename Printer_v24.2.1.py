import ctypes
import time

hllDll = ctypes.WinDLL ("C:\\Users\\yeongin\\Documents\\FMC4030\\FMC4030\\FMC4030-Dll.dll")

def Open_Device (Username, ip, port):

    hllApiProto_Open_Device = ctypes.WINFUNCTYPE (  
    
    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_char_p, # Ipv4address
    ctypes.c_int, # Port
    )
    ip = ctypes.c_char_p(ip.encode("utf-8"))

    return hllApiProto_Open_Device(("FMC4030_Open_Device", hllDll))(Username, ip, port)

def Close_Device (Username):

    hllApiProto_Close_Device = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Reture value
    ctypes.c_int, # Username
    )

    return hllApiProto_Close_Device(("FMC4030_Close_Device", hllDll))(Username)

def Move_Single_Axis (Username, Axis, distance, speed, acc, dec, moving_mode):

    hllApiProto_Move_Single_Axis = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single Axis 0. X-Axis. 1. Y-Axis. 2. Z-Axis
    ctypes.c_float, # Distance (unit: mm)
    ctypes.c_float, # Speed (unit: mm/s)
    ctypes.c_float, # Acceleration (unit: mm/s^2)
    ctypes.c_float, # Deceleration (unit: mm/s^2)
    ctypes.c_int, # Mode 1. Relative motion. 2. Absolute motion
    )

    return hllApiProto_Move_Single_Axis(("FMC4030_Jog_Single_Axis", hllDll))(Username, Axis, distance, speed, acc, dec, moving_mode)

def Stop_Single_Axis (Username, Axis, stop_mode):

    hllApiProto_Stop_Single_Axis = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single Axis
    ctypes.c_int, # Mode 1. Decelerate to stop. 2. Stop immediately.
    )

    return hllApiProto_Stop_Single_Axis(("FMC4030_Stop_Single_Axis", hllDll))(Username, Axis, stop_mode)

def Check_Axis_Is_Stop (Username, Axis):

    hllApiProto_Check_Axis_Is_Stop = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single Axis   
    )

    return hllApiProto_Check_Axis_Is_Stop(("FMC4030_Check_Axis_Is_Stop", hllDll))(Username, Axis)

def Get_Axis_Current_Pos (Username, Axis):

    hllApiProto_Get_Axis_Current_Position = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single Axis
    ctypes.POINTER(ctypes.c_float), # Updated current Position (unit: mm)
    )

    pos = ctypes.c_float()

    hllApiProto_Get_Axis_Current_Position(("FMC4030_Get_Axis_Current_Pos", hllDll))(Username, Axis, ctypes.byref(pos))

    return pos.value

def Get_Axis_Current_Speed (Username, Axis):

    hllApiProto_Get_Axis_Current_Speed = ctypes.WINFUNCTYPE (

    ctypes.c_int, # Return value
    ctypes.c_int, # Username
    ctypes.c_int, # Single Axis
    ctypes.POINTER(ctypes.c_float), # Updated current speed (unit: mm/s)
    )
    
    get_speed = ctypes.c_float()

    hllApiProto_Get_Axis_Current_Speed(("FMC4030_Get_Axis_Current_Speed", hllDll))(Username, Axis, ctypes.byref(get_speed))

    return get_speed.value


# Set-up Parameter Section.

Username = 0
ip = "192.168.0.30"
port = 8088
X_Axis = 0
Y_Axis = 1
Z_Axis = 2
Distance_X_Axis = 0.0
Distance_Y_Axis = 0.0
Distance_Z_Axis = 0.0
Move_Speed = ctypes.c_float(0.0)
Move_Acc = ctypes.c_float(0.0)
Move_Dec = ctypes.c_float(0.0)
Move_Mode = ctypes.c_int(2) # Operating Mode 1. Relative motion. 2. Absolute motion.
Stop_Mode = ctypes.c_int(2) # Stopping Mode 1. Decelerate to stop. 2. Stop immediately.
Distance_X_Axis_Machine = 0.0
Distance_Y_Axis_Machine = 0.0
Distance_Z_Axis_Machine = 0.0
Pos_X_Axis = 0.0
Pos_Y_Axis = 0.0
Pos_Z_Axis = 0.0

cmd = 0
sub_cmd = 0
sec_sub_cmd = 0
# Start Program.

print("\n"*5, flush = True)
Response_Open_Device = Open_Device(Username, ip, port)
print(f"The device response: {Response_Open_Device}""\n""Connecting...")

while True :
    if Response_Open_Device == 0 :

        print("Connecting..."
            "\n""Welcome to control the 3-D printer."
            "\n""Hope your experiment goes well."
            "\n""*********************"
            "\n""*        Menu       *"
            "\n""*********************"
            "\n""1. Check the axis status."
            "\n""2. Move the single axis."
            "\n""3. Home the single axis."
            "\n""4. Close the program."
            "\n", flush = True
            )
        Pos_X_Axis = Get_Axis_Current_Pos(Username, X_Axis)
        Pos_Y_Axis = Get_Axis_Current_Pos(Username, Y_Axis)
        Pos_Z_Axis = Get_Axis_Current_Pos(Username, Z_Axis)
        print(f"The x-axis current posistion {Pos_X_Axis} mm.", flush = True)
        print(f"The y-axis current posistion {Pos_Y_Axis} mm.", flush = True)
        print(f"The z-axis current posistion {Pos_Z_Axis} mm.", flush = True)

        time.sleep(0.5) # Reduce the burden of software running multiple times

        cmd = input("Enter the value: ")

        if cmd == "1" :
            while True :

                Pos_X_Axis = Get_Axis_Current_Pos(Username, X_Axis)
                Pos_Y_Axis = Get_Axis_Current_Pos(Username, Y_Axis)
                Pos_Z_Axis = Get_Axis_Current_Pos(Username, Z_Axis)
                print(f"The x-axis current posistion {Pos_X_Axis} mm.", flush = True)
                print(f"The y-axis current posistion {Pos_Y_Axis} mm.", flush = True)
                print(f"The z-axis current posistion {Pos_Z_Axis} mm.", flush = True)
                
                time.sleep(0.5) # Reduce the burden of software running multiple times

                Response_Check_Single_Is_X_Axis = Check_Axis_Is_Stop(Username, X_Axis)
                Response_Check_Single_Is_Y_Axis = Check_Axis_Is_Stop(Username, Y_Axis)
                Response_Check_Single_Is_Z_Axis = Check_Axis_Is_Stop(Username, Z_Axis)

                if Response_Check_Single_Is_X_Axis == 1 and Response_Check_Single_Is_Y_Axis == 1 and Response_Check_Single_Is_Z_Axis == 1 :
                    
                    print("All axis is stop.", flush = True)

                elif Response_Check_Single_Is_X_Axis == 0 and Response_Check_Single_Is_Y_Axis == 1 and Response_Check_Single_Is_Z_Axis == 1 :

                    print("The x-axis is running.", flush = True)

                elif Response_Check_Single_Is_X_Axis == 1 and Response_Check_Single_Is_Y_Axis == 0 and Response_Check_Single_Is_Z_Axis == 1 :
    
                    print("The y-axis is running.", flush = True)

                elif Response_Check_Single_Is_X_Axis == 1 and Response_Check_Single_Is_Y_Axis == 1 and Response_Check_Single_Is_Z_Axis == 0 :
    
                    print("The z-axis is running.", flush = True)

                else :

                    print("More two axis are running", flush = True)
                
                time.sleep(0.5) # Reduce the burden of software running multiple times
                    
                print(
                    "\n""1. Double check."
                    "\n""2. Previous page."
                    "\n""3. Close the program."
                    "\n", flush = True
                    )
                
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "1" :

                    time.sleep(0.5) # Reduce the burden of software running multiple times
                
                elif sub_cmd == "2" :

                    break

                elif sub_cmd == "3" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}, Y-axis -> {Response_Moving_Single_Y_Axis}, Z-axis -> {Response_Moving_Single_Z_Axis}.", flush = True)
                    print("\n""The all axis are going to back home...""\n")

                    time.sleep(1) # Reduce the burden of software running multiple times

                    Response_Close_Device = Close_Device(Username)
                    print("The program will close in 3 sec.", flush = True)
                    print("3", flush = True)
                    time.sleep(1)
                    print("2", flush = True)
                    time.sleep(1)
                    print("1", flush = True)
                    print("Have a good day !""\n"*5, flush = True)

                    break

                else :

                    print("\n""Please type the correct value""\n")
                    sub_cmd = input("Enter the value: ")

        elif cmd == "2" :
            while True :

                print(
                    "\n""0. Set-up the parameters for moving."
                    "\n""1. Setting and Moving the x-axis."
                    "\n""2. Setting and Moving the y-axis."
                    "\n""3. Setting and Moving the z-axis."
                    "\n""4. Previous page."
                    "\n""5. Close the program."
                    "\n"f"Speed -> {Move_Speed.value}, Acceleration -> {Move_Acc}, Deceleration -> {Move_Dec}.", flush = True
                    )
                
                sub_cmd = 0
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "0" :

                    print("\n""Section: Set-up the parameters for moving.")
                    Pos_X_Axis = Get_Axis_Current_Pos(Username, X_Axis)
                    Pos_Y_Axis = Get_Axis_Current_Pos(Username, Y_Axis)
                    Pos_Z_Axis = Get_Axis_Current_Pos(Username, Z_Axis)
                    print(f"The x-axis current posistion {Pos_X_Axis} mm.", flush = True)
                    print(f"The y-axis current posistion {Pos_Y_Axis} mm.", flush = True)
                    print(f"The z-axis current posistion {Pos_Z_Axis} mm.", flush = True)

                    time.sleep(0.5) # Reduce the burden of software running multiple times

                    Move_Speed = ctypes.c_float(float(input("Moving speed (Positive) float number: ")))
                    Move_Acc = ctypes.c_float(float(input("Moving acceleration (Positive) float number: ")))
                    Move_Dec = ctypes.c_float(float(input("Moving deceleration (Positive) float number: ")))
                    Move_Mode= ctypes.c_int(int(input("Moving mode (1. Relative motion. 2. Absolute motion.): ")))
                
                elif sub_cmd == "1" :
                    
                    print(
                        "\n""Section: Setting and Moving the x-axis."
                        "\n""Please the enter the (Positive/ Negative) float number."
                        )

                    Distance_X_Axis = float(input("Unit: mm -> "))
                    Distance_X_Axis_Machine = ctypes.c_float(Distance_X_Axis * 10)
                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Response_Moving_Single_X_Axis}.", flush = True)
                    print("\n""The x-axis is moving...", flush = True)

                    time.sleep(2) # Reduce the burden of software running multiple times
                    
                    Pos_X_Axis = Get_Axis_Current_Pos(Username, X_Axis)
                    print(f"The x-axis current posistion {Pos_X_Axis} mm.", flush = True)
                    
                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the x-axis go back home."
                        "\n""3. Continue."
                        )

                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while True :
                        if sec_sub_cmd == "1" :

                            Response_Stop_Axis = Stop_Single_Axis(Username, X_Axis, Stop_Mode)
                            print(f"The device response: {Response_Stop_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :

                            Distance_X_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)
                            Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break

                        else :
                            print("\n""Please type the correct value""\n")
                            sec_sub_cmd = input("Enter the value: ")
                
                elif sub_cmd == "2" :
                    
                    print(
                        "\n""Section: Setting and Moving the y-axis."
                        "\n""Please the enter the (Positive/ Negative) float number."
                        )

                    Distance_Y_Axis = float(input("Unit: mm -> "))
                    Distance_Y_Axis_Machine = ctypes.c_float(Distance_Y_Axis * 10)
                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Response_Moving_Single_Y_Axis}.", flush = True)
                    print("\n""The y-axis is moving...", flush = True)

                    time.sleep(2) # Reduce the burden of software running multiple times
                    
                    Pos_Y_Axis = Get_Axis_Current_Pos(Username, Y_Axis)
                    print(f"The y-axis current posistion {Pos_Y_Axis} mm.", flush = True)
                    
                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the y-axis go back home."
                        "\n""3. Continue."
                        )

                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while True :
                        if sec_sub_cmd == "1" :

                            Response_Stop_Axis = Stop_Single_Axis(Username, Y_Axis, Stop_Mode)
                            print(f"The device response: {Response_Stop_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :

                            Distance_Y_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)
                            Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break

                        else :
                            print("\n""Please type the correct value""\n")
                            sec_sub_cmd = input("Enter the value: ")

                elif sub_cmd == "3" :
          
                    print(
                        "\n""Section: Setting and Moving the z-axis."
                        "\n""Please the enter the (Positive/ Negative) float number."
                        )

                    Distance_Z_Axis = float(input("Unit: mm -> "))
                    Distance_Z_Axis_Machine = ctypes.c_float(Distance_Z_Axis * 10)
                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis_Machine, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: {Response_Moving_Single_Z_Axis}.", flush = True)
                    print("\n""The z-axis is moving...", flush = True)

                    time.sleep(2) # Reduce the burden of software running multiple times
                    
                    Pos_Z_Axis = Get_Axis_Current_Pos(Username, Z_Axis)
                    print(f"The z-axis current posistion {Pos_Z_Axis} mm.", flush = True)
                    
                    print(
                        "\n""1. Immediately stop moviing."
                        "\n""2. Let the z-axis go back home."
                        "\n""3. Continue."
                        )

                    sec_sub_cmd = "n"
                    sec_sub_cmd = input("Enter the value: ")

                    while True :
                        if sec_sub_cmd == "1" :

                            Response_Stop_Axis = Stop_Single_Axis(Username, Z_Axis, Stop_Mode)
                            print(f"The device response: {Response_Stop_Axis}.", flush = True)

                            break

                        elif sec_sub_cmd == "2" :

                            Distance_Z_Axis = ctypes.c_float(0.0)
                            Move_Speed_Back = ctypes.c_float(50.0)
                            Move_Acc_Back = ctypes.c_float(20.0)
                            Move_Dec_Back = ctypes.c_float(20.0)
                            Move_Mode_Back = ctypes.c_int(2)
                            Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed_Back, Move_Acc_Back, Move_Dec_Back, Move_Mode_Back)
                            
                            break

                        elif sec_sub_cmd == "3" :

                            break

                        else :
                            print("\n""Please type the correct value""\n")
                            sec_sub_cmd = input("Enter the value: ")

                elif sub_cmd == "4" :

                    break
                
                elif sub_cmd == "5" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}, Y-axis -> {Response_Moving_Single_Y_Axis}, Z-axis -> {Response_Moving_Single_Z_Axis}.", flush = True)
                    print("\n""The all axis are going to back home...""\n")

                    time.sleep(1)

                    Response_Close_Device = Close_Device(Username)
                    print("The program will close in 3 sec.", flush = True)
                    print("3", flush = True)
                    time.sleep(1)
                    print("2", flush = True)
                    time.sleep(1)
                    print("1", flush = True)
                    print("Have a good day !""\n"*5, flush = True)

                    break
                
                else :

                    print("\n""Please type the correct value""\n")
                    cmd = input("Enter the value: ")


        elif cmd == "3" :
            while True :
                
                Pos_X_Axis = Get_Axis_Current_Pos(Username, X_Axis)
                Pos_Y_Axis = Get_Axis_Current_Pos(Username, Y_Axis)
                Pos_Z_Axis = Get_Axis_Current_Pos(Username, Z_Axis)
                print(f"The x-axis current posistion {Pos_X_Axis} mm.", flush = True)
                print(f"The y-axis current posistion {Pos_Y_Axis} mm.", flush = True)
                print(f"The z-axis current posistion {Pos_Z_Axis} mm.", flush = True)

                time.sleep(0.5)

                print(
                    "\n""1. Move all axis go back to home."
                    "\n""2. Move x-axis go back to home."
                    "\n""3. Move y-axis go back to home."
                    "\n""4. Move z-axis go back to home."
                    "\n""5. Previous page."
                    "\n""6. Close the program."
                    )

                sub_cmd = 0
                sub_cmd = input("Enter the value: ")

                if sub_cmd == "1" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}, Y-axis -> {Response_Moving_Single_Y_Axis}, Z-axis -> {Response_Moving_Single_Z_Axis}.", flush = True)
                    print("\n""The all axis are going to back home...""\n")

                    time.sleep(0.5)

                elif sub_cmd == "2" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}", flush = True)
                    print("\n""The x-axis is going to back home...""\n")

                    time.sleep(1)

                elif sub_cmd == "3" :

                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: Y-axis -> {Response_Moving_Single_Y_Axis}", flush = True)
                    print("\n""The y-axis is going to back home...""\n")

                    time.sleep(1)        

                elif sub_cmd == "4" :

                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: Z-axis -> {Response_Moving_Single_Z_Axis}", flush = True)
                    print("\n""The z-axis is going to back home...""\n")

                    time.sleep(1)
                
                elif sub_cmd == "5" :

                    break

                elif sub_cmd == "6" :

                    Distance_X_Axis = ctypes.c_float(0.0)
                    Distance_Y_Axis = ctypes.c_float(0.0)
                    Distance_Z_Axis = ctypes.c_float(0.0)
                    Move_Speed = ctypes.c_float(50.0)
                    Move_Acc = ctypes.c_float(20.0)
                    Move_Dec = ctypes.c_float(20.0)
                    Move_Mode = ctypes.c_int(2)

                    Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
                    print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}, Y-axis -> {Response_Moving_Single_Y_Axis}, Z-axis -> {Response_Moving_Single_Z_Axis}.", flush = True)
                    print("\n""The all axis are going to back home...""\n")

                    time.sleep(1)

                    Response_Close_Device = Close_Device(Username)
                    print("The program will close in 3 sec.", flush = True)
                    print("3", flush = True)
                    time.sleep(1)
                    print("2", flush = True)
                    time.sleep(1)
                    print("1", flush = True)
                    print("Have a good day !""\n"*5, flush = True)

                    break

                else :

                    print("\n""Please type the correct value""\n")
                    cmd = input("Enter the value: ")

        elif cmd == "4" :

            Distance_X_Axis = ctypes.c_float(0.0)
            Distance_Y_Axis = ctypes.c_float(0.0)
            Distance_Z_Axis = ctypes.c_float(0.0)
            Move_Speed = ctypes.c_float(50.0)
            Move_Acc = ctypes.c_float(20.0)
            Move_Dec = ctypes.c_float(20.0)
            Move_Mode = ctypes.c_int(2)

            Response_Moving_Single_X_Axis = Move_Single_Axis(Username, X_Axis, Distance_X_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            Response_Moving_Single_Y_Axis = Move_Single_Axis(Username, Y_Axis, Distance_Y_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            Response_Moving_Single_Z_Axis = Move_Single_Axis(Username, Z_Axis, Distance_Z_Axis, Move_Speed, Move_Acc, Move_Dec, Move_Mode)
            print(f"The device response: X-axis -> {Response_Moving_Single_X_Axis}, Y-axis -> {Response_Moving_Single_Y_Axis}, Z-axis -> {Response_Moving_Single_Z_Axis}.", flush = True)
            print("\n""The all axis are going to back home...""\n")

            time.sleep(1)

            Response_Close_Device = Close_Device(Username)
            print("The program will close in 3 sec.", flush = True)
            print("3", flush = True)
            time.sleep(1)
            print("2", flush = True)
            time.sleep(1)
            print("1", flush = True)
            print("Have a good day !""\n"*5, flush = True)

            break

        else :

            print("\n""Please type the correct value""\n")
            cmd = input("Enter the value: ")

    else :

        print("Please open FMC4030-SDK.pdf to see return value definition.")
        print("The program will close in 3 sec.", flush = True)
        print("3", flush = True)
        time.sleep(1)
        print("2", flush = True)
        time.sleep(1)
        print("1", flush = True)
        print("Have a good day !""\n"*5, flush = True)

        break
