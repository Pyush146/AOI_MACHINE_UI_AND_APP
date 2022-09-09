import shutil
import time
import pandas as pd
import serial
from complete_ssh import image_capture
import os

s = serial.Serial(port='COM3',baudrate=115200)
if not s.isOpen():
        s.open()
        print('COM7 is open', s.isOpen())
# This Function is defined to move the CNC Machine to the position relative to the last machine cordinates.

def goto_position_relative(x_position_relative, y_position_relative, feed_rate):   #Goto Relative cordinates
    g_code = f"G00 X{x_position_relative} Y{y_position_relative} F{feed_rate}"
    s.write(bytes((g_code+'\n'), encoding='utf-8'))
    time.sleep(4)

# Opening a Serial Port to Establish a connection Between GRBL and Input Machine.
# COM7 Specified may be vary with different connections and Machine port='COM7' has to be changed according to the Different Interfacing Machine.

def g_code_component():

    # Below COM changes from Machine to Machine so Check Before Initializing the Program 

    # Read the CSV File generated in alignment.py file to Get the Desired CNC Movements.

    tr_csv = pd.read_csv("cnc_movements.csv")
    data = tr_csv['CNC_movements'].to_numpy()

    # Transform Cordinates to Get X and Y axis movements in Float Values.

    for cordinate in data:
        cordinate = cordinate.replace(']', '')
        cordinate = cordinate.replace('[', '')
        cordinate = cordinate.split(" ")
        for i in cordinate:
            try:
                cordinate.remove('')
            except:
                pass

    # Calling the above defined Function to Relatively Move the CNC Head to Goto Center of Every Component. 

        goto_position_relative(cordinate[0], cordinate[1], 1000)
        time.sleep(2)

        # Captures The Image of Component.
        
        image_capture()
        time.sleep(2)

        # Stores the Component Image In The Component_image_folder by Renaming it Properly.

        shutil.move('Picture.jpg', 'Component_image_folder/Picture.jpg')
        os.rename('Component_image_folder/Picture.jpg', f'Component_image_folder/Component_at_{cordinate[0]}_{cordinate[1]}.jpg')

    # Get CNC Machine to The homing Position Otherwise The Zero Work offset of the Machine will get Changed.

    s.write(bytes(("$H"+'\n'), encoding='utf-8'))

    # This delay function is introduced because the Command sent to the CNC Machine will take time to get excecuted and if serial connection to the Machine get closed before completion of work then machine will stop

    time.sleep(20)

    # At the End of The Work Close the Serial GRBL Connection to the Machine.

    s.close()
