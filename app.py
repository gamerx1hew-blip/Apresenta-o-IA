import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Assistente de IA", page_icon="🤖", layout="centered")

# Configura a chave de API
api_key = st.secrets.get("GEMINI_API_KEY", None)
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

# Estilização CSS
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
    div[data-testid="stColumn"]:nth-child(2) { display: flex; justify-content: flex-end; }
    .reset-btn button {
        background-color: #1F2937 !important; color: #00FFA3 !important;
        border: 1px solid #00FFA3 !important; border-radius: 50% !important;
        width: 42px !important; height: 42px !important; padding: 0px !important;
        font-size: 18px !important; box-shadow: 0 2px 5px rgba(0,255,163,0.2) !important;
    }
    div[data-testid="stChatMessage"] {
        background-color: #161B22; border: 1px solid #30363D;
        border-radius: 15px; padding: 12px 16px; margin-bottom: 12px;
    }
    div[data-testid="stChatMessage"]:nth-child(even) { border-left: 4px solid #00FFA3; }
    .stButton>button {
        background-color: #161B22; color: #00FFA3; border: 1px solid #00FFA3;
        border-radius: 20px; padding: 8px 14px; font-size: 13px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #00FFA3; color: #0E1117; }
    </style>
""", unsafe_allow_html=True)

col_titulo, col_botao = st.columns([0.85, 0.15])

TODOS_TOPICOS = {
    "transito": {
        "label": "🚗 Como te ajudo no trânsito?",
        "gatilhos": ["como te ajudo no trânsito", "como você me ajuda no trânsito", "trânsito no dia a dia"],
        "texto": "Eu analiso o **tráfego de milhares de motoristas** em tempo real. Se encontro um engarrafamento, **recalculo a rota na hora** para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    "musica": {
        "label": "🎵 Como crio playlists de música?",
        "gatilhos": ["como crio playlists", "como você cria playlists", "playlists de música"],
        "texto": "Eu meço o seu **histórico de reprodução**, o ritmo das músicas que você mais escuta e o horário do dia para montar **playlists personalizadas** que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    "voz": {
        "label": "🗣️ Como entendo comandos de voz?",
        "gatilhos": ["como entendo comandos de voz", "como você entende comandos de voz"],
        "texto": "Eu processo o **som da sua voz**, entendo o comando em **milissegundos** e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800"
    },
    "programacao": {
        "label": "💻 Como automatizo programação e máquinas?",
        "gatilhos": ["como automatizo programação", "como você automatiza a programação"],
        "texto": "Eu assumo a **digitação de códigos repetitivos**, encontro erros no sistema e **comando máquinas** para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    "fraudes": {
        "label": "🛡️ Como detecto fraudes e cliques falsos?",
        "gatilhos": ["como detecto fraudes", "como a ia detecta impulsos"],
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o **assistente virtual** da apresentação. Sobre qual assunto você gostaria de saber primeiro?",
            "img": None,
            "opcoes_restantes": list(TODOS_TOPICOS.keys())
        }
    ]

def perguntar_a_ia(prompt_usuario):
    if not os.environ.get("GEMINI_API_KEY"):
        return "⚠️ A chave da API do Gemini não foi configurada nos Secrets do Streamlit."
    
    prompt_sistema = (
        "Você é um assistente virtual interativo numa apresentação sobre Inteligência Artificial. "
        "Responda em português de forma clara, breve e didática (no máximo 3 frases). "
        "Destaque em **negrito** os termos mais importantes."
    )

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"{prompt_sistema}\n\nPergunta do usuário: {prompt_usuario}"
        )
        if response and response.text:
            return response.text
    except Exception as e:
        return f"Erro ao acessar a API do Gemini: {str(e)}"
            
    return "Não foi possível obter resposta da IA no momento."

def processar_pergunta(pergunta_usuario, chave_topico=None):
    st.session_state.messages.append({"role": "user", "content": pergunta_usuario, "img": None})
    pergunta_clean = pergunta_usuario.lower().strip()
    
    opcoes_anteriores = []
    for m in reversed(st.session_state.messages[:-1]):
        if m["role"] == "assistant" and "opcoes_restantes" in m:
            opcoes_anteriores = m["opcoes_restantes"].copy()
            break

    if any(p in pergunta_clean for p in ["substituir", "humano", "emprego", "trabalho", "sim", "não", "nao", "acho", "depende", "concordo"]):
        resposta_texto = """Não importa o ponto de vista, a verdade é que minha função é **TRABALHAR JUNTO** com vocês! Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem **criatividade, empatia e decisões éticas**."""
        imagem_url = "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800"
        opcoes_novas = []
    else:
        topico_encontrado_key = chave_topico
        
        if not topico_encontrado_key:
            for key, item in TODOS_TOPICOS.items():
                if pergunta_clean in [g.lower() for g in item["gatilhos"]]:
                    topico_encontrado_key = key
                    break

        if topico_encontrado_key and topico_encontrado_key in TODOS_TOPICOS:
            dados = TODOS_TOPICOS[topico_encontrado_key]
            resposta_texto = dados["texto"]
            imagem_url = dados["imagem"]
            opcoes_novas = [k for k in opcoes_anteriores if k != topico_encontrado_key]
            
            if len(opcoes_novas) == 0:
                resposta_texto += "\n\n---\n🔥 **E afinal: você acha que a IA vai substituir os humanos? Digite sua opinião aqui no chat!**"
        else:
            resposta_texto = perguntar_a_ia(pergunta_usuario)
            imagem_url = None
            opcoes_novas = opcoes_anteriores

    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta_texto,
        "img": imagem_url,
        "opcoes_restantes": opcoes_novas
    })

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "img" in message and message["img"]:
            st.image(message["img"], use_container_width=True)
        
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
