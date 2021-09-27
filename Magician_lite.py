#Robottens navn er Yusuf

from serial.tools import list_ports
import tkinter as tk
import pydobot
import sqlite3
from time import sleep

class robotClass():
    def __init__(self):
        #Code for database
        self.palletSize = 16
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
    def get_digit(self,number, n):
        return number // 10**n % 10
    def getNumbDigits(self,pallet):
        total = [0,0,0,0,0]
        for i in range(self.palletSize):
            total[self.get_digit(pallet,i)-1] += 1
        return total
    def validateOrdre(self,pallet1,pallet2,pallet3,pallet4):
        p1t = self.getNumbDigits(pallet1)
        p2t = self.getNumbDigits(pallet2)
        p3t = self.getNumbDigits(pallet3)
        p4t = self.getNumbDigits(pallet4)

        for i in range(4):
            if p1t[i+1]+p2t[i+1]!= p3t[i+1]+p4t[i+1]:
                return False

        return True

    def solveOrdre(self,ordreID):
        c = self.con.cursor()


        output = c.execute("SELECT indhold1,indhold2,movefrom,moveto FROM ordre WHERE id = ?",[ordreID]).fetchall()
        indhold1 = output[0][0]
        indhold2 = output[0][1]
        idfrom = output[0][2]
        idto = output[0][3]

        pallet1 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idfrom]).fetchall()
        pallet2 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idto]).fetchall()
        self.con.commit()

        #We check if ordre is valid
        if self.validateOrdre(indhold1,indhold2,pallet1,pallet2):
            pass
robot = robotClass()
robot.solveOrdre(robot.getUnsolvedOrdre())

#Start konfigurationen er farverne i rækkefølgen Rød, gul, grøn og blå.
#Det er det for alle rækker


#Code for database
con = sqlite3.connect('start.db')

try:
    con.execute("""CREATE TABLE ordre (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		indhold1 INTEGER,
        indhold2 INTEGER,
        udført INTEGER,
        movefrom INTEGER,
        moveto INTEGER)""")
except Exception as e:
    print('Error Raised:')
    print(e)

try:
    con.execute("""CREATE TABLE materialer (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		indhold INTEGER,
        xkoord INTEGER,
        ykoord INTEGER
        )""")
except Exception as e:
    print('Error Raised:')
    print(e)

#Code for moving robot
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
device.suck(enable = False)





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
