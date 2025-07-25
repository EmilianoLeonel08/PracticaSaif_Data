#Cómandos de ejecución: 

# ENDPOINTS BÁSICOS:
# Enviar webhook con parámetros personalizados
#curl.exe -X POST "https://practicasaif-data-webhook.onrender.com/send-webhook?mensaje=MiMensaje&usuario=MiUsuario&tecnologia=MiTech"
# Ver estado completo
#curl.exe https://practicasaif-data-webhook.onrender.com/status
# 
# CONFIGURACIÓN DINÁMICA:
# Cambiar usuario por defecto
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/config/usuario?nuevo_usuario=NuevoUsuario"
# Cambiar tecnología por defecto
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/config/tecnologia?nueva_tecnologia=NuevaTech"
# Cambiar mensaje por defecto
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/config/mensaje?nuevo_mensaje=NuevoMensaje"
# Cambiar mensaje automático por defecto
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/config/mensaje-auto?nuevo_mensaje=NuevoMensajeAuto"
# 
# WEBHOOKS:
# Cambiar URL del webhook
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/webhook-url?new_url=https://nueva-url.com"
# Cambiar intervalo
#curl.exe -X PUT "https://practicasaif-data-webhook.onrender.com/intervalo?segundos=10"
# 
# AUTOMÁTICOS:
# Enviar webhook automático
#curl.exe -X POST https://practicasaif-data-webhook.onrender.com/start-auto-webhook
#curl.exe -X POST https://practicasaif-data-webhook.onrender.com/stop-auto-webhook
# Para ejecutar el servidor FastAPI, usa el comando:
# uvicorn server:app 
# Para Render: uvicorn server:app --host 0.0.0.0 --port $PORT
# Para probar el despliegue en Render, puedes usar el siguiente comando:
#curl.exe -X POST https://practicasaif-data-webhook.onrender.com/
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

# Para Render - detectar puerto automáticamente
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)

# Variables de entorno con valores por defecto
WEBHOOK_URL_DEFAULT = os.environ.get("WEBHOOK_URL", "https://webhook.site/5b773625-6bfe-43f4-b462-1d5634ab1df6")
USUARIO_DEFAULT = os.environ.get("USUARIO", "Usuario por defecto")
TECNOLOGIA_DEFAULT = os.environ.get("TECNOLOGIA", "FastAPI")
MENSAJE_DEFAULT = os.environ.get("MENSAJE", "Hola desde aplicación :D ")
MENSAJE_AUTO_DEFAULT = os.environ.get("MENSAJE_AUTO", "Webhook automático ")
INTERVALO_DEFAULT = int(os.environ.get("INTERVALO_DEFAULT", "5"))
MENSAJE_BIENVENIDA = os.environ.get("MENSAJE_BIENVENIDA", "¡Hola desde FastAPI ;) !")

# Variables globales de la aplicación
webhook_url = WEBHOOK_URL_DEFAULT
usuario_default = USUARIO_DEFAULT
tecnologia_default = TECNOLOGIA_DEFAULT
mensaje_default = MENSAJE_DEFAULT
mensaje_auto_default = MENSAJE_AUTO_DEFAULT
contador = 0
intervalo_segundos = INTERVALO_DEFAULT
enviando_automatico = False 

@app.get("/")
def read_root():
    return {"mensaje": MENSAJE_BIENVENIDA}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

headers = {
    "Content-Type": "application/json"
}

@app.post("/send-webhook")
def send_webhook(mensaje: str = None, usuario: str = None, tecnologia: str = None):
    global contador
    contador += 1
    
    # Usar parámetros recibidos o valores por defecto
    mensaje_final = mensaje or mensaje_default
    usuario_final = usuario or usuario_default
    tecnologia_final = tecnologia or tecnologia_default
    
    payload = {
        "mensaje": mensaje_final, 
        "usuario": usuario_final, 
        "tecnologia": tecnologia_final,
        "timestamp": datetime.datetime.now().isoformat(),
        "numero_envios": contador
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    return {
        "status": response.status_code, 
        "numero_envio": contador,
        "payload_enviado": payload
    } 

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
        "enviando_automatico": enviando_automatico,
        "configuracion": {
            "usuario_default": usuario_default,
            "tecnologia_default": tecnologia_default,
            "mensaje_default": mensaje_default,
            "mensaje_auto_default": mensaje_auto_default,
            "mensaje_bienvenida": MENSAJE_BIENVENIDA
        }
    }

@app.put("/config/usuario")
def update_usuario_default(nuevo_usuario: str):
    global usuario_default
    usuario_default = nuevo_usuario
    return {"mensaje": "Usuario por defecto actualizado", "nuevo_usuario": usuario_default}

@app.put("/config/tecnologia")
def update_tecnologia_default(nueva_tecnologia: str):
    global tecnologia_default
    tecnologia_default = nueva_tecnologia
    return {"mensaje": "Tecnología por defecto actualizada", "nueva_tecnologia": tecnologia_default}

@app.put("/config/mensaje")
def update_mensaje_default(nuevo_mensaje: str):
    global mensaje_default
    mensaje_default = nuevo_mensaje
    return {"mensaje": "Mensaje por defecto actualizado", "nuevo_mensaje": mensaje_default}

@app.put("/config/mensaje-auto")
def update_mensaje_auto_default(nuevo_mensaje: str):
    global mensaje_auto_default
    mensaje_auto_default = nuevo_mensaje
    return {"mensaje": "Mensaje automático por defecto actualizado", "nuevo_mensaje": mensaje_auto_default}

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
            "mensaje": mensaje_auto_default,
            "usuario": usuario_default,
            "tecnologia": tecnologia_default + " + Background Tasks",
            "timestamp": datetime.datetime.now().isoformat(),
            "numero_envios": contador,
            "tipo": "automatico"
        }
        try:
            requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            print(f"Webhook automático #{contador} enviado - {payload['mensaje']}")
        except Exception as e:
            print(f"Error enviando webhook: {e}")
        
        await asyncio.sleep(intervalo_segundos) 