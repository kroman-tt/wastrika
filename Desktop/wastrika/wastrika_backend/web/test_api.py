import requests
import os

# --- CONFIGURATION ---
url = "http://127.0.0.1:5000/search"
image_to_test = r"C:\Users\LENOVO\Desktop\wastrika_projects\web\static\uploads\download.jpg"

def test_wastrika_api():
    if not os.path.exists(image_to_test):
        print(f"❌ Error: {image_to_test} bhetiyena!")
        return

    print(f"🔍 Testing Wastrika Engine with: {image_to_test}...")

    try:
        with open(image_to_test, 'rb') as img:
            files = {'image': img}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            print("✅ API Response Successful!")
            
            print("\n--- TOP 5 MATCHING RESULTS ---")
            for i, match in enumerate(data.get('matches', [])):
                name = match.get('image_name', 'Unknown')
                
                # --- FIXED LINE BELOW ---
                # Paila float() ma convert garne, ani matra format (:4f) garne
                try:
                    score = float(match.get('score', 0))
                    print(f"{i+1}. 🖼️ {name} (Similarity: {score:.4f})")
                except (ValueError, TypeError):
                    # Yadi score convert garna milena bhane raw print garne
                    print(f"{i+1}. 🖼️ {name} (Similarity: {match.get('score', 'N/A')})")
        else:
            print(f"❌ API Error! Status Code: {response.status_code}")
            print(f"Message: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Failed! 'api.py' run bhairako chha? Check gara.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_wastrika_api()