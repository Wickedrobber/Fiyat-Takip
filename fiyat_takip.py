import cloudscraper
from bs4 import BeautifulSoup
import os
import time
import re

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
    try: cloudscraper.create_scraper().get(url)
    except: pass

def fiyat_ayikla(soup, link):
    try:
        if "akakce.com" in link:
            # Akakçe fiyatını bulmak için genişletilmiş arama
            etiket = soup.find("span", {"class": re.compile(r"pt_v8|v8")})
            if not etiket: etiket = soup.select_one(".p_w_v8, .pt_v8")
        else:
            # Cimri için JSON-LD veya genişletilmiş class arama
            etiket = soup.find("span", {"class": re.compile(r"Price|price")})
            if not etiket: etiket = soup.select_one('div[class*="price"], span[class*="Price"]')
        
        if etiket:
            rakam = re.sub(r'[^\d]', '', etiket.text.split(',')[0])
            return int(rakam)
    except: return None
    return None

def tarama_yap():
    # Gerçek bir tarayıcı gibi davranması için detaylı ayar
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    print("--- TARAMA BAŞLADI ---")
    
    for urun in URUNLER:
        en_ucuz = 999999
        bulunan_link = ""
        
        for link in urun['linkler']:
            try:
                res = scraper.get(link, timeout=30)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    fiyat = fiyat_ayikla(soup, link)
                    print(f"Kontrol: {urun['ad']} | Fiyat: {fiyat} TL | Kaynak: {link[:25]}...")
                    
                    if fiyat and fiyat < en_ucuz:
                        en_ucuz = fiyat
                        bulunan_link = link
                time.sleep(5) # Ban yememek için bekleme süresi
            except Exception as e:
                print(f"Hata: {e}")

        if en_ucuz <= urun['limit'] and en_ucuz != 999999:
            mesaj_gonder(f"✅ İNDİRİM YAKALANDI!\n\n📺 {urun['ad']}\n💰 Fiyat: {en_ucuz} TL\n🎯 Hedef: {urun['limit']} TL\n🔗 {bulunan_link}")
            print(f"--- Bildirim Gönderildi: {en_ucuz} TL ---")

    print("--- TARAMA BİTTİ ---")

if __name__ == "__main__":
    tarama_yap()
