import numpy as np
import math

class fussySystem():
    def __init__(self): 
        pass
    def c_fussyFuc(self,left,top,right):
        x =np.arange(left,right+1)
        y1=np.arange( 0, 1, 1/(top-left))
        y2=np.arange(1, 0, -1/(right-top))
        y3=np.zeros(1)
        result = np.hstack((x,y1,y2,y3)).reshape(2,-1) 
        return  result

    def fussyFuc(self,left,lefttop,righttop,right):
        x =np.arange(left,right+1)

        if left==lefttop:
            y1=[]
        else:
            y1=np.arange( 0, 1, 1/(lefttop-left))
        
        y2=np.ones(righttop-lefttop)

        if right==righttop:
            y3=np.ones(1)
            result = np.hstack((x,y1,y2,y3)).reshape(2,-1) 
        else:
            y3 = np.arange( 1, 0, -1/(right-righttop))
            y4=np.zeros(1)
            result = np.hstack((x,y1,y2,y3,y4)).reshape(2,-1) 
        return  result

        
    def FiringStrength(self,rl_diff,f_diff):
        all_FS = np.zeros(9)
        rl_diff= abs(round(rl_diff)) #若差距為小數 此處先以整數處理
        f_diff= round(f_diff)
        if 0<=rl_diff<=8:
            rl_FSSet = self.fussyFuc(-1,2,4,8)
            index = np.where(rl_FSSet[0]==rl_diff)
            rl_FS = rl_FSSet[1][index]

            if 3 <= f_diff <=8:
                f_FSSet = self.fussyFuc(0,4,6,8)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[0] = min(rl_FS,f_FS)
            if 6 <= f_diff <=15:
                f_FSSet = self.fussyFuc(6,8,13,15)
                index = np.where(f_FSSet==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[1] = min(rl_FS,f_FS)
            if 14 <= f_diff <=40:
                f_FSSet = self.fussyFuc(14,16,40,40)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[2] = min(rl_FS,f_FS)
        if 3 <= rl_diff <= 11:
            rl_FSSet = self.fussyFuc(3,7,9,11)
            index = np.where(rl_FSSet[0]==rl_diff)
            rl_FS = rl_FSSet[1][index]

            if 3 <= f_diff <=8:
                f_FSSet = self.fussyFuc(0,4,6,8)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[3] = min(rl_FS,f_FS)
            if 6 <= f_diff <=15:
                f_FSSet = self.fussyFuc(6,8,13,15)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[4] = min(rl_FS,f_FS)
            if 14 <= f_diff <=40:
                f_FSSet = self.fussyFuc(14,16,40,40)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[5] = min(rl_FS,f_FS)
        if 9 <= rl_diff <= 25:
            rl_FSSet = self.fussyFuc(9,13,25,25)
            index = np.where(rl_FSSet[0]==rl_diff)
            rl_FS = rl_FSSet[1][index]

            if 0 <= f_diff <=8:
                f_FSSet = self.fussyFuc(0,4,6,8)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[6] = min(rl_FS,f_FS)
            if 6 <= f_diff <=15:
                f_FSSet = self.fussyFuc(6,8,13,15)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[7] = min(rl_FS,f_FS)
            if 14 <= f_diff <=40:
                f_FSSet = self.fussyFuc(14,16,40,40)
                index = np.where(f_FSSet[0]==f_diff)
                f_FS = f_FSSet[1][index]
                all_FS[8] = min(rl_FS,f_FS)

        return all_FS
    
    def updateOutput(self,all_FS,FS_index,left,top,right,output):
        c_FSSet = self.c_fussyFuc(left,top,right)
        for i in range(len(c_FSSet[0])):
            if c_FSSet[1][i] > all_FS[FS_index]: #若Ｃ函數裡對應強度大於啟動強度
                c_FSSet[1][i] = all_FS[FS_index]#消掉大於啟動強度的部分 最大為啟動強度值 
            
            if output[1][left+i] < c_FSSet[1][i]:#若本次更新之度數跟之前度數對應強度比較大 
                output[1][left+i] = c_FSSet[1][i]#將對應度數強度更新為大者

        return output

    def Defuzzification(self,all_FS):
        output = np.arange(0,41)
        output = np.hstack((output,np.zeros(41))).reshape(2,-1)
        if all_FS[0]!=0:
            output[1][40]=all_FS[0]#因為SS需要轉彎的最大值 是單點 直接把值更新
            
        if all_FS[1]!=0:  #SM 對應為allActi的一號
            output = self.updateOutput(all_FS,1,15,20,25,output)

        if all_FS[2]!=0:
            output = self.updateOutput(all_FS,2,0,5,10,output)

        if all_FS[3]!=0:
            output = self.updateOutput(all_FS,3,20,30,40,output)

        if all_FS[4]!=0:
            output = self.updateOutput(all_FS,4,13,18,23,output)

        if all_FS[5]!=0:
            output = self.updateOutput(all_FS,5,15,20,25,output)

        if all_FS[6]!=0:
            output = self.updateOutput(all_FS,6,20,30,40,output)

        if all_FS[7]!=0:
            output = self.updateOutput(all_FS,7,15,20,25,output)

        if all_FS[8]!=0:
            output = self.updateOutput(all_FS,8,10,13,16,output)

        return output

    def CenterOfGravity(self,output):
        ySum=sum(output[1])
        productSum=0
        
        if ySum == 0:
            return 0

        for i in range(len(output[0])):
            productSum += output[0][i]*output[1][i]
        return  productSum/ySum
        

# if __name__ == "__main__":
#     fussySys=fussySystem()
#     all_FS = fussySys.FiringStrength(8,18)
#     print("all_FS",all_FS)
#     output=fussySys.Defuzzification(all_FS)
#     print("output",output)
#     steerDegree = fussySys.CenterOfGravity(output)
#     print("steerDegree=",steerDegree)
