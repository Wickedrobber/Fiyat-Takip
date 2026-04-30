import requests
from bs4 import BeautifulSoup
import os

# Ayarlar (GitHub Secrets'tan gelecek)
TOKEN = os.environ['TG_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']
HEDEF_FIYAT = 35000  # Bu fiyatın altına düşerse haber ver
URL = "https://www.hepsiburada.com/takip-ettigin-tv-linki"

def mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    requests.get(api_url)

def kontrol_et():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # Not: Bu kısım her sitede farklıdır. Örnek: Hepsiburada fiyat etiketi
    try:
        fiyat_text = soup.select_one('[data-test-id="price-current-price"]').text
        fiyat = int(fiyat_text.replace(".", "").split(",")[0])
        
        if fiyat <= HEDEF_FIYAT:
            mesaj_gonder(f"🚨 FIRSAT! TV şu an {fiyat} TL! \nLink: {URL}")
    except:
        print("Fiyat okunamadı, seçiciyi kontrol et.")

if __name__ == "__main__":
    kontrol_et()
