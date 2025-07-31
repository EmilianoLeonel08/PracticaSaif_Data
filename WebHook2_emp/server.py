# API de Empleados - Integración FastAPI + MuleSoft + Oracle
# Comandos esenciales:
# uvicorn server:app --reload
# curl.exe -X POST http://localhost:8000/employees -H "Content-Type: application/json" -d "{\"first_name\":\"Juan\",\"last_name\":\"Pérez\",\"email\":\"juan.perez@test.com\",\"hire_date\":\"2025-07-21\",\"job_id\":\"IT_PROG\",\"salary\":60000,\"department_id\":60}"
# curl -X POST http://localhost:8000/employees -H "Content-Type: application/json" -d "{\"first_name\":\"Juan\",\"last_name\":\"Pérez\",\"email\":\"juan.perez@test.com\",\"phone_number\":\"555-1234\",\"hire_date\":\"2025-07-21\",\"job_id\":\"IT_PROG\",\"salary\":60000,\"department_id\":60}"
# 
# Webhooks automáticos:
# curl.exe -X POST http://localhost:8000/start-auto-webhook
# curl.exe -X POST http://localhost:8000/stop-auto-webhook
# curl.exe -X PUT "http://localhost:8000/intervalo?segundos=5"
import requests
import json
import datetime
import asyncio
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

app = FastAPI(title="Employee API", description="API para gestión de empleados con MuleSoft", version="1.0.0")

# Modelos de datos basados en el esquema de la tabla employees
class EmployeeBase(BaseModel):
    first_name: str = Field(..., max_length=20)
    last_name: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)
    phone_number: Optional[str] = Field(None, max_length=20)
    hire_date: datetime.date
    job_id: str = Field(..., max_length=10)
    salary: Decimal = Field(..., gt=0)  # CHECK (salary > 0)
    commission_pct: Optional[Decimal] = Field(None, ge=0, le=1)  # NUMBER(2,2)
    manager_id: Optional[int] = None
    department_id: Optional[int] = None

class Employee(EmployeeBase):
    employee_id: int

class EmployeeCreate(EmployeeBase):
    pass

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
webhook_url = os.environ.get("WEBHOOK_URL", "http://localhost:8081/employee-webhook")
contador = 0
employees_db: List[Employee] = []
current_employee_id = 207
intervalo_segundos = 10
enviando_automatico = False

headers = {"Content-Type": "application/json"}

# Funciones auxiliares
def get_next_employee_id() -> int:
    global current_employee_id
    id_to_return = current_employee_id
    current_employee_id += 1
    return id_to_return

def find_employee_by_email(email: str) -> Optional[Employee]:
    return next((emp for emp in employees_db if emp.email == email), None)

