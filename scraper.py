import requests
import json

def scrape_google_places(api_key, query, location, radius):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': location,
        'radius': radius,
        'key': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        businesses = []
        
        for place in results:
            details = scrape_place_details(api_key, place['place_id'])
            if details:
                businesses.append(details)
        
        return {"search_results": businesses}
    else:
        print("Erro na requisição:", response.status_code)
        return {"search_results": []}

def scrape_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        details = response.json().get('result', {})
        
        # Formata os dados desejados
        business_info = {
            "title": details.get('name'),
            "place_id": details.get('place_id'),
            "data_id": details.get('id'),  # ID que você mencionou
            "reviews_link": f"https://api.serpdog.io/reviews?api_key=APIKEY&data_id={details.get('id')}",
            "photos_link": f"https://api.serpdog.io/maps_photos?api_key=APIKEY&data_id={details.get('id')}",
            "posts_link": f"https://api.serpdog.io/maps_post?api_key=APIKEY&data_id={details.get('id')}",
            "gps_coordinates": {
                "latitude": details.get('geometry', {}).get('location', {}).get('lat'),
                "longitude": details.get('geometry', {}).get('location', {}).get('lng')
            },
            "classificação": details.get('rating'),
            "avaliações": details.get('user_ratings_total'),
            "preço": details.get('price_level'),
            "type": details.get('types', [])[0] if details.get('types') else None,
            "address": details.get('formatted_address'),
            "open_state": details.get('opening_hours', {}).get('open_now', 'Desconhecido'),
            "hours": details.get('opening_hours', {}).get('weekday_text'),
            "operating_hours": {day: hours for day, hours in zip(
                ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                details.get('opening_hours', {}).get('weekday_text', [])
            )},
            "phone": details.get('formatted_phone_number'),
            "description": details.get('business_status', 'Sem descrição disponível'),
            "thumbnail": details.get('photos', [{}])[0].get('photo_reference', 'Sem imagem')
        }
        return business_info
    else:
        print("Erro ao obter detalhes:", response.status_code)
        return None

if __name__ == "__main__":
    API_KEY = "sua_api_key_aqui"  # Substitua pela sua chave de API
    query = "restaurantes"
    location = "23.550520,-46.633308"  # Coordenadas de São Paulo
    radius = 5000  # Raio em metros

    results = scrape_google_places(API_KEY, query, location, radius)
    
    # Exibe os resultados em formato JSON
    print(json.dumps(results, indent=4, ensure_ascii=False))