# import streamlit as st
# from streamlit_mic_recorder import mic_recorder
# import speech_recognition as sr
# from streamlit_mic_recorder import speech_to_text

# # Initialize the recognizer
# recognizer = sr.Recognizer()


# def record_and_transcribe():
#     text = speech_to_text(
#         language="en",
#         start_prompt="Start recording",
#         stop_prompt="Stop recording",
#         just_once=False,
#         use_container_width=False,
#         callback=None,
#         args=(),
#         kwargs={},
#         key=None,
#     )
#     if text is not None:
#         st.write(text)

import streamlit as st
from streamlit_mic_recorder import speech_to_text


def record_and_transcribe():
    # Using speech_to_text for handling recording and transcription
    text = speech_to_text(
        language="en-US",  # Make sure to use a supported language code
        start_prompt="Start recording",  # Button text to start recording
        stop_prompt="Stop recording",  # Button text to stop recording
        just_once=True,  # Change to True if you want to limit it to one recording per session
        use_container_width=False,
    )
    if text:
        st.write("Transcribed text:", text)

    else:
        st.write("No transcription detected, please try again.")


def main():
    st.title("Voice Recognition App")
    record_and_transcribe()


if __name__ == "__main__":
    main()
