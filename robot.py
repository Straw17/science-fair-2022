import PID

class Robot:
    def __init__(self, maxV, maxA):
        self.maxV = maxV
        self.maxA = maxA
        self.position = [0,0]
        self.velocity = [0,0]
        self.ticks = 0

    def initAuto(self, PID, target):
        self.PIDLoop = PID
        self.target = target

    def update(self, coordNum):
        plannedV = self.PIDLoop[coordNum].calculate(self.position[coordNum] - self.target[coordNum])
        if abs(plannedV) > self.maxV:
            plannedV = self.maxV * (plannedV / abs(plannedV))

        plannedA = (plannedV - self.velocity[coordNum]) / self.PIDLoop[coordNum].interval

        if abs(plannedA) < 0.001:
            plannedA = 0
        elif abs(plannedA) > self.maxA:
            plannedA = self.maxA * (plannedA / abs(plannedA))

        self.position[coordNum] += self.velocity[coordNum] * self.PIDLoop[coordNum].interval
        self.velocity[coordNum] += plannedA * self.PIDLoop[coordNum].interval

    def updateBoth(self):
        self.update(0)
        self.update(1)
        self.ticks += 1

    def isClose(self):
        xClose = abs(self.position[0] - self.target[0]) < 0.01
        yClose = abs(self.position[1] - self.target[1]) < 0.01
        return (xClose and yClose)

    def isSlow(self):
        xSlow = abs(self.velocity[0]) < 0.01
        ySlow = abs(self.velocity[1]) < 0.01
        return (xSlow and ySlow)
