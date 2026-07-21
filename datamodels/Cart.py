from dataclasses import dataclass
from typing import List
from datamodels.CartItems import CartItem

@dataclass
class Cart:
    userId: int
    date: str
    products: List[CartItem]