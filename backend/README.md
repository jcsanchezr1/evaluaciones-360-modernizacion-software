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