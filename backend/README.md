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
    "id": "017d6369-9454-48c5-8a9e-c817dd229faa",
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
        "id": "91b398bf-c92a-4ef5-8729-8939d397bbff",
        "nombre": "evaluacion_dc2f4d04",
        "fecha_insercion": "2025-07-18T20:36:35.568376",
        "esta_eliminada": false
    },
    {
        "id": "ab56f7b1-5d40-453a-bb87-547b09fe3417",
        "nombre": "evaluacion_0c73f800",
        "fecha_insercion": "2025-07-18T20:36:36.162911",
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
    "id": "adf97e88-d0ad-4b1c-82f9-06a5cd0c1662",
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