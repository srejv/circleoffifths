import json
import os

class Localization:
    def __init__(self, lang="en"):
        self.lang = lang
        self.strings = {}
        self.load_language(lang)

    def load_language(self, lang):
        path = os.path.join("locales", f"{lang}.json")
        with open(path, encoding="utf-8") as f:
            self.strings = json.load(f)

    def t(self, key, **kwargs):
        template = self.strings.get(key, key)
        return template.format(**kwargs)