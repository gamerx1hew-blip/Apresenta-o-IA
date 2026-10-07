import streamlit as st
import time

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# CSS para criar os balões de conversa e o botão minimalista no canto
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    stApp { background-color: #0E1117; }
    h1 {
        color: #00FFA3 !important;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        margin-top: -30px;
        margin-bottom: 20px;
    }
    
    /* Botão de reset minimalista no canto superior direito */
    div[data-testid="stColumn"]:nth-child(2) {
        display: flex;
        justify-content: flex-end;
    }
    .stButton>button {
        background-color: #1F2937;
        color: #00FFA3;
        border: 1px solid #00FFA3;
        border-radius: 50%;
        width: 42px;
        height: 42px;
        padding: 0px;
        font-size: 18px;
        box-shadow: 0 2px 5px rgba(0,255,163,0.2);
    }
    .stButton>button:hover {
        background-color: #00FFA3;
        color: #0E1117;
    }

    /* Estilização dos balões de conversa */
    div[data-testid="stChatMessage"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Destaque para as mensagens da IA */
    div[data-testid="stChatMessage"]:nth-child(even) {
        border-left: 4px solid #00FFA3;
    }
    </style>
""", unsafe_allow_html=True)

# Topo com título e botão minimalista posicionado no canto direito
col_titulo, col_botao = st.columns([0.85, 0.15])

with col_titulo:
    st.title("🤖 ASSISTENTE DE IA")

with col_botao:
    if st.button("🔄", help="Resetar Apresentação"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Faça uma pergunta sobre **trânsito**, **música**, **voz**, **programação** ou o **futuro do trabalho**!",
                "img": None
            }
        ]
        st.rerun()

RESPOSTAS = {
    "trânsito": {
        "texto": "Eu analiso o **tráfego de milhares de motoristas** em tempo real. Se encontro um engarrafamento, **recalculo a rota na hora** para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    "música": {
        "texto": "Eu meço o seu **histórico de reprodução**, o ritmo das músicas que você mais escuta e o horário do dia para montar **playlists personalizadas** que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    "voz": {
        "texto": "Eu processo o **som da sua voz**, entendo o comando em **milissegundos** e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"
    },
    "programação": {
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    "robótica": {
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800"
    },
    "impulsos": {
        "texto": "Eu analiso o **comportamento das redes sociais**. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, **bloqueio a ação** para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    },
    "cliques": {
        "texto": "Eu analiso o **comportamento das redes sociais**. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, **bloqueio a ação** para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    },
    "substituir": {
        "texto": "Não! Minha função é **TRABALHAR JUNTO** com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem **criatividade, empatia e decisões éticas**.",
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
            "content": "Olá! Sou o **assistente virtual** da apresentação. Faça uma pergunta sobre **trânsito**, **música**, **voz**, **programação** ou o **futuro do trabalho**!",
            "img": None
        }
    ]

# Exibição do histórico de mensagens dentro dos balões estilizados
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)

# Campo de entrada no rodapé
if prompt_usuario := st.chat_input("💬 Digite seu comando ou pergunta aqui..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Faça uma pergunta sobre **trânsito**, **música**, **voz**, **programação** ou o **futuro do trabalho**!",
                "img": None
            }
        ]
        st.rerun()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario, "img": None})
        with st.chat_message("user"):
            st.write(prompt_usuario)

        with st.chat_message("assistant"):
            texto_pergunta = prompt_usuario.lower()
            resposta_texto = "Não entendi bem a pergunta. Pode refazer usando palavras como **trânsito**, **música**, **voz**, **programação**, **impulsos** ou **substituir**?"
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
