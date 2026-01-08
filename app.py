import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER İÇİN WEB SUNUCUSU ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Haber Botu Aktif ve Taramada!", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR VE COIN LİSTESİ (TOP 100) ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

KALDIRAC = 3               
STOP_LOSS_ORAN = 0.05      
TS_AKTIF_KAR = 0.02        
TS_TAKIP_ORANI = 0.02      
BAKIYE_KULLANIM_ORANI = 0.90 

GÜVENLİ_COİNLER = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI', 'TIA', 'SEI', 'ORDI', 'BEAM', 'AAVE', 'IMX', 'KAS', 'LDO', 'FET', 'RUNE', 'ATOM', 'MKR', 'PEPE', 'GRT', 'ALGO', 'EGLD', 'QNT', 'FLOW', 'GALA', 'SNX', 'SAND', 'MANA', 'CHZ', 'AXS', 'MINA', 'DYDX', 'CRV', 'WLD', 'PYTH', 'BONK', 'JUP', 'STRK', 'LUNC', 'FLOKI', 'XMR', 'ETC', 'VET', 'THETA', 'FTM', 'HBAR', 'KAVA', 'WOO', 'ROSE', 'LRC', 'ENS', 'ANKR', 'MASK', 'BLUR', 'PENDLE', 'ALT', 'MANTA', 'PIXEL', 'PORTAL', 'TRB', 'XLM', 'EOS', 'NEO', 'IOTA', 'ZIL', 'BAT', 'ENJ', 'LPT', 'XAI', 'SATS', 'BOME', 'ENA', 'W', 'TNSR', 'IO', 'ZRO'
]

# --- 3. BAĞLANTI KONTROLÜ ---
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, {"verify": False, "timeout": 20})
client.API_URL = 'https://api1.binance.com/api'

def bakiye_sorgula():
    try:
        hesap = client.futures_account_balance()
        for varlik in hesap:
            if varlik['asset'] == 'USDT':
                return float(varlik['withdrawAvailable'])
    except: return 0
    return 0

def bot_baslat():
    print(f">>> TOP 100 Modu Aktif. Geniş tarama başlatıldı...", flush=True)
    islenenler = []
    
    while True:
        try:
            # Limit 100'e çıkarıldı
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&kind=news&filter=bullish&limit=100"
            response = requests.get(url)
            
            if response.status_code == 200:
                res = response.json()
                for post in res.get('results', []):
                    if post['id'] not in islenenler and 'currencies' in post:
                        coin = post['currencies'][0]['code']
                        if coin not in GÜVENLİ_COİNLER: continue

                        sembol = f"{coin}USDT"
                        toplam_bakiye = bakiye_sorgula()
                        islem_bakiyesi = toplam_bakiye * BAKIYE_KULLANIM_ORANI
                        
                        if islem_bakiyesi < 12: continue 

                        # İşlem Açılışı
                        client.futures_change_leverage(symbol=sembol, leverage=KALDIRAC)
                        fiyat = float(client.futures_symbol_ticker(symbol=sembol)['price'])
                        miktar = round((islem_bakiyesi * KALDIRAC) / fiyat, 1)
                        
                        client.futures_create_order(symbol=sembol, side='BUY', type='MARKET', quantity=miktar)
                        print(f"!!! İŞLEM AÇILDI: {sembol} !!!", flush=True)
                        islenenler.append(post['id'])
            else:
                print(f"Haber sitesi yanıt vermedi: {response.status_code}", flush=True)
        except Exception as e:
            print(f"Hata oluştu, devam ediliyor...", flush=True)
        
        time.sleep(30) # Siteyi yormamak için 30 saniye bekleme

if __name__ == "__main__":
    bot_baslat()
