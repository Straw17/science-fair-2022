from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import PID, robot

interval = 0.01
maxTime = 400
PIDX = PID.PID(5, 0, 0, interval)
PIDY = PID.PID(5, 0, 0, interval)
PIDLoop = [PIDX, PIDY]
myRobot = robot.Robot(27, 3)
coords = [[], [], []]

def update(coords, target):
    global myRobot, PIDLoop
    myRobot.initAuto(PIDLoop, target)
    i = 0;
    while not myRobot.isClose() and i < maxTime:
        coords[0].append(myRobot.position[0])
        coords[1].append(myRobot.position[1])
        coords[2].append(myRobot.ticks * interval)
        myRobot.updateBoth()
        i += 1
    return coords

def selectTargetList():
    options = {"1D Line": [[1,0]],
               "2D Line": [[1,1]],
               "C Curve": [[1,1], [2,0]],
               "S Curve": [[1,1], [2,-1], [3,0]],
               "Square":  [[1,0], [1,1], [0,1], [0,0]],
               "Lincoln Path": [[1,0], [2,0], [3,4], [2,10]]}

    option = ""
    print("Options:")
    for key in options.keys():
        print("-" + key)
    while option not in options.keys():
        option = input("Select option: ")

    targetList = options[option]
    return targetList

targetList = selectTargetList()
for target in targetList:
    coords = update(coords, target)

fig = plt.figure(figsize = (6, 5))
ax = plt.axes(projection = "3d")
ax.scatter3D(coords[0], coords[1], coords[2], color = "green")

ax.set_zlim3d(0, len(targetList) * maxTime * interval)
highest = max([max(coords[0]),max(coords[1])])
lowest = min([min(coords[0]),min(coords[1])])
plt.xlim([lowest,highest])
plt.ylim([lowest,highest])

plt.title("PID Path Plot")
ax.set_xlabel('X Direction (m)', fontweight ='bold')
ax.set_ylabel('Y Direction (m)', fontweight ='bold')
ax.set_zlabel('Time (s)', fontweight ='bold')

plt.show()
