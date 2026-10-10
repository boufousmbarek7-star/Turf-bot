import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def extract_horse_signals():
    target_url = "https://www.letrot.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    extracted_data = []

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن الحاويات التي تظهر فيها مؤشرات الخيول أو الحوافر
            for tag in soup.find_all(['div', 'span', 'tr', 'li', 'a', 'p']):
                text = tag.get_text(separator=' ', strip=True)
                if any(ind in text for ind in ['D4', 'DA', 'DP', 'DE', 'ferré']):
                    if 3 < len(text) < 100 and text not in extracted_data:
                        extracted_data.append(text)
    except Exception as ex:
        print(f"Parsing error: {ex}")

    if extracted_data:
        signals_text = "\n".join([f"🔹 `{item}`" for item in extracted_data[:6]])
    else:
        signals_text = "• جاري رصد تفاصيل الخيول وحوافرها للسباقات النشطة."

    report = (
        "🐎 *تقرير تتبع الخيول ووضعيات الحوافر (Smart Money)*\n\n"
        f"{signals_text}\n\n"
        "🎯 *التوجيه:* التركيز على النوايا الجادة واستبعاد الفخاخ الجماهيرية."
    )
    
    send_telegram_message(report)

if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        extract_horse_signals()
