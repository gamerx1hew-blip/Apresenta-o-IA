import streamlit as st
import time

st.title("🤖 Assistente de IA - Apresentação")

RESPOSTAS = {
    "trânsito": "Eu analiso o tráfego de milhares de motoristas em tempo real. Se encontro um engarrafamento, recalculando a rota na hora para você chegar mais rápido e sem estresse.",
    "música": "Eu meço o seu histórico de reprodução, o ritmo das músicas que você mais escuta e o horário do dia para montar playlists personalizadas que combinam com o seu momento.",
    "voz": "Eu processo o som da sua voz, entendo o comando em milissegundos e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
    "programação": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
    "robótica": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
    "impulsos": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
    "cliques": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
    "substituir": "Não! Minha função é TRABALHAR JUNTO com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem criatividade, empatia e decisões éticas."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🔄 Resetar Apresentação"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt_usuario := st.chat_input("Digite sua pergunta (ou 'reset')..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = []
        st.rerun()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.write(prompt_usuario)

        with st.chat_message("assistant"):
            texto_pergunta = prompt_usuario.lower()
            resposta_encontrada = "Não entendi bem a pergunta. Pode refazer usando palavras como trânsito, música, voz, programação, impulsos ou substituir?"
            
            for chave, resposta in RESPOSTAS.items():
                if chave in texto_pergunta:
                    resposta_encontrada = resposta
                    break
            
            time.sleep(1)
            st.write(resposta_encontrada)
            st.session_state.messages.append({"role": "assistant", "content": resposta_encontrada})
