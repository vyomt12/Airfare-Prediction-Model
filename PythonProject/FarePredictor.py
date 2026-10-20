import Route
from sklearn.linear_model import LinearRegression
import numpy as np


class FarePredictor:
    def __init__(self, customer_route: Route):
        self.customer_route = customer_route
        self.route_list = []
        self.y = []

        data = open("data.csv").read().splitlines()
        for x in data:
            a = x.split(",")
            self.y.append(a)

    def find_similar_routes(self):
        for line in self.y:
            if (
                line[2] == self.customer_route.get_city1()
                and line[3] == self.customer_route.get_city2()
                and line[1] == str(self.customer_route.get_quarter())
            ):
                self.route_list.append(
                    Route.Route(int(line[0]), int(line[1]), line[2], line[3], float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8])))
        if not self.route_list:
            print("No similar routes found. Cannot make prediction.")
            return

    def future_large_ms(self):
        years = []
        large_ms_history: list = []
        large_ms_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            large_ms_history.append(route.get_large_ms())
        years = np.array(years).reshape(-1, 1)
        large_ms_model.fit(years, large_ms_history)
        self.customer_route.set_large_ms(large_ms_model.predict([[self.customer_route.get_year()]]))

    def future_low_ms(self):
        years = []
        low_ms_history: list = []
        low_ms_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            low_ms_history.append(route.get_low_ms())
        years = np.array(years).reshape(-1, 1)
        low_ms_model.fit(years, low_ms_history)
        self.customer_route.set_low_ms(low_ms_model.predict([[self.customer_route.get_year()]]))

    def future_middle_ms(self):
        years = []
        middle_ms_history: list = []
        middle_ms_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            middle_ms_history.append(route.get_middle_ms())
        years = np.array(years).reshape(-1, 1)
        middle_ms_model.fit(years, middle_ms_history)
        self.customer_route.set_middle_ms(middle_ms_model.predict([[self.customer_route.get_year()]]))

    def future_large_fare(self):
        years = []
        large_fare_history: list = []
        large_fare_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            large_fare_history.append(route.get_large_fare())
        years = np.array(years).reshape(-1, 1)
        large_fare_model.fit(years, large_fare_history)
        self.customer_route.set_large_fare(large_fare_model.predict([[self.customer_route.get_year()]]))

    def future_low_fare(self):
        years = []
        low_fare_history: list = []
        low_fare_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            low_fare_history.append(route.get_low_fare())
        years = np.array(years).reshape(-1, 1)
        low_fare_model.fit(years, low_fare_history)
        self.customer_route.set_low_fare(low_fare_model.predict([[self.customer_route.get_year()]]))

    def future_middle_fare(self):
        years = []
        middle_fare_history: list = []
        middle_fare_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            middle_fare_history.append(route.get_middle_fare())
        years = np.array(years).reshape(-1, 1)
        middle_fare_model.fit(years, middle_fare_history)
        self.customer_route.set_middle_fare(middle_fare_model.predict([[self.customer_route.get_year()]]))

    def future_fare(self):
        years = []
        fare_history: list = []
        fare_model: LinearRegression = LinearRegression()
        for route in self.route_list:
            years.append(route.get_year())
            fare_history.append(route.get_fare())
        years = np.array(years).reshape(-1, 1)
        fare_model.fit(years, fare_history)
        self.customer_route.set_fare(fare_model.predict([[self.customer_route.get_year()]]))


def predict_fare(wanted_route: Route):
    b = wanted_route.get_large_ms() + wanted_route.get_low_ms() + wanted_route.get_middle_ms()
    if b > 1:
        wanted_route.set_middle_ms(wanted_route.get_middle_ms() - (b - 1))

    a = wanted_route.get_large_fare() * wanted_route.get_large_ms()
    a += wanted_route.get_low_fare() * wanted_route.get_low_ms()
    a += wanted_route.get_middle_fare() * wanted_route.get_middle_ms()
    a += wanted_route.get_fare()
    a = a / 2
    return a