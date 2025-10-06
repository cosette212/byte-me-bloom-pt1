from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from Predict import predict_three as pd
from . import analysis as an


def index_view(request):
    if request.method == 'POST' and request.FILES.get('imagen'):
        imagen = request.FILES['imagen']
        fs = FileSystemStorage()

        # Guarda la imagen y obtiene su ruta y URL
        filename = fs.save(imagen.name, imagen)
        image_path = fs.path(filename)
        image_url = fs.url(filename)  # 👈 URL accesible para mostrarla después

        # Ejecuta la predicción
        prediccion = pd.predict_with_ensemble(image_path)

        coordenadas = request.POST.get('coordenadas')

        if prediccion:
            clase = prediccion['class_name']
            confianza = f"{prediccion['confidence'] * 100:.2f}"
            modelo = prediccion['model_used']

            # Redirige a la página de resultados con todos los datos
            return redirect(
                f"/result/?clase={clase}"
                f"&confianza={confianza}"
                f"&modelo={modelo}"
                f"&coords={coordenadas}"
                f"&img={image_url}"  # 👈 pasamos la imagen
            )

    # Si no hay POST, solo renderiza la página inicial
    return render(request, 'index.html')


def result_view(request):
    clase = request.GET.get('clase')
    confianza = request.GET.get('confianza')
    modelo = request.GET.get('modelo')
    coords = request.GET.get('coords')
    img_url = request.GET.get('img')  # 👈 capturamos la URL de la imagen

    resultado = None
    reporte_ecologico = None 

    if clase and confianza:
        resultado = {
            'class_name': clase,
            'confidence': confianza,
            'model': modelo
        }
        
    if coords:
        try:
            # Limpia espacios extra y convierte a float
            latitud, longitud = map(float, coords.replace(" ", "").split(","))
            reporte_ecologico = an.get_ecological_report(clase, latitud, longitud)
        except ValueError:
            reporte_ecologico = "Coordenadas inválidas. Asegúrate de usar el formato correcto: latitud, longitud"

    return render(request, 'result.html', {
        'resultado': resultado,
        'reporte_ecologico': reporte_ecologico,
        'coords': coords,
        'img_url': img_url  # 👈 enviamos la imagen al template
    })
