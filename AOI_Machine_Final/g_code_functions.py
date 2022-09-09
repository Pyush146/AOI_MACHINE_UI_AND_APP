import serial
import time

# This Function is defined to Make a serial connection between GRBL and Machine that sends the Command to GRBL the COM specified in this function may vary from Machine to Machine and can be modified by changing the port='COM7' value.


def serial_connection_establishment():
    global s
    # Below COM changes from Machine to Machine so Check Before Initializing the Program.
    s = serial.Serial(port='COM3',baudrate=115200)
    if not s.isOpen():
        s.open()
        print('COM3 is open', s.isOpen())

    # Code to Wake Up GRBL

    s.write(bytes("\r\n\r\n", encoding='utf-8'))

    # Code to Unlock the CNC Machine

    s.write(bytes("$X"+'\n', encoding='utf-8'))
    time.sleep(2)                                               # Wait for grbl to initialize
    s.flushInput() 

# This Function is defined to do Homing of The CNC Machine.

def home_position(feed_rate):
    s.write(bytes((f"$H" + '\n'), encoding='utf-8'))
    time.sleep(2)

# This Function is defined to goto the Absolute cordinates of CNC Machine.

def goto_position(x_position, y_position, feed_rate):     # Goto Absolute Cordinate
    g_code=  f"G01 X{x_position} Y{y_position} F{feed_rate}"
    s.write(bytes((g_code+'\n'), encoding='utf-8'))
    time.sleep(2)

# This Function is defined to Goto the Relative position of CNC machine from last Position.

def goto_position_relative(x_position_relative, y_position_relative, feed_rate):       #Goto Relative cordinates
    g_code = f"G00 X{x_position_relative} Y{y_position_relative} F{feed_rate}"
    s.write(bytes((g_code+'\n'), encoding='utf-8'))
    time.sleep(2)

# This function is defined to stop the work of CNC Machine and goto the Home Position.

def stop_work():
    home_position(feed_rate = 1000)
    time.sleep(20)
    s.close()
