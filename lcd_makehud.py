#!/usr/bin/python
# Raspberry Pi Heads up display

# Add required Libraries, time for sleep, Adafruit_CharLCD for LCD Plate
import time
import Adafruit_CharLCD as LCD

# Python System Calls
from sys import exit
from sys import argv as sysargs

# System CMD Output parsing
import subprocess
import re

# Add interface stats
import socket, fcntl, struct

# fetch MAC Address from /sys/class, file i/o handling, takes an interface name, will return error
def getMACAddr(ifname):
    try:
        with open('/sys/class/net/' + ifname + '/address') as f:
            charList = f.read().split(':')
            return '.'.join([charList[i - 1] + charList[i] for i in range (1, len(charList), 2)])
    except IOError as ioerror:
        dbg.write('IOError ' + ioerror + ' found!')
        return 'IOError ' + ioerror + ' found!'
    except:
        dbg.write('Unexpected error ' + sys.exc_info()[0])
        return 'Unexpected error ' + sys.exc_info()[0]

# fetch IP Address from iputils, takes an interface name, will return errors
def getIPAddr(ifname):
    try:
        ipAddrOut = subprocess.Popen(['ip', 'addr', 'show', 'dev', ifname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ipAddrOut.communicate()
        return re.findall(r"\d{1,3}(?:\.\d{1,3}){3}", repr(stdout))[0]
    except:
        dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
        return 'Failed'

# get RPi Die Temperature
def getDieTemp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            readableTemp = float(f.read())/1000.
            return repr(readableTemp) + 'C'
    except:
        dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
        return 'Failed'

# get RPi Core Max Freq
def getCoreMaxFreq():
    try:
        with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq') as f:
            readableCoreMaxFreq = float(f.read())/1000000.
            return repr(readableCoreMaxFreq) + 'gHz'
    except:
        dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
        return 'Failed'

# get Rpi Hostname
def getSystemHostName():
    try:
        with open('/etc/hostname') as f:
            return str(f.read())
    except:
        dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
        return 'Failed'


# combine IP and MAC
def getIPMAC(ifname):
    try:
        dbg.write('Writing \n' + getIPAddr('eth0') + '\n' + getMACAddr('eth0') + '\n To screen! \n')
        return getIPAddr('eth0') + '\n' + getMACAddr('eth0')
    except OSError as oserror:
        dbg.write('OS Error Found: {0}'.format(err) + '\n')
        return 1
    except:
        dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
        return 2

#combine hostname, CPU Governor, and Temp
def getHUDPrintout():
    return getSystemHostName() + getCoreMaxFreq() + '   ' + getDieTemp()

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()

# Setup Debug output

dbg = open("/var/log/lcd_log-" + str(time.strftime('%y%m%d')), 'w')
print(dbg)
dbg.write('*** DEBUG FILE START ***\n')

# Do the actual things

# test display, wait 3 seconds for DHCP to catch up
lcd.clear()
dbg.write('Boot test\nStartup Complete!\n')
lcd.message('Boot test\nStartup complete!')
time.sleep(3)
lcd.clear()
dbg.write(getHUDPrintout() + '\n')
lcd.message(getHUDPrintout())

# Handle some events, maybe even a menu

try:
    # Event Handler
    while True:
        # Menu tree root
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            dbg.write(getIPMAC('eth0') + '\n')
            lcd.message(getIPMAC('eth0'))
        elif lcd.is_pressed(LCD.LEFT):
            lcd.clear()
            dbg.write('LEFT Pressed!')
            lcd.message('LEFT Pressed!')
        elif lcd.is_pressed(LCD.RIGHT):
            lcd.clear()
            dbg.write('RIGHT Pressed!')
            lcd.message('RIGHT Pressed!')
        elif lcd.is_pressed(LCD.UP):
            lcd.clear()
            dbg.write('UP Pressed!')
            lcd.message('UP Pressed!')
        elif lcd.is_pressed(LCD.DOWN):
            lcd.clear()
            dbg.write('DOWN Pressed!')
            lcd.message('DOWN Pressed!')

except:
    dbg.write('Unexpected Error: ' + sys.exc_info()[0] + '\n')
    exit()


# Close debug file gracefully
dbg.close()

exit()
