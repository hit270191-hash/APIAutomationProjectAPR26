import random
from _datetime import datetime
from faker import Faker
from datamodels.Cart import Cart
from datamodels.CartItems import CartItem
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


    def cart_payload(self):
        userId= random.randint(1,100)
        date = datetime.now().strftime("%Y-%m-%d")
        products=[]
        no_of_products= random.randint(1,5)
        for i in range(no_of_products):
            product=CartItem(
                productId=random.randint(1,10),
                quantity=random.randint(1,5),
            )
            products.append(product)

        return Cart(userId, date, products)
