import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER İÇİN WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "BOT AKTIF", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
# Binance anahtarların (Görsel 14:25 referanslı)
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = 'SECRET_KEYINIZI_BURAYA_YAZIN' 
# CryptoPanic anahtarın (Görsel 14:19 referanslı)
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'NEAR', 'UNI', 'ICP']

# --- 3. ANA DÖNGÜ ---
def bot_baslat():
    print(">>> SISTEM BASLATILDI. HABERLER TARANIYOR...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 hatasını önlemek için parametreleri ayırıyoruz
            params = {
                'auth_token': PANIC_API_KEY,
                'public': 'true'
            }
            url = "https://cryptopanic.com/api/v1/posts/"
            response = requests.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                haberler = data.get('results', [])
                print(f"--- Baglanti Basarili! {len(haberler)} haber incelendi. ---", flush=True)
                
                for post in haberler:
                    if post['id'] not in islenenler:
                        # Bullish kontrolü
                        votes = post.get('votes', {})
                        if votes.get('bullish', 0) > 0:
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"!!! KRITIK HABER YAKALANDI: {coin} !!!", flush=True)
                                        # Binance alım emri kodları buraya eklenecek
                                        islenenler.append(post['id'])
            else:
                print(f"Haber Sitesi Yanit Vermedi: {response.status_code}", flush=True)
                
        except Exception as e:
            print(f"Hata Olustu: {e}", flush=True)
        
        # Sitenin bizi engellememesi için 2 dakika bekleme
        time.sleep(120)

if __name__ == "__main__":
    bot_baslat()
