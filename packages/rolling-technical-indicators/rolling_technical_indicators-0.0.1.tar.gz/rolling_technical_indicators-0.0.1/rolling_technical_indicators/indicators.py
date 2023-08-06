
from calc import SimpleMovingAverage, StandardDeviation
from model import Node

class BollingerBands(Node):

    def __init__(self, period):
        
        self.smoothedTypical = SimpleMovingAverage(period)
        self.stdev = StandardDeviation(period)
        self.value = None

    def isFull(self):
        return self.smoothedTypical.isFull() and self.stdev.isFull()

    def calculate(self):
        smoothedValue = self.smoothedTypical.get()
        stdevValue = self.stdev.get()

        upperBandValue = smoothedValue + 2*stdevValue
        lowerBandValue = smoothedValue - 2*stdevValue

        self.value = (lowerBandValue, upperBandValue)

    def add(self, record):

        typical = (record.close + record.high + record.low) / 3
        self.smoothedTypical.put(typical)
        self.stdev.put(typical)