#!/usr/bin/env python
import itertools
import math

class Optimizer:                                            #class to find the shortest route

    def __init__(self, aircraft_holder, airport_holder, currency_holder): #constructor takes in three variables
        self.aircraft_holder = aircraft_holder                    #creating variable/class attribute
        self.airport_holder = airport_holder                      #creating variable/class attribute
        self.currency_holder = currency_holder                    #creating variable/class attribute

    def optimize(self, airportCodes, aircraftCode):               #function inside of the class takes in arguments airportCodes, aircraftCode
        aircraft = self.aircraft_holder.get_aircraft(aircraftCode)   #indexing the dict returns default value
        home_code = airportCodes[0]                                 #home code is the first entered airport code
        airports_permutations = self.get_all_permutations(airportCodes[1:5]) #rearrangement of objects airport name and code into sequence

        lowest_cost = float("inf")
        cheapest_permutation = []                                 #rearrangement of objects into sequence to find cheapest route

        for route_perm in airports_permutations:
            route_perm.extend([home_code, route_perm[0]])  #method adds elements to a list by adding on all the elements of the iterable pass to it
            roundRoute = route_perm                        #resulting list contains all of the elements of both lists.

            cost = self.calculate_cost(roundRoute, aircraft)
            if cost is None:
                continue

            elif cost == -1:
                return None, None

            if cost < lowest_cost:
                lowest_cost = cost
                cheapest_permutation = [home_code, route_perm[0], route_perm[1], route_perm[2], route_perm[3], home_code] #to dictionary

        return cheapest_permutation, lowest_cost                   #returns cheapest route from home to home airport, rearranges with permutation
        #each unique ordering is permutation
    def calculate_cost(self, destinationPermutation, aircraft):    #function inside of the class takes in arguments destinationPermutation, aircraft
        if aircraft is None:
            return None                                            #if aircraft doesn't exist returns none
        aircraft_range = aircraft.range                            #
        airport_list = self.airport_holder.getAirports(destinationPermutation)
        distanceList = []

        for i in range(0, len(airport_list) - 1):
            if airport_list[i] is None or airport_list[i + 1] is None:
                return None

            fromAirport, distance, toAirport = airport_list[i], self.spherical_distance(airport_list[i].coordinate,
                                                                                        airport_list[i + 1].coordinate), airport_list[i + 1]
            if distance > aircraft_range:
                return -1

            distanceList.append([fromAirport, distance, toAirport])

        costList = []
        for i in range(0, len(distanceList)):
            exchange_rate = self.currency_holder.exchange_rate(distanceList[i][2].country)
            costList.append(distanceList[i][1] * exchange_rate)

        return sum(costList)

    def spherical_distance(self, coordinate1, coordinate2):        #function inside of the class
        lat1 = math.radians(90 - coordinate1.latitude)             #
        long1 = math.radians(coordinate1.longitude)
        lat2 = math.radians(90 - coordinate2.latitude)
        long2 = math.radians(coordinate2.longitude)

        product1 = math.sin(lat1) * math.sin(lat2) * math.cos(long1 - long2) # Compute the spherical distance from spherical coordinates
        product2 = math.cos(lat1) * math.cos(lat2)                           # For two locations in spherical coordinates

        return round(math.acos(product1 + product2) * 6371)          #radius of the earth in km

    def get_all_permutations(self, target):                       #function inside of the class
        permutations = itertools.permutations(target)             #getting rearranged routes
        return list([list(_) for _ in permutations])
