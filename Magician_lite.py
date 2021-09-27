#Robottens navn er Yusuf

from serial.tools import list_ports
import tkinter as tk
from tkinter import *
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

butt_height = 5
butt_width = 10

class Robot_gui(tk.Frame):

    #Starter hele programmet
    def __init__(self):
        super().__init__()

        #Variabler der styrer farven af knapperne
        self.new_fill = 'white'
        self.nr_red = 0
        self.nr_yellow = 0
        self.nr_green = 0
        self.nr_blue = 0

        #opstart af robotten
        available_ports = list_ports.comports()
        self.port = available_ports[0].device

        self.device = pydobot.Dobot(port=self.port, verbose=True)
        (x, y, z, r, j1, j2, j3, j4) = self.device.pose()

        #Variabler som robotten skal benytte
        self.w = 20
        self.xstart = x
        self.ystart = y
        self.zstart = z
        self.rstart = r-135
        self.xbias = 75
        self.ybias = -126
        self.zbias = 87

        self.initUI()


    #Laver UI'en til programmet
    def initUI(self):

        self.master.title("Ordre")
        self.grid(column=0, row=0)

        #Knapper der ændre hvilken farve du vil male med
        self.red_butt = tk.Button(self.master, text = 'Rød', command = lambda: self.set_color(2))
        self.red_butt.grid(column=5, row=5)
        self.yellow_butt = tk.Button(self.master, text = 'Gul', command = lambda: self.set_color(3))
        self.yellow_butt.grid(column=6, row=5)
        self.green_butt = tk.Button(self.master, text = 'Grøn', command = lambda: self.set_color(4))
        self.green_butt.grid(column=7, row=5)
        self.blue_butt = tk.Button(self.master, text = 'Blå', command = lambda: self.set_color(5))
        self.blue_butt.grid(column=8, row=5)
        self.blank_butt = tk.Button(self.master, text = 'Blank', command = lambda: self.set_color(1))
        self.blank_butt.grid(column=9, row=5)

        #Store knapper der repræsenterer kasserne på pallerne
        self.box1 = tk.Button(self.master,bg = 'red', height = butt_height, width = butt_width)
        self.box1.configure(command= lambda: self.change_color(self.box1))
        self.box1.grid(column=1, row=1)
        self.box2 = tk.Button(self.master,bg = 'yellow', height = butt_height, width = butt_width)
        self.box2.configure(command= lambda: self.change_color(self.box2))
        self.box2.grid(column=2, row=1)
        self.box3 = tk.Button(self.master,bg = 'green', height = butt_height, width = butt_width)
        self.box3.configure(command= lambda: self.change_color(self.box3))
        self.box3.grid(column=3, row=1)
        self.box4 = tk.Button(self.master,bg = 'blue', height = butt_height, width = butt_width)
        self.box4.configure(command= lambda: self.change_color(self.box4))
        self.box4.grid(column=4, row=1)

        self.box5 = tk.Button(self.master,bg = 'red', height = butt_height, width = butt_width)
        self.box5.configure(command= lambda: self.change_color(self.box5))
        self.box5.grid(column=1, row=2)
        self.box6 = tk.Button(self.master,bg = 'yellow', height = butt_height, width = butt_width)
        self.box6.configure(command= lambda: self.change_color(self.box6))
        self.box6.grid(column=2, row=2)
        self.box7 = tk.Button(self.master,bg = 'green', height = butt_height, width = butt_width)
        self.box7.configure(command= lambda: self.change_color(self.box7))
        self.box7.grid(column=3, row=2)
        self.box8 = tk.Button(self.master,bg = 'blue', height = butt_height, width = butt_width)
        self.box8.configure(command= lambda: self.change_color(self.box8))
        self.box8.grid(column=4, row=2)

        self.box9 = tk.Button(self.master,bg = 'red', height = butt_height, width = butt_width)
        self.box9.configure(command= lambda: self.change_color(self.box9))
        self.box9.grid(column=1, row=3)
        self.box10 = tk.Button(self.master,bg = 'yellow', height = butt_height, width = butt_width)
        self.box10.configure(command= lambda: self.change_color(self.box10))
        self.box10.grid(column=2, row=3)
        self.box11 = tk.Button(self.master,bg = 'green', height = butt_height, width = butt_width)
        self.box11.configure(command= lambda: self.change_color(self.box11))
        self.box11.grid(column=3, row=3)
        self.box12 = tk.Button(self.master,bg = 'blue', height = butt_height, width = butt_width)
        self.box12.configure(command= lambda: self.change_color(self.box12))
        self.box12.grid(column=4, row=3)

        self.box13 = tk.Button(self.master,bg = 'red', height = butt_height, width = butt_width)
        self.box13.configure(command= lambda: self.change_color(self.box13))
        self.box13.grid(column=1, row=4)
        self.box14 = tk.Button(self.master,bg = 'yellow', height = butt_height, width = butt_width)
        self.box14.configure(command= lambda: self.change_color(self.box14))
        self.box14.grid(column=2, row=4)
        self.box15 = tk.Button(self.master,bg = 'green', height = butt_height, width = butt_width)
        self.box15.configure(command= lambda: self.change_color(self.box15))
        self.box15.grid(column=3, row=4)
        self.box16 = tk.Button(self.master,bg = 'blue', height = butt_height, width = butt_width)
        self.box16.configure(command= lambda: self.change_color(self.box16))
        self.box16.grid(column=4, row=4)

        #Knappen der bruges til at sende ordren afsted
        self.send_order = tk.Button(self.master,bg='red',text='SEND ORDER',height=10,width=10)
        self.send_order.grid(column=10,row=2,rowspan=2)

    #Her bliver farven der skal males med sat
    def set_color(self, f):
        if f == 1:
            self.new_fill = 'white'
        elif f == 2:
            self.new_fill = 'red'
        elif f == 3:
            self.new_fill = 'yellow'
        elif f == 4:
            self.new_fill = 'green'
        elif f == 5:
            self.new_fill = 'blue'

    #Farven på knappen, der trykkes, ændres
    def change_color(self, button):
        button.configure(bg= self.new_fill)


    def calibrate(self):
        self.device.move_to(self.xstart, self.ystart, self.zstart, 0, wait = True)

    def reset(self):
        (self.x, self.y, self.z, self.r, self.j1, self.j2, self.j3, self.j4) = device.pose()
        self.device.move_to(x, y, z+40, r, wait = True)
        self.device.move_to(xstart, ystart, zstart, rstart, wait = True)


    def produktion(self, x1, y1, x2, y2, direction = 0):
        calibrate()

        xkoord = self.xstart + self.xbias + w*x1
        ykoord = self.ystart + self.ybias + w*y1
        self.device.move_to(xkoord, ykoord, zstart, rstart, wait = True)
        self.device.move_to(xkoord, ykoord, zstart-zbias, rstart, wait = True)
        sleep(1)
        self.device.suck(enable=True)

        reset()

        xkoord = self.xstart + self.xbias + w*x2
        ykoord = self.ystart - self.ybias
        self.device.move_to(xkoord, self.ystart+67, self.zstart, self.rstart+275, wait = True)
        self.device.move_to(xkoord, self.ystart+67, self.zstart-self.zbias, self.rstart+275, wait = True)
        sleep(1)
        self.device.suck(enable = False)

        reset()


def main():
    root = Tk()
    ex = Robot_gui()
    root.geometry("1920x1080")
    root.mainloop()


if __name__ == '__main__':
    main()




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
<<<<<<< HEAD
=======

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
>>>>>>> 99230e74ba77650aaf119b2e9578855cfe22912b
