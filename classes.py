#!/usr/bin/env python
import csv  # importing csv


class Aircraft:
    def __init__(self, name, range):  # constructor takes in arguments name and range
        self.name = name  # creating variable/class attribute
        self.range = range  # creating variable/class attribute


class AircraftParser:

    def __init__(self, file):  # constructor takes in argument file
        self._aircraft_data = {}  # creating empty dictionary in the class for aircraft
        with open(file, encoding='utf-8') as csvfile:  # The AircraftParser reads the csv file for aircraft
            csv_source = csv.reader(csvfile, delimiter=',')
            for row in csv_source:
                if row[0] == 'code':  # if the datatype for column 0 is equal to the value code then  skip that line
                    continue  # first row has feature names
                range = float(row[4])  # variable range is the feature that is column 4
                name = row[3]  # variable name is the manufacturers name feature that is column 3
                if row[2] == 'imperial':  # if 'units' is imperial(miles) changing to metrical
                    range *= 1.60934
                self._aircraft_data[row[0].upper()] = Aircraft(name + ' ' + row[0], range)  # new key to the dictionary
                # mapped to the aircraft, adding to the dictionary
                # manufacturer name + code + range

    def get_aircraft(self, code):  # function inside of the class takes in argument 'code'
        code = code.upper()  # code in upper case letter
        if code in self._aircraft_data:  # accessing dictionary, if code is in dictionary
            return self._aircraft_data[code]  # return results from dictionary
        else:  # no such aircraft
            raise Exception('Aircraft code not found or data file is corrupted.')


class Coordinate:

    def __init__(self, latitude, longitude):  # constructor takes in arguments latitude and longitude
        self.latitude = latitude  # creating variable/class attribute
        self.longitude = longitude  # creating variable/class attribute


class Airport:

    def __init__(self, code, airport_name, country,
                 coordinate):  # constructor takes in arguments code,airport name, country, coordinate
        self.code = code  # creating variable/class attribute for code
        self.airport_name = airport_name  # creating variable/class attribute for airport name
        self.country = country  # creating variable/class attribute for country
        self.coordinate = coordinate  # creating variable/class attribute for coordinate


class AirportParser:

    def __init__(self, file):  # constructor takes in argument file
        self._airport_data = {}  # creating empty dictionary in the class for airport
        with open(file, encoding='utf-8') as csvfile:  # The AirportParser reads the csv file for airport
            csv_source = csv.reader(csvfile, delimiter=',')
            for row in csv_source:
                self._airport_data[row[4].upper()] = \
                    Airport(row[4], row[1], row[3], Coordinate(float(row[6]), float(row[7])))
        # new key to the dictionary mapped to the airport, adding to the dictionary airport code(4)+airport name(1)+country(3)+coordinates(6+7)

    def get_airport(self, code):  # function inside of the class takes in argument 'code'
        code = code.upper()  # code in upper case letter
        if code in self._airport_data:  # accessing dictionary, if code is in dictionary
            return self._airport_data[code]  # return results from dictionary
        else:  # no such airport
            raise Exception('Airport code not found or data file is corrupted.')

    def getAirports(self, codes):  # function inside of the class takes in argument 'code'
        codes = [c.upper() for c in codes]
        airports = []

        for code in codes:
            airports.append(self.get_airport(code))  # appends a passed set_airport(code) into the existing list

        return airports  # method does not return any value but updates existing list


class CurrencyConverter:
    def __init__(self, currencyFile, rateFile):  # constructor takes in arguments currencyFile, rateFile
        self._currency_data_currency_name = {}  # creating empty dictionary in the class for currency name
        self._currency_data_country_name = {}  # creating empty dictionary in the class for country name
        self._rate_data = {}  # creating empty dictionary in the class for rates
        with open(currencyFile, encoding='utf-8') as csvfile:  # The CurrencyConverter reads the csv file for currency
            csv_source = csv.reader(csvfile, delimiter=',')
            for row in csv_source:
                if row[0] == 'name':  # if the data type for column 0 is equal to the value name then  skip that line
                    continue  # first row has all the feature names
                self._currency_data_currency_name[row[15].upper()] = {'name': row[0], 'code': row[
                    14]}  # Duplicating dictionaries with different keys, 2 variants of country name
                self._currency_data_country_name[row[0].upper()] = {'name': row[0], 'code': row[
                    14]}  # to find corresponding currency rate, avoiding iteration through arrays
        # new key to the dictionary mapped to the currency, adding to the dictionary currency_country_name (15) which is = to name(0) and currency_alphabetic_code(14)
        # new key to the dictionary mapped to the country, adding to the dictionary name(0) which is = to name(0) and currency_alphabetic_code(14)

        with open(rateFile, encoding='utf-8') as csvfile:  # The CurrencyConverter reads the csv file for rate
            csv_source = csv.reader(csvfile, delimiter=',')
            for row in csv_source:
                if row[0] == 'name':  # if the data type for column 0 is equal to the value name then  skip that line
                    continue  # first row has all the feature names
                self._rate_data[row[1].upper()] = {'name': row[0], 'code': row[1], 'toEuro': float(row[2]),
                                                   'fromEuro': float(row[3])}

    # new key to the dictionary mapped to the rate, adding to the dictionary country and its currency(0) as a name, code(1), to Euro exchange rate(2),from Euro (3)

    def exchange_rate(self, country_name):  # function inside of the class takes in argument 'country_name'
        country_name_cleaned = country_name.upper()  # country name in upper case letter
        code = None
        if country_name_cleaned in self._currency_data_currency_name:  # Looking for currency for certain country
            code = self._currency_data_currency_name[country_name_cleaned]['code']
        elif country_name_cleaned in self._currency_data_country_name:
            code = self._currency_data_country_name[country_name_cleaned]['code']
        else:
            raise Exception('Unable to find currency for ' + country_name)

        return self._rate_data[code]['toEuro']  # return into Euro exchange rate
