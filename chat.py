from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Conversation Chatboot")

st.markdown("<h1 style='text-align: center;'>Chatbot Application</h1>", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []

# Create a horizontal layout for input and icon
input_col, icon_col = st.columns([9,1])
input_text = input_col.text_area("Input:", key="input")
if icon_col.button("🚀", key="submit-icon"):
    response=get_gemini_response(input_text)

    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    for chunk in response:
        st.write(chunk.text, unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display feedback buttons
    feedback = st.radio("Feedback:", ["👍 Positive", "🤷 Neutral", "👎 Negative"])
    st.session_state['feedback'].append(feedback)

if st.button("View History"):
# sidebar to display chat history
    st.sidebar.header("Previous Conversation")
    for role, text in st.session_state['chat_history']:
         if role == "You":
             st.sidebar.html(
                f'<div style="direction: rtl; text-align: right;">👤: {text}</div>'
            )
         else:
                st.sidebar.html(
                f'<div style="font-family: Arial, sans-serif;">🤖: {text}</div>'
            )

 # Display feedback history
    st.sidebar.header("Feedback")
    for fb in st.session_state['feedback']:
        st.sidebar.text(fb)



