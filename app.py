import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
Você é o assistente virtual de uma apresentação escolar sobre Inteligência Artificial.
Responda de forma curta e direta (máximo 3 frases) em tom amigável.
Sempre explique o conceito e sugira a solução visual correspondente.
"""

st.title("🤖 Assistente de IA - Apresentação")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if st.button("🔄 Resetar Apresentação"):
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.rerun()

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt_usuario := st.chat_input("Digite sua pergunta (ou 'reset')..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.write(prompt_usuario)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            resposta_texto = response.choices[0].message.content
            st.write(resposta_texto)
            st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
