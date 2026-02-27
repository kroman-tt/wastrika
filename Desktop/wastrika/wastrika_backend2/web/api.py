from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import numpy as np
import gc

# --- STEP 1: DYNAMIC PATH CONFIGURATION ---
# Yesle folder jaha sare pani current location bhetchha
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # web folder
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # wastrika_backend folder

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --- STEP 2: IMPORT CORE LOGICS ---
try:
    from core.cnn_model import get_embedding
    from core.similarity import find_top_matches

    print("✅ Core modules (Kroman & Aayush) loaded successfully!")
except Exception as e:
    print(f"❌ Error loading core modules: {e}")

app = Flask(__name__)
CORS(app)  # React sanga connect garna must chha

# --- STEP 3: DYNAMIC DATA PATHS (No more Hardcoded LENOVO paths) ---
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
RAW_IMAGES_PATH = os.path.join(DATA_FOLDER, "raw_images")
NAMES_PATH = os.path.join(DATA_FOLDER, "image_names.npy")
DATABASE_PATH = os.path.join(DATA_FOLDER, "all_embeddings.npy")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# --- STEP 4: PHOTO SERVING ---
# React le images access garna yo chainchha
@app.route("/clothes/<path:filename>")
def serve_clothes(filename):
    return send_from_directory(RAW_IMAGES_PATH, filename)


# --- STEP 5: SEARCH ENDPOINT ---
@app.route("/search", methods=["POST"])
def search_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    try:
        # 1. Kroman's Logic: DNA Extraction
        query_vector = get_embedding(img_path)

        # 2. Aayush's Logic: Similarity Search
        matches = find_top_matches(
            query_vector, database_path=DATABASE_PATH, names_path=NAMES_PATH
        )

        # 3. Formatting for React
        final_results = []
        for res in matches:
            raw_score = float(res["score"])
            percentage = f"{round(raw_score * 100, 2)}%"

            final_results.append(
                {
                    "image_name": res["image_name"],
                    "score": percentage,
                    "category": "Clothing",  # Bholi metadata thapepachi dynamic banaucha
                    "url": f"http://127.0.0.1:5000/clothes/{res['image_name']}",
                }
            )

        gc.collect()

        # Temp upload delete garne (Optional)
        try:
            if os.path.exists(img_path):
                os.remove(img_path)
        except:
            pass

        return jsonify({"status": "success", "matches": final_results})

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Wastrika API is running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000, threaded=False)
