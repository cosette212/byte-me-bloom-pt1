import requests
from datetime import datetime, timedelta

# Tu API Key de la NASA
NASA_API_KEY = "aZTAVcjEcpjJqHM0ni5zyrDh1PWlGnM4az92fSsk"

def get_nasa_historical_weather_for_date(lat, lon, target_date):
    # Esta línea ahora funcionará porque target_date es un objeto datetime
    date_str = target_date.strftime("%Y%m%d")
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": date_str,
        "end": date_str,
        "format": "JSON",
        "api_key": NASA_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        print(f"URL consultada: {response.url}")
        response.raise_for_status() # Lanza un error si la solicitud falló
        data = response.json()['properties']['parameter']

        max_temp = data.get('T2M_MAX', {}).get(date_str, -999)
        min_temp = data.get('T2M_MIN', {}).get(date_str, -999)
        precipitation = data.get('PRECTOTCORR', {}).get(date_str, -999)
        relative_humidity = data.get('RH2M', {}).get(date_str, -999)

        if -999 in [max_temp, min_temp, precipitation, relative_humidity]:
            print(f"Datos incompletos para la fecha {date_str}.")
            return None

        rain_prob = min(100, int(20 + precipitation * 10)) if precipitation > 0.1 else 0

        resultado = {
            "date": target_date.strftime("%Y-%m-%d"),
            "temp": round((max_temp + min_temp) / 2, 1),
            "min": round(min_temp, 1),
            "max": round(max_temp, 1),
            "rain": round(precipitation, 1),
            "rainProb": rain_prob,
            "humidity": round(relative_humidity, 1),
        }
        print(resultado)
        return resultado

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Error procesando los datos de la NASA para {date_str}: {e}")
        return None

fecha_deseada = datetime.today() - timedelta(days=3)
get_nasa_historical_weather_for_date(20.7448, -103.2474, fecha_deseada)