import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai

st.set_page_config(page_title="Assistente Inteligente", page_icon="🤖", layout="centered")

# Procura a chave nos Secrets do Streamlit ou variáveis de ambiente
api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")

# Função de Leitura de Voz (Text-to-Speech via JavaScript)
def falar_texto(texto):
    if texto:
        # Limpa caracteres de formatação Markdown para a voz ler com clareza
        texto_limpo = (
            texto.replace("**", "")
                 .replace("\n", " ")
                 .replace("---", "")
                 .replace("'", "\\'")
                 .replace('"', '\\"')
        )
        js_code = f"""
            <script>
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{texto_limpo}');
                    msg.lang = 'pt-BR';
                    msg.rate = 1.0;
                    window.speechSynthesis.speak(msg);
                }}
            </script>
        """
        components.html(js_code, height=0)

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
    
    /* Controla a altura limite e ajuste das imagens */
    div[data-testid="stImage"] img {
        max-height: 250px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

col_titulo, col_botao = st.columns([0.85, 0.15])

TODOS_TOPICOS = {
    "transito": {
        "label": "🚗 Como a IA ajuda no trânsito?",
        "gatilhos": ["como a ia ajuda no trânsito", "como a ia ajuda no transito", "trânsito", "transito"],
        "texto": "Sistemas de IA analisam o **tráfego de milhares de motoristas em tempo real**. Ao identificar congestionamentos, os algoritmos **recalculam rotas instantaneamente** para otimizar o tempo e reduzir o fluxo de veículos.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800"
    },
    "musica": {
        "label": "🎵 Como a IA recomenda músicas?",
        "gatilhos": ["como a ia recomenda músicas", "como a ia recomenda musicas", "música", "playlists"],
        "texto": "Algoritmos de recomendação analisam o **histórico de escuta**, o ritmo, os gêneros e até o horário em que você ouve música para identificar padrões e **gerar playlists personalizadas**.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800"
    },
    "voz": {
        "label": "🎙️ Como a IA entende a voz humana?",
        "gatilhos": ["como a ia entende a voz humana", "como a ia entende a voz", "voz humana", "comando de voz"],
        "texto": "Assistentes virtuais usam IA para **transformar a fala em texto**, interpretar o significado da mensagem e **executar comandos**, como tocar músicas, responder perguntas ou controlar dispositivos inteligentes.",
        "imagem": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=800"
    },
    "automacao": {
        "label": "🤖 Como a IA automatiza tarefas?",
        "gatilhos": ["como a ia automatiza tarefas", "como a ia automatiza", "automatiza tarefas", "programação e máquinas"],
        "texto": "A IA pode **automatizar rotinas repetitivas**, identificar erros em linhas de código e **orientar máquinas e robôs industriais** para executarem movimentos com alta precisão e sem cansaço.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800"
    },
    "fraudes": {
        "label": "🛡️ Como a IA detecta fraudes?",
        "gatilhos": ["como a ia detecta fraudes", "como a ia detecta fraude", "fraudes", "cliques falsos"],
        "texto": "Sistemas de IA analisam **padrões de comportamento e grandes volumes de dados**. Ao detectar anomalias, como milhares de acessos ou transações suspeitas em segundos, a IA **bloqueia ações fraudulentas**.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800"
    }
}

with col_titulo:
    st.title("🤖 ASSISTENTE INTELIGENTE")

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
    if not api_key:
        return "⚠️ A chave GEMINI_API_KEY não foi encontrada nos Secrets do Streamlit."

    prompt_sistema = (
        "Você é um assistente virtual interativo numa apresentação acadêmica sobre Inteligência Artificial. "
        "Responda em português de forma clara, técnica e didática (no máximo 3 frases). "
        "Destaque em **negrito** os termos mais importantes."
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{prompt_sistema}\n\nPergunta do usuário: {prompt_usuario}"
        )
        if response and response.text:
            return response.text
    except Exception:
        return "🤖 No momento estou recebendo muitas requisições! Por favor, aguarde alguns instantes ou escolha um dos tópicos sugeridos acima."

    return "Não foi possível obter resposta da IA no momento."

def processar_pergunta(pergunta_usuario, chave_topico=None):
    st.session_state.messages.append({"role": "user", "content": pergunta_usuario, "img": None})
    pergunta_clean = pergunta_usuario.lower().strip()
    
    opcoes_anteriores = []
    for m in reversed(st.session_state.messages[:-1]):
        if m["role"] == "assistant" and "opcoes_restantes" in m:
            opcoes_anteriores = m["opcoes_restantes"].copy()
            break

    if any(p in pergunta_clean for p in ["substituir", "humano", "emprego", "trabalho", "sim", "não", "nao", "acho", "depende", "concordo", "talvez"]):
        resposta_texto = (
            "É uma excelente reflexão! A IA já automatiza tarefas operacionais e repetitivas, "
            "mas o cenário mais provável é o de **colaboração e evolução do trabalho**. "
            "Enquanto a IA lida com processamento de dados e velocidade, os humanos continuam indispensáveis para **criatividade, empatia, pensamento crítico e decisões éticas**."
        )
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

# Renderiza as mensagens anteriores no ecrã
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

# Ativa a fala automática apenas para a última resposta do assistente
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    falar_texto(st.session_state.messages[-1]["content"])

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
