from random import randint
from DataGenerator import DataGenerator


class SchedulesDataGenerator(DataGenerator):
    """ Generates data for pools table """

    day_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    def __init__(self, faker):
        super().__init__(faker)
        self.staffIDs = []
        self.poolsID = []
        self.startTimes = []
        self.endTimes = []
        self.dayOfWeeks = []

    def generate_table_data(self, number_of_rows):
        for _ in range(0, number_of_rows//4):
            self.staffIDs.append(randint(2, number_of_rows//20))
            self.poolsID.append(randint(1, number_of_rows//100))
            [start_time, end_time] = self.create_valid_reservation_times()
            self.startTimes.append(start_time)
            self.endTimes.append(end_time)
            self.dayOfWeeks.append(
                self.day_of_week[randint(0, len(self.day_of_week)-1)])

        self.table_data = {
            'STAFFID': self.staffIDs,
            'POOLID': self.poolsID,
            'STARTTIME': self.startTimes,
            'ENDTIME': self.endTimes,
            'DAYOFWEEK': self.dayOfWeeks,
        }

    def create_valid_reservation_times(self):
        """ Creates valid employee work time in HH:MM format string"""
        start_time = DataGenerator.employee_time_list[randint(
            0, 1)]

        if start_time == 7.00:
            end_time = DataGenerator.employee_time_list[1]
        else:
            end_time = DataGenerator.employee_time_list[2]

        return [format(start_time, '.2f'), format(end_time, '.2f')]
