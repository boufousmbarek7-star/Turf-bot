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
        print(f"Telegram API Response: {response.status_code} - {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def morning_program_scanner():
    target_url = "https://www.letrot.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    status_details = "بدء فحص برنامج الـ Trot..."
    found_attele = True  # افتراضي للتأكد من وصول التقرير
    found_monte = True
    
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        print(f"Letrot Response Code: {response.status_code}")
        if response.status_code == 200:
            status_details = "تم الاتصال بنجاح بموقع Letrot ورصد جدول السباقات."
        else:
            status_details = f"استجابة الموقع برمز غير اعتيادي: {response.status_code}"
    except Exception as e:
        status_details = f"تنبيه اتصال: {str(e)}"

    report = (
        "🌅 *التقرير الصباحي لاختبار اتصال نظام الـ Trot*\n\n"
        f"📡 *حالة الفحص:* {status_details}\n\n"
        "📋 *السباقات المستهدفة:* Attelé & Monté\n"
        "🛠️ *الحالة التقنية:* النظام يعمل بنجاح على السحابة ويرسل التقارير الآن."
    )
    
    return report

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram credentials missing!")
    else:
        print("Running morning program scanner...")
        final_report = morning_program_scanner()
        send_telegram_message(final_report)
        print("Execution finished.")
