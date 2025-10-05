import argparse
import json
from PIL import Image

import torch
import torchvision.transforms as transforms

# --- Importamos las funciones clave desde los archivos existentes del repositorio ---
from utils import get_model, load_model

# --- Constantes y Configuración ---
MODEL_ARCHITECTURE = 'alexnet'
NUM_CLASSES = 1081
WEIGHTS_PATH = 'alexnet_weights_best_acc.tar'

# --- ¡NUEVO! Rutas a los archivos de mapeo ---
CLASS_IDX_TO_SPECIES_ID_PATH = 'class_idx_to_species_id.json'
SPECIES_ID_TO_NAME_PATH = 'plantnet300K_species_id_2_name.json'


def predict_single_image(image_path):
    """
    Función principal que carga el modelo, procesa una imagen y devuelve la predicción.
    """
    print("--- Iniciando el proceso de predicción ---")

    # 1. Cargar y preparar el modelo
    # --------------------------------------------------------------------------
    print(f"Cargando modelo '{MODEL_ARCHITECTURE}'...")
    
    class Args:
        model = MODEL_ARCHITECTURE
        pretrained = True
    
    args = Args()
    
    model = get_model(args, n_classes=NUM_CLASSES)
    try:
        load_model(model, WEIGHTS_PATH, use_gpu=False)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo de pesos '{WEIGHTS_PATH}'.")
        print("Asegúrate de que esté en la misma carpeta que este script.")
        return
        
    model.eval()

    # 2. Cargar los mapeos de clases (¡SECCIÓN ACTUALIZADA!)
    # --------------------------------------------------------------------------
    try:
        with open(CLASS_IDX_TO_SPECIES_ID_PATH, 'r') as f:
            idx_to_species_id = json.load(f)
        
        with open(SPECIES_ID_TO_NAME_PATH, 'r') as f:
            species_id_to_name = json.load(f)
            
        print("Mapeos de clases cargados correctamente.")
    except FileNotFoundError as e:
        print(f"ERROR: No se pudo encontrar un archivo de mapeo: {e.filename}")
        print("Asegúrate de que 'class_idx_to_species_id.json' y 'plantnet300K_species_id_2_name.json' estén en la carpeta.")
        return

    # 3. Pre-procesar la imagen de entrada
    # --------------------------------------------------------------------------
    print(f"Procesando la imagen: '{image_path}'")
    
    image_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar la imagen en la ruta: {image_path}")
        return

    tensor = image_transforms(image).unsqueeze(0)

    # 4. Realizar la predicción
    # --------------------------------------------------------------------------
    with torch.no_grad():
        outputs = model(tensor)
    
    # 5. Interpretar y mostrar el resultado (¡SECCIÓN ACTUALIZADA!)
    # --------------------------------------------------------------------------
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    
    top_prob, top_idx = torch.max(probabilities, 0)
    class_index = top_idx.item()
    confidence = top_prob.item()
    
    # --- ¡TRADUCCIÓN EN DOS PASOS! ---
    # Paso 1: De índice de clase (ej. 137) a ID de especie (ej. "1356379")
    species_id = idx_to_species_id.get(str(class_index), None)
    
    # Paso 2: De ID de especie (ej. "1356379") a Nombre de especie (ej. "Dryopteris aemula...")
    if species_id:
        class_name = species_id_to_name.get(species_id, "Especie Desconocida")
    else:
        class_name = "Especie no encontrada en el mapeo"

    print("\n--- ¡Predicción Completa! ---")
    print(f"🌿 Especie Predicha: {class_name}")
    print(f"🎯 Confianza: {confidence * 100:.2f}%")
    print("-----------------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clasifica una imagen de planta usando un modelo pre-entrenado.")
    parser.add_argument('--image', type=str, required=True, help='Ruta a la imagen que quieres clasificar (ej. images/1.jpg).')
    args = parser.parse_args()
    
    predict_single_image(args.image)


