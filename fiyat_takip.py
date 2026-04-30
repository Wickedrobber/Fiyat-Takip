import cloudscraper
from bs4 import BeautifulSoup
import os
import time
import re
import random

TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

URUNLER = [
    {"ad": "Samsung 65S90F", "limit": 110000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-65s90f-4k-ultra-hd-65-165-ekran-uydu-alicili-smart-oled-tv-fiyati,1052512435.html", "https://www.cimri.com/televizyonlar/en-ucuz-samsung-65s90f-65-inc-164-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790514"]},
    {"ad": "Samsung 55S90F", "limit": 65000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-55s90f-4k-ultra-hd-55-140-ekran-uydu-alicili-smart-oled-tv-fiyati,1052489977.html"]},
    {"ad": "LG OLED65C54LA", "limit": 70000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-lg-oled65c54la-4k-ultra-hd-65-165-ekran-uydu-alicili-webos-smart-oled-evo-tv-fiyati,1062998434.html"]},
    {"ad": "LG OLED55C54LA", "limit": 60000, "linkler": ["https://www.cimri.com/televizyonlar/en-ucuz-lg-oled55c54la-55-inc-139-ekran-4k-ultra-hd-webos-oled-evo-tv-fiyatlari,2526396033"]},
    {"ad": "TCL 65Q7C", "limit": 65000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-tcl-65q7c-4k-ultra-hd-65-165-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1090120625.html"]},
    {"ad": "TCL 55Q7C", "limit": 50000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-tcl-tcl-55q7c-4k-ultra-hd-55-140-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1091092687.html"]}
]

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    try:
        cloudscraper.create_scraper().get(url)
    except:
        pass

def fiyat_ayikla(soup):
    try:
        # Daha agresif bir fiyat yakalayici
        tags = soup.find_all(string=re.compile(r'TL'))
        for tag in tags:
            parent = tag.parent
            text = parent.get_text()
            if "TL" in text:
                rakam = re.sub(r'[^\d]', '', text.split(',')[0])
                if rakam and 1000 < int(rakam) < 250000:
                    return int(rakam)
    except:
        return None
    return None

def tarama_yap():
    # Rastgele User-Agent kullanarak kimlik gizleme
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    ]
    
    scraper = cloudscraper.create_scraper()
    print(f"--- TARAMA BAŞLADI ({len(URUNLER)} ürün) ---")
    
    for urun in URUNLER:
        en_ucuz = 999999
        bulunan_link = ""
        print(f"\nİnceleniyor: {urun['ad']}")
        
        for link in urun['linkler']:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                res = scraper.get(link, headers=headers, timeout=30)
                
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    fiyat = fiyat_ayikla(soup)
                    print(f"  - Sonuç: {fiyat} TL")
                    
                    if fiyat and fiyat < en_ucuz:
                        en_ucuz = fiyat
                        bulunan_link = link
                else:
                    print(f"  - Erişim Reddedildi: {res.status_code}")
                
                time.sleep(random.randint(5, 10)) # Rastgele bekleme süresi
            except Exception as e:
                print(f"  - Hata: {e}")

        if en_ucuz <= urun['limit'] and en_ucuz != 999999:
            mesaj_gonder(f"✅ İNDİRİM!\n\n📺 {urun['ad']}\n💰 Fiyat: {en_ucuz} TL\n🎯 Hedef: {urun['limit']} TL\n🔗 {bulunan_link}")

    print("\n--- TARAMA BİTTİ ---")

if __name__ == "__main__":
    tarama_yap()
