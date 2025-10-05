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
def get_ecological_report(class_name, user_zone, latitude, longitude):
    """
    Genera un reporte ecológico completo combinando la identificación de la planta,
    la ubicación del usuario y los datos climáticos recientes de la NASA.
    """
    print("--- Iniciando Reporte Ecológico ---")
    
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
Eres un asistente experto de IA para el proyecto "Bloom It!", actuando como un ecólogo, botánico y científico de datos climáticos. Tu propósito es generar un reporte detallado y educativo basado en los datos proporcionados.

**TAREA:**
Analiza la siguiente información y genera un reporte estructurado en español. El tono debe ser inspirador, educativo y práctico.

**DATOS DE ENTRADA:**

* **Planta Identificada:** {class_name}

* **Zona de la Observación:** {user_zone}

* **Datos Climáticos Recientes (obtenidos de la API POWER de la NASA):**
  {weather_text}

**ESTRUCTURA Y CONTENIDO DEL REPORTE:**

### Análisis de la Especie: {class_name}

* **Características de la Floración:** Describe brevemente las flores de esta planta (color, forma, aroma, temporada de floración).

* **Estado de Conservación:** Menciona su estado de conservación. Si es una especie en peligro, debes empezar esta sección con la frase en mayúsculas: **ESPECIE EN PELIGRO DE EXTINCIÓN**. A continuación, explica brevemente que, según estimaciones, alrededor del 22% de las especies de plantas del mundo enfrentan un riesgo de extinción, subrayando la importancia del hallazgo.

### Análisis Climático y Cuidados Específicos

Utiliza los **Datos Climáticos Recientes** para dar un diagnóstico y consejos prácticos:

1. **Diagnóstico Climático:** Compara los datos de temperatura (promedio, mínima y máxima), humedad y precipitación con las condiciones ideales de la planta. Por ejemplo: *"Con una temperatura promedio reciente de {weather_data['temp'] if weather_data else 'N/A'}°C, la planta se encuentra en su rango óptimo de crecimiento."* o *"La humedad relativa del {weather_data['humidity'] if weather_data else 'N/A'}% es algo baja para esta especie, lo que podría estresar sus hojas."*

2. **Consejos de Riego Basados en Datos:** Basado en la precipitación (`rain`) y la probabilidad de lluvia (`rainProb`), da un consejo de riego específico. Por ejemplo: *"Dado que la precipitación ha sido de solo {weather_data['rain'] if weather_data else 'N/A'} mm y la probabilidad de lluvia es baja, es crucial asegurar un riego manual en los próximos días."*

3. **Protección y Cuidados:** Menciona si las temperaturas mínimas o máximas recientes podrían requerir alguna acción, como proteger la planta de heladas o darle sombra.

### Implicaciones Ecológicas y Relevancia Local (Zona: {user_zone})

1. **Rol en el Ecosistema:** Explica la importancia ecológica de la planta. ¿Es una fuente de alimento clave para polinizadores? ¿Ayuda a fijar el suelo y prevenir la erosión? ¿Sirve de refugio para la fauna?

2. **Polinizadores Nativos:** Nombra 2 o 3 polinizadores nativos de la `{user_zone}` que probablemente interactúen con esta planta.

3. **Cubresuelos Nativos:** Sugiere una o dos especies de plantas cubresuelos nativas de la `{user_zone}` que podrían plantarse cerca para crear un micro-hábitat beneficioso.

### Justificación del Proyecto "Bloom It!"

Concluye con un párrafo que resuma cómo este análisis (combinando identificación, clima y ecología) demuestra el valor de "Bloom It!" para informar decisiones de conservación y manejo, permitiendo a los usuarios entender no solo *qué* planta es, sino *por qué* es importante en su entorno específico y en este momento preciso.
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