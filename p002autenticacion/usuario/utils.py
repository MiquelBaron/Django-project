import requests

def get_cat_fact():
    url = "https://catfact.ninja/fact"  # URL de la API
    response = requests.get(url)  # Hacemos una solicitud GET
    
    if response.status_code == 200:  # Si la solicitud fue exitosa
        return response.json()  # Retorna los datos en formato JSON
    else:
        return None  # Retorna None si algo falla
