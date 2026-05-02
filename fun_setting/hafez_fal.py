import random as rd
import requests
import json
from pathlib import Path
class hafezfal:
    def __init__(self,json_path='./fall_hafez/fal.json'):
        self.json_path = Path(__file__).parent / json_path
        self.fals = []
        self.load_fals()
    
    def load_fals(self):
        try:
            with open(self.json_path,'r',encoding='utf-8') as f:
                self.fals = json.load(f)
            print(f"✅ {len(self.fals)} فال بارگذاری شد")
        except FileNotFoundError:
            print(f"❌ فایل پیدا نشد: {self.json_path}")
            self.fals = []
    
    def get_random_fal(self):
        if not self.fals:
            return "فال ها لود نشده است!"
        
        fal = rd.choice(self.fals)
        return fal
    
    def get_fal_bot(self):
        fal = self.get_random_fal()
        if not fal:
            return "فال پیدا نشد"
        message = f"🍃 *فال حافظ شما* 🍃\n\n"
        message += f"📜 {fal['title']}\n\n"
        message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        message += f"📖 {fal['interpreter']}\n\n"
        message += f"━━━━━━━━━━━━━━━━━━━━\n"
        message += f"🌸 نیت خیر داشته باشید"

        return message




hafez = hafezfal()
