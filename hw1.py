import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import tkinter as tk
import math
from fussySys import fussySystem
from carMoving import Moving
class Application(tk.Frame):
    def __init__(self, master): 
        tk.Frame.__init__(self, master)
        self.window = master
        self.grid()
        self.mainControl()

        self.fig, self.ax = plt.subplots(1, 1, figsize=(4.5, 6))
        self.point = [[-6,-3],[-6,22],[18,22],[18,50],[30,50],[30,10],[6,10],[6,-3],[-6,-3]]
    
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
    
    def mainControl(self):
        print("================================Start From here================================")   
        fig=Application()  
        point=fig.point 
        fig.DrawMap()    
        car = Moving(0,0,90)
        x,y,phi=car.x,car.y,car.phi
        plt.ion()
        plt.show()
        
        fussySys=fussySystem()
        steerDegree=10

        for i in range(50):
            if(car.DetectWall()!=False):
                x,y,phi = car.UpdataPos(steerDegree)
                print("-------x,y,phi=",x,y,phi)
                F_minDis=car.CountWallDis(point,x,y,phi)
                print("Mid_minDis",F_minDis)
                R_minDis=car.CountWallDis(point,x,y,phi-45)
                print("Right_minDis",R_minDis)
                L_minDis=car.CountWallDis(point,x,y,phi+45)
                print("Left_minDis",L_minDis)
                #模糊系統-----
                all_FS = fussySys.FiringStrength(R_minDis-L_minDis,F_minDis)
                print("all_FS",all_FS)
                output=fussySys.Defuzzification(all_FS)
                print("output",output)
                steerDegree = fussySys.CenterOfGravity(output)
                if R_minDis-L_minDis<0:
                    steerDegree = - steerDegree
                print("steerDegree=",steerDegree)

            fig.DrawCar(x,y,phi)
            plt.show()
            plt.pause(0.1)
            fig.circle.remove()
            #fig.line.remove()  #待解 移除圓的線
        plt.pause(0)
            