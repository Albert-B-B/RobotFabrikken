from serial.tools import list_ports
import tkinter as tk
import pydobot
from time import sleep

available_ports = list_ports.comports()
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)
(x, y, z, r, j1, j2, j3, j4) = device.pose()

w = 20
xstart = x
ystart = y
zstart = z
rstart = r-135
xbias = 76
ybias = -(6.3*w)
zbias = 80

def calibrate():
    device.move_to(xstart, ystart, zstart, 0, wait = True)

def reset():
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    device.move_to(x, y, z+40, r, wait = True)
    device.move_to(xstart, ystart, zstart, rstart, wait = True)


def produktion(x1, y1, x2, y2, direction = 0):
    calibrate()

    xkoord = xstart + xbias + w*x1
    ykoord = ystart + ybias + w*y1
    device.move_to(xkoord, ykoord, zstart, rstart, wait = True)
    device.move_to(xkoord, ykoord, zstart-zbias, rstart, wait = True)
    sleep(5)
    device.suck(enable=True)

    xkoord = xstart + xbias + w*x2
    ykoord = ystart - ybias - w*y2
    device.move_to(xkoord, ykoord, zstart, rstart, wait = True)
    device.move_to(xkoord, ykoord, zstart-zbias, rstart, wait = True)
    sleep(5)
    device.suck(enable = False)

    reset()

#device.suck(enable=False)
produktion(0,0,0,0)
calibrate()











"""
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
GRØN = 0
RØD = 0

while GRØN <= 5 and RØD <= 5:

    farve = input('Indtast hvilken farve: ')

    if farve == 'stop':
        device.close()
        break

#If statement that moves a green package if green is called
    if farve == 'grøn':
        device.move_to(x+50, y-69-GRØN*20, z-95, r, wait=True)
        device.suck(enable=True)
        device.move_to(x, y, z+100, r, wait=True)
        device.move_to(x+52, y+135-GRØN*20, z-90, r, wait=True)
        device.suck(enable=False)
        device.move_to(x, y, z, r, wait=True)
        GRØN += 1

#If statement that moves a red package if red is called
    elif farve == 'rød':
        device.move_to(x+70, y-69-RØD*20, z-96, r, wait=True)
        device.suck(enable=True)
        device.move_to(x, y, z+100, r, wait=True)
        device.move_to(x+70, y+135-RØD*20, z-90, r, wait=True)
        device.suck(enable=False)
        device.move_to(x, y, z, r, wait=True)
        RØD += 1


device.close()
"""
print('hello world')
