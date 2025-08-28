import os
import requests
from fastapi import APIRouter, Header, HTTPException
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env
load_dotenv()

# Obtiene las variables de entorno
# NOTION_API_KEY = os.getenv("NOTION_API_KEY")
# NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Crea una instancia del enrutador de FastAPI
router = APIRouter()


def get_property_value(property_data):
    """
    Extrae el valor directo de una propiedad de Notion según su tipo.
    """
    prop_type = property_data.get("type")
    
    if prop_type == "title":
        return property_data.get("title")[0].get("plain_text") if property_data.get("title") else ""
    elif prop_type == "rich_text":
        return property_data.get("rich_text")[0].get("plain_text") if property_data.get("rich_text") else ""
    elif prop_type == "number":
        return property_data.get("number")
    elif prop_type == "select":
        return property_data.get("select").get("name") if property_data.get("select") else None
    elif prop_type == "multi_select":
        return [tag.get("name") for tag in property_data.get("multi_select")]
    elif prop_type == "status":
        return property_data.get("status").get("name")
    elif prop_type == "date":
        return property_data.get("date").get("start") if property_data.get("date") else None
    elif prop_type == "formula":
        formula_type = property_data.get("formula").get("type")
        return property_data.get("formula").get(formula_type)
    elif prop_type == "url":
        return property_data.get("url")
    elif prop_type == "email":
        return property_data.get("email")
    elif prop_type == "phone_number":
        return property_data.get("phone_number")
    elif prop_type == "checkbox":
        return property_data.get("checkbox")
    elif prop_type == "created_time":
        return property_data.get("created_time")
    elif prop_type == "last_edited_time":
        return property_data.get("last_edited_time")
    
    return None

@router.get("/db")
async def get_notion_clean_data_sorted(
    notion_key: str = Header(..., alias="Key"), 
    notion_db_id: str = Header(..., alias="Db")
):
    
    headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
    }
    
    """
    Consulta la base de datos de Notion, la ordena por fecha de creación,
    obtiene todos los datos paginados y devuelve una lista limpia.
    """
    url = f"https://api.notion.com/v1/databases/{notion_db_id}/query"
    all_results = []
    has_more = True
    next_cursor = None
    
    # Define la configuración de ordenamiento usando el campo nativo `timestamp`
    sort_payload = {
        "sorts": [
            {
                "timestamp": "created_time",
                "direction": "descending"
            }
        ]
    }

    try:
        while has_more:
            if next_cursor:
                sort_payload["start_cursor"] = next_cursor

            response = requests.post(url, headers=headers, json=sort_payload)
            response.raise_for_status()

            data = response.json()
            all_results.extend(data.get("results", []))
            
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")

        clean_results = []
        for item in all_results:
            clean_item = {"id": item.get("id")}
            for prop_name, prop_data in item.get("properties", {}).items():
                clean_item[prop_name] = get_property_value(prop_data)
            
            clean_results.append(clean_item)

        return clean_results

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"Error HTTP: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Error en la solicitud: {req_err}"}
    except Exception as err:
        return {"error": f"Ocurrió un error inesperado: {err}"}
    


@router.get("/metrics")
async def get_notion_metrics(
    notion_key: str = Header(..., alias="Key"), 
    notion_db_id: str = Header(..., alias="Db")
):
    """
    Calcula métricas clave a partir de los datos de Notion:
    - Horas totales
    - Horas por cliente
    - % de participación por cliente
    - Promedio de horas por tarea
    - Número de tareas terminadas, en curso
    """
    # Primero reutilizamos el endpoint de datos limpios
    raw_data = await get_notion_clean_data_sorted(
        notion_key=notion_key,
        notion_db_id=notion_db_id
    )
    
    if isinstance(raw_data, dict) and "error" in raw_data:
        return raw_data

    total_hours = 0
    tasks_by_customer = {}
    status_count = {"Terminé": 0, "En cours": 0, "Otros": 0}
    
    for task in raw_data:
        horas = task.get("Horas Asignadas") or 0
        customer = task.get("Customer") or "Sin Cliente"
        status = task.get("Stat") or "Otros"

        # Horas totales
        total_hours += horas

        # Horas por cliente
        tasks_by_customer[customer] = tasks_by_customer.get(customer, 0) + horas

        # Conteo por estado
        if status in status_count:
            status_count[status] += 1
        else:
            status_count["Otros"] += 1

    # Calcular % de participación por cliente
    distribution = []
    for cust, hours in tasks_by_customer.items():
        pct = round((hours / total_hours * 100), 2) if total_hours > 0 else 0
        distribution.append({"Customer": cust, "Horas": hours, "Porcentaje": pct})

    metrics = {
        "total_hours": total_hours,
        "tasks_count": len(raw_data),
        "avg_hours_per_task": round(total_hours / len(raw_data), 2) if raw_data else 0,
        "status_count": status_count,
        "hours_distribution": distribution
    }

    return metrics
