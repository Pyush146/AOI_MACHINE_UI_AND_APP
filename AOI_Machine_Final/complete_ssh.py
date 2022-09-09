from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import time
import webbrowser

# User Name and Password is Static for a Particular Raspberry Pi but IP is Changing as Static IP is not Generated.

ip='169.254.113.51'
user='pi'
password='raspberry'

# Python code to Capture the Image by Raspberry Pi camera by Establishing the Connection with Raspberry Pi using the SSH (Secure Shell Protocol).

def image_capture():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('python "/home/pi/camera.py"')
    time.sleep(2)
    with SCPClient(client.get_transport()) as scp:
        scp.get('picture.jpg')
    client.close()

# Python Code to Turn on The lights mounted on Head as Sequence of RED, GREEN, BLUE to get Correct image by camera.

def light_on():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('"/home/pi/led_on.py"')
    client.close()

# Python Code to Turn off the Lights mounted on Head.

def light_off():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('"/home/pi/led_off.py"')
    client.close()

# This Function is defined to Get Camera preview of Raspberry Pi

def camera_preview():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('"sudo python3 /home/pi/pi-camera-stream-flask/main.py"')
    client.close()
    ip_address=f"http://{ip}:5000/"
    webbrowser.open('http://{ip}:5000/')

# This function is Defined to Turn on The light mounted in Head as White Light not as Sequential Combination of RED, GREEN, BLUE.

def white_light_on():
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('"/home/pi/white_led_on.py"')
    client.close()


image_capture()