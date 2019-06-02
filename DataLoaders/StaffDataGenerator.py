from random import randint
from DataGenerator import DataGenerator
import random


class StaffDataGenerator(DataGenerator):
    """ Generates data for staff table """

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
        self.create_supervisors()
        for i in range(6, number_of_rows//20):
            self.names.append(self.fake.first_name())
            self.surnames.append(self.fake.last_name())
            job = self.staff_jobs[randint(0, len(self.staff_jobs)-1)]
            self.jobs.append(job)
            self.salaries.append(self.create_valid_salary(job))
            shouldGetSupervisor = randint(1, 10)
            # not all workers should have supervisor
            if i not in (9, 10):
                # only first 4 rows specifie supervisors so assign other to them
                if job == 'Ratownik' or job == 'Młodszy ratownik':
                    self.supervisors.append(2)
                elif job == 'Sprzątacz':
                    self.supervisors.append(3)
                elif job == 'Kasjer':
                    self.supervisors.append(4)
                elif job == 'Ochroniarz':
                    self.supervisors.append(5)
                else:
                    self.supervisors.append(6)
            else:
                self.supervisors.append('')         # no supervisor

        self.table_data = {
            'NAME': self.names,
            'SURNAME': self.surnames,
            'SALARY': self.salaries,
            'JOBS': self.jobs,
            'supervisors': self.supervisors
        }

    def create_valid_salary(self, staff_job):
        if staff_job in ('Kasjer', 'Sprzątacz', 'Szatniarz', 'Młodszy ratownik'):
            return int(random.uniform(2000, 3000))

        if staff_job in ('Ratownik', 'Ochroniarz'):
            return int(random.uniform(4000, 6000))

        if staff_job == 'Dyrektor':
            return 10000

    def create_supervisors(self):
        # before generating normal workers, generate supervisors for them and the director
        # 1. Create director
        for i in range(1, 7):
            self.names.append(self.fake.first_name())
            self.surnames.append(self.fake.last_name())
            if i == 1:
                job = 'Dyrektor'
            elif i == 2:
                job = 'Ratownik'
            elif i == 3:
                job = 'Sprzątacz'
            elif i == 4:
                job = 'Kasjer'
            elif i == 5:
                job = 'Ochroniarz'
            elif i == 6:
                job = 'Szatniarz'
            self.jobs.append(job)
            self.salaries.append(self.create_valid_salary(job))
            if i in (2, 3, 4, 5, 6):
                # supervisors diffrent from directror have director as their supervisor
                self.supervisors.append(1)
            else:
                self.supervisors.append('')
