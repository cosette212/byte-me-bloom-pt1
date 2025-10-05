import argparse
import json
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.transforms.functional import five_crop, to_tensor, normalize

# --- Importamos las funciones clave del repositorio ---
from utils import get_model, load_model

# --- CONFIGURACIÓN DEL ENSAMBLE DE MODELOS ---
# Lista de los modelos que queremos usar como nuestro "comité de expertos"
MODELS_TO_USE = {
    'alexnet': {
        'weights_path': 'alexnet_weights_best_acc.tar',
        'crop_size': 224,
        'resize_size': 256,
    },
    'vgg11': {
        'weights_path': 'vgg11_weights_best_acc.tar',
        'crop_size': 224,
        'resize_size': 256,
    },
    'efficientnet_b4': {
        'weights_path': 'efficientnet_b4_weights_best_acc.tar',
        'crop_size': 224,
        'resize_size': 256,
    },
    'inception_resnet_v2': {
        'weights_path': 'inception_resnet_v2_weights_best_acc.tar',
        'crop_size': 299,
        'resize_size': 342,
    }
}
# ------------------------------------------------

CLASS_IDX_TO_SPECIES_ID_PATH = 'class_idx_to_species_id.json'
SPECIES_ID_TO_NAME_PATH = 'plantnet300K_species_id_2_name.json'

def predict_with_ensemble(image_path):
    """
    Carga múltiples modelos, hace una predicción con cada uno y devuelve la que tenga mayor confianza.
    """
    print("--- Iniciando predicción con un ensamble de modelos ---")
    
    # Cargar los archivos de mapeo una sola vez
    with open(CLASS_IDX_TO_SPECIES_ID_PATH, 'r') as f:
        idx_to_species_id = json.load(f)
    with open(SPECIES_ID_TO_NAME_PATH, 'r') as f:
        species_id_to_name = json.load(f)

    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar la imagen en la ruta: {image_path}")
        return

    best_prediction = {"class_name": "Ninguna", "confidence": -1.0, "model_used": "N/A"}

    # Iterar sobre cada modelo en nuestro "comité"
    for model_name, config in MODELS_TO_USE.items():
        print(f"\nConsultando al experto: {model_name}...")
        
        # 1. Cargar el modelo actual
        class Args:
            model = model_name
            pretrained = True
        
        args = Args()
        try:
            model = get_model(args, n_classes=1081)
            load_model(model, config['weights_path'], use_gpu=False)
            model.eval()
        except FileNotFoundError:
            print(f"ADVERTENCIA: No se encontró el archivo de pesos '{config['weights_path']}'. Saltando este modelo.")
            continue
        
        # 2. Pre-procesar la imagen para el modelo actual
        transform = transforms.Compose([transforms.Resize(config['resize_size'])])
        normalization = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        
        temp_image = transform(image)
        five_cropped_images = five_crop(temp_image, size=config['crop_size'])
        tensor_batch = torch.stack([normalization(to_tensor(crop)) for crop in five_cropped_images])
        
        # 3. Realizar la predicción
        with torch.no_grad():
            outputs = model(tensor_batch)
        
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        avg_probabilities = torch.mean(probabilities, dim=0)
        
        top_prob, top_idx = torch.max(avg_probabilities, 0)
        confidence = top_prob.item()
        
        # 4. Comparar con la mejor predicción hasta ahora
        if confidence > best_prediction['confidence']:
            class_index = top_idx.item()
            species_id = idx_to_species_id.get(str(class_index), None)
            class_name = species_id_to_name.get(species_id, "Especie Desconocida") if species_id else "ID no encontrado"
            
            best_prediction['class_name'] = class_name
            best_prediction['confidence'] = confidence
            best_prediction['model_used'] = model_name
            print(f"¡Nueva mejor predicción encontrada! Confianza: {confidence*100:.2f}%")

    # Imprimir el resultado final del comité con lógica condicional
    print("\n--- ¡Decisión Final del Comité de Expertos! ---")
    print(f"🌿 Especie Predicha: {best_prediction['class_name']}")

    confidence = best_prediction['confidence']
    confidence_text = "" # Inicializamos el texto como vacío
    
    if confidence > 0.8:
        # Si es mayor al 80%, muestra el número exacto
        confidence_text = f"🎯 Confianza Final: {confidence * 100:.2f}%"
    elif confidence >= 0.7:
        # Si está entre 70% y 80%
        confidence_text = "🎯 Confianza Final: Arriba del 70% de seguridad"
    elif confidence >= 0.6:
        # NUEVA REGLA: Si está entre 60% y 70%
        confidence_text = "🎯 Confianza Final: Arriba del 60% de seguridad"
    elif confidence >= 0.5:
        # Si está entre 50% y 60%
        confidence_text = "🎯 Confianza Final: Confianza mayoritaria"
    # Si es menor al 50%, no se asigna ningún texto y no se imprimirá nada.

    # Solo imprimimos la línea de confianza si tiene contenido
    if confidence_text:
        print(confidence_text)
        
    print(f"🏆 Modelo Ganador: {best_prediction['model_used']}")
    print("-------------------------------------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clasifica una imagen usando un ensamble de modelos.")
    parser.add_argument('--image', type=str, required=True, help='Ruta a la imagen que quieres clasificar.')
    args = parser.parse_args()
    
    predict_with_ensemble(args.image)



