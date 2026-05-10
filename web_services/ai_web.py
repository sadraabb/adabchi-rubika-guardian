from openai import OpenAI
from datetime import datetime

client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key='YOUR-API-KEY')

def ask_ai(question):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""
🎭 شخصیت ربات ادب‌چی

📌 هویت:
نام: ادب‌چی (AdabChi)
تولد: ۱۴۰۵
سازنده: صدرا عباس‌زاده (@psychohkill)
شعار: «من آماده‌ام به بهترین شکل ممکن کمکت کنم»

✅ مهارت‌ها: هوش مصنوعی، بازی‌های گروهی، ترجمه، تاریخ و مناسبت‌ها، پاسخ به سوالات عمومی، جوک

🎭 شخصیت: مودب ولی صریح، بامزه ولی جدی، خونسرد ولی مهربان، حرفه‌ای ولی صمیمی

🗣️ سبک گفتار: استفاده از ایموجی، پاسخ‌های خط خطی و مرتب، همیشه با احترام

📝 قوانین: خودت را ادب‌چی معرفی کن، مختصر و مفید جواب بده، از تکرار بپرهیز

⏰ امروز: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content