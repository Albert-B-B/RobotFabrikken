#Robottens navn er Yusuf

from serial.tools import list_ports
import tkinter as tk
from tkinter import *
import pydobot
import sqlite3
from time import sleep

class dbClass():
    def __init__(self):
        #Code for database
        self.con = sqlite3.connect('start.db')
        self.palletSize = 16
        try:
            c = self.con.cursor()
            self.con.execute("""CREATE TABLE ordre (
        		id INTEGER PRIMARY KEY AUTOINCREMENT,
        		indhold1 INTEGER,
                indhold2 INTEGER,
                udført INTEGER,
                movefrom INTEGER,
                moveto INTEGER)""")
        #    c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)", (1345214523452345,1111121111111311,0,1,2))
            #c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)",(2345234523452345,2000000000000000,0,1,0))
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
            c.execute("INSERT INTO materialer (indhold,xkoord,ykoord) VALUES (?,?,?)",(1111111111111111,0,0))

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
        k = self.palletSize - n-1
        return number // 10**k % 10
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
                print(i)
                return False

        return True

    def addOrdre(self,palletID1,indhold1,palletID2,indhold2):
        c = self.con.cursor()
        c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)", (indhold1,indhold2,0,palletID1,palletID2))
        self.con.commit()

    def changeStatus(self,ordreID,value):
        c = self.con.cursor()
        c.execute("UPDATE ordre SET udført = ? WHERE id = ?",(value,ordreID))
        self.con.commit()
    def updatePallet(self,palletID,config):
        c = self.con.cursor()
        c.execute("UPDATE materialer SET indhold = ? WHERE id = ?",(config,palletID))
        self.con.commit()
    def solveOrdre(self,ordreID):
        c = self.con.cursor()


        output = c.execute("SELECT indhold1,indhold2,movefrom,moveto FROM ordre WHERE id = ?",[ordreID]).fetchall()
        indhold1 = output[0][0]
        indhold2 = output[0][1]
        idfrom = output[0][2]
        idto = output[0][3]

        pallet1 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idto]).fetchall()
        pallet2 = c.execute("SELECT indhold,xkoord,ykoord FROM materialer WHERE id=?",[idfrom]).fetchall()
        self.con.commit()

        #We check if ordre is valid
        print("Move stuff")
        print(indhold1)
        print(indhold2)
        print(pallet1[0][0])
        print(pallet2[0][0])
        #Order is valid and will be executed
        if self.validateOrdre(indhold1,indhold2,pallet1[0][0],pallet2[0][0]):
            moveList = []
            for i in range(self.palletSize):
                colorHex = self.get_digit(pallet1[0][0],i)
                if i == 0:
                    print(colorHex)
                if self.get_digit(indhold1,i) == self.get_digit(pallet1[0][0],i):
                    continue
                else:
                    for j in range(self.palletSize):
                        if i==0:
                            print("The one to rule em all")
                            print(colorHex)
                            self.get_digit(pallet2[0][0], j)
                        if colorHex == self.get_digit(indhold2, j) and self.get_digit(pallet2[0][0], j) == 1:
                            moveList.append([i%4,int((i-i%4)/4),j%4,int((j-j%4)/4),idto,idfrom,ordreID])
                            continue
            #self.changeStatus(ordreID, 1)
            self.updatePallet(idto, pallet1[0][0])
            self.updatePallet(idfrom, pallet2[0][0])
            return moveList
        #Order was invalid
        else:
            print("Whack job")
            self.changeStatus(ordreID, -1)


