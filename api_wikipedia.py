import requests

# Tu Access Token (pon aquí el tuyo)
access_token = "TqeHNG1qwhHTSfH5AeXjAuKSnPjN"

# Función para obtener código IATA de la ciudad
def obtener_codigo_ciudad(token, nombre_ciudad):
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "keyword": nombre_ciudad,
        "subType": "CITY"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]["iataCode"]
    print("No se encontró código IATA para la ciudad.")
    return None

# Función para hacer búsquedas de aeropuertos u hoteles
def buscar(token, keyword, tipo):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    if tipo == "hotel":
        city_code = obtener_codigo_ciudad(token, keyword)
        if not city_code:
            return None
        url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
        params = {
            "cityCode": city_code
        }

    elif tipo == "aeropuerto":
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        params = {
            "keyword": keyword,
            "subType": "AIRPORT"
        }

    else:
        print("Tipo no reconocido.")
        return None

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error en la consulta:", response.text)
        return None

# Programa principal
def main():
    print("¿Qué quieres buscar?")
    print("1. Aeropuertos")
    print("2. Hoteles")

    opcion = input("Elige una opción (1/2): ")
    if opcion not in ["1", "2"]:
        print("Opción no válida.")
        return

    ciudad = input("¿Qué ciudad quieres buscar? (En inglés, ejemplo: Paris, Madrid, Tokyo): ")

    tipo = "aeropuerto" if opcion == "1" else "hotel"

    resultados = buscar(access_token, ciudad, tipo)

    if resultados:
        if "data" in resultados and len(resultados["data"]) > 0:
            if tipo == "hotel":
                print("\nHoteles encontrados:")
                for loc in resultados["data"]:
                    # Mostramos el nombre si está disponible
                    print(f"Hotel: {loc.get('name', 'Nombre no disponible')}")
            else:
                print("\nAeropuertos encontrados:")
                for loc in resultados["data"]:
                    nombre = loc.get("name", "Nombre no disponible")
                    iata = loc.get("iataCode", "Sin código")
                    ciudad = loc.get("address", {}).get("cityName", "Ciudad no disponible")
                    print(f"Nombre: {nombre} ({iata}) - {ciudad}")
        else:
            print("No se encontraron resultados.")
    else:
        print("No se pudo completar la búsqueda.")

if __name__ == "__main__":
    main()
