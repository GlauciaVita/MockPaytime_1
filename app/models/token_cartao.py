from pydantic import BaseModel
from typing import List, Optional  

class Address(BaseModel):
    street: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    
class Card(BaseModel):
    holder_name: str
    expiration_month: str
    expiration_year: str
    card_number: str
    security_code: str

class TokenCartao(BaseModel):
    first_name: str
    last_name: str
    document: str
    email: str
    address: Address
    card: Card

    