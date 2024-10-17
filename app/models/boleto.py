from pydantic import BaseModel
from typing import List, Optional

from app.models.transacao import History, PaymentMethod, PointOfSale  

# classes do body
class Address(BaseModel):
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    
class FineObject(BaseModel):
    mode: str
    value: int
    
class FeesObject(BaseModel):
    mode: str
    value: int            
    
class Billet(BaseModel):
    amount: str
    instruction: str
    expiration: str
    fine: FineObject
    fees: FeesObject
    payment_type: str

class Boleto(BaseModel):
    first_name: str
    last_name: str
    document: str
    email: str
    address: Address
    billet: Billet
    
    
# classes de response Transacao do arquivo transacao.py
    
    
    
    

    