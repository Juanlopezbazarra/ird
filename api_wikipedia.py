import requests

# URL base de la API de Wikipedia en español
url = "https://es.wikipedia.org/w/api.php"

# Parámetros de la consulta
params = {
    "action": "query",        # Hacer una consulta
    "format": "json",         # Respuesta en formato JSON
    "prop": "extracts",       # Queremos el texto extraído
    "titles": "Tokio",        # Ciudad a insertar
    "exintro": 1,             # Solo la introducción
    "explaintext": 1          # Sin formato HTML, solo texto plano
}

# Hacer la solicitud GET
response = requests.get(url, params=params)

# Comprobar si la respuesta fue exitosa
if response.status_code == 200:
    # Convertir la respuesta a JSON
    data = response.json()
    
    # Acceder a las páginas encontradas
    pages = data["query"]["pages"]
    
    # Iterar sobre las páginas
    for page_id, page_data in pages.items():
        print(f"Título: {page_data['title']}\n")
        print(f"Extracto:\n{page_data['extract']}")
else:
    print("Error en la solicitud:", response.status_code)
