# backend/main.py
from datetime import datetime
import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()


WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhooks/new-subscription")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "10"))


app = FastAPI(title="Webhook Automático cada 10s")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React client
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Subscription(BaseModel):
    username: str
    monthly_fee: float
    start_date: datetime

last_subscription: Subscription | None = None

@app.post("/webhooks/new-subscription")
async def new_subscription(body: Subscription, request: Request):
    global last_subscription
    last_subscription = body
    print("Webhook recibido:", body)
    return {
        "message": "Suscripción procesada automáticamente",
        "data": body.dict()
    }

@app.get("/last-subscription")
def get_last_subscription():
    if last_subscription:
        return last_subscription.dict()
    return {"message": "No hay suscripciones aún"}

@app.get("/users/")
def read_users():
    return ["Rick", "Morty"]

async def disparar_webhook():
    payload = {
        "username": "leonardo",
        "monthly_fee": 19.99,
        "start_date": datetime.utcnow().isoformat()
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8000/webhooks/new-subscription", json=payload)
            print(f"Webhook enviado [{response.status_code}]")
            print(f"🌐 Usando URL: {WEBHOOK_URL}")
            print(f"🕒 Intervalo configurado: {INTERVAL_SECONDS} segundos")

        except Exception as e:
            print("Error:", str(e))

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def arrancar_scheduler():
    scheduler.add_job(disparar_webhook, "interval", seconds=10)
    scheduler.start()
    print("Webhook activado cada 10 segundos")