"""
Module name: variable_action_class.py
Purpose: Finds reactions, shear and moments as the vehicle moves over a simply supported beam.
       : Finds maximum moment and shear and the location they occur along the simply supported a simply beam.
Author: Kelvin Macharia
Year: 2021
"""

import logging
import numpy as np
import pandas as pd

from vehicle_data import vehicle_data_class as vdc
from moving_load_simulator import MovingLoadSimulator as mls

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class AnalysisClass:
    def __init__(self, axle_loads, influence_ordinates_arr):
        self.axle_loads = axle_loads
        self.influence_ordinates_arr = influence_ordinates_arr

        # call class methods
        self.reactions = self.fn_calculate_reactions(axle_loads, influence_ordinates_arr)
        # self.moments = self.fn_calculate_moments()

    @staticmethod
    def fn_calculate_reactions(axle_loads_: np, influence_ordinates_arr_: np) -> np:
        """
        Compute reactions i.e R1 & R2
        :param influence_ordinates_arr_:
        :param axle_loads_:
        :return reactions:
        """
        # Reaction on support 1
        R1 = axle_loads_ * influence_ordinates_arr_
        logging.info(f"R1 = {R1}")

        R1_arr = np.empty((R1.shape[0], 1), dtype=float)
        logging.info(f"R1_arr = {R1_arr}")
        R1_copy = R1.copy()
        for index in range(R1_copy.shape[0]):
            R1_arr[index] = sum(R1[index])

        logging.info(f"Reactions = {R1_arr}")

        return R1  # return


if __name__ == "__main__":
    # get vehicle data from vehicle class
    vehicle_data = vdc()("lm1", 0)
    axle_loads = np.array(vehicle_data.standard_axle_loads["NL1"])  # make it a user input later, for debugging just provide from vehicle data class
    axle_positions = vehicle_data.axle_positions
    logging.info(f"axle_loads: {axle_loads}")
    logging.info(f"axle_positions: {axle_positions}")

    # get simulation data i.e ordinates and axle distances
    simulation_data = mls()(5, 1.0, axle_positions)
    logging.info(f"simulation_data.axle_locations_arr: {simulation_data.axle_locations_arr}")
    logging.info(f"influence_ordinates_arr: {simulation_data.influence_ordinates_arr}")

    sba = AnalysisClass(axle_loads, simulation_data.influence_ordinates_arr)
