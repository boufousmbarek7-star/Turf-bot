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

def filter_smart_money_signals():
    target_url = "https://www.letrot.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    signals_found = []

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن أي نصوص تتضمن رموز الحوافر المستهدفة D4 أو DA أو تفاصيل الخيول
            for tag in soup.find_all(['span', 'div', 'p', 'a', 'td']):
                txt = tag.get_text(strip=True)
                if txt in ['D4', 'DA', 'Déferré des quatre pieds', 'Déferré des antérieurs']:
                    if txt not in signals_found:
                        signals_found.append(txt)
            
            # فحص عام للنصوص التي تحتوي على المؤشرات
            for el in soup.find_all(text=True):
                if 'd4' in el.lower() or 'da' in el.lower():
                    clean_txt = el.strip()
                    if 2 <= len(clean_txt) <= 20 and clean_txt not in signals_found:
                        signals_found.append(clean_txt)

    except Exception as ex:
        print(f"Parsing error: {ex}")

    if signals_found:
        signals_text = "\n".join([f"🟢 مؤشر مرصود: `{s}`" for s in signals_found[:8]])
    else:
        signals_text = "• جارِ ترصد وتفعيل رصد وضعيات (D4 / DA) في سباقات اليوم."

    report = (
        "🎯 *تقرير فلترة Smart Money (D4 / DA)*\n\n"
        f"{signals_text}\n\n"
        "⚡ *الحالة:* المحرك يركز حصرياً على رصد النوايا الجادة واستبعاد الفخاخ."
    )
    
    send_telegram_message(report)

if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        filter_smart_money_signals()
