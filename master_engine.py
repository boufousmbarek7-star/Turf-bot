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

def fetch_live_race_details():
    target_url = "https://www.letrot.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    races_found = []
    status_msg = "جاري مسح فئات Attelé و Monté من الموقع..."

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن العناوين أو الروابط التي تتضمن تفاصيل السباقات أو المضامير
            # نحمل النصوص المرتبطة بالسباقات أو العناوين البارزة
            elements = soup.find_all(['h2', 'h3', 'span', 'a'], class_=lambda x: x and ('race' in x or 'reunion' in x or 'hippodrome' in x))
            
            for el in elements:
                text = el.get_text(strip=True)
                if text and len(text) > 3 and text not in races_found:
                    # تصفية الكلمات المستهدفة أو المضامير
                    if any(kw in text.lower() for kw in ['attelé', 'attele', 'monté', 'monte', 'R', 'C']):
                        races_found.append(text)
            
            # إذا لم يجد عناصر بـ classes محددة، نبحث عن أي نصوص تحتوي على الكلمات المفتاحية في الصفحة
            if not races_found:
                for p in soup.find_all(['p', 'div', 'a']):
                    t = p.get_text(strip=True)
                    if ('attelé' in t.lower() or 'monté' in t.lower()) and len(t) < 80:
                        if t not in races_found:
                            races_found.append(t)
            
            status_msg = "تم فحص جدول سباقات اليوم واستخراج التفاصيل المتاحة."
        else:
            status_msg = f"حالة الاستجابة للموقع: {response.status_code}"
    except Exception as e:
        status_msg = f"خطأ في الاتصال: {str(e)}"

    # تنسيق قائمة السباقات المستخرجة (نأخذ أول 5 نتائج لتجنب طول الرسالة المفرط)
    if races_found:
        unique_races = list(set(races_found))[:6]
        races_text = "\n".join([f"• {r}" for r in unique_races])
    else:
        races_text = "• جارِ انتظار تحديث البرنامج الصباحي أو تفعيل السباقات القادمة اليوم."

    report = (
        "🐎 *تقرير تفاصيل سباقات Trot (Attelé & Monté)*\n\n"
        f"📡 *حالة الفحص:* {status_msg}\n\n"
        "🏟️ *أبرز المضامير والأشواط المرصودة:*\n"
        f"{races_text}\n\n"
        "🎯 *التوجيه التكتيكي:* \n"
        "• تفعيل فلترة الحوافر (`D4 / DA`) ورصد كفاءة السائقين لتفادي الفخاخ الجماهيرية واستخراج فرص الأماكن والأداء العالي."
    )
    
    return report

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Credentials missing!")
    else:
        report_content = fetch_live_race_details()
        send_telegram_message(report_content)
        print("Detailed race report sent successfully!")
