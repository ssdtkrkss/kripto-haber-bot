import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "BOT CALISIYOR", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI', 'TIA', 'SEI', 'ORDI', 'BEAM', 'AAVE', 'IMX', 'KAS', 'LDO', 'FET', 'RUNE', 'ATOM', 'MKR', 'PEPE', 'GRT', 'ALGO', 'EGLD', 'QNT', 'FLOW', 'GALA', 'SNX', 'SAND', 'MANA', 'CHZ', 'AXS', 'MINA', 'DYDX', 'CRV', 'WLD', 'PYTH', 'BONK', 'JUP', 'STRK', 'LUNC', 'FLOKI', 'XMR', 'ETC', 'VET', 'THETA', 'FTM', 'HBAR', 'KAVA', 'WOO', 'ROSE', 'LRC', 'ENS', 'ANKR', 'MASK', 'BLUR', 'PENDLE', 'ALT', 'MANTA', 'PIXEL', 'PORTAL', 'TRB', 'XLM', 'EOS', 'NEO', 'IOTA', 'ZIL', 'BAT', 'ENJ', 'LPT', 'XAI', 'SATS', 'BOME', 'ENA', 'W', 'TNSR', 'IO', 'ZRO']

# --- 3. BOT DÖNGÜSÜ ---
def bot_baslat():
    print(">>> BOT AKTIF. HABERLER TARANIYOR...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 HATASINI COZMEK ICIN EN TEMEL URL
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={PANIC_API_KEY}&public=true"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                res = response.json()
                for post in res.get('results', []):
                    # Bullish filtrelemesini kodun icinde yapiyoruz (URL'de degil)
                    if post['id'] not in islenenler and 'bullish' in str(post.get('votes', {})):
                        if 'currencies' in post:
                            coin = post['currencies'][0]['code']
                            if coin in GÜVENLİ_COİNLER:
                                print(f"!!! YUKSELIS HABERI: {coin} !!!", flush=True)
                                # BINANCE ISLEM KODU BURAYA GELECEK
                                islenenler.append(post['id'])
            else:
                print(f"Hata Kodu: {response.status_code}. Baglanti deneniyor...", flush=True)
                
        except Exception as e:
            print(f"Hata: {e}", flush=True)
        
        time.sleep(45)

if __name__ == "__main__":
    bot_baslat()
