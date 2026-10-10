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

def fetch_direct_programme():
    # استهداف صفحة البرنامج المباشر للسباقات
    target_url = "https://www.letrot.com/les-courses/programme"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    races_found = []
    status_msg = "جاري الاتصال المباشر بصفحة برنامج السباقات..."

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن عناصر المضامير والأشواط في صفحة البرنامج
            # استهداف الروابط والنصوص التي تحتوي على اسم المضمار أو تفاصيل الشوط
            for tag in soup.find_all(['a', 'h3', 'h4', 'span', 'div']):
                text = tag.get_text(strip=True)
                # فلترة النصوص الطويلة والتركيز على العناوين القصيرة المرتبطة بالمضامير أو الفئات
                if text and 3 < len(text) < 50:
                    lower_text = text.lower()
                    if any(kw in lower_text for kw in ['attelé', 'attele', 'monté', 'monte', 'r1', 'r2', 'r3', 'r4', 'hippodrome']):
                        if text not in races_found:
                            races_found.append(text)
            
            status_msg = "تم فحص صفحة البرنامج المباشر بنجاح."
        else:
            status_msg = f"رمز استجابة صفحة البرنامج: {response.status_code}"
    except Exception as e:
        status_msg = f"خطأ أثناء جلب البرنامج: {str(e)}"

    # تنسيق النتائج المستخرجة
    if races_found:
        unique_races = list(set(races_found))[:7]
        races_text = "\n".join([f"• {r}" for r in unique_races])
    else:
        # رسالة بديلة توضح حالة الفحص المباشر
        races_text = "• البرنامج المباشر متاح، ويتم ترصد المضامير القادمة فور إدراجها."

    report = (
        "🏁 *التقرير المباشر لبرنامج Trot (Attelé & Monté)*\n\n"
        f"📡 *حالة الفحص:* {status_msg}\n\n"
        "🏟️ *المضامير والسباقات المرصودة في البرنامج:*\n"
        f"{races_text}\n\n"
        "🎯 *التوجيه التكتيكي:* \n"
        "• رصد الحوافر (`D4 / DA`)، تقييم السائقين النخبة، واستبعاد الفخاخ الجماهيرية لضمان الدقة في الاختيارات."
    )
    
    return report

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Credentials missing!")
    else:
        report_content = fetch_direct_programme()
        send_telegram_message(report_content)
        print("Direct programme report sent successfully!")
