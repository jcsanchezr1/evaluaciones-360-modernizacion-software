# Backend evaluaciones-360-modernizacion-software

## Descripción general

El servicio de gestión de evaluaciones permite administrar las evaluaciones del sistema.

## Instalación
### Prerrequisitos

- Python 3.9 o 3.10
- Docker
- Docker Compose
- Postgres
- Postman
- Clonar el repositorio

### Configuración del entorno (Opción 1)

En la raíz del proyecto de backend `./backend`, debe existir un archivo ```.env``` con la siguiente configuración:
```
DB_USER: Usuario de la base de datos
DB_PASSWORD: Contraseña de la base de datos
DB_HOST: Host de la base de datos
DB_PORT: Puerto de la base de datos (default: 5432)
DB_NAME: Nombre de la base de datos
```

1. Crear un entorno virtual:

```
python -m venv venv
```
2. Activar el entorno virtual:

```
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```
3. Instalar dependencias:

```
pip install -r requirements.txt
```

4. Ejecutar la aplicación:
```
flask run --host=0.0.0.0 --port=8080
```

### Uso de Docker Compose (Opción 2)

#### Levantar solo el servicio de Evaluaciones

1. Levantar solo el servicio de Evaluaciones desde el nivel de backend, se puede ejecutar el siguiente comando para levantar solo los servicios relacionados con Evaluaciones:
   Para levantar el servicio puedes ejecutar el siguiente comando:

```
docker-compose up -d
```

Esto iniciará los siguientes servicios:
- evaluaciones_db: Base de datos PostgreSQL para el servicio de evaluaciones.
- evaluaciones: Servicio de evaluaciones que se conectará a evaluaciones_db.
- evaluaciones_net: Red de Docker utilizada por estos servicios.

## Descripción de los Endpoints

### 1. Creación de una evaluación
**URL:** `/evaluaciones`  
**Método:** `POST`
**Descripción:** Añade una evaluacion en el sistema.
**Datos de entrada (JSON):**
```json
{
    "nombre": "Nombre de la evaluacion"
}
```
- Cuando una solicitud POST se procesa correctamente, el servidor devuelve un código de estado 201 Created y los datos de la nueva evaluacion:
Datos de salida (JSON):
```json
{
    "id": "d86c4de8-dd3a-457d-9aba-d20356f90473",
    "id_consecutivo": 2,
    "nombre": "evaluacion_6c87fe1a",
    "message": "Evaluacion creada correctamente"
}
```

### 2. Consultar listado de evaluaciones
**URL:** `/evaluaciones`  
**Método:** `GET`  
**Descripción:** Retorna el listado de evaluaciones creadas.
Respuesta exitosa (200):
```json
[
    {
        "id": "6a376045-2d73-4446-9bd9-e1cacb2bc7d5",
        "id_consecutivo": 1,
        "nombre": "evaluacion_bdc2f23b",
        "fecha_insercion": "2025-07-18T21:31:52.535934",
        "esta_eliminada": false
    },
    {
        "id": "18421cb4-6d04-429a-89fe-c3d833acfff7",
        "id_consecutivo": 2,
        "nombre": "evaluacion_718eb353",
        "fecha_insercion": "2025-07-18T21:31:53.127103",
        "esta_eliminada": false
    }
]
```

### 3. Actualización de una evaluación
**URL:** `/evaluaciones/{id}`  
**Método:** `PUT`  
**Descripción:** Actualiza los datos de una evaluacion con los datos brindados.       
**Datos de entrada (URL Params):**
 - id: ID de la evaluacion (requerido)
**Datos de entrada (JSON):**
```json
{
    "nombre": "Nombre de la evaluacion"
}
```
Respuesta exitosa (200):
```json
{
    "id": "18421cb4-6d04-429a-89fe-c3d833acfff7",
    "id_consecutivo": 2,
    "nombre": "evaluacion_cdffbf57",
    "message": "Evaluacion actualizada correctamente"
}
```

