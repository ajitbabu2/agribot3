from googletrans import Translator

translator = Translator()
translation = translator.translate("பண்ணை பற்றி சொல்", dest="en")
print(translation.text)
