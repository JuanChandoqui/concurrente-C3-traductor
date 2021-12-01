# from deep_translator import GoogleTranslator
# from googletrans import Translator
from translate import Translator

def translate_text(text:str):
    # translator = GoogleTranslator(source='auto', target='es').translate(text)
    translator= Translator(to_lang="zh")
    translation = translator.translate(text=text)
    print(translation)
    return translation

# translate_text('hola como estan')