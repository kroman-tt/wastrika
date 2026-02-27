import os
import sys
import torch
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import gc

# Windows ko DLL load hune issue fix garna (Stability ko lagi)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# --- STEP 1: AI MODEL SETUP ---
device = torch.device("cpu")
print(f"🚀 Wastrika Engine is running on: {device}")

# Model load garne function (API le use garchha)
def load_wastrika_model():
    try:
        weights = ResNet50_Weights.DEFAULT
        model = models.resnet50(weights=weights)
        # Feature extractor matra rakhne (Classifier hataune)
        model = torch.nn.Sequential(*(list(model.children())[:-1]))
        model = model.to(device)
        model.eval()
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

# Global model variable (Jasle garda har choti load garnu pardaina)
global_model = None

# --- STEP 2: IMAGE PREPROCESSING ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# --- STEP 3: FEATURE EXTRACTION FUNCTION ---
def get_embedding(img_path):
    global global_model
    
    # Yadi model load bhako chaina bhane load garne
    if global_model is None:
        global_model = load_wastrika_model()
        
    try:
        img = Image.open(img_path).convert('RGB')
        img_t = transform(img).unsqueeze(0).to(device)
        
        with torch.no_grad():
            vector = global_model(img_t)
        
        # Memory release garna
        embedding = vector.flatten().cpu().numpy()
        del img_t
        return embedding
    except Exception as e:
        print(f"❌ Error in image {img_path}: {e}")
        return None

# --- STEP 4: MAIN EXECUTION (Folder scan garne bela matra chalcha) ---
if __name__ == "__main__":
    # Settings: Timro laptop ko path fix cha
    image_dir = r"C:\Users\LENOVO\Desktop\wastrika_projects\data\raw_images"
    all_embeddings = []
    image_names = []

    if os.path.exists(image_dir):
        files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg', '.avif'))]
        print(f"Found {len(files)} images. Memory-safe processing start bhayo...")

        for i, img_name in enumerate(files):
            img_path = os.path.join(image_dir, img_name)
            
            vector = get_embedding(img_path)
            
            if vector is not None:
                all_embeddings.append(vector)
                image_names.append(img_name)
                print(f"[{i+1}/{len(files)}] ✅ Processed: {img_name}")
            
            # Har 5 image pachi memory garbage collection garne (Stability Fix)
            if (i + 1) % 5 == 0:
                gc.collect()

        # --- STEP 5: SAVE RESULTS ---
        # Data folder ma results save garne
        save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if len(all_embeddings) > 0:
            np.save(os.path.join(save_path, 'all_embeddings.npy'), np.array(all_embeddings))
            np.save(os.path.join(save_path, 'image_names.npy'), np.array(image_names))
            print("\n--- MISSION SUCCESSFUL ---")
            print(f"Total {len(image_names)} images ko data '{save_path}' ma save bhayo.")
        else:
            print("Kunai pani image process bhayena!")
    else:
        print(f"Path bhetiyena: {image_dir}")