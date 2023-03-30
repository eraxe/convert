from fastapi import FastAPI
from get.router import router as get_router
from convert.router import router as convert_router
from send.router import router as send_router

app = FastAPI()

app.include_router(get_router, prefix="/get", tags=["get"])
app.include_router(convert_router)
app.include_router(send_router, prefix="/send", tags=["send"])
