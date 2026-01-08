import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "HABER BOTU CALISIYOR", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
# Binance anahtarların (image_1425 referanslı)
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = 'BURAYA_SECRET_KEYINI_YAZ' # Secret key sadece ilk olusturmada gorunur
# CryptoPanic anahtarın (image_1419 referanslı)
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI']

# --- 3. BINANCE BAGLANTISI ---
# Baglanti hatalarini onlemek icin dogrudan baglaniyoruz
try:
    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
except Exception as e:
    print(f"Binance Baglanti On Hazirlik Hatasi: {e}", flush=True)

def bot_baslat():
    print(">>> SISTEM BASLADI. HABERLER BEKLENIYOR...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 hatasini cozmek icin en temiz URL yapisi
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&public=true"
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                haberler = data.get('results', [])
                print(f"--- Tarama Basarili: {len(haberler)} yeni veri ---", flush=True)
                
                for post in haberler:
                    if post['id'] not in islenenler:
                        # Sadece yukselis (bullish) oyu olanlari al
                        if 'bullish' in str(post.get('votes', {})):
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"!!! HABER GELDİ: {coin} YÜKSELİŞ SİNYALİ !!!", flush=True)
                                        # Not: Binance IP kısıtlaması nedeniyle burası hata verebilir
                                        islenenler.append(post['id'])
            elif response.status_code == 429:
                print("Hiz siniri asildi, 3 dakika bekleniyor...", flush=True)
                time.sleep(180)
            else:
                print(f"Haber Sitesi Hatasi: {response.status_code}", flush=True)
                
        except Exception as e:
            print(f"Döngü Hatası: {e}", flush=True)
        
        time.sleep(120) # 2 dakika bekleme

if __name__ == "__main__":
    bot_baslat()
