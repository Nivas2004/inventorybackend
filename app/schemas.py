from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    category: str
    supplier: str
    purchasePrice: float
    sellingPrice: float
    stock: int


