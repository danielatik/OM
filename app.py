import streamlit as st
import time
import requests
import json
import logging
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(filename='chat.log', level=logging.INFO)

# test..


# st.markdown("<!-- Hotjar Tracking Code for OM Iris --><script>(function(h,o,t,j,a,r){h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};h._hjSettings={hjid:3602316,hjsv:6};a=o.getElementsByTagName('head')[0];r=o.createElement('script');r.async=1;r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;a.appendChild(r);})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');</script>")
# Hello
st.set_page_config(layout="wide")  

# col1, col2 = st.columns([1,2])
st.markdown(("<h2 style='text-align: center;'>Hola 👋, Soy Iris, tu asistente de Open Montessori, ¿en qué puedo ayudarte?</h2>", unsafe_allow_html=True)

st.markdown("""
    <style>
    .css-zq5wmm{
        display:none;
    }
    .css-usj992 {
        padding-bottom:100px!important;
    }
    </style>
    """, unsafe_allow_html=True)

# with col1:
#     st.title("Hola 👋, Soy Iris, ¿en qué puedo ayudarte?")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Pregunta lo que quieras sobre OM..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    logging.info('User: ', prompt)

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        #Judini
        api_key= os.getenv("JUDINI_API_KEY")
        agent_id= os.getenv("JUDINI_AGENT_ID")
        url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+api_key}
        data = {
            "messages": st.session_state.messages
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        raw_data = ''
        tokens = ''
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                raw_data = chunk.decode('utf-8').replace("data: ", '')
                if raw_data != "":
                    lines = raw_data.strip().splitlines()
                    for line in lines:
                        line = line.strip()
                        if line and line != "[DONE]":
                            try:
                                json_object = json.loads(line) 
                                result = json_object['data']
                                full_response += result
                                time.sleep(0.05)
                                # Add a blinking cursor to simulate typing
                                message_placeholder.markdown(full_response + "▌")
                            except json.JSONDecodeError:
                                print(f'Error al decodificar el objeto JSON en la línea: {line}')
        message_placeholder.markdown(full_response)
        logging.info('Agent: ', full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})