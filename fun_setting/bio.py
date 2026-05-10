import requests
API_url = "http://hakhamanesh-bot.ir/api/bio/"
def get_bio():
    response = requests.get(API_url)
    if response.status_code == 200:
        bio_text = response.text
        message = bio_text
        return message
    else:
        print("نشد")
