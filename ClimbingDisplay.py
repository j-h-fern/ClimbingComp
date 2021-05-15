
import tkinter as Tkinter 
from datetime import datetime
import time
import adafruit_ssd1306 
import digitalio 
from PIL import Image, ImageDraw, ImageFont
import adafruit_bmp280
# from tkinter import *
import tkinter as tk
import board 
import busio

#initiliaze the i2c connection using the scl and sda pins 3&5 on the pi
i2c = busio.I2C(board.SCL,board.SDA)
#set the reset pin
rest_pin = digitalio.DigitalInOut(board.D4)
# init the firmware for the oled
oled = adafruit_ssd1306.SSD1306_I2C(128,32,i2c,reset=rest_pin)
# create the bmp pressure sensor object
pressSen= adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
# this sets the sea level pressure for altitude calculation reletive the mean global sea leavel
#pressure is 1013.25 using the local value would in crease accuracy
pressSen.sea_level_pressure = 1024
counter = -1
running = False
displayType = 0
dist=20
start_alt = pressSen.altitude
class TimeKeeper:
    start =0
    current =-1
    

    def __init__(self,) -> None:
        self.start = time.monotonic()
        self.current = self.start
        
        pass

    def Elasped(self):
        current = time.monotonic() - self.start
        return current

def counter_label(label): 
    def count(): 
        if running: 
            global counter 
    
            
            if counter==-1:             
                display="Starting..."
           
            if displayType == 0:
                tt = datetime.fromtimestamp(_time.Elasped())
                string = "Elapsed time" + tt.strftime("%M:%S")
                display=string 
                BlackScreen(oled,image)
                write(string,1)
                oled.image(image)
                oled.show() 
            if displayType == 1:
                string ="vertical speed  %0.2f m"%vert_speed(pressSen.altitude-start_alt,_time.Elasped())
                display=string
                BlackScreen(oled,image)
                write(string,1)
                oled.image(image)
                oled.show() 
            if displayType == 2:
                string = "Altitude:%0.2f m"%pressSen.altitude
                display = string
                BlackScreen(oled,image)
                write("Alt: %0.2f M"%pressSen.altitude,1)
                print("\nAltitude:%0.2f metere"%pressSen.altitude)
                oled.image(image)
                oled.show() 
            if displayType ==3:
                string = "Tempreture:%0.1f C"%pressSen.temperature
                display = string
                BlackScreen(oled,image)
                write("temp:%0.1f C"%pressSen.temperature,1)
                print("\nTempreture:%0.1f C"%pressSen.temperature)
                oled.image(image)
                oled.show()
    
            label['text']=display   
           
            label.after(1000, count)  
            counter += 1
    
    # Triggering the start of the counter. 
    count()      
    
# start function of the stopwatch 
def Start(label): 
    global running 
    running=True
    
    counter_label(label) 
    start['state']='disabled'
    stop['state']='normal'
    reset['state']='normal'
    
# Stop function of the stopwatch 
def Stop(): 
    global running 
    start['state']='normal'
    stop['state']='disabled'
    reset['state']='normal'
    running = False
    
# Reset function of the stopwatch 
def Reset(label): 
    global counter 
    counter=-1
    global _time
    _time = TimeKeeper()
    _time.__init__()
    
    # If rest is pressed after pressing stop. 
    if running==False:       
        reset['state']='disabled'
        label['text']='Welcome!'
    
    # If reset is pressed while the stopwatch is running. 
    else:                
        label['text']='Starting...'
def Speed():
    global displayType
    displayType=1
    timerBtn['state']='normal'
    SpeedBtn['state']='disabled'
    altBtn['state']='normal'
    tempBtn['state']='normal'

def Timer():
    global displayType
    displayType = 0
    timerBtn['state']='disabled'
    SpeedBtn['state']='normal'
    altBtn['state']='normal'
    tempBtn['state']='normal'

def Alt():
    global displayType
    displayType =2
    timerBtn['state']='normal'
    SpeedBtn['state']='normal'
    altBtn['state']='disabled'
    tempBtn['state']='normal'
def Temp():
    global displayType
    displayType =3
    timerBtn['state']='normal'
    SpeedBtn['state']='normal'
    altBtn['state']='normal'
    tempBtn['state']='disabled'
def vert_speed(dist,elasped):
    
    
    return((dist)/elasped)

def BlackScreen(oled,image):
	oled.fill(0)
	oled.show


	draw.rectangle((0,0,oled.width,oled.height), outline=0,fill=0)
	oled.image(image)
	oled.show

def write(text,textColour):
	font = ImageFont.load_default()
	(font_width,font_height)=font.getsize(text)
	draw.text((oled.width/2-font_width/2,oled.height/2-font_height/2),text,font=font , fill=textColour)
	print (text)
    
root = Tkinter.Tk() 
root.title("Climbing Computer") 
_time = TimeKeeper()
_time.__init__()
image = Image.new('1',(oled.width,oled.height))

draw = ImageDraw.Draw(image)


    
# Fixing the window size. 
root.minsize(width=500, height=70) 
label = Tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold") 
label.pack() 
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label)) 
stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop) 
reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(label))
SpeedBtn = Tkinter.Button(f,text='Speed', width=6,command=Speed)
timerBtn = Tkinter.Button(f,text='timer', width=6,command=Timer)
altBtn = Tkinter.Button(f,text='altitude', width=10,command=Alt)
tempBtn = Tkinter.Button(f,text='Tempreture', width=10,command=Temp)
f.pack(anchor = 'center',pady=5)
start.pack(side="left") 
stop.pack(side ="left") 
reset.pack(side="left")
SpeedBtn.pack(side="bottom")
timerBtn.pack(side="bottom")
altBtn.pack(side="bottom")
tempBtn.pack(side="bottom")

root.mainloop()