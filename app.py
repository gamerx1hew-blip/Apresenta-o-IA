import streamlit as st
import time

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# Estilização CSS personalizada para os balões, botões de sugestão e layout
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
    .reset-btn button {
        background-color: #1F2937 !important;
        color: #00FFA3 !important;
        border: 1px solid #00FFA3 !important;
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        padding: 0px !important;
        font-size: 18px !important;
        box-shadow: 0 2px 5px rgba(0,255,163,0.2) !important;
    }
    .reset-btn button:hover {
        background-color: #00FFA3 !important;
        color: #0E1117 !important;
    }

    /* Balões de mensagem estilo chat */
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

    /* Estilo dos botões de sugestão rápida (Chips/Balões clicáveis) */
    .stButton>button {
        background-color: #161B22;
        color: #00FFA3;
        border: 1px solid #00FFA3;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00FFA3;
        color: #0E1117;
    }
    </style>
""", unsafe_allow_html=True)

# Topo com título e botão de reset
col_titulo, col_botao = st.columns([0.85, 0.15])

with col_titulo:
    st.title("🤖 ASSISTENTE DE IA")

with col_botao:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄", help="Resetar Apresentação"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Por onde prefere começar?",
                "img": None,
                "sugestoes": [
                    "Como você me ajuda no trânsito?",
                    "Como você cria playlists de música?",
                    "Como você entende comandos de voz?"
                ]
            }
        ]
        st.session_state.topicos_vistos = set()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Definição dos tópicos do roteiro
TOPICOS = [
    {
        "id": "transito",
        "gatilhos": ["trânsito", "transito", "gps", "rota", "carro", "motorista", "engarrafamento", "waze", "caminho", "tráfego", "trafego"],
        "texto": "Eu analiso o **tráfego de milhares de motoristas** em tempo real. Se encontro um engarrafamento, **recalculo a rota na hora** para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800",
        "proxima_sugestao": "Que tal perguntar agora: **'Como você personaliza minhas músicas?'**"
    },
    {
        "id": "musica",
        "gatilhos": ["música", "musica", "playlist", "som", "spotify", "ouvir", "ritmo", "cancao", "canção"],
        "texto": "Eu meço o seu **histórico de reprodução**, o ritmo das músicas que você mais escuta e o horário do dia para montar **playlists personalizadas** que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800",
        "proxima_sugestao": "Próximo passo: **'Como funcionam as assistentes de voz em casa?'**"
    },
    {
        "id": "voz",
        "gatilhos": ["voz", "falar", "comando", "alexa", "siri", "assistente", "casa", "luz", "alarme", "ouvir"],
        "texto": "Eu processo o **som da sua voz**, entendo o comando em **milissegundos** e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800",
        "proxima_sugestao": "Experimente perguntar: **'Como você automatiza a programação e máquinas?'**"
    },
    {
        "id": "programacao",
        "gatilhos": ["programação", "programacao", "código", "codigo", "sistema", "máquina", "maquina", "robô", "robo", "repetitivo", "automação", "automacao"],
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800",
        "proxima_sugestao": "Dica de pergunta: **'Como a IA detecta impulsos e cliques falsos nas redes?'**"
    },
    {
        "id": "fraudes",
        "gatilhos": ["impulso", "clique", "fraude", "perfil", "fake", "redes", "social", "curtida", "bloqueio", "bloquear", "segurança", "seguranca"],
        "texto": "Eu analiso o **comportamento das redes sociais**. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, **bloqueio a ação** para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800",
        # Penúltima pergunta: conduz para a pergunta final!
        "proxima_sugestao": "✨ **Para fechar com chave de ouro:** Que tal perguntar se a **IA vai substituir os humanos**?"
    },
    {
        "id": "substituir",
        "gatilhos": ["substituir", "trocar", "emprego", "trabalho", "futuro", "humano", "mão de obra", "mao de obra", "demitir", "junto"],
        "texto": "Não! Minha função é **TRABALHAR JUNTO** com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem **criatividade, empatia e decisões éticas**.",
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800",
        "proxima_sugestao": "🎉 **Obrigado por participar da demonstração!** Se quiser testar outro assunto, é só perguntar!"
    }
]

def stream_texto(texto):
    for palavra in texto.split(" "):
        yield palavra + " "
        time.sleep(0.04)

# Inicialização do estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o **assistente virtual** da apresentação. Por qual tópico você prefere começar?",
            "img": None,
            "sugestoes": [
                "Como você me ajuda no trânsito?",
                "Como você cria playlists de música?",
                "Como você entende comandos de voz?"
            ]
        }
    ]

if "topicos_vistos" not in st.session_state:
    st.session_state.topicos_vistos = set()

# Processamento da Pergunta
def processar_pergunta(pergunta_usuario):
    pergunta_clean = pergunta_usuario.lower()
    
    # Adiciona a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": pergunta_usuario, "img": None})
    
    resposta_texto = None
    imagem_url = None
    proxima_dica = None
    topico_encontrado = None

    for item in TOPICOS:
        for gatilho in item["gatilhos"]:
            if gatilho in pergunta_clean:
                resposta_texto = item["texto"]
                imagem_url = item["imagem"]
                proxima_dica = item["proxima_sugestao"]
                topico_encontrado = item["id"]
                break
        if resposta_texto:
            break

    if not resposta_texto:
        resposta_texto = "Sou um assistente focado em **Inteligência Artificial e Automação no cotidiano**. Posso responder sobre trânsito, músicas, voz, programação, redes sociais ou o futuro do trabalho!"
        proxima_dica = "Tente perguntar: **'Como a IA ajuda no trânsito?'** ou **'A IA vai substituir os humanos?'**"
    else:
        st.session_state.topicos_vistos.add(topico_encontrado)

    # Conteúdo final unindo a resposta e a sugestão para o próximo passo
    conteudo_completo = f"{resposta_texto}\n\n💡 _{proxima_dica}_"
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": conteudo_completo,
        "img": imagem_url
    })

# Exibição do histórico no Chat
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)
        
        # Exibe balões/botões de sugestão clicáveis apenas na última mensagem da IA
        if message["role"] == "assistant" and i == len(st.session_state.messages) - 1:
            if "sugestoes" in message and message["sugestoes"]:
                st.write("---")
                st.caption("👇 **Sugestões para começar:**")
                cols = st.columns(len(message["sugestoes"]))
                for idx, sug in enumerate(message["sugestoes"]):
                    with cols[idx]:
                        if st.button(sug, key=f"sug_{i}_{idx}"):
                            processar_pergunta(sug)
                            st.rerun()

# Campo de entrada de texto manual
if prompt_usuario := st.chat_input("💬 Digite sua pergunta sobre a IA..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Por qual tópico você prefere começar?",
                "img": None,
                "sugestoes": [
                    "Como você me ajuda no trânsito?",
                    "Como você cria playlists de música?",
                    "Como você entende comandos de voz?"
                ]
            }
        ]
        st.session_state.topicos_vistos = set()
        st.rerun()
    else:
        processar_pergunta(prompt_usuario)
        st.rerun()
