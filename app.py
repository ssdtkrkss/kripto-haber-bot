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
    return "Bot Aktif!", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI', 'TIA', 'SEI', 'ORDI', 'BEAM', 'AAVE', 'IMX', 'KAS', 'LDO', 'FET', 'RUNE', 'ATOM', 'MKR', 'PEPE', 'GRT', 'ALGO', 'EGLD', 'QNT', 'FLOW', 'GALA', 'SNX', 'SAND', 'MANA', 'CHZ', 'AXS', 'MINA', 'DYDX', 'CRV', 'WLD', 'PYTH', 'BONK', 'JUP', 'STRK', 'LUNC', 'FLOKI', 'XMR', 'ETC', 'VET', 'THETA', 'FTM', 'HBAR', 'KAVA', 'WOO', 'ROSE', 'LRC', 'ENS', 'ANKR', 'MASK', 'BLUR', 'PENDLE', 'ALT', 'MANTA', 'PIXEL', 'PORTAL', 'TRB', 'XLM', 'EOS', 'NEO', 'IOTA', 'ZIL', 'BAT', 'ENJ', 'LPT', 'XAI', 'SATS', 'BOME', 'ENA', 'W', 'TNSR', 'IO', 'ZRO']

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, {"verify": False})

def bot_baslat():
    print(">>> Bot Taramaya Basliyor...", flush=True)
    islenenler = []
    
    while True:
        try:
            # En guvenli URL yapisi
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&kind=news&filter=bullish"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                res = response.json()
                for post in res.get('results', []):
                    if post['id'] not in islenenler and 'currencies' in post:
                        coin = post['currencies'][0]['code']
                        if coin in GÜVENLİ_COİNLER:
                            print(f"Haber yakalandi: {coin}", flush=True)
                            # Binance islemi burada devreye girer
                            islenenler.append(post['id'])
            else:
                print(f"Site Baglanti Hatasi: {response.status_code}", flush=True)
        except Exception as e:
            print(f"Hata: {e}", flush=True)
        
        time.sleep(60) # Engel yememek icin 60 saniye bekliyoruz

if __name__ == "__main__":
    bot_baslat()
