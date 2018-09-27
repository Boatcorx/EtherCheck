#!/usr/bin/python

"""
Goal: Wait for ethernet detection, then use tcpdump for switch & port info
Equipment for this build:
Raspberry PI
Adafruit 16x2 LCD plate
LCD Plate Library
portable power supply (battery bank)

How it works - start the script at bootup

Edit /etc/rc.local and add the following line at the end, before the line "exit 0":
home/pi/scripts/EtherCheck.py &

Script then waits for an ethernet connection:

Ethernet_Status=subprocess.check_output("sudo cat /sys/class/net/eth0/operstate|tr -d '\n' ", shell = True)

After a connection is detected, cdptump executes, and writes to a temporary file, for string manipulation:

os.system('sudo tcpdump -nn -v -i eth0 -s 1500 -c 1 ether[20:2] == 0x2000 > packet.txt ')

The Switch and Port info are then extracted from the txt file:

String1=commands.getoutput("grep -i vtp packet.txt")
a,Ethernet_Switch,c=String1.split("'")
print(Ethernet_Switch)
String1=commands.getoutput("grep -i port-id packet.txt")
#a,b,c,d,e,f,Ethernet_Port=String1.split("t")
a,b,c,d,e,f,String2=String1.split("t")
Ethernet_Port=String2.rstrip("'")
print(Ethernet_Port)

After it's complete, the switch and port info are displayed:

lcd.clear()
lcd.message(Ethernet_Switch)
lcd.message("\n")
lcd.message(Ethernet_Port)

Some housekeeping:

os.system('rm packet.txt')

Lather, Rinse, Repeat.

#setup Python
import os
import commands
import sys
import subprocess
import time
import Adafruit_CharLCD as LCD

#Initialize LCD
lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(1.0, 1.0, 1.0)
lcd.clear()

z=0
#start main program loop

while z==0:


        #Wait for ethernet
        # clear plate
        lcd.set_color(1.0, 1.0, 1.0)
        lcd.clear()
        lcd.message('Waiting for\n')
        lcd.message('Ethernet...')

        #check interface state with "sudo cat /sys/class/net/eth0/operstate"
        Ethernet_Status=subprocess.check_output("sudo cat /sys/class/net/eth0/operstate|tr -d '\n' ", shell = True)
        #print (Ethernet_Status)

        if Ethernet_Status== "up":
                lcd.clear()
                lcd.message("Connected\n")
                lcd.message("Sniffing...")

                #Wait for tcpdump
                os.system('sudo tcpdump -nn -v -i eth0 -s 1500 -c 1 ether[20:2] == 0x2000 > packet.txt ')



                #Get info from dump
		String1=commands.getoutput("grep -i vtp packet.txt")
                a,Ethernet_Switch,c=String1.split("'")
                print(Ethernet_Switch)
                String1=commands.getoutput("grep -i port-id packet.txt")
                #a,b,c,d,e,f,Ethernet_Port=String1.split("t")
                a,b,c,d,e,f,String2=String1.split("t")
                Ethernet_Port=String2.rstrip("'")
                print(Ethernet_Port)

                #output info
                lcd.clear()
                lcd.message(Ethernet_Switch)
                lcd.message("\n")
                lcd.message(Ethernet_Port)

                #remove packet.txt
                os.system('rm packet.txt')

                #wait for disconnect, start over
                Ethernet_Status=subprocess.check_output("sudo cat /sys/class/net/eth0/operstate|tr -d '\n' ", shell = True)
                print(Ethernet_Status)
                #break
                while (Ethernet_Status=="up"):
                        time.sleep(1)
                        Ethernet_Status=subprocess.check_output("sudo cat /sys/class/net/eth0/operstate|tr -d '\n' ", shell = True)
