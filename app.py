import streamlit as st
import google.generativeai as ggi
from datetime import datetime
import base64




doc_path = "pdf/LVUSD_Robotics_Agreement.pdf"

# st.info("Hey there! I'm LabChat, your personal AI assistant to help you throughout your journey in Mrs. Servin's Robotics Lab. Ask me anything!")

with open(doc_path, "rb") as doc_file:
    doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")




fetched_api_key = st.secrets["API_Key"]
ggi.configure(api_key = fetched_api_key)

#2.0 Flash with Thinking is my preffered model for this use case
model_name = "gemini-2.0-flash-thinking-exp-01-21"

model = ggi.GenerativeModel(model_name)



st.title("LabChat")
result = None

temperature = 0.7
question = st.text_input("Ask me anything", placeholder="Type away")
button = st.button("Submit")

if 'api_call_history' not in st.session_state:
    st.session_state.api_call_history = []

# Program to track the API calls of the foundation model
my_history = []
def track_api_call(question, response, temperature):
    return (question, response, temperature)

error = False
def LLM_Response(question):
    try:
        global response
        with st.spinner('Processing request ...'):
            response = model.generate_content([{'mime_type': 'application/pdf', 'data': doc_data}, question], stream = True, generation_config = ggi.GenerationConfig(temperature=temperature))
        error = False
        st.session_state.api_call_history.append(track_api_call(question, response, temperature))
        st.success("Request Processed")
        return response
    except Exception as e:
        error = True
        response = f"Could not connect to the API: {e}"

if button and question:
    result = LLM_Response(question)
    st.subheader("Response: ")
    sentence = ""
    for word in result:
        word = word.text
        sentence += word
    st.write(sentence)
    st.balloons()

# st.subheader("FM API Calls")
# print(st.session_state.api_call_history)
# st.write(st.session_state.api_call_history)

st.caption("Made with " + model_name)



