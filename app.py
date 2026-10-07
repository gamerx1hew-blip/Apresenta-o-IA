import streamlit as st
import time

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# CSS para o design de conversa e botão minimalista no canto
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
    
    /* Botão de reset no canto superior direito */
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

    /* Balões de conversa estilo chat */
    div[data-testid="stChatMessage"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 12px 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stChatMessage"]:nth-child(even) {
        border-left: 4px solid #00FFA3;
    }
    </style>
""", unsafe_allow_html=True)

# Topo com título e botão minimalista no canto direito
col_titulo, col_botao = st.columns([0.85, 0.15])

# Mensagem Inicial com sugestões de perguntas guiadas
MENSAGEM_INICIAL = """Olá! Sou o **assistente virtual** da apresentação. 🤖

Você pode me perguntar sobre diversos tópicos do dia a dia. Por onde prefere começar?

• **Como ajudo no trânsito e rotas?** *(ex: "como funciona no GPS?")*
• **Como personalizo músicas e rotina?** *(ex: "como você cria playlists?")*
• **Como entendo comandos de voz?** *(ex: "como funcionam as assistentes em casa?")*
• **Como automatizo tarefas e programação?** *(ex: "você consegue programar ou controlar máquinas?")*
• **Como detecto fraudes na internet?** *(ex: "como identifica curtidas falsas?")*
• **Qual é o futuro do trabalho humano?** *(ex: "a IA vai substituir os humanos?")*"""

with col_titulo:
    st.title("🤖 ASSISTENTE DE IA")

with col_botao:
    if st.button("🔄", help="Resetar Apresentação"):
        st.session_state.messages = [
            {"role": "assistant", "content": MENSAGEM_INICIAL, "img": None}
        ]
        st.rerun()

# Base de conhecimento mapeando múltiplos gatilhos/palavras para cada tópico
TOPICOS = [
    {
        "gatilhos": ["trânsito", "transito", "gps", "rota", "carro", "motorista", "engarrafamento", "waze", "caminho", "tráfego", "trafego"],
        "texto": "Eu analiso o **tráfego de milhares de motoristas** em tempo real. Se encontro um engarrafamento, **recalculo a rota na hora** para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    {
        "gatilhos": ["música", "musica", "playlist", "som", "spotify", "ouvir", "ritmo", "cancao", "canção"],
        "texto": "Eu meço o seu **histórico de reprodução**, o ritmo das músicas que você mais escuta e o horário do dia para montar **playlists personalizadas** que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    {
        "gatilhos": ["voz", "falar", "comando", "alexa", "siri", "assistente", "casa", "luz", "alarme", "ouvir"],
        "texto": "Eu processo o **som da sua voz**, entendo o comando em **milissegundos** e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"
    },
    {
        "gatilhos": ["programação", "programacao", "código", "codigo", "sistema", "máquina", "maquina", "robô", "robo", "repetitivo", "automação", "automacao"],
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    {
        "gatilhos": ["impulso", "clique", "fraude", "perfil", "fake", "redes", "social", "curtida", "bloqueio", "bloquear", "segurança", "seguranca"],
        "texto": "Eu analiso o **comportamento das redes sociais**. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, **bloqueio a ação** para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    },
    {
        "gatilhos": ["substituir", "trocar", "emprego", "trabalho", "futuro", "humano", "mão de obra", "mao de obra", "demitir", "junto"],
        "texto": "Não! Minha função é **TRABALHAR JUNTO** com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem **criatividade, empatia e decisões éticas**.",
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800"
    }
]

def buscar_resposta(pergunta_usuario):
    pergunta_clean = pergunta_usuario.lower()
    
    for item in TOPICOS:
        for gatilho in item["gatilhos"]:
            if gatilho in pergunta_clean:
                return item["texto"], item["imagem"]
                
    # Caso a pergunta não esteja relacionada ao tema da apresentação
    resposta_padrao = (
        "Sou um assistente focado em **Inteligência Artificial e Automação no cotidiano**. "
        "Posso responder sobre **trânsito**, **músicas**, **comandos de voz**, **programação**, **fraudes digitais** ou o **futuro do trabalho**!"
    )
    return resposta_padrao, None

def stream_texto(texto):
    for palavra in texto.split(" "):
        yield palavra + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": MENSAGEM_INICIAL, "img": None}
    ]

# Exibição do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)

# Entrada do chat
if prompt_usuario := st.chat_input("💬 Digite sua pergunta sobre a IA..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = [
            {"role": "assistant", "content": MENSAGEM_INICIAL, "img": None}
        ]
        st.rerun()
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_usuario, "img": None})
        with st.chat_message("user"):
            st.write(prompt_usuario)

        with st.chat_message("assistant"):
            resposta_texto, imagem_url = buscar_resposta(prompt_usuario)
            
            st.write_stream(stream_texto(resposta_texto))
            
            if imagem_url:
                with st.spinner("🎨 Gerando imagem ilustrativa com IA..."):
                    time.sleep(1.2)
                st.image(imagem_url, use_container_width=True)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta_texto,
                "img": imagem_url
            })
