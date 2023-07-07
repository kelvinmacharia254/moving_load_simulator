#!/usr/bin/python3
"""
Module name: vehicle_data.py
Purpose: Generate vehicle data
Author: Kelvin Macharia
Year: 2021
"""

import logging
from sys import argv
from collections import namedtuple

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# disable()
class vehicle_data_class:
    """
    vehicle data class. Contains or settings/properties for all load models and vehicles.
    Any property of a load model or vehicle can be request from this class.
    """

    def __call__(self, vehicle_type: str, critical_distance: float = 1.2) -> namedtuple:
        """
        Object of this class is called as a function and returns vehicle data
        :param: vehicle_type:
        :param: critical_distance: # this is a kwarg therefore optional. Only special vehicles have this parameter. Default is 1.2m
        :return: vehicle_data
        """
        try:
            # Ensure only possible critical distance as defined in the UKNA to EN1991 are used
            assert critical_distance == 1.2 or critical_distance == 5.0 or critical_distance == 9.0, \
                str(critical_distance) + " is not a valid critical distance for " + str(vehicle_type)
            # Ensure vehicle_type is of str type
            assert type(vehicle_type) == str, \
                "Vehicle type error. Valid vehicle type: 'LM1', 'LM2', 'SV80', 'SV100' or 'SV196' passed as string."
            # Ensure valid vehicle type are requested.
            assert vehicle_type.upper() == "LM1" or vehicle_type.upper() == "LM2" or vehicle_type.upper() == "SV80" or vehicle_type.upper() == "SV100" \
                   or vehicle_type.upper() == "SV196", \
                str(vehicle_type) + " is not a valid vehicle type.Valid vehicle type:  'LM1', 'LM2', 'SV80', 'SV100' or 'SV196'"

            vehicle_data = self.get_vehicle_data(vehicle_type,
                                                 critical_distance)  # call self.get_vehicle_data to generate vehicle data requested

            return vehicle_data
        except Exception as error_message:
            return error_message

    def get_vehicle_data(self, vehicle_type: str, critical_distance: float) -> namedtuple:
        """
        Generates data for the vehicle type requested by self.__call__().
        :param: str
            vehicle_type
        :param: float
            critical_distance
        :return: namedtuple
            vehicle_data # named tuple data type
        """
        # variable to handle error

        # create a named tuple to store vehicle data
        vehicle_data = namedtuple("vehicle_data", "vehicle_type vehicle_length axle_number standard_udl \
                                                  axle_positions axle_spacings standard_axle_loads  units")

        if vehicle_type.upper() == "LM1":
            vehicle_type = "LM1"
            axle_number = 2
            axle_positions = [0, 1.2]
            axle_spacings = {"s1": 1.2}
            vehicle_length = 1.2
            standard_axle_loads = {"NL1": [300, 300], "NL2": [100, 100], "NL3": [50, 50],
                                   "RA": [0, 0]}  # standard axle load as in Eurocodes & UK N.A
            standard_udl = {"NL1": 5.49, "NL2": 5.50, "NL3": 5.50, "RA": 5.50}

        elif vehicle_type.upper() == "LM2":
            vehicle_type = "LM2"
            axle_number = 0
            axle_positions = [0]
            axle_spacings = {}
            vehicle_length = 0
            standard_axle_loads = {"NL": [400]}  # standard axle load as in Eurocodes & UK N.A
            standard_udl = 0

        elif vehicle_type.upper() == "SV80" or vehicle_type.upper() == "SV100":
            axle_number = 6
            axle_positions = [0, 1.2, 2.4,
                              round((2.4 + critical_distance), 2),
                              round((2.4 + critical_distance + 1.2), 2),
                              round((2.4 + critical_distance + 1.2 + 1.2), 2)]
            axle_spacings = {"s1": 1.2, "s2": 1.2, "s3": float(critical_distance), "s4": 1.2, "s5": 1.2}
            vehicle_length = axle_positions[-1]

            if vehicle_type.upper() == "SV80":
                vehicle_type = "LM3_SV80"
                standard_axle_loads = {
                    "NL": [130, 130, 130, 130, 130, 130]}  # standard axle load as in Eurocodes & UK N.A

            elif vehicle_type.upper() == "SV100":
                vehicle_type = "LM3_SV100"
                standard_axle_loads = {
                    "NL": [165, 165, 165, 165, 165, 165]}  # standard axle load as in Eurocodes & UK N.A

            standard_udl = 0

        elif vehicle_type.upper() == "SV196":
            vehicle_type = "LM3_SV196"
            axle_number = 12
            axle_positions = [0, 4.4, 6.0, 10, 11.2, 12.4, 13.6,
                              round((13.6 + critical_distance), 2),
                              round((13.6 + critical_distance + 1.2), 2),
                              round((13.6 + critical_distance + 1.2 + 1.2), 2),
                              round((13.6 + critical_distance + 1.2 + 1.2 + 1.2), 2),
                              round((13.6 + critical_distance + 1.2 + 1.2 + 1.2 + 1.2), 2)
                              ]
            axle_spacings = {"s1": 4.4, "s2": 1.6, "s3": 4.0, "s4": 1.2, "s5": 1.2, "s6": 1.2,
                             "s7": float(critical_distance), "s8": 1.2, "s9": 1.2, "s10": 1.2, "s11": 1.2}
            vehicle_length = axle_positions[-1]
            standard_axle_loads = {"NL": [165, 165, 165, 165, 165, 165, 165, 165, 165, 180, 180,
                                          100]}  # standard axle load as in Eurocodes & UK N.A
            standard_udl = 0

        units = {"linear": "m", "point_loads": "kN", "udl": "kN/m\u00b2"}

        vehicle_data = vehicle_data(vehicle_type, vehicle_length, axle_number, standard_udl,
                                    axle_positions, axle_spacings, standard_axle_loads,  units)

        return vehicle_data  # return named tuple containing vehicle data requested


# self test code
# Find out about argparse and implement to prevent bugs when running on console
if __name__ == "__main__":
    if len(argv) > 1:
        # run from command line
        vehicle_data = vehicle_data_class()(str(argv[1]), float(argv[2]))
        logging.info(vehicle_data)
    else:
        vehicle_data = vehicle_data_class()("sv80", 1.2)
        logging.info(vehicle_data.axle_positions)

# Refactoring possibilities
# use of numpy and pandas
