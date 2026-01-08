import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "BOT AKTIF", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = 'BURAYA_SECRET_KEYINI_YAZ' 
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'NEAR', 'UNI', 'ICP']

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# --- 3. ALIM FONKSİYONU ---
def binance_al(symbol):
    try:
        # Piyasa fiyatindan 15 USDT'lik alim
        order = client.order_market_buy(symbol=f"{symbol}USDT", quoteOrderQty=15)
        print(f"✅ BAŞARILI: {symbol} satın alındı!", flush=True)
    except Exception as e:
        print(f"❌ BINANCE HATASI ({symbol}): {e}", flush=True)

# --- 4. ANA DÖNGÜ ---
def bot_baslat():
    print(">>> BOT SIFIRLANDI VE BASLATILDI...", flush=True)
    islenenler = []
    
    while True:
        try:
            # 404 hatasini cozmek icin alternatif API adresi
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {'auth_token': PANIC_API_KEY, 'public': 'true', 'kind': 'news'}
            
            response = requests.get(url, params=params, timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                for post in data.get('results', []):
                    if post['id'] not in islenenler:
                        # Bullish kontrolü
                        votes = post.get('votes', {})
                        if votes.get('bullish', 0) > 0:
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"🔥 SİNYAL: {coin} için alım yapılıyor...", flush=True)
                                        binance_al(coin)
                                        islenenler.append(post['id'])
            elif response.status_code == 429:
                print("Hız sınırı! 5 dakika mola...", flush=True)
                time.sleep(300)
            else:
                print(f"Bağlantı Sorunu ({response.status_code}). Yeniden deneniyor...", flush=True)
                
        except Exception as e:
            print(f"Hata: {e}", flush=True)
        
        # Engellenmemek icin sorgu araligini 150 saniyeye cikardik
        time.sleep(150)

if __name__ == "__main__":
    bot_baslat()
