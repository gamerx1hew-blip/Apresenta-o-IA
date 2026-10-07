import streamlit as st
import time

st.title("🤖 Assistente de IA - Apresentação")

# Dicionário com textos e imagens correspondentes a cada tema
RESPOSTAS = {
    "trânsito": {
        "texto": "Eu analiso o tráfego de milhares de motoristas em tempo real. Se encontro um engarrafamento, recalculando a rota na hora para você chegar mais rápido e sem estresse.",
        "imagem": "https://images.unsplash.com/photo-1548345680-f5475ea5df84?w=800" # Foto real de GPS/Mapa de navegação no trânsito
    },
    "música": {
        "texto": "Eu meço o seu histórico de reprodução, o ritmo das músicas que você mais escuta e o horário do dia para montar playlists personalizadas que combinam com o seu momento.",
        "imagem": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800" # Fones de ouvido e aplicativo de música
    },
    "voz": {
        "texto": "Eu processo o som da sua voz, entendo o comando em milissegundos e me conecto aos aparelhos da casa para tocar músicas, acender luzes ou programar alarmes.",
        "imagem": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800" # Coluna de som / Assistente de voz inteligente
    },
    "programação": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800" # Código de programação num ecrã
    },
    "robótica": {
        "texto": "Eu assumo a digitação de códigos repetitivos, encontro erros no sistema e comando máquinas para executarem movimentos precisos sem cansar ou errar.",
        "imagem": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800" # Braço robótico futurista
    },
    "impulsos": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800" # Ecrã de telemóvel com redes sociais
    },
    "cliques": {
        "texto": "Eu analiso o comportamento das redes sociais. Quando vejo milhares de curtidas vindas de perfis falsos em poucos segundos, bloqueio a ação para evitar fraudes.",
        "imagem": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800" # Ecrã de telemóvel com redes sociais
    },
    "substituir": {
        "texto": "Não! Minha função é TRABALHAR JUNTO com vocês. Eu faço os cálculos rápidos e tarefas repetitivas, mas só os humanos possuem criatividade, empatia e decisões éticas.",
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800" # Pessoas e tecnologia a trabalharem juntas em equipa
    }
}
