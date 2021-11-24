from translate import Translator

def translate_text(text:str):
    translator= Translator(to_lang="zh")

    translation = translator.translate(text=text)
    print(translation)

translate_text("my pencil")