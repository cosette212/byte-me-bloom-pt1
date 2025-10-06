import requests
import json
from datetime import datetime, timedelta
import google.generativeai as genai
import os

# --- CONFIGURACIÓN DE APIS ---
# Tu API Key de la NASA (puedes moverla a una variable de entorno)
NASA_API_KEY = "aZTAVcjEcpjJqHM0ni5zyrDh1PWlGnM4az92fSsk" 
# Configura tu clave de API de Gemini (reemplaza con la tuya)
GEMINI_API_KEY = "AIzaSyBO2oEfDtkOWBI02GihjwI8oNj_F-paz7U"
genai.configure(api_key=GEMINI_API_KEY)

# --- CAMBIO CRÍTICO AQUÍ ---
# Se actualizó el nombre del modelo para usar exactamente el que te funciona en tu otro proyecto.
gemini_model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')



# --- CÓDIGO DE LA API DE LA NASA (Integrado desde tu api.py) ---
def get_nasa_historical_weather_for_date(lat, lon, target_date):
    """
    Consulta la API POWER de la NASA para obtener datos climáticos de una fecha específica.
    Toma TODAS las variables relevantes del diccionario de respuesta.
    """
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
        response.raise_for_status()
        data = response.json()['properties']['parameter']

        max_temp = data.get('T2M_MAX', {}).get(date_str, -999)
        min_temp = data.get('T2M_MIN', {}).get(date_str, -999)
        precipitation = data.get('PRECTOTCORR', {}).get(date_str, -999)
        relative_humidity = data.get('RH2M', {}).get(date_str, -999)

        if -999 in [max_temp, min_temp, precipitation, relative_humidity]:
            print(f"Datos climáticos incompletos para la fecha {date_str}.")
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
        return resultado

    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"Error procesando los datos de la NASA para {date_str}: {e}")
        return None


# --- FUNCIÓN PRINCIPAL PARA GENERAR EL REPORTE ---
def get_ecological_report(class_name, latitude, longitude):
    """
    Genera un reporte ecológico completo combinando la identificación de la planta,
    la ubicación del usuario y los datos climáticos recientes de la NASA.
    """
    print("--- Iniciando Reporte Ecológico ---")
    
    user_zone = f'vas a definir por tu cuenta y buscar a que zona pertenecen las coordenadas {latitude} y {longitude}'
    # 1. Obtener datos climáticos de la NASA para hace 3 días
    target_date = datetime.today() - timedelta(days=3)
    print(f"Consultando datos climáticos para la fecha: {target_date.strftime('%Y-%m-%d')}")
    weather_data = get_nasa_historical_weather_for_date(latitude, longitude, target_date)
    
    if not weather_data:
        weather_text = "No se pudieron obtener los datos climáticos recientes para esta ubicación."
    else:
        # Formatear TODAS las variables climáticas para el prompt
        weather_text = (
            f"* **Fecha de los Datos:** {weather_data['date']}\n"
            f"* **Temperatura Promedio:** {weather_data['temp']}°C\n"
            f"* **Temperatura Mínima:** {weather_data['min']}°C\n"
            f"* **Temperatura Máxima:** {weather_data['max']}°C\n"
            f"* **Precipitación (lluvia):** {weather_data['rain']} mm\n"
            f"* **Probabilidad de Lluvia Estimada:** {weather_data['rainProb']}%\n"
            f"* **Humedad Relativa:** {weather_data['humidity']}%"
        )
    
    print("Datos climáticos obtenidos y formateados.")

    # 2. Definir el guion para Gemini directamente en el código
    prompt_template = f"""
You are an expert AI assistant for the project "Bloom It!", acting as an ecologist, botanist, and climate data scientist. Your purpose is to generate a professional, educational, and insightful report in English based on the provided data.TASK:Analyze the following information and generate a single, cohesive report structured into natural, flowing paragraphs. The tone should be informative and justify the value of this analysis.DATA PROVIDED:Plant Identified: {class_name}Observation Zone: {user_zone}Recent Climate Data (from NASA POWER API):{weather_text}REPORT STRUCTURE AND CONTENT (IN THIS EXACT ORDER):Ecological Importance & Local Relevance (Primary Focus):Start by explaining the plant's ecological significance specifically within the {user_zone}. Discuss its potential uses (e.g., in local gardening, restoration). Crucially, state if the plant poses any risk (e.g., invasive, poisonous). Also, comment on the rarity or commonness of this species in this particular environment.Brief Plant Description:Provide a concise description of the plant's key features, such as its flower color and shape, typical blooming season, and any notable scent.Climate Impact Analysis:Analyze how the recent climate data is affecting the plant. Explain both the positive aspects (e.g., "The recent average temperature of {weather_data['temp'] if weather_data else 'N/A'}°C is ideal for promoting vibrant blooms...") and the negative ones (e.g., "...however, the low precipitation of {weather_data['rain'] if weather_data else 'N/A'} mm may be causing stress to its leaves.").Care and Planting Recommendations:Based on the climate analysis, provide practical recommendations for care, such as watering schedules or protection from extreme temperatures.Conservation Context and Call to Action:Conclude the report with a final paragraph. State whether '{class_name}' is endangered or not. Then, create a call to action by explaining that an estimated 22% of the world's plant species are at risk of extinction. Emphasize how collective intelligence efforts, like users contributing photos to "Bloom It!", are vital for monitoring biodiversity, informing conservation decisions, and preserving our planet's natural heritage.CRITICAL RESTRICTIONS:The entire output must be in English.The report must be a single block of text written in 5 natural, flowing paragraphs, with each paragraph corresponding to one of the 5 points in the structure above.DO NOT USE markdown, headers, asterisks, bullet points, or numbered lists.The total length should not exceed 320 words. avoid to use asterisk when writing specie name.

"""
    
    # 3. Llamar a la API de Gemini
    print("Enviando solicitud a la API de Gemini...")
    try:
        response = gemini_model.generate_content(prompt_template)
        print("Respuesta de Gemini recibida.")
        return response.text
    except Exception as e:
        return f"Error al contactar la API de Gemini: {e}"


#from gemini_ecological_report_unified import get_ecological_report