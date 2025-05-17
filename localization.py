import json
import os
from typing import Dict, Any, Optional

class Localization:
    """
    Singleton class for loading and retrieving localized strings for the application.
    """

    _instance: Optional["Localization"] = None

    def __new__(cls, lang: str = "en") -> "Localization":
        if cls._instance is None or cls._instance.lang != lang:
            cls._instance = super(Localization, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, lang: str = "en") -> None:
        """
        Initializes the Localization object and loads the specified language.

        Args:
            lang (str): Language code (e.g., "en", "sv").
        """
        if getattr(self, "_initialized", False) and self.lang == lang:
            return
        self.lang: str = lang
        self.strings: Dict[str, str] = {}
        self.load_language(lang)
        self._initialized = True

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