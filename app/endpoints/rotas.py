from concurrent.futures import ThreadPoolExecutor
import datetime
import secrets
import random
from fastapi import APIRouter, HTTPException, Header, Request
from app.models.boleto import Boleto
from app.models.token_cartao import TokenCartao
from app.models.transacao import History, PaymentMethod, PointOfSale, Transacao, TransacaoBody

router = APIRouter()
executor = ThreadPoolExecutor() 

client_token_fixed = "testepdv123"
client_token_access = ""
client_refresh_token = ""
store_id_fixed = 10
list_transaction_id = []

@router.post("/oauth")
async def criarToken(request: Request):
    global client_token_access 
    global client_refresh_token 
    
    body = await request.json()
    if body.get("client_token") == client_token_fixed:
        token = secrets.token_hex(16)
        refresh_token = secrets.token_hex(32)
        
        client_refresh_token = refresh_token
        client_token_access = token
        print("token salvo", client_token_access)
        print("refreshtoken salvo", client_refresh_token)

        return {
            "type": "teste pdv",
            "token": token,
            "refreshToken": refresh_token
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid client token")

@router.post("/refresh")
async def refreshToken(request: Request):
    global client_token_access 
    global client_refresh_token 
    
    body = await request.json()
    if body.get("refresh_token") == client_refresh_token:
        token = secrets.token_hex(16)
        refresh_token = secrets.token_hex(32)
        
        client_refresh_token = refresh_token
        print("refreshtoken salvo", client_refresh_token)
        
        return {
            "type": "teste pdv",
            "token": token,
            "refreshToken": refresh_token
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid refresh token")    

    
@router.post("/stores/{storeId}/cards/token")
async def criarTokenCard(
    storeId: int, 
    token_cartao_body: TokenCartao,
    authorization: str = Header(None)):
    
    print("storeId:", storeId)
    print("body:", token_cartao_body)
    print(f"Authorization header recebido: {authorization}")
    print(f"Token esperado: Bearer {client_token_access}")
    
    if storeId != store_id_fixed:
        raise HTTPException(status_code=401, detail="Invalid store id")

    if authorization != f"Bearer {client_token_access}":
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization token")
    
    token = secrets.token_hex(16)
    
    return {
        "token": token,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
    
    
@router.post("/stores/{storeId}/transactions")
async def criaTransacao(
    storeId: int, 
    transacao_body: TransacaoBody,
    authorization: str = Header(None)):
    
    global list_transaction_id
    
    if storeId != store_id_fixed:
        raise HTTPException(status_code=401, detail="Invalid store id")

    if authorization != f"Bearer {client_token_access}":
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization token")
    
    valor_dividido = transacao_body.amount / transacao_body.installment
    
    id_aleatorio = random.randrange(0,100)
    print("id",  id_aleatorio)
    
    list_transaction_id.append(id_aleatorio)
    print("lista de ids", list_transaction_id)

    transacao = Transacao(
    id=str(id_aleatorio),
    resource="payment",
    status="approved",
    amount=float(valor_dividido),
    original_amount=transacao_body.amount,
    currency="BRL",
    description="Pagamento de serviço",
    payment_type=transacao_body.card.payment_type,
    gateway_authorizer="zoop",
    on_behalf_of="empresa_teste",
    customer=transacao_body.card.holder_name,
    statement_descriptor="Pagamento",
    payment_method=PaymentMethod(
        id="pm_001",
        zoop_boleto_id="",
        resource="debito",
        description=transacao_body.card.description,
        reference_number="12345678910",
        document_number="123456",
        expiration_date="",
        recipient="empresa_recebedora",
        bank_code="",
        customer=transacao_body.card.holder_name,
        sequence="",
        url="",
        accepted=True,
        printed=False,
        downloaded=False,
        barcode="",
        metadata={"extra_info": "metadata geral"},
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
        status="pago"
    ),
    point_of_sale=PointOfSale(
        entry_mode="online",
    ),
    refunded=False,
    voided=False,
    captured=True,
    fees="",
    metadata={"info": "point of sale metadata"},
    created_at=str(datetime.datetime.now()),
    updated_at=str(datetime.datetime.now()),
    history=[
        History(
            id="hist_001",
            transaction="trans_001",
            amount=transacao_body.amount,
            operation_type="capture",
            status="approved",
            created_at=str(datetime.datetime.now()),
        )
    ],
    gateway_key="gateway_key_001"
    )
    
    return transacao


@router.post("/stores/{storeId}/transactions/{transactionId}/reversal")
async def estornaTransacao(
    storeId: int, 
    transactionId: int,
    authorization: str = Header(None)):
    
    global list_transaction_id
    
    if storeId != store_id_fixed:
        raise HTTPException(status_code=401, detail="Invalid store id")
    
    if authorization != f"Bearer {client_token_access}":
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization token")
    
    if(transactionId not in list_transaction_id):
        raise HTTPException(status_code=401, detail="Invalid transaction id")
    else:
        list_transaction_id.remove(transactionId)
        print("lista de ids", list_transaction_id)
        return f"Transação {transactionId} estornada com sucesso!"
    


@router.post("/stores/{storeId}/billet")
async def criaBoleto(
    storeId: int,
    boleto_body: Boleto,
    authorization: str = Header(None)):
    
    global list_transaction_id
    
    if storeId != store_id_fixed:
        raise HTTPException(status_code=401, detail="Invalid store id")

    if authorization != f"Bearer {client_token_access}":
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization token")
    
    id_aleatorio = random.randrange(0,100)
    print("id",  id_aleatorio)
    list_transaction_id.append(id_aleatorio)
    print("lista de ids", list_transaction_id)
    
    billet = Transacao(
    id=str(id_aleatorio),
    resource="payment",
    status="approved",
    amount=boleto_body.billet.amount,
    original_amount=boleto_body.billet.amount,
    currency="BRL",
    description="Pagamento de serviço",
    payment_type="boleto",
    gateway_authorizer="zoop",
    on_behalf_of="empresa_teste",
    customer= boleto_body.first_name,
    statement_descriptor="Pagamento",
    payment_method=PaymentMethod(
        id="pm_002",
        zoop_boleto_id="zpb_001",
        resource="boleto",
        description=boleto_body.billet.payment_type,
        reference_number="12345",
        document_number="987654321",
        expiration_date="2024-12-31",
        recipient="empresa_recebedora",
        bank_code="001",
        customer=boleto_body.first_name,
        sequence="001",
        url="https://boleto.com.br/download",
        accepted=True,
        printed=False,
        downloaded=False,
        barcode="12345678901234567890",
        metadata={"extra_info": "metadata geral"},
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
        status="emitido"
    ),
    point_of_sale=PointOfSale(
        entry_mode="online",
    ),
    refunded=False,
    voided=False,
    captured=True,
    fees=boleto_body.billet.fees.mode,
    metadata={"info": "point of sale metadata"},
    created_at=str(datetime.datetime.now()),
    updated_at=str(datetime.datetime.now()),
    history=[
        History(
            id="hist_001",
            transaction="trans_001",
            amount=boleto_body.billet.amount,
            operation_type="capture",
            status="approved",
            created_at=str(datetime.datetime.now()),
        )
    ],
    gateway_key="gateway_key_001"
    )
    
    return billet
    
    
    
    
    
    
        




