import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Obtiene las variables de entorno
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Crea una instancia del enrutador de FastAPI
router = APIRouter()

# Define las cabeceras para la solicitud a la API de Notion
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

@router.get("/db")
async def get_all_notion_data():
    """
    Consulta la base de datos de Notion y devuelve todos los datos paginados.
    """
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    all_results = []
    has_more = True
    next_cursor = None

    try:
        while has_more:
            payload = {}
            if next_cursor:
                payload["start_cursor"] = next_cursor

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            data = response.json()
            all_results.extend(data.get("results", []))
            
            # Actualiza las variables para la siguiente paginación
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")

        # Devuelve la respuesta completa como un objeto JSON
        return {"object": "list", "results": all_results, "has_more": False, "next_cursor": None}

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        return {"error": f"Error HTTP al conectar con la API de Notion: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud: {req_err}")
        return {"error": f"Error en la solicitud a la API de Notion: {req_err}"}
    except Exception as err:
        print(f"Otro error: {err}")
        return {"error": f"Ocurrió un error inesperado: {err}"}