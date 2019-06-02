from random import randint
from DataGenerator import DataGenerator
import pandas as pd
import random as rd


class ReservationDataGenerator(DataGenerator):
    """ Generates data for reservations table """

    def __init__(self, faker):
        super().__init__(faker)
        self.clientIDs = []
        self.poolIDs = []
        self.reservationDates = []
        self.start_times = []
        self.end_times = []
        self.prices = []

    def generate_table_data(self, number_of_rows):
        self.read_csv_files()
        i = 0
        while i < number_of_rows//2:
            clientID = rd.randint(1, number_of_rows//4)
            poolID = rd.randint(1, number_of_rows//100)

            # check if pair meet condition that given client swimming skill is greater or equal than required skill on given pool
            # in order to check this we have to read other two csv files (PoolsData.csv and ClientsData.csv)
            if self.client_data_frame['SWIMMINGSKILL'][clientID] >= self.pool_data_frame['REQUIREDSKILL'][poolID]:
                # if condition is met we need to check if any spots are available on given pool
                if self.pool_data_frame['NUMBEROFPLACES'][poolID] > 0:
                    self.clientIDs.append(clientID)
                    self.poolIDs.append(poolID)
                    reservation_date_object = self.fake.date_this_year(
                        before_today=False, after_today=True)
                    self.reservationDates.append(
                        reservation_date_object.strftime('%d-%b-%Y'))
                    [start_time, end_time] = self.create_valid_reservation_times()
                    self.start_times.append(start_time)
                    self.end_times.append(end_time)
                    self.prices.append(
                        format(DataGenerator.spot_price_list[randint(
                            0, len(DataGenerator.spot_price_list) - 1)], '.2f'))
                    # update number of places
                    self.pool_data_frame.at[poolID,
                                            'NUMBEROFPLACES'] = self.pool_data_frame['NUMBEROFPLACES'][poolID] - 1
                    i += 1

        self.table_data = {
            'CLIENTID': self.clientIDs,
            'POOLID': self.poolIDs,
            'RESERVATIONDATE': self.reservationDates,
            'STARTTIME': self.start_times,
            'ENDTIME': self.end_times,
            'PRICE': self.prices
        }

    def create_valid_reservation_times(self):
        """ Creates valid reservation time in HH:MM format as string """
        start_time = DataGenerator.client_time_list[randint(
            0, len(DataGenerator.spot_price_list) - 3)]
        end_time = DataGenerator.client_time_list[randint(
            0, len(DataGenerator.spot_price_list) - 1)]

        while end_time <= start_time:
            end_time = DataGenerator.client_time_list[randint(
                0, len(DataGenerator.spot_price_list) - 1)]

        return [format(start_time, '.2f'), format(end_time, '.2f')]

    def read_csv_files(self):
        self.client_data_frame = pd.read_csv('../dataLoadersCtl/databaseData/ClientData.csv',
                                             index_col='ID_C',
                                             names=[
                                                 'ID_C', 'NAME', 'SURNAME', 'PERSONALIDENTITYNUMBER', 'PHONENUMBER', 'SWIMMINGSKILL', 'AGE'])
        self.pool_data_frame = pd.read_csv('../dataLoadersCtl/databaseData/PoolData.csv',
                                           index_col='ID_P',
                                           names=['ID_P', 'NUMBEROFPLACES', 'REQUIREDSKILL', 'SPOTPRICE'])
        # replace empty values with 0
        self.pool_data_frame = self.pool_data_frame.fillna(0)
