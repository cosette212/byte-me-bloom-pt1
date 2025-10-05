import argparse
import json
from PIL import Image

import torch
import torchvision.transforms as transforms
from torchvision.transforms.functional import five_crop, to_tensor, normalize

# --- Importamos las funciones clave desde los archivos existentes del repositorio ---
from utils import get_model, load_model

# --- ¡CONFIGURACIÓN ACTUALIZADA PARA USAR INCEPTION-RESNET-V2! ---
MODEL_ARCHITECTURE = 'inception_resnet_v2' # <-- Usamos la nueva arquitectura
NUM_CLASSES = 1081
WEIGHTS_PATH = 'inception_resnet_v2_weights_best_acc.tar' # <-- Usamos el nuevo archivo de pesos
# ------------------------------------------------

CLASS_IDX_TO_SPECIES_ID_PATH = 'class_idx_to_species_id.json'
SPECIES_ID_TO_NAME_PATH = 'plantnet300K_species_id_2_name.json'

def predict_with_inception(image_path):
    """
    Función que usa un modelo Inception-ResNet-v2 y TTA para la máxima precisión.
    """
    print(f"--- Iniciando predicción con el modelo avanzado '{MODEL_ARCHITECTURE}' ---")

    # 1. Cargar modelo y mapeos
    # --------------------------------------------------------------------------
    class Args:
        model = MODEL_ARCHITECTURE
        pretrained = True
    
    args = Args()
    try:
        model = get_model(args, n_classes=NUM_CLASSES)
        load_model(model, WEIGHTS_PATH, use_gpu=False)
        model.eval()
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo de pesos '{WEIGHTS_PATH}'.")
        print("Asegúrate de haberlo descargado y colocado en la misma carpeta.")
        return
    except Exception as e:
        print(f"Ocurrió un error al cargar el modelo: {e}")
        return

    with open(CLASS_IDX_TO_SPECIES_ID_PATH, 'r') as f:
        idx_to_species_id = json.load(f)
    with open(SPECIES_ID_TO_NAME_PATH, 'r') as f:
        species_id_to_name = json.load(f)

    # 2. Pre-procesar la imagen con TTA
    # --------------------------------------------------------------------------
    print(f"Procesando la imagen con 5 recortes: '{image_path}'")
    
    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"ERROR: No se pudo encontrar la imagen en la ruta: {image_path}")
        return

    # Inception_v2 requiere un tamaño de entrada de 299x299
    transform = transforms.Compose([
        transforms.Resize(342), # Un tamaño un poco más grande para recortar
    ])
    
    normalization = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    
    image = transform(image)
    five_cropped_images = five_crop(image, size=299) # Tamaño de recorte específico para Inception
    tensor_batch = torch.stack([normalization(to_tensor(crop)) for crop in five_cropped_images])

    # 3. Realizar la predicción
    # --------------------------------------------------------------------------
    with torch.no_grad():
        outputs = model(tensor_batch)
    
    # 4. Promediar los resultados
    # --------------------------------------------------------------------------
    probabilities = torch.nn.functional.softmax(outputs, dim=1)
    avg_probabilities = torch.mean(probabilities, dim=0)
    
    top_prob, top_idx = torch.max(avg_probabilities, 0)
    class_index = top_idx.item()
    confidence = top_prob.item()
    
    species_id = idx_to_species_id.get(str(class_index), None)
    class_name = species_id_to_name.get(species_id, "Especie Desconocida") if species_id else "ID no encontrado"

    print("\n--- ¡Predicción Completa (Inception-ResNet-v2)! ---")
    print(f"🌿 Especie Predicha: {class_name}")
    print(f"🎯 Confianza (promediada): {confidence * 100:.2f}%")
    print("---------------------------------------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Clasifica una imagen usando un modelo Inception-ResNet-v2 y TTA.")
    parser.add_argument('--image', type=str, required=True, help='Ruta a la imagen que quieres clasificar.')
    args = parser.parse_args()
    
    predict_with_inception(args.image)
