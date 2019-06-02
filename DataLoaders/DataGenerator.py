from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class DataGenerator(ABC):
    """ Defines abstract skeleton for all data generators for specific tables """

    spot_price_list = np.arange(10.5, 100, 5.5)

    client_time_list = (pd.timedelta_range(
        '07:00:00', periods=33, freq="30T")).astype(str)

    client_time_list = [float(x[0:4].replace(':', '.'))
                        for x in client_time_list]

    employee_time_list = [7.00, 15.00, 23.00]

    def __init__(self, faker):
        self.fake = faker
        self.table_data = {}
        super().__init__()

    @abstractmethod
    def generate_table_data(self, number_of_rows_to_generate):
        pass

    def get_table_data(self):
        return self.table_data

    def calculate_age_based_on_social_number(self, social_number_string):
        """ Calculates age based on SSN"""
        year = int(social_number_string[0:2])
        month = int(social_number_string[2:4])
        year += {
            0: 1900,
            1: 2000,
            2: 2100,
            3: 2200,
            4: 1800,
        }[month // 20]
        return 2019 - year
