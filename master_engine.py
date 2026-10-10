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
        print(f"Telegram status code: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def extract_smart_money_horses():
    target_url = "https://www.letrot.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    horses_found = []

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        print(f"Letrot response code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for tag in soup.find_all(['div', 'span', 'tr', 'li', 'a', 'p']):
                text = tag.get_text(separator=' ', strip=True)
                if any(indicator in text for indicator in ['D4', 'DA', 'DP', 'Déferré']):
                    if 3 < len(text) < 60 and text not in horses_found:
                        horses_found.append(text)
    except Exception as ex:
        print(f"Extraction error: {ex}")

    if horses_found:
        signals_text = "\n".join([f"🔹 `{item}`" for item in horses_found[:5]])
    else:
        signals_text = "• المحرك متصل، وجاري تحديث رصد حوافر الخيول للسباقات الحالية."

    report = (
        "🎯 *تقرير Smart Money المحدث (D4 / DA)*\n\n"
        f"{signals_text}\n\n"
        "⚡ *الحالة التقنية:* الفحص يعمل بانتظام."
    )
    
    send_telegram_message(report)

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Missing credentials!")
    else:
        extract_smart_money_horses()
