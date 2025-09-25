class Route:
   def __init__(self, year, quarter, city1, city2, large_ms, large_fare, low_ms, low_fare, fare):
       self.year = year
       self.quarter = quarter
       self.city1 = city1
       self.city2 = city2
       self.large_ms = large_ms
       self.large_fare = large_fare
       self.low_ms = low_ms
       self.low_fare = low_fare
       self.fare = fare
       self.middle_ms = 1 - self.large_ms - self.low_ms
       self.middle_fare = round((self.fare - (self.low_fare * self.low_ms) - (self.large_fare * self.large_ms)) / self.middle_ms, 2)

   def get_year(self):
       return self.year

   def get_quarter(self):
       return self.quarter

   def get_city1(self):
       return self.city1

   def get_city2(self):
       return self.city2

   def get_large_ms(self):
       return self.large_ms

   def get_large_fare(self):
       return self.large_fare

   def get_low_ms(self):
       return self.low_ms

   def get_low_fare(self):
       return self.low_fare

   def get_fare(self):
       return self.fare

   def get_middle_fare(self):
       return self.middle_fare

   def get_middle_ms(self):
       return self.middle_ms

   def set_large_ms(self, new):
       self.large_ms = new

   def set_large_fare(self, new):
       self.large_fare = new

   def set_low_ms(self, new):
       self.low_ms = new

   def set_low_fare(self, new):
       self.low_fare = new

   def set_fare(self, new):
       self.fare = new

   def set_middle_ms(self, new):
       self.middle_ms = new

   def set_middle_fare(self, new):
       self.middle_fare = new