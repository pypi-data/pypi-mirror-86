
from queue import Queue 
from model import Node

class ExponentialMovingAverage(Node):

    def __init__(self, period):
        
        self.value = None
        self.alpha = 2/(period+1)

    def put(self, data):

        if self.value == None:
            self.value = data
        
        else:
            self.value = self.alpha*data + (1-self.alpha)*self.value

    def isFull(self):
        return self.value != None

class MovingSum(Node):

    def __init__(self, period):
        
        self.queue = Queue(maxsize = period)
        self.value = 0

    def put(self, data):

        if self.isFull():
            oldestDataPoint = self.queue.get()
            self.value -= oldestDataPoint

        self.queue.put(data)
        self.value += data

    def isFull(self):
        return self.queue.full()

class SimpleMovingAverage(Node):

    def __init__(self, period):
        
        self.movingSum = MovingSum(period)
        self.period = period
        self.value = None

    def isFull(self):
        return self.movingSum.isFull()

    def calculate(self):
        self.value = self.movingSum.get()/self.period

    def add(self, data):
        self.movingSum.put(data)  

class StandardDeviation(Node):

    def __init__(self, period):
        
        self.movingAvg = SimpleMovingAverage(period)
        self.squaredMovingSum = MovingSum(period)
        self.movingSum = MovingSum(period)
        self.period = period

        self.value = None

    def isFull(self):
        return self.movingSum.isFull()

    def add(self, data):
        
        self.movingAvg.put(data)
        self.squaredMovingSum.put(data**2)
        self.movingSum.put(data)

    def calculate(self):

        a = self.squaredMovingSum.get() 
        b = self.movingAvg.get() 
        c = self.movingSum.get() 
                
        summation = a -2*b*c + self.period*b**2

        self.value = (summation/(self.period-1))**.5