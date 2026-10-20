from Route import Route
from FarePredictor import FarePredictor
from FarePredictor import predict_fare

year = int(input("What year do you want to fly in? "))
quarter = int(input("What quarter do you want to fly in? "))
city1 = input("What city do you want to fly from? ")
city2 = input("What city do you want to fly to? ")
large_ms = 0
large_fare = 0
low_ms = 0
low_fare = 0
fare = 0

customer_route: Route= Route(year, quarter, city1, city2, large_ms, large_fare, low_ms, low_fare, fare)

predictor: FarePredictor = FarePredictor(customer_route)
predictor.find_similar_routes()
predictor.future_large_ms()
predictor.future_low_ms()
predictor.future_middle_ms()
predictor.future_large_fare()
predictor.future_low_fare()
predictor.future_middle_fare()
predictor.future_fare()

print(predict_fare(customer_route))
