# importing only those functions
# which are needed
#python libraries used
from tkinter import *
import tkinter
from tkinter.ttk import *
from time import strftime
from turtle import down, left
from PIL import Image, ImageTk
import cv2
from matplotlib.pyplot import annotate, step
import webbrowser
import os
import serial
import time
import csv
import shutil
import webview
from ipaddress import ip_address
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import webbrowser
import tkinter.messagebox
from tkinterweb import HtmlFrame
from threading import Timer
global x
x=0
global y
y=0
# creating tkinter window
root = Tk()
root.geometry("1300x900")
root.title('Menu Demonstration')

# Creating Menubar
menubar = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label ='New File', command = None)
file.add_command(label ='Open...', command = None)
file.add_command(label ='Save', command = None)
file.add_separator()
file.add_command(label ='Exit', command = root.destroy)

# Adding Edit Menu and commands
edit = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Edit', menu = edit)
edit.add_command(label ='Cut', command = None)
edit.add_command(label ='Copy', command = None)
edit.add_command(label ='Paste', command = None)
edit.add_command(label ='Select All', command = None)
edit.add_separator()
edit.add_command(label ='Find...', command = None)
edit.add_command(label ='Find again', command = None)

# Adding Help Menu
help_ = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help_)
help_.add_command(label ='Tk Help', command = None)
help_.add_command(label ='Demo', command = None)
help_.add_separator()
help_.add_command(label ='About Tk', command = None)

# display Menu
root.config(menu = menubar)

#Camera screen
label =Label(root)
label.grid(row=1, column=0,sticky=NW)
cap= cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 100)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)

# Define function to show frame

def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   cv2.imwrite("Captured_Image.jpg",cv2image)
   shutil.move("Captured_Image.jpg", "Captured_Image_Folder/Captured_Image.jpg")
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

def show_frames_1():
   # Get the latest frame and convert into Image
   cv2image_1= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img_1 = Image.fromarray(cv2image_1)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img_1)
   cv2.imwrite("Standard_Image.jpg",cv2image_1)
   shutil.move("Standard_Image.jpg", "Standard_Image_Folder/Standard_Image.jpg")
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

# capture image
capture = Button(root, text = 'CAPTURE',command = show_frames)
capture.grid(row=0,column=0,sticky=SW)

# Standard Capture

stdcap = Button(root, text = 'STANDARD CAPTURE',command = show_frames_1)
stdcap.grid(row=0,column=0,sticky=S,padx=(0,400),pady=(0,25))

#xy_coordinates
Label(root,text="X").grid(row=0,column=0,sticky=S,padx=(0,250))
Label(root,text="Y").grid(row=0,column=0,sticky=S,padx=(0,0))
xc=Entry(root,width=10)
yc=Entry(root,width=10)
xc.grid(row=0,column=0,sticky=S,padx=(0,150))
yc.grid(row=0,column=0,sticky=S,padx=(75,0))
def show_x():
    global x
    xc.delete(0,END)
    xc.insert(0,x)
def show_y():
    global y
    yc.delete(0,END)
    yc.insert(0,y)

#Feed rate slider
v1= IntVar()
def sc1(event):
    vl1.configure(text="Feed "+str(v1.get()))
s1=Scale(root,variable=v1,from_=0, to=1000,orient=VERTICAL,command=sc1)
s1.set(500)
s1.grid(row=1,column=0,sticky=NE,pady=50,padx=(0,50))
# value label
vl1 =Label(root,text="Feed "+str(v1.get()))
vl1.grid(row=1,column=0,sticky=NE,pady=30,padx=(0,50))
p1=str(v1.get())

#Step size slider
v2= IntVar()
def sc2(event):
    vl2.configure(text="Step "+str(v2.get()))
    
s2=Scale(root,variable=v2,from_=0, to=20,orient=VERTICAL,command=sc2)
s2.set(5)
s2.grid(row=1,column=0,sticky=N,pady=50,padx=(200,0))
# value label
vl2 =Label(root,text="Step "+str(v2.get()))
vl2.grid(row=1,column=0,sticky=N,pady=30,padx=(200,0))
p2=str(v2.get())

