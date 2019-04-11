from random import randint
from DataGenerator import DataGenerator
import random


class StaffDataGenerator(DataGenerator):
    """ Generates data for client table """

    def __init__(self, faker):
        super().__init__(faker)
        self.names = []
        self.surnames = []
        self.salaries = []
        self.jobs = []
        self.supervisors = []

    def generate_table_data(self, number_of_rows):
        for _ in range(0, number_of_rows):
            self.names.append(self.fake.first_name())
            self.surnames.append(self.fake.last_name())
            self.salaries.append(round(random.uniform(2500, 20000), 2))
            self.jobs.append(self.fake.job())
            self.supervisors.append(randint(1, 100))

        self.table_data = {
            'NAME': self.names,
            'SURNAME': self.surnames,
            'SALARY': self.salaries,
            'JOBS': self.jobs,
            'supervisors': self.supervisors
        }