def send_employee_webhook(action: str, employee: Employee) -> Optional[int]:
    """Envía un webhook en formato XML a MuleSoft cuando se crea un empleado"""
    import xml.etree.ElementTree as ET
    global contador
    contador += 1

    # Construir el XML
    root = ET.Element("webhook")
    ET.SubElement(root, "messageId").text = f"EMP_{contador}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    ET.SubElement(root, "action").text = action
    ET.SubElement(root, "timestamp").text = datetime.datetime.now().isoformat()
    ET.SubElement(root, "source").text = "FastAPI-Employee-Management"
    emp = ET.SubElement(root, "employee")
    ET.SubElement(emp, "employee_id").text = str(employee.employee_id)
    ET.SubElement(emp, "first_name").text = employee.first_name
    ET.SubElement(emp, "last_name").text = employee.last_name
    ET.SubElement(emp, "email").text = employee.email
    ET.SubElement(emp, "phone_number").text = employee.phone_number if employee.phone_number else ""
    ET.SubElement(emp, "hire_date").text = employee.hire_date.isoformat() if employee.hire_date else ""
    ET.SubElement(emp, "job_id").text = employee.job_id
    ET.SubElement(emp, "salary").text = str(float(employee.salary))
    ET.SubElement(emp, "commission_pct").text = str(float(employee.commission_pct)) if employee.commission_pct else ""
    ET.SubElement(emp, "manager_id").text = str(employee.manager_id) if employee.manager_id else ""
    ET.SubElement(emp, "department_id").text = str(employee.department_id) if employee.department_id else ""

    xml_payload = ET.tostring(root, encoding="utf-8", method="xml")

    try:
        response = requests.post(
            webhook_url,
            data=xml_payload,
            headers={"Content-Type": "application/xml"},
            timeout=30
        )
        print(f" Webhook XML enviado a MuleSoft: {action} para empleado {employee.employee_id} - Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f" Error enviando webhook XML a MuleSoft: {e}")
        return None

# ENDPOINTS PRINCIPALES

@app.get("/")
def read_root():
    return {"mensaje": " API de Empleados con MuleSoft integrada", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat(), "total_empleados": len(employees_db)}

@app.post("/employees", response_model=Employee)
def create_employee(employee_data: EmployeeCreate):
    """Crear un nuevo empleado y enviarlo a MuleSoft"""
    # Validar email único
    if find_employee_by_email(employee_data.email):
        raise HTTPException(status_code=400, detail="Email ya existe")
    
    # Crear empleado
    employee = Employee(
        employee_id=get_next_employee_id(),
        **employee_data.model_dump()
    )
    
    employees_db.append(employee)
    
    # Enviar webhook a MuleSoft
    send_employee_webhook("CREATE", employee)
    
    return employee

@app.get("/employees", response_model=List[Employee])
def get_all_employees():
    """Obtener todos los empleados"""
    return employees_db

@app.put("/webhook-url")
def update_webhook_url(new_url: str):
    """Actualizar URL del webhook de MuleSoft"""
    global webhook_url
    webhook_url = new_url
    return {"mensaje": "Webhook URL actualizado", "nueva_url": webhook_url}

@app.get("/status")
def get_status():
    """Ver estado del sistema"""
    return {
        "webhook_url": webhook_url, 
        "total_envios": contador,
        "total_empleados": len(employees_db),
        "enviando_automatico": enviando_automatico,
        "intervalo_segundos": intervalo_segundos
    }

@app.post("/start-auto-webhook")
async def start_auto_webhook(background_tasks: BackgroundTasks):
    """Iniciar envío automático de webhooks"""
    global enviando_automatico
    if enviando_automatico:
        return {"mensaje": "Ya hay webhooks automáticos ejecutándose"}
    
    enviando_automatico = True
    background_tasks.add_task(enviar_webhooks_automaticos)
    return {"mensaje": f"Webhooks automáticos iniciados cada {intervalo_segundos} segundos"}

@app.post("/stop-auto-webhook")
def stop_auto_webhook():
    """Detener envío automático de webhooks"""
    global enviando_automatico
    enviando_automatico = False
    return {"mensaje": "Webhooks automáticos detenidos"}

@app.put("/intervalo")
def update_intervalo(segundos: int):
    """Cambiar intervalo de webhooks automáticos"""
    global intervalo_segundos
    if segundos <= 0:
        return {"error": "El intervalo debe ser mayor a 0"}
    intervalo_segundos = segundos
    return {"mensaje": "Intervalo actualizado", "nuevo_intervalo": segundos}

async def enviar_webhooks_automaticos():
    """Función que envía webhooks automáticos en segundo plano"""
    global contador, enviando_automatico, current_employee_id
    while enviando_automatico:
        contador += 1
        
        # Crear un empleado automático con ID secuencial REAL
        auto_employee_id = get_next_employee_id()
        
        # Crear el empleado automático como objeto Employee completo
        auto_employee = Employee(
            employee_id=auto_employee_id,
            first_name="AutoWebhook",
            last_name=f"User{auto_employee_id}",
            email=f"auto{auto_employee_id}@web.com",
            phone_number=f"555-{auto_employee_id}",
            hire_date=datetime.datetime.now().date(),
            job_id="IT_PROG",
            salary=50000,
            commission_pct=None,
            manager_id=100 + (auto_employee_id % 5),
            department_id=60
        )
        
        # Agregar a la base de datos local
        employees_db.append(auto_employee)
        
        # Enviar webhook usando la función estándar
        send_employee_webhook("AUTO_CREATE", auto_employee)
        
        await asyncio.sleep(intervalo_segundos)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port) 