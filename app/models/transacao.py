from pydantic import BaseModel, Field
from typing import List, Optional

from app.models.token_cartao import Address

# classe do body
class CardTransacao(BaseModel):
    id: int
    holder_name: str
    expiration_month: str
    expiration_year: str
    card_number: str
    security_code: str
    payment_type: str
    description: str

class TransacaoBody(BaseModel):
    amount: int
    first_name: str
    last_name: str
    document: str
    email: str
    address: Address
    card: CardTransacao
    installment: int


#classes de response
class PaymentMethod(BaseModel):
    id: str
    zoop_boleto_id: str
    resource: str
    description: str
    reference_number: str
    document_number: str
    expiration_date: str
    recipient: str
    bank_code: str
    customer: str
    sequence: str
    url: str
    accepted: bool
    printed: bool
    downloaded: bool
    barcode: str
    metadata: object
    created_at: str
    updated_at: str
    status: str

class PointOfSale(BaseModel):
    entry_mode: str
    

class History(BaseModel):
    id: str
    transaction: str
    amount: str
    operation_type: str
    status: str
    created_at: str
    

class Transacao(BaseModel):
    id: str
    resource: str
    status: str
    amount: float
    original_amount: float
    currency: str
    description: str
    payment_type: str
    gateway_authorizer: str
    on_behalf_of: str
    customer: str
    statement_descriptor: str
    payment_method: PaymentMethod
    point_of_sale: PointOfSale
    refunded: Optional[bool] = None
    voided: Optional[bool] = None
    captured: Optional[bool] = None
    fees: Optional[str] = None
    metadata: object
    created_at: str
    updated_at: str
    history: List[History]
    gateway_key: str

