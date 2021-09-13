#Robottens navn er Yusuf

from serial.tools import list_ports
import tkinter as tk
import pydobot
import sqlite3
from time import sleep

class dorobot():
    def __init__(self):
        #Code for database
        self.con = sqlite3.connect('start.db')
        
        try:
            c = self.con.cursor()
            self.con.execute("""CREATE TABLE ordre (
        		id INTEGER PRIMARY KEY AUTOINCREMENT,
        		indhold1 INTEGER,
                indhold2 INTEGER,
                udført INTEGER,
                movefrom INTEGER,
                moveto INTEGER)""")
            c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)",(2345234523452345,2000000000000000,0,1,0))
            c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)",(2345234523452345,2000000000000000,0,1,0))
        except Exception as e:
            print('Error Raised Ordre:')
        
        
            print(e)
            
        try:
            self.con.execute("""CREATE TABLE materialer (
        		id INTEGER PRIMARY KEY AUTOINCREMENT,
        		indhold INTEGER,
                xkoord INTEGER,
                ykoord INTEGER
                )""")
            c = self.con.cursor()
            c.execute("INSERT INTO materialer (indhold,xkoord,ykoord) VALUES (?,?,?)",(2345234523452345,0,0))
            c.execute("INSERT INTO materialer (indhold,xkoord,ykoord) VALUES (?,?,?)",(0000000000000000,0,0))
        
        except Exception as e:
            print('Error Raised materialer:')
            print(e)
    
        def getUnsolvedOrdre(self):
            c = self.con.cursor()
            ordreID = None
            c.execute("SELECT id FROM ordre WHERE udført = 0")
            for p in c:
                ordreID = p[0]
                break
            self.con.commit()
            return ordreID
            
        def solveOrdre(ordreID):
            c = self.con.cursor()
        
        
            output = c.execute("SELECT indhold1,indhold2,movefrom,moveto FROM ordre WHERE id = ?",[ordreID]).fetchall()
            indhold1 = output[0][0]
            indhold2 = output[0][1]
            idfrom = output[0][2]
            idto = output[0][3]
            
            pallet1 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idfrom]).fetchall()
            pallet2 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idto]).fetchall()
            self.con.commit()
        def get_digit(number, n):
            return number // 10**n % 10

#Code for moving robot
"""
available_ports = list_ports.comports()
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=True)
(x, y, z, r, j1, j2, j3, j4) = device.pose()

w = 20
xstart = x
ystart = y
zstart = z
rstart = r-135
xbias = 75
ybias = -126
zbias = 87


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
    sleep(1)
    device.suck(enable=True)

    reset()

    xkoord = xstart + xbias + w*x2
    ykoord = ystart - ybias
    device.move_to(xkoord, ystart+67, zstart, rstart+275, wait = True)
    device.move_to(xkoord, ystart+67, zstart-zbias, rstart+275, wait = True)
    sleep(1)
    device.suck(enable = False)

    reset()


tilstand = 0

produktion(0,0,0,0)
calibrate()
<<<<<<< HEAD
device.suck(enable = False)
=======
"""

print('hello world')
