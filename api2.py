import requests

def fetch_airport_data(code='KAVL'):
    airport_url = f'https://api.aviationapi.com/v1/airports?apt={code}'
    response = requests.get(airport_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None
    
if __name__ == "__main__":
    airport_data = fetch_airport_data()
    if airport_data:
        print(airport_data)
    else:
        print("Failed to fetch weather data.")