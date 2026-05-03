import random as rd
import json
from pathlib import Path

class joke:
    def __init__(self,json_path = './joke_json/joke.json'):
        self.json_path = Path(__file__).parent / './joke_json/joke.json'
        self.jokes = []
        self.load_jokes()
    
    def load_jokes(self):
        try:
            with open(self.json_path,'r',encoding='utf-8') as f:
                self.jokes = json.load(f)
            print(f"✅ {len(self.jokes)} جوک بارگذاری شد")
        except FileNotFoundError:
            print(f"❌ فایل پیدا نشد: {self.json_path}")
            self.jokes = []
    def get_random_joke(self):
        if not self.jokes:
            return "جوک یافت نشد"
        joke_get = rd.choice(self.jokes)
        return joke_get
    
    def get_joke_bot(self):
        joke_get = self.get_random_joke()
        if not joke_get:
            return "جوک یافت نشد"
        message = f"{joke_get['joke']}"

        return message


joke_create = joke()