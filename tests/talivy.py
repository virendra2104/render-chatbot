import os
import requests
from dotenv import load_dotenv
load_dotenv()

# ==============================
# 1. CONFIGURATION
# ==============================

# 👉 CHANGE THIS to the REAL Talvy base URL
# Examples:
# BASE_URL = "http://localhost:8000"
# BASE_URL = "http://127.0.0.1:8080"
# BASE_URL = "https://<official-talvy-domain>"

BASE_URL = "http://localhost:8000"   # <-- MOST COMMON CASE

# API key from environment variable
TALVY_API_KEY = os.getenv("TALVY_API_KEY")

# ==============================
# 2. BASIC VALIDATIONS
# ==============================

print("🔍 Checking API key...")
if not TALVY_API_KEY:
    raise RuntimeError("❌ TALVY_API_KEY not found in environment variables")

print("✅ API key loaded")

headers = {
    "Authorization": f"Bearer {TALVY_API_KEY}",
    "Content-Type": "application/json"
}

# ==============================
# 3. CONNECTIVITY TEST
# ==============================

print(f"\n🌐 Testing connectivity to: {BASE_URL}")

try:
    health = requests.get(BASE_URL, timeout=5)
    print("✅ Server reachable")
except requests.exceptions.ConnectionError:
    raise RuntimeError("❌ Cannot connect to Talvy server (wrong URL or server not running)")
except requests.exceptions.Timeout:
    raise RuntimeError("❌ Server timeout")

# ==============================
# 4. AUTH + MODELS TEST
# ==============================

print("\n🔐 Testing API key with /v1/models endpoint")

try:
    response = requests.get(
        f"{BASE_URL}/v1/models",
        headers=headers,
        timeout=10
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 200:
        print("\n🎉 SUCCESS: Talvy API key is VALID and WORKING")
    elif response.status_code == 401:
        print("\n❌ INVALID API KEY")
    else:
        print("\n⚠️ Unexpected response (check Talvy docs)")

except Exception as e:
    print("\n❌ Request failed:", str(e))
