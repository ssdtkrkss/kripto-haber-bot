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
    print(">>> SİSTEM RESETLENDİ. TARAMA BAŞLIYOR...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 HATASINI BİTİREN YENİ URL YAPISI
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {
                'auth_token': PANIC_API_KEY,
                'public': 'true'
            }
            response = requests.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                res = response.json()
                for post in res.get('results', []):
                    # 'Bullish' kontrolünü kodun içinde yapıyoruz
                    if post['id'] not in islenenler:
                        votes = post.get('votes', {})
                        if votes.get('bullish', 0) > 0: # En az 1 kişi bullish demişse
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"!!! HABER YAKALANDI: {coin} !!!", flush=True)
                                        # Binance işlem emri buraya gelecek
                                        islenenler.append(post['id'])
            else:
                print(f"Haber Sitesi Hatasi: {response.status_code}", flush=True)
                
        except Exception as e:
            print(f"Sistemsel Hata: {e}", flush=True)
        
        time.sleep(60) # 429 (Hız sınırı) hatası almamak için 1 dakika bekleme

if __name__ == "__main__":
    bot_baslat()
