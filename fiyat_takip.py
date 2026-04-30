import requests
from bs4 import BeautifulSoup
import os

# GitHub Secrets'tan bilgileri çekiyoruz
TOKEN = os.environ['TG_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']
URL = "TAKIP_ETMEK_ISTEDIGIN_TV_LINKINI_BURAYA_YAPISTIR" 

def mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    requests.get(api_url)

def kontrol_et():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # Burası kritik: Takip ettiğin siteye göre bu kısım değişebilir.
        # Şimdilik genel bir kontrol ekleyelim.
        print("Sayfa başarıyla çekildi, fiyat aranıyor...")
        
        # Örnek mesaj (Sistemin çalıştığını görmek için):
        mesaj_gonder("Sistem aktif! TV fiyatını kontrol etmeye başladım.")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    kontrol_et()
