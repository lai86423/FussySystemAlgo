import matplotlib.pyplot as plt
import numpy as np
import math
from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from fussySys import fussySystem
from carMoving import Moving

class Application():
    def __init__(self): 
        self.fig, self.ax = plt.subplots(1, 1, figsize=(4.5, 6))
        self.point = np.loadtxt("case01.txt", delimiter=',', skiprows=3)
        # self.point = [[-6,-3],[-6,22],[18,22],[18,50],[30,50],[30,10],[6,10],[6,-3],[-6,-3]]
        self.DrawMap() 

    def DrawMap(self):
        plt.xlim(-10, 35 ,1)
        plt.ylim(-10,55,1)
        my_x_ticks = np.arange(-6, 33, 3)
        my_y_ticks = np.arange(-3,53, 3)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)


        for i in range(len(self.point)-1):
            self.ax.plot([self.point[i][0],self.point[i+1][0]],[self.point[i][1],self.point[i+1][1]],'b')

        self.ax.plot([18, 30], [40, 37], 'r')
        self.ax.plot([-7, 7], [0,0 ], 'k')

    def DrawCar(self,posX,posY,phi):
        self.circle=plt.Circle((posX,posY),3, color='r', fill=False)
        self.ax.add_artist(self.circle)
        self.line = self.ax.plot([posX,posX+(math.cos(phi / 180 * math.pi))*4],[posY,posY+math.sin(phi / 180 * math.pi)*4], 'r')

def Main():
    print("================================Start From here================================")      
    draw=Application()
    car=Moving(0,0,90)
    x,y,phi=car.x,car.y,car.phi
    plt.ion()
    plt.show()        
    fussySys=fussySystem()
    steerDegree=10

    while (car.DetectWall()!=False):
        x,y,phi = car.UpdataPos(steerDegree)
        
        F_minDis=car.CountWallDis(draw.point,x,y,phi)
        
        
        R_minDis=car.CountWallDis(draw.point,x,y,phi-45)
        
        L_minDis=car.CountWallDis(draw.point,x,y,phi+45)
        
        #模糊系統-----
        all_FS = fussySys.FiringStrength(R_minDis-L_minDis,F_minDis)
        
        output=fussySys.Defuzzification(all_FS)
        
        steerDegree = fussySys.CenterOfGravity(output)
        if R_minDis-L_minDis<0:
            steerDegree = - steerDegree
        
        # data=open("train4D.txt",'w+') 
        # print(self.F_minDis,self.R_minDis,self.L_minDis,steerDegree,file=data)
        # print("\n",file=data)                
        # data.close()
        #f = open("train4D.txt",'a')
        #f.write('asd')
        #f.close()
        
        draw.DrawCar(x,y,phi)
        plt.show()
        plt.pause(0.1)
        print(F_minDis)
        var.set(F_minDis)
        #ShowDis_label1.config(text=round(F_minDis))
        draw.circle.remove()
        #self.line.remove()  #待解 移除圓的線
    plt.pause(0)
       
#GUI
#介面基本設定
window= tk.Tk()
window.geometry('200x200')
window.title('HW1-FussySystem')

label_top = tk.Label(window,text = "Choose Trail file")
label_top.pack()         

#開始訓練按鈕


Dis_frame = tk.Frame(window)
Dis_frame.pack(side=tk.TOP)

Dis_label1 = tk.Label(Dis_frame,text='Front Distance')
Dis_label1.pack(side=tk.LEFT)

var = tk.StringVar()
ShowDis_label1 = tk.Label(Dis_frame, textvariable=var)
ShowDis_label1.pack(side=tk.LEFT)

button_start = tk.Button(window,text='開始',command=Main)
button_start.pack()

window.mainloop()