### 3. Eliminación de una evaluación
**URL:** `/evaluaciones/{id}`  
**Método:** `DELETE`  
**Descripción:** Elimina una evaluacion con los datos brindados.       
**Datos de entrada (URL Params):**
 - id: ID de la evaluacion (requerido)
Respuesta exitosa (200):
```json
{
    "message": "Evaluación eliminada correctamente"
}
```

### 5. Verificar el estado del servicio
**URL:** `/evaluaciones/ping`  
**Método:** `GET`  
**Descripción:** Verifica si el servicio de evaluaciones está activo.
Respuesta exitosa (200):
```
"pong"
```

### 6. Limpiar la base de datos
**URL:** `/evaluaciones/reset`  
**Método:** `POST`  
**Descripción:** Limpia todas las evaluaciones en la base de datos.
Respuesta exitosa (200):
```json
{
    "message": "Todos los datos fueron eliminados"
}
```


# Pruebas Unitarias

## Descripción

Suite  de pruebas unitarias para la API REST de Evaluaciones. las pruebas están diseñadas para mockear la capa de base de datos y enfocarse en la lógica de los controladores.

##  Estructura de Pruebas

```
tests/
├── __init__.py                     # Paquete de tests
├── conftest.py                     # Configuración globales
├── test_evaluaciones_view.py       # Pruebas para EvaluacionesView (POST/GET)
├── test_evaluacion_detail_view.py  # Pruebas para EvaluacionDetailView (PUT/DELETE)
├── test_health_check_view.py       # Pruebas para HealthCheckView
├── test_reset_database_view.py     # Pruebas para ResetDatabaseView
├── test_utils.py                   # Pruebas para funciones utilitarias

```

## 🚀 Configuración

### Instalación de Dependencias

```bash
# Instalar dependencias de testing
pip install -r requirements-test.txt
```

### Variables de Entorno

Las pruebas establecen automáticamente `TESTING=True` para evitar conexiones a la base de datos real.

## Ejecutar Pruebas

### Todas las pruebas
```bash
pytest
```

### Con cobertura de código
```bash
pytest --cov=views --cov=models --cov-report=html
```

### Pruebas específicas
```bash
# Solo pruebas de EvaluacionesView
pytest tests/test_evaluaciones_view.py

# Solo pruebas de POST
pytest tests/test_evaluaciones_view.py::TestEvaluacionesViewPost

# Prueba específica
pytest tests/test_evaluaciones_view.py::TestEvaluacionesViewPost::test_crear_evaluacion_exitosa
```

### Modo verbose
```bash
pytest -v
```

## 📊 Cobertura

Las pruebas están configuradas para:
- **90%+ cobertura mínima** requerida
- **Reporte HTML** en `htmlcov/`
- **Reporte terminal** con líneas faltantes

## Casos de Prueba Cubiertos

### EvaluacionesView (POST /evaluaciones)
- Creación exitosa de evaluación
- Primer consecutivo cuando no hay evaluaciones
- Error 400: campo nombre obligatorio
- Error 400: nombre vacío
- Error 412: nombre duplicado
- Error 500: problema de base de datos

### EvaluacionesView (GET /evaluaciones)
- Obtener lista de evaluaciones exitosa
- Lista vacía cuando no hay evaluaciones
- Error 500: problema de base de datos

### EvaluacionDetailView (PUT /evaluaciones/{id})
- Actualización exitosa
- Error 400: ID obligatorio
- Error 400: nombre obligatorio
- Error 400: nombre vacío
- Error 404: evaluación no encontrada
- Error 404: evaluación eliminada
- Error 500: problema de base de datos

### EvaluacionDetailView (DELETE /evaluaciones/{id})
- Eliminación exitosa (soft delete)
- Error 404: ID obligatorio
- Error 404: evaluación no encontrada
- Error 404: evaluación ya eliminada
- Error 500: problema de base de datos

