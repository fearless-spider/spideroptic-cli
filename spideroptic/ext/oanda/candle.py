class Candle(object):

    def __init__(self, date, open, high, low, close):
         self.Date = date
         self.Open = open
         self.Close = close
         self.High = high
         self.Low = low

    def HL(self):
        return self.High-self.Low