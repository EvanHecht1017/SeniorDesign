## Senior Design Semester 2 Repo


### Use

To connect to the printer you must use 32-bit python. I am using 3.11.7 32-bit. 

Make sure the FMC4030 folder is in your C: Drive otherwise you will have to rest the path in the python files. 

Run ping 192.168.0.30 in CMD to check and see if you are connected to the printer 

The printer scales inputs by 1/10. So we have to add "Distance_X_Axis_Machine = ctypes.c_float(Distance_X_Axis * 10) into our inputs"

The current gcode path is hardcoded in the python script. To use your own gcode, replace the file path with your desired path.

Once you have that complete, you can run `python3 gcode.py` in your terminal.
