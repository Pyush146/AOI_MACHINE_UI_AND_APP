import os

import shutil

import pandas as pd

import time

import alignment

from super_imposer import draw_annotations

import serial

from complete_ssh import image_capture

 

# Start the Alignement and Generate the All Neccessary CSV files for CNC movement.

 

s = serial.Serial(port='COM3',baudrate=115200)

if not s.isOpen():

    s.open()

    print('COM3 is open', s.isOpen())

 

def goto_position_relative(x_position_relative, y_position_relative, feed_rate):       #Goto Relative cordinates

    g_code = f"G00 X{x_position_relative} Y{y_position_relative} F{feed_rate}"

    s.write(bytes((g_code+'\n'), encoding='utf-8'))

    time.sleep(2)

 

def complete_jogger():

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

 

alignment.complete_alignment()

 

# Draw the Superimposed Standard Image Annotations.

 

draw_annotations()

 

# It is seen that when Raspberry camera is at 7 CM then External camera is at 25.5 CM on Scale.

# External Camera and Raspberry Camera is at same position on X axis only difference is on Y axis.

 

goto_position_relative(0, -185, 1000)

 

time.sleep(6)

 

complete_jogger()

 

s.write(bytes(("$H"+'\n'), encoding='utf-8'))

time.sleep(20)

s.close()

