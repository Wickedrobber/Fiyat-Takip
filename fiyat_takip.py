import cloudscraper
from bs4 import BeautifulSoup
import os
import time

TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

URUNLER = [
    {"ad": "Samsung 65S90F", "limit": 110000, "linkler": ["https://www.akakce.com/televizyon/en-ucuz-samsung-65s90f-4k-ultra-hd-65-165-ekran-uydu-alicili-smart-oled-tv-fiyati,1052512435.html", "https://www.cimri.com/televizyonlar/en-ucuz-samsung-65s90f-65-inc-164-ekran-4k-ultra-hd-tizen-oled-tv-fiyatlari,2426790514"]},
    # Diğer ürünlerini buraya ekleyebilirsin...
]

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    try:
        cloudscraper.create_scraper().get(url)
    except: pass

def fiyat_temizle(metin):
    try:
        # Virgül ve noktayı temizleyip tam sayıya çevirir
        parca = metin.split(',')[0]
        temiz = "".join(filter(str.isdigit, parca))
        return int(temiz)
    except: return None

def tarama_yap():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    print("--- TARAMA BAŞLADI ---")
    
    for urun in URUNLER:
        en_ucuz = 999999
        bulunan_link = ""
        
        for link in urun['linkler']:
            try:
                res = scraper.get(link, timeout=20)
                soup = BeautifulSoup(res.content, 'html.parser')
                fiyat = None
                
                if "akakce" in link:
                    # Akakçe için alternatif tüm etiketleri deniyoruz
                    tag = soup.select_one('span.pt_v8, span.v8, #hp-package span.p')
                    if tag: fiyat = fiyat_temizle(tag.text)
                elif "cimri" in link:
                    # Cimri için güncel etiketler
                    tag = soup.select_one('div[class*="price"], span[class*="Price"], .s1wnv990-1')
                    if tag: fiyat = fiyat_temizle(tag.text)

                print(f"{urun['ad']} - Kaynak: {link[:25]}... - Bulunan Fiyat: {fiyat}")

                if fiyat and fiyat < en_ucuz:
                    en_ucuz = fiyat
                    bulunan_link = link
                
                time.sleep(2)
            except Exception as e:
                print(f"Bağlantı hatası: {e}")

        if en_ucuz <= urun['limit'] and en_ucuz != 999999:
            print(f"!!! LİMİT ALTI: {en_ucuz} <= {urun['limit']}")
            mesaj_gonder(f"🔥 İNDİRİM: {urun['ad']}\n💰 Fiyat: {en_ucuz} TL\n🎯 Hedef: {urun['limit']} TL\n🔗 {bulunan_link}")
        else:
            print(f"Bildirim gönderilmedi: Fiyat ({en_ucuz}) limitin ({urun['limit']}) üzerinde.")

    print("--- TARAMA BİTTİ ---")

if __name__ == "__main__":
    tarama_yap()
