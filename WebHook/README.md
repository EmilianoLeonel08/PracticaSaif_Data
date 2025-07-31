# Webhook FastAPI

API para envío de webhooks desarrollada con FastAPI.

## Características

- ✅ Envío manual de webhooks
- ✅ Envío automático de webhooks con intervalo configurable
- ✅ Gestión del estado de envíos
- ✅ Cambio dinámico de URL de webhook
- ✅ API REST completa

## Endpoints

### GET `/`
Mensaje de bienvenida

### POST `/send-webhook`
Envía un webhook manual

### GET `/status`
Obtiene el estado actual del sistema

### PUT `/webhook-url?new_url=<URL>`
Actualiza la URL del webhook

### POST `/start-auto-webhook`
Inicia el envío automático de webhooks

### POST `/stop-auto-webhook`
Detiene el envío automático de webhooks

### PUT `/intervalo?segundos=<SEGUNDOS>`
Configura el intervalo de envío automático

## Desarrollo local

1. Activar entorno virtual:
```bash
venv\Scripts\Activate.ps1
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar servidor:
```bash
uvicorn server:app --reload
```

## Despliegue

Desplegado en Render.com con auto-deploy desde GitHub.

URL de producción: [Tu URL de Render aquí]
