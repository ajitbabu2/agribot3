import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from st_audiorec import st_audiorec

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the translator
translator = Translator()


def main():
    st.set_page_config("Agribot")
    st.header("Agri Helpline Bot 🧑🏻‍🌾")
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format="audio/wav")
    tamil_text = recognizer.recognize_google(wav_audio_data.raw_audio_data)
    print("Transcribed Tamil Text:", tamil_text)


# Function to record audio in Tamil and translate it to English
def record_and_transcribe_tamil():
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)

    try:
        # Recognizing the Tamil speech
        tamil_text = recognizer.recognize_google(audio)
        print("Transcribed Tamil Text:", tamil_text)

        # Translating to English
        translated_text = translator.translate(tamil_text, dest="en")
        return translated_text.text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
    except Exception as e:
        print(f"An error occurred during translation: {e}")


# Call the function to record and transcribe audio
# transcribed_and_translated_text = record_and_transcribe_tamil()
# if transcribed_and_translated_text:
#     print("Translated Text to English:", transcribed_and_translated_text)

if __name__ == "__main__":
    main()
