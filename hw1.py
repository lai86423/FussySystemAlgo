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
        global lines
        try:
            self.circle.remove()
            self.ax.lines.remove(lines[0])
        except Exception:
            pass
        self.circle=plt.Circle((posX,posY),3, color='r', fill=False)
        self.ax.add_artist(self.circle)
        lines = self.ax.plot([posX,posX+(math.cos(phi / 180 * math.pi))*4],[posY,posY+math.sin(phi / 180 * math.pi)*4], 'r')

def Main():
    print("================================Start From here================================")      
    draw=Application()
    car=Moving(0,0,90)
    x,y,phi=car.x,car.y,car.phi
    plt.ion()
    plt.show()        
    fussySys=fussySystem()
    steerDegree=10
    f = open("train4D.txt",'w')
        
    while (car.DetectWall()!=False):
        x,y,phi = car.UpdataPos(steerDegree)
        
        F_minDis=round(car.CountWallDis(draw.point,x,y,phi),3)
        
        
        R_minDis=round(car.CountWallDis(draw.point,x,y,phi-45),3)
        
        L_minDis=round(car.CountWallDis(draw.point,x,y,phi+45),3)
        
        #模糊系統-----
        all_FS = fussySys.FiringStrength(R_minDis-L_minDis,F_minDis)
        
        output=fussySys.Defuzzification(all_FS)
        
        steerDegree = fussySys.CenterOfGravity(output)
        if R_minDis-L_minDis<0:
            steerDegree = - steerDegree
       
        f.writelines(str(F_minDis)+','+str(R_minDis)+','+str(L_minDis)+','+str(steerDegree)+'\n')
        
        draw.DrawCar(x,y,phi)
        plt.show()
        plt.pause(0.1)
        print("F_minDis",F_minDis)
        var.set(F_minDis)
        print("R_minDis",R_minDis)
        var2.set(R_minDis)
        print("L_minDis",L_minDis)
        var3.set(L_minDis)
       
    plt.pause(0)
    f.close()   
#GUI
#介面基本設定
window= tk.Tk()
window.geometry('200x200')
window.title('HW1-FussySystem')

label_top = tk.Label(window,text = "Reading Trail file : ")
label_top.pack()         
label_right = tk.Label(window,text = "case01.txt",fg="red")
label_right.pack() 

#開始訓練按鈕


Dis_frame = tk.Frame(window)
Dis_frame.pack(side=tk.TOP)

button_start = tk.Button(Dis_frame,text='Run',command=Main)
button_start.pack(side=tk.TOP)


Dis_frame1 = tk.Frame(window)
Dis_frame1.pack(side=tk.TOP)
Dis_label1 = tk.Label(Dis_frame1,text='Front Distance')
Dis_label1.pack(side=tk.LEFT)
var = tk.StringVar()
ShowDis_label1 = tk.Label(Dis_frame1, textvariable=var)
ShowDis_label1.pack(side=tk.LEFT)

Dis_frame2 = tk.Frame(window)
Dis_frame2.pack(side=tk.TOP)
Dis_label2 = tk.Label(Dis_frame2,text='Right Distance')
Dis_label2.pack(side=tk.LEFT)
var2 = tk.StringVar()
ShowDis_label2 = tk.Label(Dis_frame2, textvariable=var2)
ShowDis_label2.pack(side=tk.LEFT)

Dis_frame3 = tk.Frame(window)
Dis_frame3.pack(side=tk.TOP)
Dis_label3 = tk.Label(Dis_frame3,text='Left Distance')
Dis_label3.pack(side=tk.LEFT)
var3 = tk.StringVar()
ShowDis_label3 = tk.Label(Dis_frame3, textvariable=var3)
ShowDis_label3.pack(side=tk.LEFT)

window.mainloop()