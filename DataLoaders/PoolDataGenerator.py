from random import randint
from DataGenerator import DataGenerator


class PoolDataGenerator(DataGenerator):
    """ Generates data for pools table """

    def __init__(self, faker):
        super().__init__(faker)
        self.number_of_places = []
        self.required_skill = []
        self.spot_price = []

    def generate_table_data(self, number_of_rows):
        for _ in range(0, number_of_rows//100):
            self.number_of_places.append(randint(20, 150))
            self.required_skill.append(randint(1, 10))
            self.spot_price.append(
                DataGenerator.spot_price_list[randint(
                    0, len(DataGenerator.spot_price_list) - 1)]
            )

        self.table_data = {
            'NUMBEROFPLACES': self.number_of_places,
            'REQUIREDSKILL': self.required_skill,
            'SPOTPRICE': self.spot_price
        }
