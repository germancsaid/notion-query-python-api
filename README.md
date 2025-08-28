# Notion Query Python API

## Objetivo

Este proyecto proporciona una API RESTful construida con FastAPI que actúa como una capa de integración entre Notion y sistemas externos. Permite realizar operaciones CRUD (crear, leer, actualizar y eliminar) sobre tareas almacenadas en Notion, facilitando la gestión de tareas y la integración con sistemas de inteligencia artificial para automatización y análisis.

## Características

- **CRUD de tareas:** Permite crear, leer, actualizar y eliminar tareas en Notion mediante endpoints REST.
- **Abstracción de Notion:** Los consumidores de la API no necesitan conocer los detalles internos de la API de Notion.
- **Extensible:** Pensada para integrarse fácilmente con sistemas de IA y otras plataformas de gestión de tareas.
- **Validación de datos:** Uso de Pydantic para asegurar la integridad de los datos.
- **Fácil despliegue:** Basada en FastAPI y Uvicorn para un despliegue rápido y eficiente.

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/notion-query-python-api.git
   cd notion-query-python-api
   ```

2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

3. Configura tus credenciales de Notion en las variables de entorno o en un archivo `.env`.

## Uso

1. Inicia el servidor:
   ```sh
   uvicorn app.main:app --reload
   ```

2. Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

## Endpoints principales

- `GET /tasks/` — Lista todas las tareas
- `POST /tasks/` — Crea una nueva tarea
- `GET /tasks/{id}` — Obtiene una tarea específica
- `PUT /tasks/{id}` — Actualiza una tarea existente
- `DELETE /tasks/{id}` — Elimina una tarea

## Contribución

¡Las contribuciones son bienvenidas! Por favor, abre un issue o un pull request para sugerencias o