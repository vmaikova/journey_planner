#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sys
from classes import *
from optimizer import Optimizer


def main():
    print("main")


def check_airport_codes(airport_codes):
    for code in airport_codes:
        if code.strip() == "":
            return False
        if len(code) != 3:
            return False

    return True


"""Main module."""
def main():
    if len(sys.argv) != 1 and len(sys.argv) != 7:
        print(
            "Parameters: 1 - aircraft data, 2 - airportdata, 3 - country and currency data, 4 - corresponding currency rates data, 5 - batch input file, 6 - Output result file")
        exit(0)
    aircraft_holder = AircraftParser(sys.argv[1] if len(sys.argv) > 1 else './input/aircraft.csv')
    airport_holder = AirportParser(sys.argv[2] if len(sys.argv) > 1 else './input/airport.csv')
    currency_holder = CurrencyConverter(sys.argv[3] if len(sys.argv) > 1 else './input/countrycurrency.csv',
                                        sys.argv[4] if len(sys.argv) > 1 else './input/currencyrates.csv')

    optimizer = Optimizer(aircraft_holder, airport_holder, currency_holder)

    with open(sys.argv[6] if len(sys.argv) > 1 else './input/output.csv', 'w', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        with open(sys.argv[5] if len(sys.argv) > 1 else './input/testinputs.csv', encoding='utf-8') as csvfile:
            csv_source = csv.reader(csvfile, delimiter=',')
            for row in csv_source:
                try:
                    if len(row) != 6:
                        continue
                    airport_codes = row[0:5]
                    aircraft_code = row[5]
                    if not check_airport_codes(airport_codes) or aircraft_code.strip() == "":
                        continue
                    cheapest_route, lowest_cost = optimizer.optimize(airport_codes, aircraft_code)

                    airports_joined = ""
                    price_cost = ""
                    feasibility = "Unfeasible"
                    if cheapest_route != None and lowest_cost != None:
                        airports_joined = ', '.join(cheapest_route)
                        price_cost = "" + str(lowest_cost)
                        feasibility = "Feasible"

                    input_airports_joined = ', '.join(airport_codes)
                    writer.writerow([aircraft_code, input_airports_joined, airports_joined, price_cost, feasibility])
                except:
                    continue

if __name__ == "__main__":
    main()
