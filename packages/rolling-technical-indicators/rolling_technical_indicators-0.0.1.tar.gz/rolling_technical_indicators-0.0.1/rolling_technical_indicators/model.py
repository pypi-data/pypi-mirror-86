
import enum

class Record:

    def __init__(self):

        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None
        self.date = None
        self.time = None

class Node:

    def put(self, data):
        
        self.add(data)

        if self.isFull():
            self.calculate()

    def get(self):
        return self.value

class PredictionType(enum.Enum):
   
   BUY = "Buy"
   SELL = "Sell"
   HOLD = "Hold"
   NULL = None


