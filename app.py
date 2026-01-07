import time
import requests
import sys
from binance.client import Client

# 1. IP ADRESİNİ GÖRENE KADAR SÜREKLİ YAZDIR (Flush aktif)
print(">>> IP ADRESİ SORGULANIYOR...", flush=True)
for i in range(10):
    try:
        current_ip = requests.get('https://api.ipify.org').text
        print(f"\n--- BİNANCE'E EKLEMEN GEREKEN GÜNCEL IP: {current_ip} ---\n", flush=True)
    except:
        print("IP adresi henüz alınamadı, tekrar deneniyor...", flush=True)
    time.sleep(1)

# --- BİNANCE API ANAHTARLARIN ---
BINANCE_API_KEY = 'a5duZhCrP6nBJduimWprHwWgqV2Gv7LsiR9tzTTGAp7EBy0FMlcNpANeNrgarH8I'
BINANCE_SECRET_KEY = '2hYYevQtdctBD1PxQaFNlKeDg4kcW7wU0aPA2n51ziEaoF6J9iPK1Tx3Ec92Vm4a'
PANIC_API_KEY = '2ae878976ba826131c7eb75e81803fbd42dab6da'

try:
    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY, {"verify": False, "timeout": 20})
    client.API_URL = 'https://api1.binance.com/api'
    print(">>> Binance baglantisi kuruldu (IP kontrolü bekleniyor).", flush=True)
except Exception as e:
    print(f"Hata: {e}", flush=True)

# --- STRATEJİ AYARLARI ---
KALDIRAC = 3               
STOP_LOSS_ORAN = 0.05      
TS_AKTIF_KAR = 0.02        
TS_TAKIP_ORANI = 0.02      
BAKIYE_KULLANIM_ORANI = 0.90 

GÜVENLİ_COİNLER = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'DOGE', 'TRX', 'LINK', 'MATIC', 'LTC', 'NEAR', 'UNI', 'ICP', 'BCH', 'FIL', 'APT', 'ARB', 'OP', 'STX', 'RNDR', 'INJ', 'SUI']

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
                    if coin not in GÜVENLİ_COİNLER: continue

                    sembol = f"{coin}USDT"
                    toplam_bakiye = bakiye_sorgula()
                    islem_bakiyesi = toplam_bakiye * BAKIYE_KULLANIM_ORANI
                    
                    if islem_bakiyesi < 15: continue 

                    client.futures_change_leverage(symbol=sembol, leverage=KALDIRAC)
                    fiyat = float(client.futures_symbol_ticker(symbol=sembol)['price'])
                    miktar = round((islem_bakiyesi * KALDIRAC) / fiyat, 1)
                    
                    client.futures_create_order(symbol=sembol, side='BUY', type='MARKET', quantity=miktar)
                    client.futures_create_order(symbol=sembol, side='SELL', type='TRAILING_STOP_MARKET', quantity=miktar, callbackRate=TS_TAKIP_ORANI * 100, activationPrice=round(fiyat * (1 + TS_AKTIF_KAR), 4))
                    client.futures_create_order(symbol=sembol, side='SELL', type='STOP_MARKET', stopPrice=round(fiyat * (1 - STOP_LOSS_ORAN), 4), closePosition='true')
                    
                    print(f"İŞLEM AÇILDI: {sembol} (Kasa %90)", flush=True)
                    islenenler.append(post['id'])
        except Exception as e:
            print(f"Hata: {e}", flush=True)
        time.sleep(25)

if __name__ == "__main__":
    bot_baslat()
