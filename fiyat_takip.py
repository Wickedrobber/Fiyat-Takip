import cloudscraper
from bs4 import BeautifulSoup
import os
import time

# GitHub Secrets
TOKEN = os.environ['TG_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']

# TAKİP LİSTESİ
# Her ürün için bakılacak tüm linkleri buraya ekleyebilirsin.
# "limit" değeri, o linkteki fiyat bu rakama düşerse haber ver demektir.
URUNLER = [
    {
        "ad": "Samsung 65Q80C TV",
        "limit": 45000,
        "linkler": [
            "https://www.akakce.com/televizyon/en-ucuz-samsung-65q80c-fiyati,123.html",
            "https://www.cimri.com/televizyonlar/en-ucuz-samsung-65q80c-fiyatlari",
            "https://www.amazon.com.tr/dp/EXAMPLE123",
            "https://www.hepsiburada.com/samsung-65q80c-p-HBCV00004"
        ]
    },
    # Diğer 5 TV modelini de aynı bu formatta ekle...
]

def mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
    cloudscraper.create_scraper().get(api_url)

def fiyat_ayikla(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        if "akakce.com" in url:
            etiket = soup.select_one('span.pt_v8, span.v8')
        elif "cimri.com" in url:
            etiket = soup.select_one('.s188582-12') # Cimri fiyat class'ı
        elif "amazon.com.tr" in url:
            etiket = soup.select_one('.a-price-whole')
        elif "hepsiburada.com" in url:
            etiket = soup.select_one('[data-test-id="price-current-price"]')
        elif "trendyol.com" in url:
            etiket = soup.select_one('.prc-dsc')
        elif "n11.com" in url:
            etiket = soup.select_one('.newPrice ins')
        else:
            return None

        if etiket:
            # Rakam dışındaki her şeyi temizle
            fiyat_text = etiket.text.split(",")[0].replace(".", "").replace(" ", "").replace("TL", "").strip()
            return int(fiyat_text)
    except:
        return None
    return None

def tarama_yap():
    scraper = cloudscraper.create_scraper()
    for urun in URUNLER:
        print(f"--- {urun['ad']} Kontrol Ediliyor ---")
        for link in urun['linkler']:
            try:
                response = scraper.get(link, timeout=20)
                fiyat = fiyat_ayikla(link, response.content)
                
                if fiyat:
                    print(f"Kaynak: {link[:30]}... | Fiyat: {fiyat} TL")
                    if fiyat <= urun['limit']:
                        mesaj_gonder(f"🚨 İNDİRİM BULDUM!\n📦 Ürün: {urun['ad']}\n💰 Fiyat: {fiyat} TL\n🔗 Kaynak: {link}")
                
                time.sleep(3) # Banlanmamak için kısa bekleme
            except Exception as e:
                print(f"Bağlantı hatası ({link[:20]}): {e}")

if __name__ == "__main__":
    tarama_yap()
