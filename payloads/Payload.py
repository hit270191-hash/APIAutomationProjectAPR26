import random

from faker import Faker
from datamodels.Product import Product


class Payload:
    faker = Faker()
    categories= ["electronics", "fitness", "home", "furniture", "wearables"]

    def products_payload(self):
        title = self.faker.unique.catch_phrase()
        description = self.faker.sentence()
        price= float(self.faker.pricetag().replace("$","").replace(",",""))
        category= random.choice(self.categories)
        stock= random.randint(1,100)
        return Product(title, price, description, category, stock)