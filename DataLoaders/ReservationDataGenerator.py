from random import randint
from DataGenerator import DataGenerator


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
        for _ in range(0, number_of_rows):
            self.clientIDs.append(randint(1, 100))
            self.poolIDs.append(randint(1, 100))
            reservation_date_object = self.fake.date_this_year(
                before_today=False, after_today=True)
            self.reservationDates.append(
                reservation_date_object.strftime('%d-%m-%Y'))
            [start_time, end_time] = self.create_valid_reservation_times()
            self.start_times.append(start_time)
            self.end_times.append(end_time)
            self.prices.append(
                format(DataGenerator.spot_price_list[randint(
                    0, len(DataGenerator.spot_price_list) - 1)], '.2f')
            )

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
