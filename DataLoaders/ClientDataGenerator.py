from random import randint
from DataGenerator import DataGenerator


class ClientDataGenerator(DataGenerator):
    """ Generates data for client table """

    def __init__(self, faker):
        super().__init__(faker)
        self.names = []
        self.surnames = []
        self.social_numbers = []
        self.phone_numbers = []
        self.swimming_skills = []
        self.ages = []

    def generate_table_data(self, number_of_rows):
        for _ in range(0, number_of_rows):
            self.names.append(self.fake.first_name())
            self.surnames.append(self.fake.last_name())
            social_number_string = self.create_valid_social_number()
            self.social_numbers.append(social_number_string)
            self.ages.append(
                self.calculate_age_based_on_social_number(social_number_string))
            self.swimming_skills.append(randint(1, 10))
            self.phone_numbers.append(self.fake.phone_number())

        self.table_data = {
            'NAME': self.names,
            'SURNAME': self.surnames,
            'PERSONALITYIDENTITYNUMBER': self.social_numbers,
            'PHONENUMBER': self.phone_numbers,
            'SWIMINGSKILL': self.swimming_skills,
            'AGE': self.ages
        }

    def create_valid_social_number(self):
        """ We don't want to allow clients with ssn starting with 1 because they are to young """

        social_number_string = self.fake.ssn()

        while social_number_string[0] == '1':
            social_number_string = self.fake.ssn()
        else:
            return social_number_string
