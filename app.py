import time
import requests
import threading
import os
from flask import Flask
from binance.client import Client

# --- 1. RENDER İÇİN WEB SUNUCUSU ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "BOT AKTIF VE AVDA", 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# --- 2. AYARLAR VE ANAHTARLAR ---
# Binance Ayarları
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'

# CryptoPanic Ayarları
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

# İşlem Yapılacak Güvenli Coin Listesi
GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'NEAR', 'UNI', 'ICP', 'FET', 'RNDR', 'TIA', 'SUI', 'PEPE']

# Binance Bağlantısı
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# --- 3. ALIM FONKSİYONU ---
def binance_al(symbol):
    try:
        # Piyasa fiyatından yaklaşık 15 USDT'lik alım emri
        order = client.order_market_buy(symbol=f"{symbol}USDT", quoteOrderQty=15)
        print(f"✅ İŞLEM BAŞARILI: {symbol} satın alındı!", flush=True)
    except Exception as e:
        print(f"❌ BINANCE ALIM HATASI ({symbol}): {e}", flush=True)

# --- 4. ANA DÖNGÜ ---
def bot_baslat():
    print(">>> BOT SIFIRLANDI. TARAMA VE ALIM MODU AKTİF.", flush=True)
    islenenler = []
    
    while True:
        try:
            # CryptoPanic API bağlantısı
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {
                'auth_token': PANIC_API_KEY,
                'public': 'true',
                'kind': 'news'
            }
            
            response = requests.get(url, params=params, timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                haberler = data.get('results', [])
                print(f"--- Tarama Tamamlandı: {len(haberler)} haber inceleniyor. ---", flush=True)
                
                for post in haberler:
                    if post['id'] not in islenenler:
                        # Bullish (Olumlu) oy kontrolü
                        votes = post.get('votes', {})
                        if votes.get('bullish', 0) > 0:
                            if 'currencies' in post:
                                for c in post['currencies']:
                                    coin = c['code']
                                    if coin in GÜVENLİ_COİNLER:
                                        print(f"🔥 SİNYAL YAKALANDI: {coin}! Binance emri gönderiliyor...", flush=True)
                                        binance_al(coin)
                                        islenenler.append(post['id'])
            elif response.status_code == 429:
                print("Hız sınırı uyarısı. 5 dakika bekleniyor...", flush=True)
                time.sleep(300)
                continue
            else:
                print(f"Haber Sitesi Bağlantı Sorunu: {response.status_code}", flush=True)
                
        except Exception as e:
            print(f"Sistem Hatası: {e}", flush=True)
        
        # Engellenmemek için 2.5 dakika bekleme süresi
        time.sleep(150)

if __name__ == "__main__":
    bot_baslat()
