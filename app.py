import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER İÇİN WEB SUNUCUSU (BOTUN KAPANMAMASI İÇİN) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_web_server():
    # Render'ın verdiği PORT'u kullan, yoksa 10000 kullan
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Web sunucusunu arka planda başlat
threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. BİNANCE VE STRATEJİ AYARLARI ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

KALDIRAC = 3               
STOP_LOSS_ORAN = 0.05      
TS_AKTIF_KAR = 0.02        
TS_TAKIP_ORANI = 0.02      
BAKIYE_KULLANIM_ORANI = 0.90 

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI']

# --- 3. IP ADRESİ VE BAĞLANTI KONTROLÜ ---
print(">>> IP ADRESİ SORGULANIYOR...", flush=True)
try:
    current_ip = requests.get('https://api.ipify.org').text
    print(f"\n--- BİNANCE'E EKLEMEN GEREKEN GÜNCEL IP: {current_ip} ---\n", flush=True)
except:
    print("IP adresi alınamadı!", flush=True)

try:
    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, {"verify": False, "timeout": 20})
    client.API_URL = 'https://api1.binance.com/api'
    print(">>> Binance baglantisi kuruldu.", flush=True)
except Exception as e:
    print(f"Bağlantı Hatası: {e}", flush=True)

# --- 4. FONKSİYONLAR VE ANA DÖNGÜ ---
def bakiye_sorgula():
    try:
        hesap = client.futures_account_balance()
        for varlik in hesap:
            if varlik['asset'] == 'USDT':
                return float(varlik['withdrawAvailable'])
    except: return 0
    return 0

def bot_baslat():
    print(f">>> %90 Bakiye Modu Aktif. Elite 25 taranıyor...", flush=True)
    islenenler = []
    
    while True:
        try:
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&kind=news&filter=bullish"
            res = requests.get(url).json()
            
            for post in res.get('results', []):
                if post['id'] not in islenenler and 'currencies' in post:
                    coin = post['currencies'][0]['code']
                    if coin not in GÜVENLİ_COİANS: continue

                    sembol = f"{coin}USDT"
                    toplam_bakiye = bakiye_sorgula()
                    islem_bakiyesi = toplam_bakiye * BAKIYE_KULLANIM_ORANI
                    
                    if islem_bakiyesi < 15: continue 

                    client.futures_change_leverage(symbol=sembol, leverage=KALDIRAC)
                    fiyat = float(client.futures_symbol_ticker(symbol=sembol)['price'])
                    miktar = round((islem_bakiyesi * KALDIRAC) / fiyat, 1)
                    
                    client.futures_create_order(symbol=sembol, side='BUY', type='MARKET', quantity=miktar)
                    print(f"İŞLEM AÇILDI: {sembol} (Kasa %90)", flush=True)
                    islenenler.append(post['id'])
        except Exception as e:
            print(f"Döngü Hatası: {e}", flush=True)
        time.sleep(25)

if __name__ == "__main__":
    bot_baslat()
