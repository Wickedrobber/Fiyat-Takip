import os
import requests

# GitHub Secrets'tan gelen verileri çekiyoruz
TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

def test_mesaji():
    print(f"--- TEST BAŞLADI ---")
    print(f"Chat ID: {CHAT_ID}") # Loglarda ID'yi kontrol etmek için
    
    # Telegram'a gönderilecek mesaj
    test_metni = "✅ Selam! GitHub ile Telegram arasındaki köprü başarıyla kuruldu. Botun artık çalışıyor!"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={test_metni}"
    
    try:
        r = requests.get(url)
        print(f"Telegram Yanıt Kodu: {r.status_code}")
        print(f"Telegram Yanıt Detayı: {r.text}")
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")

if __name__ == "__main__":
    test_mesaji()
