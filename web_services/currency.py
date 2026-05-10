import requests
currency_api_key ="YOUR-API-KEY"
API_KEY = currency_api_key
API_URL = f"https://api.nerkh.io/v1/prices/json/currency?x-api-key={API_KEY}"


def get_currency():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        prices = data['data']['prices']
        usd = prices['USD']['current']
        eur = prices['EUR']['current']
        aed = prices['AED']['current']
        gbp = prices['GBP']['current']
        try_currency = prices['TRY']['current']
        date = data['data']['date']
        message = "💰 نرخ ارز امروز 💰\n\n"
        message += "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        message += f"┃  📅 تاریخ: {date}  ┃\n"
        message += "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        message += "🇺🇸 دلار آمریکا (USD)\n"
        message += f"└ {usd} تومان\n\n"
        message += "🇪🇺 یورو (EUR)\n"
        message += f"└ {eur} تومان\n\n"
        message += "🇬🇧 پوند (GBP)\n"
        message += f"└ {gbp} تومان\n\n"
        message += "🇹🇷 لیر ترکیه (TRY)\n"
        message += f"└ {try_currency} تومان\n\n"
        message += "🇦🇪 درهم امارات (AED)\n"
        message += f"└ {aed} تومان\n\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        message += "🔄 قیمت‌ها لحظه‌ای به‌روزرسانی می‌شوند\n"
        message += "💡 برای مشاهده مجدد، دوباره درخواست دهید"
        return message
    else:
        print("پیدا نشد")