#serial connection wwith GRBL
s = serial.Serial(port='COM3',baudrate=115200)
if not s.isOpen():
    s.open()
    print('COM3 is open', s.isOpen())
    # Wake up grbl
s.write(bytes("\r\n\r\n", encoding='utf-8'))
time.sleep(2)                                       # Wait for grbl to initialize
s.flushInput()                                      # Flush startup text in serial input
s.write(bytes(("$X" + '\n'), encoding='utf-8'))     # Unlock GRBL to make Machine Work
s.write(bytes(("G10 L20 P1 X0 Y0" + '\n'), encoding='utf-8'))
feed=str(v1.get())
step=str(v2.get())
step1=v2.get()

#JOGGING BUTTONS
#home button
def home():
        feed=str(v1.get())
        step=str(v2.get())
        step1=v2.get()

        s.write(bytes(("G90 G01 X0 Y0 F500" + '\n'), encoding='utf-8'))
        grbl_out = s.readline()
        print(' : ' + str(grbl_out.strip()))
        global x
        global y
        x=0
        y=0
        show_x()
        show_y()
home = Button(root, text = 'HOME',command =home)
home.grid(row=1, column=0, pady=(175,0))

#up
def u():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()

    gcode = 'G91 G01 X'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x+=step1
    y+=0
    show_x()
    show_y()
up = Button(root, text = 'UP',command = u)
up.grid(row=1,column=0,pady=(125,0))    

#down
def d():
     feed=str(v1.get())
     step=str(v2.get())
     step1=v2.get()
     gcode = 'G91 G01 X-'+step+' F'+feed
     s.write(bytes((gcode + '\n'), encoding='utf-8'))
     grbl_out = s.readline()
     print(' : ' + str(grbl_out.strip()))
     global x
     global y
     x-=step1
     y+=0
     show_x()
     show_y()
down = Button(root, text = 'DOWN',command = d)
down.grid(row=1,column=0,pady=(225,0))   

#left
def l():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 Y'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x+=0
    y+=step1
    show_x()
    show_y()
left = Button(root, text = 'LEFT',command = l)
left.grid(row=1,column=0,padx=(0,150),pady=(175,0))

#right
def r():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 Y-'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x+=0
    y-=step1
    show_x()
    show_y()
right = Button(root, text = 'RIGHT',command = r)
right.grid(row=1,column=0,padx=(150,0),pady=(175,0))    

#upper left
def ul():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 X'+step+' Y'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x+=step1
    y+=step1
    show_x()
    show_y()
up_left = Button(root, text = 'UP-LEFT',command = ul)
up_left.grid(row=1,column=0,padx=(0,150),pady=(125,0))

#upper right
def ur():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 X'+step+' Y-'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x+=step1
    y-=step1
    show_x()
    show_y()
up_right = Button(root, text = 'UP_RIGHT',command = ur)
up_right.grid(row=1,column=0,padx=(150,0),pady=(125,0))

#down right
def dr():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 X-'+step+' Y-'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x-=step1
    y-=step1
    show_x()
    show_y()
down_right = Button(root, text = 'DOWN-RIGHT',command = dr)
down_right.grid(row=1,column=0,padx=(150,0),pady=(225,0))

#down left
def dl():
    feed=str(v1.get())
    step=str(v2.get())
    step1=v2.get()
    gcode = 'G91 G01 X-'+step+' Y'+step+' F'+feed
    s.write(bytes((gcode + '\n'), encoding='utf-8'))
    grbl_out = s.readline()
    print(' : ' + str(grbl_out.strip()))
    global x
    global y
    x-=step1
    y+=step1
    show_x()
    show_y()
down_left = Button(root, text = 'DOWN-LEFT',command = dl)
down_left.grid(row=1,column=0,padx=(0,150),pady=(225,0))

#Annotation
#open image in s3a
def s3a():
    try:
        shutil.copy('Standard_Image_folder/Standard_Image.jpg', 'C:\\Users\Relax\.s3a\s3aprj\images')
    except:
        pass
    os.system('py -m s3a --image="Standard_Image.jpg"')
