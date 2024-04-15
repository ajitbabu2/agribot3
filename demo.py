import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to record audio and convert to text
def record_and_transcribe_tamil():
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ta-IN")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")


# Call the function to record and transcribe audio
transcribed_text = record_and_transcribe_tamil()
if transcribed_text:
    print("Transcribed text:", transcribed_text)
