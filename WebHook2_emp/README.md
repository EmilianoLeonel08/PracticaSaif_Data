# Employee Management Webhook API

API para gestión de empleados con webhooks desarrollada con FastAPI, basada en el esquema de base de datos Oracle HR.

## Características

- ✅ Gestión completa de empleados (CRUD)
- ✅ Webhooks automáticos para acciones de empleados
- ✅ Validaciones basadas en el esquema de BD Oracle
- ✅ Envío manual de webhooks
- ✅ Envío automático de webhooks con intervalo configurable
- ✅ Gestión del estado de envíos
- ✅ Cambio dinámico de URL de webhook
- ✅ API REST completa con documentación Swagger

## Esquema de Datos

Basado en la tabla `employees` de Oracle HR con las siguientes características:
- **employee_id**: Clave primaria (autoincremental desde 207)
- **Campos obligatorios**: first_name, last_name, email, hire_date, job_id, salary
- **Restricciones**: email único, salary > 0, commission_pct entre 0 y 1
- **Relaciones**: manager_id (autorreferencia), department_id

## Endpoints

### Endpoints Básicos
- **GET** `/` - Mensaje de bienvenida
- **GET** `/health` - Verificación de salud
- **GET** `/status` - Estado del sistema y estadísticas de empleados

### Gestión de Empleados
- **POST** `/employees` - Crear nuevo empleado
- **GET** `/employees` - Obtener todos los empleados
- **GET** `/employees/{employee_id}` - Obtener empleado por ID
- **PUT** `/employees/{employee_id}` - Actualizar empleado
- **DELETE** `/employees/{employee_id}` - Eliminar empleado
- **GET** `/employees/by-department/{department_id}` - Empleados por departamento
- **GET** `/employees/by-manager/{manager_id}` - Empleados por manager
- **GET** `/employees/search` - Búsqueda avanzada
- **POST** `/employees/init-sample-data` - Inicializar datos de ejemplo

### Webhooks
- **POST** `/send-webhook` - Envía webhook manual
- **PUT** `/webhook-url?new_url=<URL>` - Actualiza URL del webhook
- **POST** `/start-auto-webhook` - Inicia webhooks automáticos
- **POST** `/stop-auto-webhook` - Detiene webhooks automáticos
- **PUT** `/intervalo?segundos=<SEGUNDOS>` - Configura intervalo

### Configuración
- **PUT** `/config/usuario` - Actualizar usuario por defecto
- **PUT** `/config/tecnologia` - Actualizar tecnología por defecto
- **PUT** `/config/mensaje` - Actualizar mensaje por defecto
- **PUT** `/config/mensaje-auto` - Actualizar mensaje automático

## Ejemplos de Uso

### 1. Inicializar datos de ejemplo
```bash
curl.exe -X POST http://localhost:8000/employees/init-sample-data
```

### 2. Crear un nuevo empleado
```bash
curl.exe -X POST http://localhost:8000/employees \
  -H "Content-Type: application/json" \
  -d "{
    \"first_name\": \"Ana\",
    \"last_name\": \"Martín\",
    \"email\": \"ana.martin@company.com\",
    \"phone_number\": \"555-0004\",
    \"hire_date\": \"2024-01-15\",
    \"job_id\": \"IT_PROG\",
    \"salary\": 70000,
    \"department_id\": 60
  }"
```

### 3. Obtener todos los empleados
```bash
curl.exe http://localhost:8000/employees
```

### 4. Buscar empleados
```bash
curl.exe "http://localhost:8000/employees/search?first_name=Juan&job_id=IT_PROG"
```

### 5. Actualizar salario
```bash
curl.exe -X PUT http://localhost:8000/employees/208 \
  -H "Content-Type: application/json" \
  -d "{\"salary\": 80000}"
```

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
