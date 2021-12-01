from deep_translator import GoogleTranslator
from googletrans import Translator

def translate_text(text:str, language: str):
    language_selected = language[0:2]
    translated = GoogleTranslator(source='auto', target=language_selected).translate(text=text)
    return translated 