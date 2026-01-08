import time
import requests
import threading
import os
from flask import Flask

# --- 1. WEB SUNUCUSU (Render'ın botu kapatmaması için) ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Bot Aktif", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
# Token'ı tırnak içine hatasız kopyaladığından emin ol
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

def bot_baslat():
    print(">>> BAGLANTI TESTI BASLADI...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 HATASINI COZEN EN TEMEL URL
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}"
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200:
                res = response.json()
                print(f"Baglanti basarili! {len(res.get('results', []))} haber bulundu.", flush=True)
                # Buraya haber işleme ve Binance kodları gelecek
            else:
                print(f"Hata: {response.status_code}. API anahtarini kontrol et!", flush=True)
                
        except Exception as e:
            print(f"Sistemsel Hata: {e}", flush=True)
        
        time.sleep(60)

if __name__ == "__main__":
    bot_baslat()