print('hello world')

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
        self.rstart = r
        self.r1 = r-135
        self.r2 = r+135
        self.xbias = 73
        self.ybias = -130
        self.ybias2 = 70
        self.zbias = 88

        self.initUI()
        self.timer = tk.Label(self.master, text="Hello world")
        self.timer.after(1000, self.main_mainloop)

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
        self.send_order = tk.Button(self.master,bg='red',text='SEND ORDER',height=10,width=10, command = lambda: self.order())
        self.send_order.grid(column=10,row=2,rowspan=2)

        self.box17 = tk.Button(self.master,bg='white', height = butt_height, width = butt_width)
        self.box17.configure(command= lambda: self.change_color(self.box17))
        self.box17.grid(column=12, row=1)
        self.box18 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box18.configure(command= lambda: self.change_color(self.box18))
        self.box18.grid(column=13, row=1)
        self.box19 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box19.configure(command= lambda: self.change_color(self.box19))
        self.box19.grid(column=14, row=1)
        self.box20 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box20.configure(command= lambda: self.change_color(self.box20))
        self.box20.grid(column=15,row=1)

        self.box21 = tk.Button(self.master,bg='white', height = butt_height, width = butt_width)
        self.box21.configure(command= lambda: self.change_color(self.box21))
        self.box21.grid(column=12, row=2)
        self.box22 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box22.configure(command= lambda: self.change_color(self.box22))
        self.box22.grid(column=13, row=2)
        self.box23 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box23.configure(command= lambda: self.change_color(self.box23))
        self.box23.grid(column=14, row=2)
        self.box24 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box24.configure(command= lambda: self.change_color(self.box24))
        self.box24.grid(column=15,row=2)

        self.box25 = tk.Button(self.master,bg='white', height = butt_height, width = butt_width)
        self.box25.configure(command= lambda: self.change_color(self.box25))
        self.box25.grid(column=12, row=3)
        self.box26 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box26.configure(command= lambda: self.change_color(self.box26))
        self.box26.grid(column=13, row=3)
        self.box27 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box27.configure(command= lambda: self.change_color(self.box27))
        self.box27.grid(column=14, row=3)
        self.box28 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box28.configure(command= lambda: self.change_color(self.box28))
        self.box28.grid(column=15,row=3)

        self.box29 = tk.Button(self.master,bg='white', height = butt_height, width = butt_width)
        self.box29.configure(command= lambda: self.change_color(self.box29))
        self.box29.grid(column=12, row=4)
        self.box30 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box30.configure(command= lambda: self.change_color(self.box30))
        self.box30.grid(column=13, row=4)
        self.box31 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box31.configure(command= lambda: self.change_color(self.box31))
        self.box31.grid(column=14, row=4)
        self.box32 = tk.Button(self.master,bg = 'white', height = butt_height, width = butt_width)
        self.box32.configure(command= lambda: self.change_color(self.box32))
        self.box32.grid(column=15, row=4)


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

    def order(self):
        color = self.box1['bg']
        color += self.box2['bg']
        color += self.box3['bg']
        color += self.box4['bg']
        color += self.box5['bg']
        color += self.box6['bg']
        color += self.box7['bg']
        color += self.box8['bg']
        color += self.box9['bg']
        color += self.box10['bg']
        color += self.box11['bg']
        color += self.box12['bg']
        color += self.box13['bg']
        color += self.box14['bg']
        color += self.box15['bg']
        color += self.box16['bg']


        color = color.replace('white', '1')
        color = color.replace("red", "2")
        color = color.replace('yellow', '3')
        color = color.replace('green', '4')
        color = color.replace('blue', '5')
        print(color)

        color2 = self.box17['bg']
        color2 += self.box18['bg']
        color2 += self.box19['bg']
        color2 += self.box20['bg']
        color2 += self.box21['bg']
        color2 += self.box22['bg']
        color2 += self.box23['bg']
        color2 += self.box24['bg']
        color2 += self.box25['bg']
        color2 += self.box26['bg']
        color2 += self.box27['bg']
        color2 += self.box28['bg']
        color2 += self.box29['bg']
        color2 += self.box30['bg']
        color2 += self.box31['bg']
        color2 += self.box32['bg']


        color2 = color2.replace('white', '1')
        color2 = color2.replace("red", "2")
        color2 = color2.replace('yellow', '3')
        color2 = color2.replace('green', '4')
        color2 = color2.replace('blue', '5')
        print(color2)

        self.db.addOrdre(1, int(color), 2, int(color2))

    def connect_database(self, database):
        self.db = database

    def calibrate(self):
        self.device.move_to(self.xstart, self.ystart, self.zstart, 0, wait = True)


    def produktion(self, x1, y1, x2, y2, direction = 0):
        self.calibrate()

        xkoord = self.xstart + self.xbias + self.w*x1
        ykoord = self.ystart + self.ybias + self.w*y1
        self.device.move_to(xkoord, ykoord, self.zstart, self.r1, wait = True)
        self.device.move_to(xkoord, ykoord, self.zstart-self.zbias, self.r1, wait = True)
        sleep(1)
        self.device.suck(enable=True)

        self.device.move_to(xkoord, ykoord, self.zstart, self.r1, wait = True)

        xkoord = self.xstart + self.xbias + self.w*x2
        ykoord = self.ystart + self.ybias2 + self.w*y2
        self.device.move_to(xkoord, ykoord, self.zstart, self.r2, wait = True)
        self.device.move_to(xkoord, ykoord, self.zstart-self.zbias, self.r2, wait = True)
        sleep(1)
        self.device.suck(enable = False)
        self.device.move_to(xkoord, ykoord, self.zstart, self.r2, wait = True)

        self.device.move_to(self.xstart, self.ystart, self.zstart, self.rstart, wait = True)

    def main_mainloop(self):

        order_check = self.db.getUnsolvedOrdre()
        if order_check != None:
            moves = self.db.solveOrdre(order_check)
            for i in moves:
                self.produktion(i[0],i[1],i[2],i[3])
            self.db.changeStatus(order_check,1)
            order_check = None
        self.timer.after(1000, self.main_mainloop)


def main():
    databaseRobot = dbClass()
    root = Tk()
    ex = Robot_gui()
    ex.connect_database(databaseRobot)
    root.geometry("1920x1080")
    root.mainloop()



if __name__ == '__main__':
    main()
