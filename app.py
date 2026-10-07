import streamlit as st
import time

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# Estilização CSS para o tema escuro e botões estilo balão
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

    /* Estilo dos botões/balões clicáveis de opção */
    .stButton>button {
        background-color: #161B22;
        color: #00FFA3;
        border: 1px solid #00FFA3;
        border-radius: 20px;
        padding: 8px 14px;
        font-size: 13px;
        font-weight: bold;
        transition: all 0.3s ease;
        margin-top: 4px;
        margin-bottom: 4px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00FFA3;
        color: #0E1117;
    }
    </style>
""", unsafe_allow_html=True)

# Topo com título e botão de reset
col_titulo, col_botao = st.columns([0.85, 0.15])

# Lista completa dos tópicos iniciais
TODOS_TOPICOS = {
    "transito": {
        "label": "🚗 Como te ajudo no trânsito?",
        "gatilhos": ["trânsito", "transito", "gps", "rota", "carro", "motorista", "engarrafamento", "waze"],
        "texto": "Eu analiso o **tráfego de milhares de motoristas** em tempo real. Se encontro um engarrafamento, **recalculo a rota na hora** para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    "musica": {
        "label": "🎵 Como crio playlists de música?",
        "gatilhos": ["música", "musica", "playlist", "som", "spotify", "ritmo"],
        "texto": "Eu meço o seu **histórico de reprodução**, o ritmo das músicas que você mais escuta e o horário do dia para montar **playlists personalizadas** que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    "voz": {
        "label": "🗣️ Como entendo comandos de voz?",
        "gatilhos": ["voz", "falar", "comando", "alexa", "siri", "assistente", "casa"],
        "texto": "Eu processo o **som da sua voz**, entendo o comando em **milissegundos** e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"
    },
    "programacao": {
        "label": "💻 Como automatizo programação e máquinas?",
        "gatilhos": ["programação", "programacao", "código", "codigo", "sistema", "máquina", "maquina", "robô", "robo"],
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    "fraudes": {
        "label": "🛡️ Como detecto fraudes e cliques falsos?",
        "gatilhos": ["impulso", "clique", "fraude", "perfil", "fake", "redes", "social", "curtida"],
        "texto": "Eu analiso o **comportamento das redes sociais**. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, **bloqueio a ação** para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    }
}

with col_titulo:
    st.title("🤖 ASSISTENTE DE IA")

with col_botao:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄", help="Resetar Apresentação"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Sobre qual assunto você gostaria de saber primeiro?",
                "img": None,
                "opcoes_restantes": list(TODOS_TOPICOS.keys())
            }
        ]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Inicialização da sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o **assistente virtual** da apresentação. Sobre qual assunto você gostaria de saber primeiro?",
            "img": None,
            "opcoes_restantes": list(TODOS_TOPICOS.keys())
        }
    ]

# Função para processar perguntas e gerenciar opções restantes
def processar_pergunta(pergunta_usuario, chave_topico=None):
    st.session_state.messages.append({"role": "user", "content": pergunta_usuario, "img": None})
    pergunta_clean = pergunta_usuario.lower()
    
    # Identifica as opções restantes anteriores
    opcoes_anteriores = []
    for m in reversed(st.session_state.messages[:-1]):
        if m["role"] == "assistant" and "opcoes_restantes" in m:
            opcoes_anteriores = m["opcoes_restantes"].copy()
            break

    # Caso seja a resposta final sobre a IA substituir os humanos
    if any(p in pergunta_clean for p in ["substituir", "humano", "emprego", "trabalho", "sim", "não", "nao", "acho", "depende", "com certeza", "concordo"]):
        resposta_texto = "Não importa o ponto de vista, a verdade é que minha função é **TRABALHAR JUNTO** com vocês! Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem **criatividade, empatia e decisões éticas**."
        imagem_url = "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800"
        opcoes_novas = []
    else:
        topico_encontrado_key = chave_topico
        
        # Tenta identificar o tópico por palavra-chave caso não venha pelo clique direto do botão
        if not topico_encontrado_key:
            for key, item in TODOS_TOPICOS.items():
                if any(gatilho in pergunta_clean for gatilho in item["gatilhos"]):
                    topico_encontrado_key = key
                    break

        if topico_encontrado_key and topico_encontrado_key in TODOS_TOPICOS:
            dados = TODOS_TOPICOS[topico_encontrado_key]
            resposta_texto = dados["texto"]
            imagem_url = dados["imagem"]
            opcoes_novas = [k for k in opcoes_anteriores if k != topico_encontrado_key]
            
            # Se não restam mais opções dos botões, faz a pergunta grifada no texto!
            if len(opcoes_novas) == 0:
                resposta_texto += "\n\n---\n🔥 **E afinal: você acha que a IA vai substituir os humanos? Digite sua opinião aqui no chat!**"
        else:
            resposta_texto = "Sou um assistente focado em **Inteligência Artificial e Automação no cotidiano**. Escolha um dos tópicos disponíveis ou faça sua pergunta!"
            imagem_url = None
            opcoes_novas = opcoes_anteriores

    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta_texto,
        "img": imagem_url,
        "opcoes_restantes": opcoes_novas
    })

# Exibe o histórico de mensagens
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)
        
        # Exibe os balões/botões restantes APENAS na última resposta da IA
        if message["role"] == "assistant" and i == len(st.session_state.messages) - 1:
            opcoes = message.get("opcoes_restantes", [])
            if opcoes:
                st.write("---")
                st.caption("👇 **Escolha o próximo assunto:**")
                for key in opcoes:
                    label_botao = TODOS_TOPICOS[key]["label"]
                    if st.button(label_botao, key=f"btn_{i}_{key}"):
                        processar_pergunta(label_botao, chave_topico=key)
                        st.rerun()

# Campo para resposta/pergunta digitada no chat
if prompt_usuario := st.chat_input("💬 Responda à IA ou digite sua pergunta..."):
    if prompt_usuario.strip().lower() == "reset":
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o **assistente virtual** da apresentação. Sobre qual assunto você gostaria de saber primeiro?",
                "img": None,
                "opcoes_restantes": list(TODOS_TOPICOS.keys())
            }
        ]
        st.rerun()
    else:
        processar_pergunta(prompt_usuario)
        st.rerun()
