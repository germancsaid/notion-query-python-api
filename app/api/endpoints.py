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
async def get_notion_clean_data():
    """
    Consulta la base de datos de Notion, obtiene todos los datos paginados
    y devuelve solo el id y las propiedades de cada resultado.
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
            
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")

        # Procesa los resultados para extraer solo el id y las propiedades
        clean_results = []
        for item in all_results:
            clean_item = {
                "id": item.get("id"),
                "properties": item.get("properties")
            }
            clean_results.append(clean_item)

        # Devuelve la lista limpia de resultados
        return clean_results

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
        return {"error": f"Error HTTP al conectar con la API de Notion: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud: {req_err}")
        return {"error": f"Error en la solicitud a la API de Notion: {req_err}"}
    except Exception as err:
        print(f"Otro error: {err}")
        return {"error": f"Ocurrió un error inesperado: {err}"}