### HealthCheckView (GET /evaluaciones/ping)
- Respuesta exitosa con "pong"
- Error 405: métodos no permitidos

### ResetDatabaseView (POST /evaluaciones/reset)
- Reset exitoso de base de datos
- Reset exitoso cuando no hay datos
- Error 500: problema de base de datos
- Error 405: métodos no permitidos

### Funciones Utilitarias
- `existe_evaluacion()` con diferentes casos

## Mocking

### Base de Datos
- **SQLAlchemy mockeado** - No hay conexiones reales
- **Sesiones de BD simuladas** - Todas las operaciones son mocks
- **Transacciones simuladas** - Commits y rollbacks tracked

### Fixtures Principales
- `mock_db`: Mock automático de la base de datos
- `app`: Aplicación Flask configurada para testing
- `client`: Cliente de testing Flask
- `mock_evaluacion`: Objeto evaluación mock

# API de Evaluaciones

##  Descripción

API REST para gestionar evaluaciones con campos completos de información incluyendo instrucciones y formularios asociados.

##  Arquitectura

- **Framework**: Flask + Flask-RESTful
- **Base de Datos**: PostgreSQL con SQLAlchemy
- **Serialización**: Marshmallow
- **Testing**: pytest con 35+ pruebas unitarias
- **Cobertura**: 99%+ de código

## Modelo de Datos

### Evaluaciones

| Campo | Tipo | Descripción | Requerido |
|-------|------|-------------|-----------|
| `id` | String(50) | UUID único de la evaluación | ✅ |
| `id_consecutivo` | Integer | Número consecutivo incremental | ✅ |
| `nombre` | String(140) | Nombre de la evaluación | ✅ |
| `instrucciones` | Text | Instrucciones detalladas para la evaluación | ❌ |
| `nombre_formulario` | String(200) | Nombre del formulario asociado | ❌ |
| `fecha_insercion` | DateTime | Timestamp de creación (UTC) | ✅ |
| `esta_eliminada` | Boolean | Marcador de eliminación lógica | ✅ |

## ndpoints

### 1. Crear Evaluación
```http
POST /evaluaciones
Content-Type: application/json

{
  "nombre": "Evaluación de Desempeño Q1",
  "instrucciones": "Completar todas las secciones antes del viernes. Incluir ejemplos específicos.",
  "nombre_formulario": "Formulario Desempeño 2024"
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "id_consecutivo": 1,
  "nombre": "Evaluación de Desempeño Q1",
  "instrucciones": "Completar todas las secciones antes del viernes. Incluir ejemplos específicos.",
  "nombre_formulario": "Formulario Desempeño 2024",
  "message": "Evaluacion creada correctamente"
}
```

**Errores:**
- `400`: Campo nombre obligatorio
- `412`: Evaluación con ese nombre ya existe

### 2. Listar Evaluaciones
```http
GET /evaluaciones
```

**Respuesta Exitosa (200):**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "id_consecutivo": 1,
    "nombre": "Evaluación de Desempeño Q1",
    "instrucciones": "Completar todas las secciones antes del viernes.",
    "nombre_formulario": "Formulario Desempeño 2024",
    "fecha_insercion": "2024-01-15T10:30:00.000Z",
    "esta_eliminada": false
  },
  {
    "id": "456e7890-e89b-12d3-a456-426614174001",
    "id_consecutivo": 2,
    "nombre": "Evaluación Técnica Backend",
    "instrucciones": null,
    "nombre_formulario": "Formulario Técnico",
    "fecha_insercion": "2024-01-16T14:20:00.000Z",
    "esta_eliminada": false
  }
]
```

### 3. Actualizar Evaluación
```http
PUT /evaluaciones/{id}
Content-Type: application/json

