import random
from DataGenerator import DataGenerator


class PoolDataGenerator(DataGenerator):
    """ Generates data for pools table """

    def __init__(self, faker):
        super().__init__(faker)
        self.number_of_places = []
        self.required_skill = []
        self.spot_price = []
        self.number_of_places_values = [20, 30, 40, 50, 60,  70,  80, 90, 100]

    def generate_table_data(self, number_of_rows):
        for i in range(0, number_of_rows//100):
            self.number_of_places.append(
                random.choice(self.number_of_places_values))
            # two pools have their required skill set to null and that means that anyone can join it
            if i in (4, 19):
                self.required_skill.append('')
            else:
                self.required_skill.append(random.randint(1, 10))

            self.spot_price.append(
                DataGenerator.spot_price_list[random.randint(
                    0, len(DataGenerator.spot_price_list) - 1)]
            )

        self.table_data = {
            'NUMBEROFPLACES': self.number_of_places,
            'REQUIREDSKILL': self.required_skill,
            'SPOTPRICE': self.spot_price
        }
