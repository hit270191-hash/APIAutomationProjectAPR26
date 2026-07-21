from dataclasses import dataclass

@dataclass
class CartItem:
    productId: int
    quantity: int