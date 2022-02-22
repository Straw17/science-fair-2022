class PID:
    def __init__(self, P, I, D, interval):
        self.P = P
        self.I = I
        self.D = D
        self.errorSum = 0
        self.lastError = 0
        self.isFirstLoop = True
        self.interval = interval

    def getLastError(self, error):
        if self.isFirstLoop:
            return error
        else:
            return self.lastError

    def calculate(self, error):
        self.errorSum += ((self.getLastError(error) + error)/2) * self.interval #trapezoidal reimann sum
        self.errorChange = (error - self.getLastError(error)) / self.interval
        result = (self.P * error) + (self.I * self.errorSum) + (self.D * self.errorChange)
        self.lastError = error

        self.isFirstLoop = False

        return -result
