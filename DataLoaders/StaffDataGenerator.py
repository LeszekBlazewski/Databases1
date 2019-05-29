from random import randint
from DataGenerator import DataGenerator
import random


class StaffDataGenerator(DataGenerator):
    """ Generates data for client table """

    staff_jobs = ['Ratownik', 'Sprzątacz',
                  'Kasjer', 'Ochroniarz', 'Młodszy ratownik', 'Szatniarz']

    def __init__(self, faker):
        super().__init__(faker)
        self.names = []
        self.surnames = []
        self.salaries = []
        self.jobs = []
        self.supervisors = []

    def generate_table_data(self, number_of_rows):
        for i in range(0, number_of_rows):
            self.names.append(self.fake.first_name())
            self.surnames.append(self.fake.last_name())
            job = self.staff_jobs[randint(0, len(self.staff_jobs)-1)]
            self.jobs.append(job)
            self.salaries.append(self.create_valid_salary(job))
            if i % 10 != 0:                                         # not all workers should have supervisor
                self.supervisors.append(randint(1, number_of_rows))
            else:
                self.supervisors.append('')

        self.table_data = {
            'NAME': self.names,
            'SURNAME': self.surnames,
            'SALARY': self.salaries,
            'JOBS': self.jobs,
            'supervisors': self.supervisors
        }

    def create_valid_salary(self, staff_job):
        if staff_job == 'Kasjer' or staff_job == 'Sprzątacz' or staff_job == 'Szatniarz' or staff_job == 'Młodszy ratownik':
            return round(random.uniform(2000, 3000), 2)

        if staff_job == 'Ratownik' or staff_job == 'Ochroniarz':
            return round(random.uniform(4000, 6000), 2)
