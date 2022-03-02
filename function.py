import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import time 


def StringToList(elem):
    a = elem.split("[")
    b = a[1].split("]")
    c = b[0].split(",")
    return list(c)

def dist(x,y):
    dist = math.sqrt((x*x)+(y*y))
    return dist 

def angle(x, y) :
    angle = math.atan(y/x)*180/math.pi
    if x > 0 and y > 0 :
        return 360-angle 
    if x < 0 and y > 0 :
        return 180 - angle
    if x < 0 and y < 0 :
        return 180-angle
    if x > 0 and y < 0 :
        return -angle

def plot3d(value):
    pass


def WriteAllLandMark(value, txtName):
    x_data, y_data, z_data = [], [], []
    for i in range(len(value)):
        try : 
            x_data.append(value[i].x)
        except:
            x_data.append(0)
        try : 
            y_data.append(value[i].y)
        except:
            y_data.append(0)
        try : 
            z_data.append(value[i].z)
        except:
            z_data.append(0)
            
    file1 = open("PoseData/"+str(txtName)+"_X"+".txt","a") 
    file1.write(str(x_data)+"\n")
    file1.close()
    
    file2 = open("PoseData/"+str(txtName)+"_Y"+".txt","a") 
    file2.write(str(y_data)+"\n")
    file2.close()
    
    file3 = open("PoseData/"+str(txtName)+"_Z"+".txt","a") 
    file3.write(str(z_data)+"\n")
    file3.close()
    
def TriAllLandMark(txtName):
    X, Y, Z = [], [], []
    file1 = open("PoseData/"+str(txtName)+"_X"+".txt", "r")
    for ligne in file1:
        X.append(StringToList(ligne))
    file2 = open("PoseData/"+str(txtName)+"_Y"+".txt", "r")
    for ligne in file2:
        Y.append(StringToList(ligne))
    file3 = open("PoseData/"+str(txtName)+"_Z"+".txt", "r")
    for ligne in file3:
        Z.append(StringToList(ligne))
    return X, Y, Z

def triStringtoFloat(X,Y,Z):
    
    X_data, Y_data, Z_data, conv = [], [], [], []
    
    for i in range(len(X)):
        for j in range(len(X[i])):
            conv.append(float(X[i][j]))
        X_data.append(conv)
        conv = [] 
    
    for i in range(len(Y)):
        for j in range(len(Y[i])):
            conv.append(float(Y[i][j]))
        Y_data.append(conv)
        conv = [] 
    
    for i in range(len(Z)):
        for j in range(len(Z[i])):
            conv.append(float(Z[i][j]))
        Z_data.append(conv)
        conv = [] 

    return X_data, Y_data, Z_data
        
    # plt.tight_layout()
    #plt.show()
 
X,Y,Z = TriAllLandMark("premierTest")
X_data, Y_data, Z_data = triStringtoFloat(X,Y,Z)
