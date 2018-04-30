#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `journey_planer` package."""

import unittest
from classes import *
from optimizer import Optimizer


class Test(unittest.TestCase):

    def test_spherical_distance(self):
        optimizer = Optimizer(None, None, None)
        assert optimizer.spherical_distance(Coordinate(0.0, 0.0), Coordinate(0.0, 0.0)) == 0
        assert optimizer.spherical_distance(Coordinate(0.0, 1.1), Coordinate(1.1, 1.1)) == 122

    def test_premutations(self):
        optimizer = Optimizer(None, None, None)
        all_permutations = optimizer.get_all_permutations(['A', 'B'])
        assert len(all_permutations) == 2
        all_permutations = optimizer.get_all_permutations(['A', 'B', 'C', 'D'])
        assert len(all_permutations) == 24

    def test_aircraft_holder(self):
        aircraft_holder = AircraftParser('./input/aircraft.csv')
        aircraft = aircraft_holder.get_aircraft('747')
        assert aircraft != None
        assert aircraft.name == 'Boeing 747'

    def test_airport_holder(self):
        airport_holder = AirportParser('./input/airport.csv')
        airport = airport_holder.get_airport('DUB')
        assert airport != None
        assert airport.country == 'Ireland'

    def test_currency(self):
        currency_holder = CurrencyConverter('./input/countrycurrency.csv', './input/currencyrates.csv')
        assert currency_holder.exchange_rate('Ireland') == 1.0
        assert currency_holder.exchange_rate('IRELAND') == 1.0
        assert currency_holder.exchange_rate('Russia') == 0.01524
        assert currency_holder.exchange_rate('Russian Federation') ==  0.01524

    def test_optimizer(self):
        aircraft_holder = AircraftParser('./input/aircraft.csv')
        airport_holder = AirportParser('./input/airport.csv')
        currency_holder = CurrencyConverter('./input/countrycurrency.csv', './input/currencyrates.csv')
        optimizer = Optimizer(aircraft_holder, airport_holder, currency_holder)
        result, price = optimizer.optimize(['JOK','STE','TMP','YUL','KPC'], '747')
        assert len(result) == 6
        assert price == 12018.82634

if __name__ == '__main__':
    unittest.main()
