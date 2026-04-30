import cloudscraper
import os

TOKEN = os.environ['TG_TOKEN']
CHAT_ID = os.environ['TG_CHAT_ID']

def test_mesajı():
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Selam! GitHub sistemin şu an başarıyla bağlandı."
    res = cloudscraper.create_scraper().get(api_url)
    print(f"Telegram Yanıtı: {res.status_code}")
    if res.status_code == 200:
        print("Mesaj başarıyla gönderildi!")
    else:
        print(f"Hata kodu: {res.status_code}. Token veya Chat ID hatalı olabilir.")

if __name__ == "__main__":
    test_mesajı()
