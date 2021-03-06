from ClientDataGenerator import ClientDataGenerator
from PoolDataGenerator import PoolDataGenerator
from ReservationDataGenerator import ReservationDataGenerator
from SchedulesDataGenerator import SchedulesDataGenerator
from StaffDataGenerator import StaffDataGenerator


import pandas as pd
from faker import Faker


class CsvCreator(object):

    def __init__(self):
        # initialize the random generator which is passed to each object
        fake = Faker('pl_PL')
        # Create Generators
        client_generator = ClientDataGenerator(fake)
        pool_generator = PoolDataGenerator(fake)
        reservation_generator = ReservationDataGenerator(fake)
        schedule_generator = SchedulesDataGenerator(fake)
        staff_generator = StaffDataGenerator(fake)
        # Add all generators to list for easier management
        self.generators = [client_generator,
                           pool_generator,
                           staff_generator,
                           reservation_generator,
                           schedule_generator]
        # Set file names
        self.file_names = ["../dataLoadersCtl/databaseData/ClientData.csv",
                           "../dataLoadersCtl/databaseData/PoolData.csv",
                           "../dataLoadersCtl/databaseData/StaffData.csv",
                           "../dataLoadersCtl/databaseData/ReservationData.csv",
                           "../dataLoadersCtl/databaseData/ScheduleData.csv"]

    def generate_database_data(self, number_of_rows_for_table):
        # for each generator create new data, convert it to dataframe and save to csv
        file_iter = 0
        for generator in self.generators:
            generator.generate_table_data(number_of_rows_for_table)
            data_frame = pd.DataFrame(generator.get_table_data())
            data_frame.index = data_frame.index + 1
            # because tables ReservationData and ScheduleData does not inlcude ID as PK skip indexes generated by pd
            if self.file_names[file_iter] == "../dataLoadersCtl/databaseData/ReservationData.csv" or self.file_names[file_iter] == "../dataLoadersCtl/databaseData/ScheduleData.csv":
                data_frame.to_csv(
                    self.file_names[file_iter], header=False, index=False)
            else:
                data_frame.to_csv(
                    self.file_names[file_iter], header=False)
            file_iter += 1


def main():
    csv_creator = CsvCreator()
    csv_creator.generate_database_data(2000)


if __name__ == "__main__":
    main()
