# lcdplate
Adafruit CharLCD Project

Uses Adafruit's CharLCD Library:
https://github.com/adafruit/Adafruit_Python_CharLCD

Adafruit's CharLCD library is completely unmodified and is only used here as a matter of installation convenience.

# TODO

 - Add installation Script
 - Add menus and stuff for the case handler
 - Use case statements
 - Find cool applications for this
 - Make things pretty

# Setup

mkdir /usr/lib/python/lcdplate
cp lcd_makehud.py /usr/lib/python/lcdplate
cp Adafruit_CharLCD.py /usr/lib/python/lcdplate
cp alert-hud.service /etc/systemd/system/
systemctl daemon-reload
chmod 744 /usr/lib/python/lcdplate/lcd_makehud.py


