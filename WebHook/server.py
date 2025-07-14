#Cómandos de ejecución: 
# Enviar webhook
#curl.exe -X POST http://localhost:8000/send-webhook
# Ver estado
#curl.exe http://localhost:8000/status
# Cambiar URL del webhook
#curl.exe -X PUT "http://localhost:8000/webhook-url?new_url=https
#://nueva-url.com"
# Enviar webhook automático
#curl.exe -X POST http://localhost:8000/start-auto-webhook
# Enviar webhook automático con intervalo
#curl.exe -X POST http://localhost:8000/start-auto-webhook?intervalo=
#curl.exe -X POST http://localhost:8000/stop-auto-webhook
# Para ejecutar el servidor FastAPI, usa el comando:
# uvicorn server:app 
# Para Render: uvicorn server:app --host 0.0.0.0 --port $PORT
import requests
import json
import time
import datetime
import asyncio
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Webhook API", description="API para envío de webhooks", version="1.0.0")

# Configurar CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

webhook_url = "https://webhook.site/5b773625-6bfe-43f4-b462-1d5634ab1df6"
contador = 0
intervalo_segundos = 2  # Tiempo por defecto
enviando_automatico = False 

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI en Render!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

headers = {
    "Content-Type": "application/json"
}

@app.post("/send-webhook")
def send_webhook():
    global contador
    contador += 1
    payload = {
        "mensaje": "Hola desde Python xd", 
        "usuario": "Emiliano:", 
        "tecnologia": "FastAPI",
        "timestamp": datetime.datetime.now().isoformat(),
        "numero_envios": contador
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return {"status": response.status_code, "numero_envio": contador} 

@app.put("/webhook-url")
def update_webhook_url(new_url: str):
    global webhook_url
    webhook_url = new_url
    return {"mensaje": "Webhook URL actualizado", "nueva_url": webhook_url}

@app.get("/status")
def get_status():
    return {
        "webhook_url": webhook_url, 
        "total_envios": contador,
        "intervalo_segundos": intervalo_segundos,
        "enviando_automatico": enviando_automatico
    }

@app.put("/intervalo")
def update_intervalo(segundos: int):
    global intervalo_segundos
    if segundos <= 0:
        return {"error": "El intervalo debe ser mayor a 0"}
    intervalo_segundos = segundos
    return {"mensaje": "Intervalo actualizado", "nuevo_intervalo": segundos}
#Para iniciar el envío automático de webhooks puede ser directamente desde el powershell con el comando: curl.exe -X POST http://localhost:8000/start-auto-webhook

@app.post("/start-auto-webhook")
async def start_auto_webhook(background_tasks: BackgroundTasks):
    global enviando_automatico
    if enviando_automatico:
        return {"mensaje": "Ya hay webhooks automáticos ejecutándose"}
    
    enviando_automatico = True
    background_tasks.add_task(enviar_webhooks_automaticos)
    return {"mensaje": f"Iniciando webhooks automáticos cada {intervalo_segundos} segundos"}

#Para iniciar el envío automático de webhooks puede ser directamente desde el powershell con el comando: curl.exe -X POST http://localhost:8000/stop-auto-webhook
@app.post("/stop-auto-webhook")
def stop_auto_webhook():
    global enviando_automatico
    enviando_automatico = False
    return {"mensaje": "Webhooks automáticos detenidos"}

async def enviar_webhooks_automaticos():
    global contador, enviando_automatico
    while enviando_automatico:
        contador += 1
        payload = {
            "mensaje": "Webhook automático desde FastAPI",
            "usuario": "Emiliano:",
            "tecnologia": "FastAPI + Background Tasks",
            "timestamp": datetime.datetime.now().isoformat(),
            "numero_envios": contador
        }
        try:
            requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            print(f"Webhook automático #{contador} enviado")
        except Exception as e:
            print(f"Error enviando webhook: {e}")
        
        await asyncio.sleep(intervalo_segundos) 