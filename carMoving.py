import matplotlib.pyplot as plt
import numpy as np
import math

class Moving():
    def __init__(self,x,y,phi):
        self.x=x
        self.y=y
        self.phi = phi
        self.canMove = True 

    def UpdataPos(self,theta):
        self.x = self.x + math.cos((self.phi+theta) / 180 * math.pi)  + math.sin(theta/ 180 * math.pi)* math.sin(self.phi/ 180 * math.pi)
        self.y = self.y + math.sin((self.phi+theta) / 180 * math.pi)  - math.sin(theta/ 180 * math.pi)* math.sin(self.phi/ 180 * math.pi)
        self.phi = self.phi - (math.asin( 2* math.sin(theta / 180 *math.pi) / 6 ))* 180 / math.pi
        return self.x,self.y,self.phi 

    def DetectWall(self):
        if self.y<= 10-3:
            if(self.x>=6-3 or self.x<=-6+3 or self.y<-3+3):
                self.canMove = False
                return False
            else:
                self.canMove = True
        elif self.y<=22-3:
            if(self.x<=-6+3 or self.x>=30-3):
                self.canMove = False
                return False
            else:
                self.canMove = True
        elif self.y<40:
            if(self.x<=18+3 or self.x>=30-3):
                self.canMove = False
                return False
            else:
                self.canMove = True
        else:
            self.canMove = False
            return False
            

    def CountWallDis(self,point,x,y,phi):
         
        minDis=3000.0
        minxm=0.0
        minym=0.0
        #horizontal Wall #Distance from point to Wall = (wallX - pointx)/cos(phi)
        for n in range(1,len(point)-1,2):
            Dis =( point[n][1] - y) / (math.sin(phi / 180 * math.pi))
            if (Dis < minDis) and (Dis >0):
                xm = x + math.cos(phi / 180 * math.pi)*Dis
                ym = point[n][1]
                if (point[n+1][0] >= xm >= point[n][0])or(point[n+1][0] <= xm <= point[n][0]):
                    minDis = Dis
                    minxm = xm
                    minym = ym
        #vertical Wall  #Distance from point to Wall = (wallY - pointy)/sin(phi)       
        for i in range(0,len(point)-2,2):   
            Dis = (point[i][0] - x) / (math.cos(phi / 180 * math.pi))
            #print("x, V_Dis ",point[i][0],Dis)
            if (Dis < minDis) and (Dis >0):
                xm = point[i][0]
                ym = y + math.sin(phi / 180 * math.pi)*Dis
                if (point[i][1] >= ym >= point[i+1][1])or(point[i][1] <= ym <= point[i+1][1]):
                    minDis = Dis
                    minxm = xm
                    minym = ym    

        
        return minDis