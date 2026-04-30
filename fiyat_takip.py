import cloudscraper
from bs4 import BeautifulSoup
import os
import time

# Secrets
TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

# TAKİP LİSTESİ
URUNLER = [
    {"ad": "Samsung 65S90F", "limit": 110000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-65s90f-4k-ultra-hd-65-165-ekran-uydu-alicili-smart-oled-tv-fiyati,1052512435.html", "https://www.cimri.com/televizyonlar/en-ucuz-samsung-65s90f-65-inc-164-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790514"]},
    {"ad": "Samsung 55S90F", "limit": 65000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-55s90f-4k-ultra-hd-55-140-ekran-uydu-alicili-smart-oled-tv-fiyati,1052489977.html", "https://www.cimri.com/televizyonlar/en-ucuz-samsung-55s90f-55-inc-140-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790505"]},
    {"ad": "LG OLED65C54LA", "limit": 70000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-lg-oled65c54la-4k-ultra-hd-65-165-ekran-uydu-alicili-webos-smart-oled-evo-tv-fiyati,1062998434.html", "https://www.cimri.com/televizyonlar/en-ucuz-lg-oled65c54la-65-inc-165-ekran-4k-ultra-hd-webos-oled-evo-tv-fiyatlari,2475515119"]},
    {"ad": "LG OLED55C54LA", "limit": 60000, "linkler": ["https://www.cimri.com/televizyonlar/en-ucuz-lg-oled55c54la-55-inc-139-ekran-4k-ultra-hd-webos-oled-evo-tv-fiyatlari,2526396033"]},
    {"ad": "TCL 65Q7C", "limit": 65000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-tcl-65q7c-4k-ultra-hd-65-165-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1090120625.html", "https://www.cimri.com/televizyonlar/en-ucuz-tcl-65q7c-65-inc-165-ekran-4k-ultra-hd-google-miniled-tv-fiyatlari,2485555032"]},
    {"ad": "TCL 55Q7C", "limit": 50000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-tcl-tcl-55q7c-4k-ultra-hd-55-140-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1091092687.html", "https://www.cimri.com/televizyonlar/en-ucuz-tcl-55q7c-55-inc-139-ekran-4k-ultra-hd-google-miniled-tv-fiyatlari,2504857761"]}
]

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    try:
        cloudscraper.create_scraper().get(url)
    except:
        pass

def fiyat_temizle(metin):
    try:
        return int(metin.split(',')[0].replace('.', '').replace(' ', '').replace('TL', '').strip())
    except:
        return None

def tarama_yap():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    print("Tarama işlemi başladı...")
    
    for urun in URUNLER:
        en_ucuz = 999999
        link_adresi = ""
        
        for link in urun['linkler']:
            try:
                res = scraper.get(link, timeout=20)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, 'html.parser')
                    fiyat = None
                    
                    if "akakce" in link:
                        tag = soup.select_one('span.pt_v8, span.v8')
                        if tag: fiyat = fiyat_temizle(tag.text)
                    elif "cimri" in link:
                        tag = soup.select_one('div[class*="price"], span[class*="Price"]')
                        if tag: fiyat = fiyat_temizle(tag.text)
                        
                    if fiyat and fiyat < en_ucuz:
                        en_ucuz = fiyat
                        link_adresi = link
                time.sleep(3)
            except:
                continue
        
        if en_ucuz <= urun['limit']:
            mesaj_gonder(f"🔥 İNDİRİM: {urun['ad']}\n💰 Fiyat: {en_ucuz} TL\n🎯 Hedef: {urun['limit']} TL\n🔗 {link_adresi}")
        
    print("Tarama bitti.")

if __name__ == "__main__":
    tarama_yap()
