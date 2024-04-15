import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
import time
from streamlit_mic_recorder import mic_recorder
from googletrans import Translator

import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()
translator = Translator()

# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # new_db = FAISS.load_local(
    #     "faiss_index", embeddings, allow_dangerous_deserialization=True
    # )
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    print(response)
    st.write("Reply: ", response["output_text"])


def record_and_transcribe(text):
    try:
        text = recognizer.recognize_google(audio)
        # st.write("Transcribed text:", text)
        user_input(text)
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the audio.")
    except sr.RequestError:
        st.error("Could not request results; check your internet connection.")


def record_and_transcribe_tamil():
    with sr.Microphone() as source:
        st.write("Please speak something...")
        audio = recognizer.listen(source)

    try:
        # Recognizing the Tamil speech
        tamil_text = recognizer.recognize_google(audio, language="ta-IN")
        print("Transcribed Tamil Text:", tamil_text)

        # Translating to English
        translated_text = translator.translate(tamil_text, dest="en")
        # return translated_text.text
        user_input(translated_text.text)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
    except sr.RequestError:
        print("Could not request results; check your internet connection.")
    except Exception as e:
        print(f"An error occurred during translation: {e}")


def main():
    st.set_page_config("Agribot")
    st.header("Agri Helpline Bot 🧑🏻‍🌾")

    user_question = st.text_input("Ask a question to your Agribot agent")
    text = speech_to_text(
        language="en-US",  # Make sure to use a supported language code
        start_prompt="English",  # Button text to start recording
        stop_prompt="Stop recording",  # Button text to stop recording
        just_once=True,  # Change to True if you want to limit it to one recording per session
        use_container_width=False,
    )
    if text:
        record_and_transcribe(text)
    # if st.button("தமிழ்"):
    #     record_and_transcribe_tamil()
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button",
            accept_multiple_files=True,
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
