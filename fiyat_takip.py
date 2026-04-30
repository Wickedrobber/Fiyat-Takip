import requests
import os
import time
import re
from bs4 import BeautifulSoup

TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

# Not: Eğer yine 403 alırsak, bu linkleri doğrudan vatanbilgisayar.com veya mediamarkt.com.tr linkleriyle değiştireceğiz.
URUNLER = [
    {"ad": "Samsung 65S90F", "limit": 110000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-65s90f-4k-ultra-hd-65-165-ekran-uydu-alicili-smart-oled-tv-fiyati,1052512435.html"]},
    {"ad": "Samsung 55S90F", "limit": 65000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-55s90f-4k-ultra-hd-55-140-ekran-uydu-alicili-smart-oled-tv-fiyati,1052489977.html"]},
    {"ad": "LG OLED65C54LA", "limit": 70000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-lg-oled65c54la-4k-ultra-hd-65-165-ekran-uydu-alicili-webos-smart-oled-evo-tv-fiyati,1062998434.html"]}
]

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    requests.get(url)

def fiyat_bul(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }
    try:
        session = requests.Session()
        # Önce ana sayfaya gidip çerez alıyormuş gibi yapalım
        session.get("https://www.akakce.com/", headers=headers, timeout=10)
        time.sleep(2)
        
        response = session.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Akakce'deki büyük fiyatı bulalım
            fiyat_alanı = soup.find("span", {"class": "pt_v8"})
            if not fiyat_alanı:
                fiyat_alanı = soup.find("span", {"class": "v8"})
            
            if fiyat_alanı:
                fiyat_text = fiyat_alanı.get_text().split(',')[0]
                return int(re.sub(r'[^\d]', '', fiyat_text))
        return response.status_code
    except Exception as e:
        return str(e)

print("--- TARAMA BAŞLADI ---")
for urun in URUNLER:
    for link in urun['linkler']:
        sonuc = fiyat_bul(link)
        if isinstance(sonuc, int) and sonuc < 500: # Bu bir HTTP hata kodudur
            print(f"{urun['ad']} - Hata Kodu: {sonuc}")
        elif isinstance(sonuc, int):
            print(f"{urun['ad']} - Fiyat: {sonuc} TL")
            if sonuc <= urun['limit']:
                mesaj_gonder(f"🚨 İNDİRİM: {urun['ad']} şu an {sonuc} TL! \nLink: {link}")
        else:
            print(f"{urun['ad']} - Hata: {sonuc}")
        time.sleep(5)
print("--- TARAMA BİTTİ ---")
