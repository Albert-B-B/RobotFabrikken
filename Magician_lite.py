#Robottens navn er Yusuf

from serial.tools import list_ports
import tkinter as tk
import pydobot
import sqlite3
from time import sleep

class dbClass():
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
            c.execute("INSERT INTO ordre (indhold1,indhold2,udført,moveto,movefrom) VALUES (?,?,?,?,?)", (1345234523452345,2111111111111111,0,1,2))
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
                print(i)
                return False

        return True
    def changeStatus(self,ordreID,value):
        c = self.con.cursor()
        c.execute("UPDATE ordre SET udført = ? WHERE id = ?",(value,ordreID))        
        self.con.commit()
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
        print(indhold1)
        print(indhold2)
        print(pallet1[0][0])
        print(pallet2[0][0])
        #Order is valid and will be executed
        if self.validateOrdre(indhold1,indhold2,pallet1[0][0],pallet2[0][0]):
            self.changeStatus(ordreID, 1)
        #Order was invalid
        else:
            self.changeStatus(ordreID, -1)
robot = dbClass()
print(robot.getUnsolvedOrdre())
robot.solveOrdre(robot.getUnsolvedOrdre())

print('hello world')
