import json
import os
from typing import Dict, Any

class Localization:
    """
    Handles loading and retrieving localized strings for the application.
    """

    def __init__(self, lang: str = "en") -> None:
        """
        Initializes the Localization object and loads the specified language.

        Args:
            lang (str): Language code (e.g., "en", "sv").
        """
        self.lang: str = lang
        self.strings: Dict[str, str] = {}
        self.load_language(lang)

    def load_language(self, lang: str) -> None:
        """
        Loads the localization strings from the specified language file.

        Args:
            lang (str): Language code (e.g., "en", "sv").
        """
        path = os.path.join("locales", f"{lang}.json")
        with open(path, encoding="utf-8") as f:
            self.strings = json.load(f)

    def t(self, key: str, **kwargs: Any) -> str:
        """
        Retrieves a localized string by key and formats it with any provided arguments.

        Args:
            key (str): The key for the localized string.
            **kwargs: Arguments to format the string.

        Returns:
            str: The formatted localized string, or the key if not found.
        """
        template = self.strings.get(key, key)
        return template.format(**kwargs)