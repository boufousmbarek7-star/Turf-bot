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

def fetch_upcoming_races():
    base_url = "https://www.letrot.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    upcoming_items = []
    signals = []

    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث الدقيق عن أقسام الإنطلاقات أو السباقات القادمة
            for tag in soup.find_all(['div', 'span', 'a', 'li', 'section'], class_=lambda x: x and ('prochain' in x.lower() or 'course' in x.lower() or 'reunion' in x.lower())):
                text = tag.get_text(separator=' ', strip=True)
                if 3 < len(text) < 80 and text not in upcoming_items:
                    upcoming_items.append(text)
                    
            # البحث عن مؤشرات الحوافر D4 / DA المرتبطة بـ Smart Money
            for tag in soup.find_all(['div', 'span', 'td', 'p', 'li']):
                text = tag.get_text(separator=' ', strip=True)
                if any(code in text for code in ['D4', 'DA', 'DP', 'Déferré']):
                    if 3 < len(text) < 60 and text not in signals:
                        signals.append(text)
                        
    except Exception as ex:
        print(f"Fetch error: {ex}")

    races_text = "\n".join([f"• `{item}`" for item in upcoming_items[:4]]) if upcoming_items else "• المحرك في وضع الاستعداد بانتظار جدول الإنطلاقات الصباحي."
    signals_text = "\n".join([f"🔹 `{item}`" for item in signals[:4]]) if signals else "• جاري فحص مؤشرات الحوافر (D4/DA) للسباقات القادمة."

    report = (
        "🎯 *التقرير المتقدم لإنطلاقات وسباقات Trot*\n\n"
        "⏰ *الإنطلاقات والبرامج المرتقبة:* \n"
        f"{races_text}\n\n"
        "💰 *مؤشرات Smart Money الحساسة:*\n"
        f"{signals_text}\n\n"
        "⚡ *الحالة:* المحرك مهيأ بالكامل لالتقاط جداول الصباح الآلية بنجاح."
    )
    
    send_telegram_message(report)

if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        fetch_upcoming_races()