annotate = Button(root, text = 'ANNOTATE',command = s3a)
annotate.grid(row=1,column=0,sticky=W,pady=(300,0))

#Default table
def default():
    frame2 = Frame(root)
    frame2.grid(row=0,column=0,sticky=N) 
    TableMargin = Frame(frame2)
    TableMargin.pack(side=TOP)
        #scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    scrollbary.pack(side=RIGHT, fill=Y)
    tree =Treeview(TableMargin, columns=("empId", "name", "Address"), yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree.yview)
        #scrollbarx.config(command=tree.xview)
        #scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('empId', text="Instance ID", anchor=W)
    tree.heading('name', text="Image File", anchor=W)
    tree.heading('Address', text="Vertices", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=75)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()
    frame1 = Frame(root)
    frame1.grid(row=0,column=1,rowspan=4,columnspan=4,pady=(0,200))
    fr=HtmlFrame(frame1)
    fr.load_website("http://www.google.com") #load a website
    fr.pack(fill=BOTH,expand=YES)
    show_x()
    show_y()
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    cv2.imwrite("pic.png",cv2image)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    label.after(20, show_frames)


#Annotate Table
def table():
    frame2 = Frame(root)
    frame2.grid(row=0,column=0,sticky=N) 
    TableMargin = Frame(frame2)
    TableMargin.pack(side=TOP)
    #scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    scrollbary.pack(side=RIGHT, fill=Y)
    tree =Treeview(TableMargin, columns=("empId", "name", "Address"), yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree.yview)
    #scrollbarx.config(command=tree.xview)
    #scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('empId', text="Instance ID", anchor=W)
    tree.heading('name', text="Image File", anchor=W)
    tree.heading('Address', text="Vertices", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=75)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()
    
    with open('annotations/Standard_Image.jpg.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            empId = row['Instance ID']
            name = row['Image File']
            address = row['Vertices']
            tree.insert("", 0, values=(empId, name, address))
table_annotate = Button(root, text = 'ANNOTATE TABLE',command = table)
table_annotate.grid(row=1,column=0,sticky=W,padx=(75,0),pady=(300,0))

clear = Button(root, text = 'CLEAR',command = default)
clear.grid(row=1,column=0,sticky=W,padx=(200,0),pady=(300,0))



"""x=0
y=0
Label(root,text="X").grid(row=1,column=0,sticky=N)
Label(root,text="Y").grid(row=1,column=0,sticky=N,pady=(0,50))
xc=Entry(root)
yc=Entry(root)
xc.grid(row=1,column=0,sticky=N,padx=(0,50))
yc.grid(row=1,column=0,sticky=N,padx=(0,50),pady=(0,50))
def show_x():
    xc.insert(0,x)
show_x()"""

#Web view of camera
def sshweb():
    ip='169.254.113.51'
    user='pi'
    password='raspberry'
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    if session.active:
        #print(True)
        session.exec_command('"sudo python3 /home/pi/pi-camera-stream-flask/main.py"')
        webbrowser.open('http://169.254.113.51:5000/')

#Camera View
def preview():
    frame1 = Frame(root)
    frame1.grid(row=0,column=1,rowspan=4,columnspan=4,pady=(0,200))
    fr=HtmlFrame(frame1)
    ip='169.254.113.51'
    user='pi'
    password='raspberry'
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    session = client.get_transport().open_session()
    fr.pack(fill=BOTH,expand=YES)
    if session.active:
        #print(True)
        session.exec_command('python "/home/pi/pi-camera-stream-flask/main.py"')
    fr.load_website("http://169.254.113.51:5000/") #load a website
    
camview = Button(root, text = 'Camera View',command = preview)
camview.grid(row=1,column=0,sticky=SW)

def mainpy():
    s.close()


    os.system('py .\main.py')
align = Button(root, text = 'Alignment',command = mainpy)
align.grid(row=1,column=0,sticky=S)

default()
mainloop()