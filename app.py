import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "HABER BOTU AKTIF", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI', 'TIA', 'SEI', 'ORDI', 'BEAM', 'AAVE', 'IMX', 'KAS', 'LDO', 'FET', 'RUNE', 'ATOM', 'MKR', 'PEPE', 'GRT', 'ALGO', 'EGLD', 'QNT', 'FLOW', 'GALA', 'SNX', 'SAND', 'MANA', 'CHZ', 'AXS', 'MINA', 'DYDX', 'CRV', 'WLD', 'PYTH', 'BONK', 'JUP', 'STRK', 'LUNC', 'FLOKI', 'XMR', 'ETC', 'VET', 'THETA', 'FTM', 'HBAR', 'KAVA', 'WOO', 'ROSE', 'LRC', 'ENS', 'ANKR', 'MASK', 'BLUR', 'PENDLE', 'ALT', 'MANTA', 'PIXEL', 'PORTAL', 'TRB', 'XLM', 'EOS', 'NEO', 'IOTA', 'ZIL', 'BAT', 'ENJ', 'LPT', 'XAI', 'SATS', 'BOME', 'ENA', 'W', 'TNSR', 'IO', 'ZRO'
]

# --- 3. BINANCE BAĞLANTISI ---
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, {"verify": False})

def bot_baslat():
    print(">>> BOT BASLATILDI. HABERLER DINLENIYOR...", flush=True)
    islenenler = []
    
    while True:
        try:
            # CryptoPanic API Sorgusu
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&public=true"
            response = requests.get(url, timeout=20)
            
            if response.status_code == 200:
                res = response.json()
                haberler = res.get('results', [])
                print(f"--- Tarama Yapıldı: {len(haberler)} haber inceleniyor. ---", flush=True)
                
                for post in haberler:
                    if post['id'] not in islenenler:
                        # Bullish (Yükseliş) oyu var mı kontrol et
                        votes = post.get('votes', {})
                        if votes.get('bullish', 0) > 0:
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"!!! KRITIK HABER: {coin} YUKSELIS BEKLENTISI !!!", flush=True)
                                        # İşlem mantığı buraya entegre edilebilir
                                        islenenler.append(post['id'])
            elif response.status_code == 429:
                print("Site hızı sınırladı (429). 3 dakika mola...", flush=True)
                time.sleep(180)
                continue
            else:
                print(f"Bağlantı Sorunu: {response.status_code}", flush=True)
                
        except Exception as e:
            print(f"Sistem Hatası: {e}", flush=True)
        
        # Sitenin bizi engellememesi için 2 dakika bekliyoruz
        time.sleep(120)

if __name__ == "__main__":
    bot_baslat()