{
  "nombre": "Evaluación de Desempeño Q1 - Actualizada",
  "instrucciones": "Instrucciones actualizadas con nuevos criterios.",
  "nombre_formulario": "Formulario Desempeño 2024 v2"
}
```

**Respuesta Exitosa (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "id_consecutivo": 1,
  "nombre": "Evaluación de Desempeño Q1 - Actualizada",
  "instrucciones": "Instrucciones actualizadas con nuevos criterios.",
  "nombre_formulario": "Formulario Desempeño 2024 v2",
  "message": "Evaluacion actualizada correctamente"
}
```

**Errores:**
- `400`: ID o campo nombre obligatorio
- `404`: Evaluación no encontrada

**Notas:**
- `nombre` es obligatorio
- `instrucciones` y `nombre_formulario` son opcionales
- Solo se actualizan los campos proporcionados

### 4. Eliminar Evaluación (Soft Delete)
```http
DELETE /evaluaciones/{id}
```

**Respuesta Exitosa (200):**
```json
{
  "message": "Evaluación eliminada correctamente"
}
```

**Errores:**
- `400`: ID obligatorio
- `404`: Evaluación no encontrada

### 5. Health Check
```http
GET /evaluaciones/ping
```

**Respuesta (200):**
```json
"pong"
```

### 6. Reset Base de Datos
```http
POST /evaluaciones/reset
```

**Respuesta (200):**
```json
{
  "message": "Todos los datos fueron eliminados"
}
```

## Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
python -m pytest tests/ -v

# Con cobertura
python -m pytest tests/ --cov=views --cov=models --cov-report=html

# Pruebas específicas
python -m pytest tests/test_evaluaciones_view.py -v
```

### Cobertura de Pruebas
- **35+ pruebas unitarias**
- **99%+ cobertura de código**
- **Todos los endpoints cubiertos**
- **Casos de error y edge cases**
- **Nuevos campos completamente testados**

### Casos de Prueba Incluidos

#### Crear Evaluación (POST)
- Creación exitosa con todos los campos
- Creación con solo campos obligatorios
- Creación con nuevos campos específicos
- Error: nombre obligatorio
- Error: nombre duplicado
- Error: problemas de base de datos

#### Actualizar Evaluación (PUT)
- Actualización exitosa completa
- Actualización parcial de campos nuevos
- Compatibilidad hacia atrás
- Error: campos obligatorios
- Error: evaluación no encontrada

## Configuración

## Variables de Entorno
```bash
DB_USER=####
DB_PASSWORD=####
DB_HOST=####
DB_PORT=####
DB_NAME=####
```

### Ejecutar la Aplicación
```bash
# Desarrollo
flask run

# Producción
gunicorn app:app
```

## Docker

```bash
# Ejecutar con Docker Compose
docker-compose up

# Solo base de datos
docker-compose up postgres
```

## Ejemplos de Uso

### Caso 1: Evaluación Completa
```bash
curl -X POST http://localhost:5000/evaluaciones \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Evaluación 360 - Liderazgo",
    "instrucciones": "Esta evaluación mide competencias de liderazgo. Complete todas las secciones y proporcione ejemplos específicos de situaciones donde demostró cada competencia.",
    "nombre_formulario": "Formulario 360 Liderazgo 2024"
  }'
```

### Caso 2: Evaluación Mínima
```bash
curl -X POST http://localhost:5000/evaluaciones \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Evaluación Rápida"
  }'
```

### Caso 3: Actualización Parcial
```bash
curl -X PUT http://localhost:5000/evaluaciones/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Evaluación Rápida",
    "instrucciones": "Nuevas instrucciones agregadas posteriormente"
  }'
```

## Recursos Adicionales

- **Postman Collection**: `Evaluaciones.postman_collection.json`
- **Tests**: Directorio `tests/` con 35+ pruebas
- **Coverage Report**: `htmlcov/index.html`
- **Configuración**: `pytest.ini`, `requirements-test.txt`