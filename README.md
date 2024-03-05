# Modular Additive Manufacturing Device

This project provides Python scripts for both manually controlling a FUYU FMC4030 gantry system as well as interpreting G-code commands from a file and controlling a machine's movement in real-time along the X, Y, and Z axes. It is designed to interface with hardware through a low-level API, executing precise movements based on the parsed G-code instructions and/or keyboard control.

As well, this repository contains a python3 script that can convert a DXF file to a series of Gerber and Excellon files suitable for e.g. PCB Train. This script was leveraged from a now non-usable script built as a now-deprecated Python 2 script.

## Connection

To establish a connection with the printer, it is essential to use a 32-bit version of Python, specifically version 3.11.7 (32-bit).
Run ping 192.168.0.30 in CMD to verify connection to the printer 

## FYI

The printer interprets inputs at a scale of 1/10th. Therefore, it's crucial to adjust your inputs accordingly by incorporating the line Distance_X_Axis_Machine = ctypes.c_float(Distance_X_Axis * 10) into your code.

## Custom Set-up

The path to the G-code file is currently hardcoded within the script. To utilize a custom G-code file, you should update the script with your file's specific path.

After configuring the setup as described, execute the command python3 gcode.py in your terminal to run the script.

To enable keyboard control functionalities found in the keyboard_movement.py script, execute `pip install keyboard`.

## Dev container

This project is configured to run through GitHub Workspaces. To learn more, please go to `https://github.com/features/codespaces`

## Usability

To run the Keyboard movement script, run the command `python3 Keyboard_movement.py` and use your arrow keys in the following design:

To move up: Press the `up arrow key`

To move down: Press the `down arrow key`

To move right: Press the `right arrow key`

To move left: Press the `left arrow key`

To run the GCode_Movement.py script, run the command `python3 GCode_Movement.py ${gcode_file_path}` with `${gcode_file_path}` being the location of your desired GCode movement file.

## Credits

This project is currently being developed by Evan Hecht, Ian Graham, Jack McKain, and Zach Higgins under the guidance of Dr. Yeongin Kim.
Credit to the inital QGC movement program goes to Qun-Gao Chen.