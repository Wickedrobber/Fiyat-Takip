import cloudscraper
from bs4 import BeautifulSoup
import os
import time

# GitHub Secrets üzerinden gelen bilgiler
TOKEN = os.environ['TG_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']

# TAKİP LİSTESİ
URUNLER = [
    {
        "ad": "Samsung 65S90F",
        "limit": 100000,
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-samsung-65s90f-4k-ultra-hd-65-165-ekran-uydu-alicili-smart-oled-tv-fiyati,1052512435.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-samsung-65s90f-65-inc-164-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790514"
        ]
    },
    {
        "ad": "Samsung 55S90F",
        "limit": 65000,
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-samsung-55s90f-4k-ultra-hd-55-140-ekran-uydu-alicili-smart-oled-tv-fiyati,1052489977.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-samsung-55s90f-55-inc-140-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790505"
        ]
    },
    {
        "ad": "LG OLED65C54LA",
        "limit": 70000,
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-lg-oled65c54la-4k-ultra-hd-65-165-ekran-uydu-alicili-webos-smart-oled-evo-tv-fiyati,1062998434.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-lg-oled65c54la-65-inc-165-ekran-4k-ultra-hd-webos-oled-evo-tv-fiyatlari,2475515119"
        ]
    },
    {
        "ad": "LG OLED55C54LA",
        "limit": 60000,
        "linkler": [
            "https://www.cimri.com/televizyonlar/en-ucuz-lg-oled55c54la-55-inc-139-ekran-4k-ultra-hd-webos-oled-evo-tv-fiyatlari,2526396033"
        ]
    },
    {
        "ad": "TCL 65Q7C",
        "limit": 65000,
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-tcl-65q7c-4k-ultra-hd-65-165-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1090120625.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-tcl-65q7c-65-inc-165-ekran-4k-ultra-hd-google-miniled-tv-fiyatlari,2485555032"
        ]
    },
    {
        "ad": "TCL 55Q7C",
        "limit": 50000, # 0.000 TL yazmıştınız, 50.000 olarak varsaydım
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-tcl-tcl-55q7c-4k-ultra-hd-55-140-ekran-uydu-alicili-google-smart-miniled-tv-fiyati,1091092687.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-tcl-55q7c-55-inc-139-ekran-4k-ultra-hd-google-miniled-tv-fiyatlari,2504857761"
        ]
    }
]

def mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    try:
        cloudscraper.create_scraper().get(api_url)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def fiyat_temizle(metin):
    # Metindeki gereksiz karakterleri temizleyip sayıya çevirir
    try:
        # "79.999,00 TL" -> "79999"
        temiz = metin.split(',')[0].replace('.', '').replace(' ', '').replace('TL', '').strip()
        return int(temiz)
    except:
        return None

def tarama_yap():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    for urun in URUNLER:
        print(f"--- {urun['ad']} Kontrol Ediliyor ---")
        en_ucuz_fiyat = 999999
        bulunan_link = ""

        for link in urun['linkler']:
            try:
                response = scraper.get(link, timeout=30)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    fiyat = None
                    
                    if "akakce.com" in link:
                        f_etiket = soup.select_one('span.pt_v8, span.v8')
                        if f_etiket: fiyat = fiyat_temizle(f_etiket.text)
                    
                    elif "cimri.com" in link:
                        # Cimri'nin güncel fiyat class yapısı
                        f_etiket = soup.select_one('div[class*="price"], span[class*="Price"]')
                        if f_etiket: fiyat = fiyat_temizle(f_etiket.text)

                    if fiyat and fiyat < en_ucuz_fiyat:
                        en_ucuz_fiyat = fiyat
                        bulunan_link = link
                
                time.sleep(5) # Sitelerden ban yememek için bekleme
            except Exception as e:
                print(f"Hata ({link[:25]}): {e}")

        if en_ucuz_fiyat <= urun['limit']:
            mesaj_gonder(f"🔥 TV İNDİRİMİ!\n\n📺 Model: {urun['ad']}\n💰 Fiyat: {en_ucuz_fiyat} TL\n🎯 Hedef: {urun['limit']} TL\n🔗 Link: {bulunan_link}")
        
        print(f"Sonuç: {en_ucuz_fiyat} TL")

if __name__ == "__main__":
    tarama_yap()
