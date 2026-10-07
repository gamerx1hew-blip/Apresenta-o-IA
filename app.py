import streamlit as st
import time

st.title("🤖 Assistente de IA - Apresentação")

# Dicionário com textos e imagens correspondentes a cada tema
RESPOSTAS = {
    "trânsito": {
        "texto": "Eu analiso o tráfego de milhares de motoristas em tempo real. Se encontro um engarrafamento, recalculando a rota na hora para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=600"
    },
    "música": {
        "texto": "Eu meço o seu histórico de reprodução, o ritmo das músicas que você mais escuta e o horário do dia para montar playlists personalizadas que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600"
    },
    "voz": {
        "texto": "Eu processo o som da sua voz, entendo o comando em milissegundos e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1589254065878-42c9da997008?w=600"
    },
    "programação": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600"
    },
    "robótica": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600"
    },
    "impulsos": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=600"
    },
    "cliques": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=600"
    },
    "substituir": {
        "texto": "Não! Minha função é TRABALHAR JUNTO com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem criatividade, empatia e decisões éticas.",
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600"
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🔄 Resetar Apresentação"):
    st.session_state.messages = []
    st.rerun()

# Exibe as mensagens e imagens já salvas na conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)

# Campo de entrada para as perguntas
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
            resposta_texto = "Não entendi bem a pergunta. Pode refazer usando palavras como trânsito, música, voz, programação, impulsos ou substituir?"
            imagem_url = None
            
            for chave, dados in RESPOSTAS.items():
                if chave in texto_pergunta:
                    resposta_texto = dados["texto"]
                    imagem_url = dados["imagem"]
                    break
            
            time.sleep(1)
            st.write(resposta_texto)
            if imagem_url:
                st.image(imagem_url, use_container_width=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta_texto,
                "img": imagem_url
            })
