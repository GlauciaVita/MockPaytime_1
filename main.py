from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from app.endpoints import rotas

app = FastAPI()
executor = ThreadPoolExecutor()  

app.include_router(rotas.router, prefix="/mock/paytime/v1", tags=["paytime"])

@app.get('/', summary='Go to the docs')
def root():
    return RedirectResponse(url='/docs')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
