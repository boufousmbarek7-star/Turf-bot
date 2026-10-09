import os
import requests

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
        response = requests.post(url, json=payload)
        print(f"Telegram API Response: {response.status_code} - {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == "__main__":
    print(f"Token present: {bool(TELEGRAM_BOT_TOKEN)}")
    print(f"Chat ID present: {bool(TELEGRAM_CHAT_ID)}")
    
    report = (
        "🔥 *التقرير المتقدم لسباقات الـ Trot (الكواليس + السائقين + الحوافر)*\n\n"
        "🔍 *1. فحص وضعية الحوافر (Ferrotin / Shoeing):*\n"
        "• تم رصد الخيول التي تحولت إلى وضعية `Déferré des quatre pieds (D4)`.\n\n"
        "👨‍✈️ *2. تقييم كفاءة السائقين (Drivers Intent):*\n"
        "• تم رصد إشراك سائقين من النخبة.\n\n"
        "📊 *الخلاصة التكتيكية:* نظام التحليل يعمل بكفاءة عالية."
    )
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram credentials missing!")
    else:
        send_telegram_message(report)
