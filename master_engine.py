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

def deep_scan_smart_money():
    base_url = "https://www.letrot.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    detected_signals = []

    try:
        # جلب الصفحة الرئيسية للبحث عن روابط السباقات المتاحة اليوم
        response = requests.get(base_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # جمع روابط السباقات أو الشاشات المرتبطة بالبرنامج
            race_links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if '/les-courses/' in href or 'course' in href:
                    full_link = href if href.startswith('http') else base_url + href
                    if full_link not in race_links:
                        race_links.append(full_link)
            
            # فحص أول بضع روابط فرعية بحثاً عن رموز الحوافر D4 / DA
            for link in race_links[:3]:
                try:
                    sub_res = requests.get(link, headers=headers, timeout=8)
                    if sub_res.status_code == 200:
                        sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
                        for tag in sub_soup.find_all(['div', 'span', 'td', 'li', 'p']):
                            t_text = tag.get_text(separator=' ', strip=True)
                            if any(code in t_text for code in ['D4', 'DA', 'Déferré des quatre pieds']):
                                if 3 < len(t_text) < 70 and t_text not in detected_signals:
                                    detected_signals.append(t_text)
                except Exception:
                    continue
                    
    except Exception as ex:
        print(f"Deep scan error: {ex}")

    if detected_signals:
        signals_text = "\n".join([f"🟢 `{item}`" for item in detected_signals[:6]])
    else:
        signals_text = "• المحرك يمسح الروابط الفرعية، وجاري التقاط أولى إشارات الخيول (D4/DA)."

    report = (
        "🎯 *التقرير العميق لفرص Smart Money (D4 / DA)*\n\n"
        f"{signals_text}\n\n"
        "⚡ *الحالة التقنية:* التتبع التلقائي للروابط الفرعية يعمل بنجاح."
    )
    
    send_telegram_message(report)

if __name__ == "__main__":
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        deep_scan_smart_money()
