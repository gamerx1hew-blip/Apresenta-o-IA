import streamlit as st
import time

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# Estilo Visual Futurista
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    stApp { background-color: #0E1117; }
    h1 {
        color: #00FFA3 !important;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 0px;
    }
    .status-bar {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1F2937;
        color: #00FFA3;
        border: 1px solid #00FFA3;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 5px;
    }
    .stButton>button:hover {
        background-color: #00FFA3;
        color: #0E1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 ASSISTENTE DE IA")
st.markdown("<div class='status-bar'>🔴 AO VIVO | Status: Sistema Operacional</div>", unsafe_allow_html=True)

RESPOSTAS = {
    "trânsito": {
        "texto": "Eu analiso o tráfego de milhares de motoristas em tempo real. Se encontro um engarrafamento, recalculando a rota na hora para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    "música": {
        "texto": "Eu meço o seu histórico de reprodução, o ritmo das músicas que você mais escuta e o horário do dia para montar playlists personalizadas que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    "voz": {
        "texto": "Eu processo o som da sua voz, entendo o comando em milissegundos e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"
    },
    "programação": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    "robótica": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800"
    },
    "impulsos": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    },
    "cliques": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    },
    "substituir": {
        "texto": "Não! Minha função é TRABALHAR JUNTO com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem criatividade, empatia e decisões éticas.",
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800"
    }
}

def stream_texto(texto):
    for palavra in texto.split(" "):
        yield palavra + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o assistente virtual da apresentação. Escolha um tema abaixo ou faça sua pergunta!",
            "img": None
        }
    ]

# Botões de Atalho Rápido no Topo
st.write("**Atalhos de Pergunta:**")
col1, col2, col3 = st.columns(3)

pergunta_clicada = None
with col1:
    if st.button("🚦 Trânsito"): pergunta_clicada = "IA, como você ajuda no trânsito?"
    if st.button("💻 Programação"): pergunta_clicada = "IA, como você ajuda na programação?"
with col2:
    if st.button("🎵 Música"): pergunta_clicada = "IA, como você recomenda música?"
    if st.button("🛡️ Impulsos"): pergunta_clicada = "IA, como combate fazendas de impulsos?"
with col3:
    if st.button("🎙️ Voz"): pergunta_clicada = "IA, como funciona assistente de voz?"
    if st.button("👥 Futuro"): pergunta_clicada = "IA, você vai substituir os humanos?"

if st.button("🔄 Resetar Apresentação"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o assistente virtual da apresentação. Escolha um tema abaixo ou faça sua pergunta!",
            "img": None
        }
    ]
    st.rerun()

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)

# Captura entrada (seja digitada ou via botão de atalho)
prompt_input = st.chat_input("Digite sua pergunta (ou 'reset')...")
prompt_final = pergunta_clicada or prompt_input

if prompt_final:
    if prompt_final.strip().lower() == "reset":
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o assistente virtual da apresentação. Escolha um tema abaixo ou faça sua pergunta!",
                "img": None
            }
        ]
        st.rerun()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_final, "img": None})
        with st.chat_message("user"):
            st.write(prompt_final)

        with st.chat_message("assistant"):
            texto_pergunta = prompt_final.lower()
            resposta_texto = "Não entendi bem a pergunta. Pode refazer usando palavras como trânsito, música, voz, programação, impulsos ou substituir?"
            imagem_url = None
            
            for chave, dados in RESPOSTAS.items():
                if chave in texto_pergunta:
                    resposta_texto = dados["texto"]
                    imagem_url = dados["imagem"]
                    break
            
            st.write_stream(stream_texto(resposta_texto))
            
            if imagem_url:
                with st.spinner("🎨 Gerando imagem ilustrativa com IA..."):
                    time.sleep(1.5)
                st.image(imagem_url, use_container_width=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta_texto,
                "img": imagem_url
            })
            st.rerun()
