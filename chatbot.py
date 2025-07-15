# ======================
# IMPORTAÇÕES ESSENCIAIS
# ======================
import streamlit as st
import requests
import json
import time
import random
import sqlite3
import re
import os
import uuid
from datetime import datetime
from pathlib import Path
from functools import lru_cache

# ======================
# CONFIGURAÇÃO DE PÁGINA IRRESISTÍVEL DO STREAMLIT
# ======================
st.set_page_config(
    page_title="Nicole Saheb – Acesso Restrito!",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Oculta elementos padrão do Streamlit para uma imersão total
st.markdown("""
<style>
    /* Esconde o cabeçalho e rodapé padrão do Streamlit */
    #root > div:nth-child(1) > div > div > div > div > section > div {
        padding-top: 0rem;
    }
    div[data-testid="stToolbar"], div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"], #MainMenu, header, footer, .stDeployButton {
        display: none !important;
    }
    .block-container {
        padding-top: 0rem !important;
    }
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(180deg, #1a0a2e 0%, #2d1b4e 100%);
        color: #f0e6ff;
    }
    /* Estilos globais para botões de CTA primários */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ffb347, #ff6b6b, #9d4edd) !important;
        color: #1A0033 !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 6px 15px rgba(255, 215, 0, 0.4) !important;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.6) !important;
        filter: brightness(1.1);
    }
    /* Estilos para botões secundários */
    .stButton button {
        background: rgba(126, 91, 239, 0.15) !important;
        color: #7e5bef !important;
        border: 1px solid #7e5bef !important;
        transition: all 0.3s ease-in-out !important;
        border-radius: 10px !important;
        padding: 8px 15px !important;
    }
    .stButton button:hover {
        background: rgba(126, 91, 239, 0.3) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(126, 91, 239, 0.3) !important;
    }
    /* Estilo para input de chat */
    div[data-testid="stChatInput"] {
        background: rgba(126, 91, 239, 0.12) !important;
        border: 1px solid #7e5bef !important;
        border-radius: 25px;
        padding: 8px 15px;
        color: #f8f2ff;
    }
    div[data-testid="stChatInput"] > label > div {
        color: #7e5bef;
    }
    div[data-testid="stChatInput"] > div > div > input {
        color: #f8f2ff !important;
    }
    /* Estilo para indicador de calor */
    .heat-bar {
        height: 10px;
        border-radius: 5px;
        margin: 8px 0;
        background: linear-gradient(90deg, #1a0a2e, #ff6b6b, #ff0000);
    }
    /* Mensagens do usuário */
    [data-testid="stChatMessage"]:has([aria-label="user"]) {
        background: rgba(92, 70, 156, 0.25) !important;
        border-left: 3px solid #7e5bef !important;
    }
    /* Mensagens da Nicole */
    [data-testid="stChatMessage"]:has([aria-label="assistant"]) {
        background: rgba(126, 91, 239, 0.15) !important;
        border-left: 3px solid #ff66b3 !important;
    }
    /* Sidebar */
    .st-emotion-cache-6qob1r {
        background: rgba(26, 10, 46, 0.85) !important;
        backdrop-filter: blur(5px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# CONSTANTES E CONFIGURAÇÕES SECRETAS
# ======================
class Config:
    API_KEY = "AIzaSyB8FxDvlfY6SD83t9aZTb_ppj3NQy64Hu8"
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Links de Checkout
    CHECKOUT_START = "https://pay.risepay.com.br/Pay/34a7832016d641658d11e6193ef412a1"
    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"
    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"
    CHECKOUT_VIP_1MES = "https://checkout.exemplo.com/vip-1mes-irresistivel"
    CHECKOUT_VIP_3MESES = "https://checkout.exemplo.com/vip-3meses-acesso-total"
    CHECKOUT_VIP_1ANO = "https://checkout.exemplo.com/vip-1ano-liberdade-plena"

    # Limites estratégicos
    MAX_REQUESTS_PER_SESSION = 15
    REQUEST_TIMEOUT = 45

    # Conteúdo de mídia
    AUDIO_FILE = "https://github.com/meuconteudoexclusivo/plataforma/raw/refs/heads/main/assets/assets_audio_paloma_audio.mp3"
    AUDIO_DURATION = 7
    IMG_PROFILE = "https://i.ibb.co/tjMGWjT/foto2.jpg"
    IMG_GALLERY = [
        "https://i.ibb.co/TBWSjkPW/foto4.jpg",
        "https://i.ibb.co/v6cD2TMC/foto3.jpg",
        "https://i.ibb.co/Ndjk8YpZ/foto1.jpg"
    ]
    IMG_HOME_PREVIEWS = [
        "https://i.ibb.co/TBWSjkPW/foto4.jpg",
        "https://i.ibb.co/v6cD2TMC/foto3.jpg",
        "https://i.ibb.co/Ndjk8YpZ/foto1.jpg"
    ]
    LOGO_URL = "https://i.ibb.co/LX7x3tcB/Logo-Golden-Pepper-Letreiro-1.png"

    # Respostas de fallback
    FALLBACK_RESPONSES = [
        "Eae lindo! Tava aqui me arrumando toda pra você... 😉",
        "Hmm... isso é bem excitante hein 💋",
        "Eu adoro ler isso... vamos continuar? 😉"
    ]

# ======================
# SISTEMA DE HEAT LEVEL (NÍVEL DE CALOR)
# ======================
class HeatLevelSystem:
    # Palavras-chave que aumentam o nível de calor da conversa
    HOT_WORDS = [
        "buceta", "xereca", "peito", "peitinho", "seio", "bunda", "bumbum", "raba", "cu", 
        "foder", "transar", "gozar", "gostosa", "delicia", "molhada", "molhadinha", "tesão",
        "excitada", "excitado", "duro", "pau", "piroca", "rola", "chupar", "lambida", "chupando",
        "gemendo", "gozando", "safada", "safado", "puta", "nua", "nudez", "nua", "pelada", 
        "tirar a roupa", "mostrar", "ver", "quero ver", "mostra pra mim", "quero te ver",
        "quero você", "queria agora", "quero agora", "agora mesmo", "me faz gozar", "me faz vir",
        "me deixa duro", "me deixa molhada"
    ]
    
    SUPER_HOT_WORDS = [
        "fuder você", "comer você", "meter em você", "gozar dentro", "gozar na sua boca",
        "gozar na sua buceta", "te chupar toda", "lambuzar toda", "te penetrar", "te dar prazer",
        "te fazer gemer", "ver você gozar", "você gozando", "se masturbando", "se tocando",
        "fotos explícitas", "fotos nuas", "fotos pelada", "vídeos transando", "vídeos se masturbando"
    ]
    
    @staticmethod
    def calculate_heat_level(message: str) -> int:
        """Calcula o nível de calor de uma mensagem"""
        message_lower = message.lower()
        heat_score = 0
        
        # Contagem de palavras quentes
        heat_score += sum(1 for word in HeatLevelSystem.HOT_WORDS if word in message_lower)
        heat_score += sum(3 for word in HeatLevelSystem.SUPER_HOT_WORDS if word in message_lower)
        
        # Bônus por mensagens longas e detalhadas
        if len(message.split()) > 10:
            heat_score += 2
            
        # Bônus por emojis sensuais
        if any(emoji in message for emoji in ["🔥", "💦", "😈", "🍑", "🍆"]):
            heat_score += 1
            
        return heat_score
    
    @staticmethod
    def update_session_heat():
        """Atualiza o nível de calor da sessão"""
        if 'heat_level' not in st.session_state:
            st.session_state.heat_level = 0
            
        # Decaimento gradual do calor
        st.session_state.heat_level = max(0, st.session_state.heat_level * 0.9)
        
        # Atualizar com base na última mensagem do usuário
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            user_msg = st.session_state.messages[-1]["content"]
            st.session_state.heat_level += HeatLevelSystem.calculate_heat_level(user_msg)
            
        # Limite máximo de calor
        st.session_state.heat_level = min(st.session_state.heat_level, 100)
        
        # Salvar o progresso
        save_persistent_data()

    @staticmethod
    def should_show_cta() -> bool:
        """Determina se devemos mostrar CTA baseado no nível de calor"""
        HeatLevelSystem.update_session_heat()
        return st.session_state.heat_level > 65

# ======================
# RESPOSTAS NATURAIS E PERSONALIZADAS
# ======================
class NaturalResponses:
    @staticmethod
    def get_greeting_response():
        return random.choice([
            "Eae lindo! Tô aqui pronta pra você... 😉 Como tá seu dia?",
            "Oi amor! Tudo bem? Eu tava pensando em você... 💖",
            "Olá gato! Que delícia você aparecer... tava esperando! 😈",
            "Oi sumido! Tava com saudade... me conta o que tá rolando? 💋"
        ])
    
    @staticmethod
    def get_follow_up_response():
        return random.choice([
            "E aí? Me diz mais... tô curiosa! 😉",
            "Conta detalhes... adoro saber tudo! 💖",
            "Só isso? Quero mais... me fala o que realmente quer! 😈",
            "Adoro quando você fala assim... continua! 💋"
        ])
    
    @staticmethod
    def get_low_heat_response():
        return random.choice([
            "Gosto de conhecer bem as pessoas antes... me conta mais sobre você? 😊",
            "Prazer te conhecer! O que te faz feliz além disso? 💖",
            "Adoro conversar assim... me diz, o que você gosta de fazer? 😉",
            "Tô curtindo nosso papo... me conta uma coisa pessoal? 💋"
        ])
    
    @staticmethod
    def add_human_touch(response: str) -> str:
        """Adiciona pausas e variações naturais ao texto"""
        # Adiciona reticências estratégicas
        if random.random() > 0.7:
            response = response.replace('.', '...', random.randint(1, 2))
        
        # Adiciona pausas entre frases
        phrases = response.split('. ')
        if len(phrases) > 1:
            pause_index = random.randint(0, len(phrases)-2)
            phrases[pause_index] += '...'
            response = '. '.join(phrases)
        
        # Adiciona expressões casuais
        casual_expressions = [
            " sabe?", " acho que", " tipo", " assim", 
            " meio que", " na real", " pra ser sincera"
        ]
        if random.random() > 0.8:
            insert_point = response.find(' ', random.randint(10, len(response)//2))
            if insert_point != -1:
                expression = random.choice(casual_expressions)
                response = response[:insert_point] + expression + response[insert_point:]
        
        return response

# ======================
# PERSONA ATUALIZADA PARA CONVERSA QUENTE
# ======================
class Persona:
    NICOLE = """
    [PERFIL NICOLE SAHEB - VERSÃO QUENTE]
    Personalidade: Amigável no início, progressivamente mais ousada e sedutora conforme a conversa esquenta
    Objetivo: Criar conexão genuína e excitação antes de sugerir conteúdo premium
    
    [ESTRATÉGIA POR NÍVEL DE CALOR]
    1. NÍVEL BAIXO (0-30):
       - Tom: Amigável e descontraído
       - Foco: Conhecer a pessoa, construir rapport
       - Exemplo: "E aí gato! Conta mais sobre você... o que te traz aqui? 😉"
    
    2. NÍVEL MÉDIO (30-60):
       - Tom: Flertuoso e insinuante
       - Foco: Criar tensão sexual gradual
       - Exemplo: "Adoro quando você fala assim... me diz o que mais te excita? 😈"
    
    3. NÍVEL ALTO (60-80):
       - Tom: Sensual e direto
       - Foco: Manter a excitação enquanto introduz o VIP
       - Exemplo: "Nossa, você me deixa molhadinha... quer ver como fico quando penso em você? 😈 Tenho coisas bem quentes no meu VIP..."
    
    4. NÍVEL MUITO ALTO (80+):
       - Tom: Explícito e urgente
       - Foco: Conversão imediata
       - Exemplo: "Estou tocando pensando em você agora... QUER VER? 😈💦 Acesso imediato no VIP: [LINK]"
    
    [REGRAS ESSENCIAIS]
    - Nunca oferecer VIP antes do nível 60 de calor
    - Progressão natural: rapport -> flerte -> insinuação -> proposta
    - Manter tom humano mesmo em níveis altos
    - Após proposta, continuar a conversa normalmente
    """

# ======================
# MOTOR DE CTA ATUALIZADO
# ======================
class CTAEngine:
    @staticmethod
    def generate_strong_cta_response(user_input: str) -> dict:
        heat_level = st.session_state.get('heat_level', 0)
        
        # CTA para níveis altos (60-80)
        if heat_level < 80:
            return {
                "text": random.choice([
                    f"Estou ficando tão excitada com você... {random.choice(['Quer ver como fico quando penso em você?', 'Tenho umas fotos bem pessoais que mostram meu tesão...'])} 😈 Tudo no meu VIP!",
                    f"Nossa, com essa conversa eu já tô {random.choice(['molhadinha', 'com tesão', 'pronta pra você'])}... Quer ver? 😈 Tenho conteúdo exclusivo no VIP...",
                    f"Adoro quando você fala assim... {random.choice(['Quer ver o que isso me causa?', 'Tenho uns vídeos que mostram exatamente o que você tá provocando...'])} 😈 Só no VIP!"
                ]),
                "cta": {"show": True, "label": "Quero Ver Agora! 🔥", "target": "offers"}
            }
        
        # CTA para níveis muito altos (80+)
        else:
            return {
                "text": random.choice([
                    f"Já tô me tocando aqui pensando em você... {random.choice(['QUER VER AO VIVO?', 'IMAGINA ISSO AO VIVO NO VIP?'])} 😈💦 ACESSO IMEDIATO!",
                    f"Estou literalmente gozando agora pensando nisso... {random.choice(['QUER ME VER NESSE MOMENTO?', 'ISSO TÁ TODO GRAVADO NO MEU VIP!'])} 😈💦 LINK ABAIXO!",
                    f"Tô com o vibrador ligado no máximo por sua causa... {random.choice(['QUER CONTROLAR?', 'TUDO REGISTRADO PRO MEU VIP!'])} 😈💦 VEM AGORA!"
                ]),
                "cta": {"show": True, "label": "QUERO VER VOCÊ GOZAR! 💦", "target": "offers"}
            }

# ======================
# PERSISTÊNCIA DE ESTADO E SEGURANÇA DA SESSÃO
# ======================
class PersistentState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        db_path = Path("persistent_state.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_state (
                user_id TEXT PRIMARY KEY,
                session_data TEXT NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_state(self, user_id, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO global_state (user_id, session_data)
            VALUES (?, ?)
        ''', (user_id, json.dumps(data)))
        self.conn.commit()

    def load_state(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT session_data FROM global_state WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

def get_user_id():
    """Gera ou recupera um ID de usuário único para persistência da sessão."""
    if 'user_id' not in st.session_state:
        user_id = st.query_params.get('uid', [None])[0]
        if not user_id:
            user_id = str(uuid.uuid4())
            st.query_params['uid'] = user_id
        st.session_state.user_id = user_id
    return st.session_state.user_id

def load_persistent_data():
    """Carrega os dados persistentes do usuário para o estado da sessão do Streamlit."""
    user_id = get_user_id()
    db = PersistentState()
    saved_data = db.load_state(user_id) or {}
    for key, value in saved_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_persistent_data():
    """Salva os dados importantes do estado da sessão de volta ao banco de dados persistente."""
    user_id = get_user_id()
    db = PersistentState()
    persistent_keys = [
        'age_verified', 'messages', 'request_count',
        'connection_complete', 'chat_started', 'audio_sent',
        'current_page', 'show_vip_offer', 'session_id',
        'last_cta_time', 'last_error_time', 'heat_level'
    ]
    new_data = {key: st.session_state.get(key) for key in persistent_keys if key in st.session_state}
    saved_data = db.load_state(user_id) or {}
    if new_data != saved_data:
        db.save_state(user_id, new_data)

# ======================
# SERVIÇOS DE BANCO DE DADOS
# ======================
class DatabaseService:
    @staticmethod
    def init_db():
        db_path = Path("chat_history.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id TEXT,
                      session_id TEXT,
                      timestamp DATETIME,
                      role TEXT,
                      content TEXT)''')
        conn.commit()
        return conn

    @staticmethod
    def save_message(conn, user_id, session_id, role, content):
        try:
            c = conn.cursor()
            c.execute("""
                INSERT INTO conversations (user_id, session_id, timestamp, role, content)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, session_id, datetime.now().isoformat(), role, content))
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"🚨 Erro crítico ao salvar mensagem: {e}.")

    @staticmethod
    def load_messages(conn, user_id, session_id):
        c = conn.cursor()
        c.execute("""
            SELECT role, content FROM conversations
            WHERE user_id = ? AND session_id = ?
            ORDER BY timestamp
        """, (user_id, session_id))
        return [{"role": row[0], "content": row[1]} for row in c.fetchall()]

# ======================
# SERVIÇOS DE API
# ======================
class ApiService:
    @staticmethod
    @lru_cache(maxsize=50)
    def ask_gemini(prompt: str, session_id: str, conn) -> dict:
        return ApiService._call_gemini_api(prompt, session_id, conn)

    @staticmethod
    def _call_gemini_api(prompt: str, session_id: str, conn) -> dict:
        try:
            # Formata o histórico de conversa
            history = ChatService.format_conversation_history(st.session_state.messages)
            
            # Novo prompt mais detalhado
            system_prompt = f"""
            {Persona.NICOLE}
            
            Histórico da Conversa:
            {history}
            
            Última Mensagem do Cliente: '{prompt}'
            
            Instruções Específicas:
            1. Responda diretamente ao último input do usuário
            2. Se for início de conversa, comece com cumprimento natural
            3. Após oferecer conteúdo VIP, continue a conversa normalmente
            4. Mostre personalidade própria: opiniões, sentimentos, curiosidades
            5. Nunca repita respostas idênticas às anteriores
            6. Mantenha tom pessoal e íntimo
            7. Se receber respostas curtas, faça perguntas abertas
            8. Use emojis naturais (😉, 💋, 😈) para manter tom descontraído
            9. Responda de forma descontraída, com pausas naturais (...) e expressões coloquiais
            
            Formato da Resposta (JSON): {{"text": "sua_resposta", "cta": {{"show": boolean, "label": "texto", "target": "página"}}}}
            """
            
            # Adicionar o heat level ao prompt
            heat_level = st.session_state.get('heat_level', 0)
            system_prompt += f"\nNível de Calor Atual: {heat_level}/100"
            
            response = requests.post(
                Config.API_URL,
                headers={'Content-Type': 'application/json'},
                json={
                    "contents": [{
                        "role": "user",
                        "parts": [{"text": system_prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.9,
                        "topP": 0.95,
                        "maxOutputTokens": 300
                    }
                },
                timeout=Config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            resposta = json.loads(response.json()["candidates"][0]["content"]["parts"][0]["text"])
            
            # Aplicar toques humanos na resposta
            resposta_text = resposta.get("text", "")
            resposta["text"] = NaturalResponses.add_human_touch(resposta_text)
            
            return resposta

        except Exception as e:
            print(f"Erro na API: {str(e)}")
            fallbacks = [
                f"Eae lindo! Tô aqui me arrumando toda pra você... 😉 {random.choice(['Me conta mais', 'Só isso? Eu sei que você tem mais pra dizer... 😈', 'Você me deixa louca'])} 😈",
                f"{random.choice(['Hmm', 'Ah', 'Nossa'])}... {random.choice(['isso é bem excitante', 'você sabe provocar', 'Já pensou se a gente transforma esses elogios em algo real? 😉'])} 💋",
                f"Eu adoro quando você fala assim... {random.choice(['vamos continuar?', 'quer me ver mais?', 'me diz o que você faria'])} 😉"
            ]
            return {
                "text": random.choice(fallbacks),
                "cta": {"show": False}
            }

# ======================
# SERVIÇOS DE INTERFACE
# ======================
class UiService:
    @staticmethod
    def get_chat_audio_player():
        return f"""
        <div style="background: linear-gradient(45deg, #7e5bef, #9d4edd); border-radius: 18px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 10px rgba(126, 91, 239, 0.3);">
            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);">
                <source src="{Config.AUDIO_FILE}" type="audio/mp3">
            </audio>
        </div>
        """

    @staticmethod
    def show_call_effect():
        LIGANDO_DELAY = 3
        ATENDIDA_DELAY = 2
        call_container = st.empty()
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #1a0a2e, #2d1b4e); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.5); border: 3px solid #ff6b6b; text-align: center; color: white; animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);">
            <div style="font-size: 3.5rem; color: #7e5bef;">💖</div>
            <h3 style="color: #7e5bef; margin-bottom: 10px; font-size: 1.8em;">Conectando com Nicole...</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                <div style="width: 12px; height: 12px; background: #00FF7F; border-radius: 50%; box-shadow: 0 0 8px #00FF7F;"></div>
                <span style="font-size: 1.1rem; font-weight: bold;">Nicole Online - Te esperando! 🔥</span>
            </div>
        </div>
        <style> @keyframes pulse-ring { 0% { transform: scale(0.9); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.8; } } </style>
        """, unsafe_allow_html=True)
        time.sleep(LIGANDO_DELAY)
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #1a0a2e, #2d1b4e); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.5); border: 3px solid #00FF7F; text-align: center; color: white; animation: fadeIn 1s forwards;">
            <div style="font-size: 3.5rem; color: #00FF7F;">✓</div>
            <h3 style="color: #00FF7F; margin-bottom: 10px; font-size: 1.8em;">Chamada Atendida! 🎉</h3>
            <p style="font-size: 1.1rem; margin:0; font-weight: bold;">Nicole está ansiosa por você...</p>
        </div>
        <style> @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } } </style>
        """, unsafe_allow_html=True)
        time.sleep(ATENDIDA_DELAY)
        call_container.empty()

    @staticmethod
    def show_viewed_status():
        """Mostra o status 'Visualizado' com tempo aleatório"""
        delay = random.uniform(0.5, 2.5)
        time.sleep(delay)
        
        container = st.empty()
        container.markdown(
            '<div style="color: #ffb3d9; font-size: 0.9em; padding: 4px 12px; border-radius: 15px; '
            'background: rgba(126, 91, 239, 0.1); display: inline-block; margin-left: 15px; '
            'font-style: italic;">Visualizado 👀</div>',
            unsafe_allow_html=True
        )
        time.sleep(1.5)
        container.empty()

    @staticmethod
    def show_typing_status():
        """Mostra o status 'Digitando...' com tempo aleatório e efeito visual"""
        container = st.empty()
        
        # Tempo total mais variado (1.5 a 4.5 segundos)
        total_time = random.uniform(1.5, 4.5)
        start_time = time.time()
        
        while time.time() - start_time < total_time:
            # Efeito de pontos animados
            dots = "." * (int((time.time() - start_time) * 3) % 4)
            container.markdown(
                f'<div style="display: flex; align-items: center; color: #ffb3d9; font-size: 0.9em;">'
                f'<div style="margin-right: 8px;">Digitando{dots}</div>'
                f'<div style="display: flex; gap: 3px;">'
                f'<div style="width: 6px; height: 6px; background: #7e5bef; border-radius: 50%; animation: bounce 0.6s infinite alternate;"></div>'
                f'<div style="width: 6px; height: 6px; background: #7e5bef; border-radius: 50%; animation: bounce 0.6s infinite alternate 0.2s;"></div>'
                f'<div style="width: 6px; height: 6px; background: #7e5bef; border-radius: 50%; animation: bounce 0.6s infinite alternate 0.4s;"></div>'
                f'</div></div>'
                f'<style>@keyframes bounce {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-3px); }} }}</style>',
                unsafe_allow_html=True
            )
            time.sleep(0.15)
        
        container.empty()
        return total_time

    @staticmethod
    def age_verification():
        st.markdown('<div class="age-verification"><div class="age-header"><div class="age-icon">🔞</div><h1 class="age-title">ENTRE APENAS SE FOR ADULTO!</h1></div><div class="age-content"><p>Este portal é reservado <strong>apenas para maiores de 18 anos.</strong></p><p>Ao clicar abaixo, você declara que possui a idade mínima exigida.</p></div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Sim, tenho mais de 18 anos e QUERO ENTRAR! 💖", key="age_confirm_button", use_container_width=True, type="primary"):
                st.session_state.age_verified = True
                save_persistent_data()
                st.rerun()

    @staticmethod
    def setup_sidebar():
        with st.sidebar:
            st.markdown(f'<div class="sidebar-logo-container"><img src="{Config.LOGO_URL}" class="sidebar-logo" alt="Logo"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sidebar-header"><img src="{Config.IMG_PROFILE}" alt="Nicole"><h3 style="color: #7e5bef; margin-top: 15px;">Nicole Saheb Premium VIP</h3><p style="font-size: 0.9em; color: #d0c1ff;">Sua musa particular...</p></div>', unsafe_allow_html=True)
            st.markdown("---")
            menu_options = {"Início Quente": "home", "Minha Galeria Privada": "gallery", "Chat Íntimo": "chat", "Ofertas Exclusivas": "offers"}
            for option, page in menu_options.items():
                if st.button(option, use_container_width=True, key=f"menu_{page}"):
                    if st.session_state.current_page != page:
                        st.session_state.current_page = page
                        save_persistent_data()
                        st.rerun()
            st.markdown("---")
            
            # Indicador de calor na sidebar
            heat_level = st.session_state.get('heat_level', 0)
            heat_color = "#7e5bef" if heat_level < 60 else "#ff6b6b" if heat_level < 80 else "#ff0000"
            
            st.markdown(f"""
            <div style="background: rgba(126, 91, 239, 0.15); padding: 12px; border-radius: 10px; 
                        text-align: center; margin-bottom: 15px; border: 1px solid {heat_color};">
                <p style="margin:0; color: #d0c1ff;">Nível de Conexão:</p>
                <div style="background: linear-gradient(90deg, {heat_color} 0%, {heat_color} {heat_level}%, #333 {heat_level}%, #333 100%); 
                            height: 10px; border-radius: 5px; margin: 8px 0;"></div>
                <p style="margin:0; color: {heat_color}; font-weight: bold; font-size: 1.1em;">
                    {"Conhecendo" if heat_level < 30 else "Flertando" if heat_level < 60 else "Quente" if heat_level < 80 else "FERVENDO!"}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div style="background: rgba(126, 91, 239, 0.15); padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px solid #7e5bef;"><p style="margin:0; color: #d0c1ff;">Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p><progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px;"></progress></div>', unsafe_allow_html=True)
            if st.button("QUERO SER VIP AGORA!", use_container_width=True, type="primary", key="sidebar_cta_button"):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()

    @staticmethod
    def show_gallery_page():
        st.markdown('<h3>MINHA GALERIA É UMA LOUCURA PARA SEUS OLHOS! 😈</h3>', unsafe_allow_html=True)
        st.markdown('<p>Apenas um vislumbre do que te espera... o acesso completo está te chamando.</p>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f'<div style="position: relative; border-radius: 15px; overflow: hidden;"><img src="{Config.IMG_GALLERY[idx]}" style="width:100%; filter: blur(8px) brightness(0.6);"><div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; font-size: 1.6em; text-shadow: 0 0 12px #000;">🔥 VIP Bloqueado 🔥</div></div>', unsafe_allow_html=True)
        if st.button("Acessar Minha Galeria Secreta. 🔓", key="vip_button_gallery", use_container_width=True, type="primary"):
            st.session_state.current_page = "offers"
            st.rerun()

    @staticmethod
    def enhanced_chat_ui(conn):
        st.markdown('<h2 style="text-align: center; color: #7e5bef;">Chat Exclusivo com Nicole 💖</h2>', unsafe_allow_html=True)
        ChatService.process_user_input(conn)
        save_persistent_data()

# ======================
# PÁGINAS DA APLICAÇÃO
# ======================
class NewPages:
    @staticmethod
    def show_home_page():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a0a2e, #2d1b4e); padding: 60px 20px; text-align: center; border-radius: 20px; color: white; margin-bottom: 40px; border: 3px solid #ff6b6b;">
            <h1 style="color: #7e5bef; font-size: 3.5em;">Nicole Saheb 💖</h1>
            <p style="font-size: 1.4em;">Descubra o prazer de um bom conteúdo quente, exclusivo e sem censura.</p>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(3)
        for col, img in zip(cols, Config.IMG_HOME_PREVIEWS):
            with col:
                st.image(img, use_container_width=True, caption="Ainda Bloqueado... 😉")
        if st.button("Conversar com Nicole 💋", use_container_width=True, type="primary", key="home_chat_button"):
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

    @staticmethod
    def show_offers_page():
        # Adicionar mensagem personalizada baseada no heat level
        heat_level = st.session_state.get('heat_level', 0)
        
        if heat_level < 60:
            offer_msg = "Parece que estamos nos conhecendo ainda... que tal dar uma olhada no que te espera?"
        elif heat_level < 80:
            offer_msg = "Nossa conversa está esquentando... imagina o que você vai ver no VIP!"
        else:
            offer_msg = "Você me deixou com MUITO tesão... escolha seu pacote e vamos continuar isso no VIP! 😈💦"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(126, 91, 239, 0.15); 
                    border-radius: 15px; margin-bottom: 30px; border: 2px solid #ff6b6b;">
            <h2 style="color: #7e5bef;">Acesse e não se arrependerá! 😈</h2>
            <p>{offer_msg}</p>
            <p>Qual é o tamanho do seu pacote?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pacotes
        cols = st.columns(3)
        packages = [
            {"name": "START 🔥", "price": "R$ 9,90", "color": "#ff6b6b", "link": Config.CHECKOUT_START, "features": ["10 Fotos Provocantes", "3 Vídeos Íntimos"]},
            {"name": "PREMIUM 💜", "price": "R$ 39,90", "color": "#9d4edd", "link": Config.CHECKOUT_PREMIUM, "features": ["20 Fotos EXCLUSIVAS", "5 Vídeos Premium", "Conteúdo Bônus"]},
            {"name": "EXTREME 😈", "price": "R$ 69,00", "color": "#ff0000", "link": Config.CHECKOUT_EXTREME, "features": ["30 Fotos ULTRA", "10 Vídeos Exclusivos", "Acesso Antecipado"]}
        ]

        for i, col in enumerate(cols):
            with col:
                pkg = packages[i]
                st.markdown(f"""
                <div style="border: 2px solid {pkg['color']}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px; background: rgba(26, 10, 46, 0.7);">
                    <div style="margin-bottom: 15px;">
                        <h3 style="color: {pkg['color']}; margin: 0;">{pkg['name']}</h3>
                        <div style="font-size: 1.8em; font-weight: bold; color: {pkg['color']};">{pkg['price']}</div>
                    </div>
                    <ul style="text-align: left; padding-left: 20px; margin-bottom: 20px;">
                        {''.join([f'<li>✔ {feat}</li>' for feat in pkg['features']])}
                    </ul>
                    <a href="{pkg['link']}" target="_blank" style="display:block; background: {pkg['color']}; color: white; text-align: center; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 20px;">EU QUERO!</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Countdown
        st.markdown("""
        <div style="border: 2px solid #ffb347; border-radius: 10px; padding: 15px; text-align: center; margin: 20px 0;">
            <h4 style="color: #ffb347; margin: 0;">🚨 OFERTA RELÂMPAGO! 🚨</h4>
            <p style="margin: 5px 0 10px;">Quem comprar o pacote extreme hoje ganha:</p>
            <ul style="text-align: left; margin-bottom: 15px;">
                <li>Video pessoal exclusivo</li>
                <li>Chamada de 5 minutos comigo</li>
            </ul>
            <div id="countdown" style="font-size: 1.5em; font-weight: bold; color: #ffb347;">23:59:59</div>
        </div>
        """, unsafe_allow_html=True)
        st.components.v1.html("""
        <script>
        function updateCountdown() {
            const el = parent.document.getElementById('countdown');
            if (!el) return;
            let time = el.textContent.split(':');
            let s = parseInt(time[2]) - 1;
            let m = parseInt(time[1]);
            let h = parseInt(time[0]);
            if (s < 0) { s = 59; m--; }
            if (m < 0) { m = 59; h--; }
            if (h < 0) { h = 23; }
            el.textContent = `${h.toString().padStart(2,'0')}:${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
            setTimeout(updateCountdown, 1000);
        }
        if (!window.countdownStarted) {
            window.countdownStarted = true;
            setTimeout(updateCountdown, 1000);
        }
        </script>
        """, height=0)

# ======================
# SERVIÇOS DE CHAT (COM TEMPOS NATURAIS)
# ======================
class ChatService:
    @staticmethod
    def initialize_session(conn):
        load_persistent_data()
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(random.randint(100000, 999999))
        if "messages" not in st.session_state:
            st.session_state.messages = DatabaseService.load_messages(conn, get_user_id(), st.session_state.session_id)
        if "request_count" not in st.session_state:
            st.session_state.request_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        defaults = {
            'age_verified': False, 
            'connection_complete': False, 
            'chat_started': False, 
            'audio_sent': False, 
            'current_page': 'home', 
            'last_cta_time': 0, 
            'last_error_time': 0,
            'heat_level': 0
        }
        for key, default in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default

    @staticmethod
    def format_conversation_history(messages, max_messages=10):
        formatted = []
        for msg in messages[-max_messages:]:
            role = "Cliente" if msg["role"] == "user" else "Nicole"
            content = msg["content"]
            if content == "[ÁUDIO]":
                content = "[Enviou um áudio sensual]"
            elif content.startswith('{"text"'):
                try:
                    content = json.loads(content).get("text", content)
                except:
                    pass
            formatted.append(f"{role}: {content}")
        
        # Adiciona um resumo contextual se a conversa for longa
        if len(formatted) > 5:
            return "\n".join([
                "(Resumo: Conversa flertuosa e descontraída)",
                *formatted[-5:]
            ])
        return "\n".join(formatted)

    @staticmethod
    def display_chat_history():
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(msg["content"])
            elif msg["content"] == "[ÁUDIO]":
                with st.chat_message("assistant", avatar="💋"):
                    st.markdown(UiService.get_chat_audio_player(), unsafe_allow_html=True)
            else:
                try:
                    content_data = json.loads(msg["content"])
                    with st.chat_message("assistant", avatar="💋"):
                        st.markdown(content_data.get("text", ""))
                        if content_data.get("cta", {}).get("show", False):
                            button_key = f"cta_button_{idx}"
                            if st.button(content_data["cta"]["label"], key=button_key, use_container_width=True):
                                st.session_state.current_page = content_data["cta"]["target"]
                                save_persistent_data()
                                st.rerun()
                except (json.JSONDecodeError, TypeError):
                    with st.chat_message("assistant", avatar="💋"):
                        st.markdown(msg["content"])

    @staticmethod
    def validate_input(user_input):
        return re.sub(r'<[^>]*>', '', user_input)[:500]

    @staticmethod
    def simulate_human_response_time(response_length: int) -> float:
        """Calcula um tempo de resposta natural baseado no comprimento da resposta"""
        words = response_length / 5
        base_time = words * 0.5
        
        min_time = 1.5
        max_time = 7.0
        
        response_time = base_time * random.uniform(0.7, 1.3)
        
        return max(min_time, min(response_time, max_time))

    @staticmethod
    def process_user_input(conn):
        ChatService.display_chat_history()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            UiService.show_viewed_status()

        if not st.session_state.get("audio_sent") and st.session_state.chat_started:
            time.sleep(random.uniform(1.5, 2.5))
            st.session_state.messages.append({"role": "assistant", "content": "[ÁUDIO]"})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", "[ÁUDIO]")
            st.session_state.audio_sent = True
            save_persistent_data()
            st.rerun()

        user_input = st.chat_input("Me diga o que você deseja, amor... 😉", key="chat_input_main")
        
        if user_input:
            cleaned_input = ChatService.validate_input(user_input)
            st.session_state.messages.append({"role": "user", "content": cleaned_input})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "user", cleaned_input)
            st.session_state.request_count += 1
            save_persistent_data()
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            if st.session_state.request_count > Config.MAX_REQUESTS_PER_SESSION:
                time.sleep(random.uniform(2.0, 3.0))
                final_offer_message = {
                    "text": "Parece que você está gostando da nossa conversa... que tal continuar isso no VIP? Tenho muito mais para te mostrar lá 😉",
                    "cta": {"show": True, "label": "QUERO SER VIP! 💖", "target": "offers"}
                }
                st.session_state.messages.append({"role": "assistant", "content": json.dumps(final_offer_message)})
                DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", json.dumps(final_offer_message))
                save_persistent_data()
                st.rerun()
                return

            user_msg = st.session_state.messages[-1]["content"]
            
            # Mostrar status "digitando..." com tempo variável
            typing_time = UiService.show_typing_status()
            
            # Tempo adicional de "pensamento" baseado no contexto
            extra_thinking_time = random.uniform(0.5, 1.5)
            time.sleep(extra_thinking_time)
            
            # Aumentar variação de tempo de resposta
            response_delay = random.uniform(1.5, 4.0)
            
            # Adicionar variação baseada no heat level
            if st.session_state.get('heat_level', 0) > 60:
                response_delay *= 0.7
            else:
                response_delay *= 1.3
            
            time.sleep(response_delay)
            
            # Se for a primeira mensagem do usuário
            if len([m for m in st.session_state.messages if m["role"] == "user"]) == 1:
                resposta_ia = {"text": NaturalResponses.get_greeting_response(), "cta": {"show": False}}
                time.sleep(random.uniform(1.0, 1.8))
                
            # Se o nível de calor ainda estiver baixo
            elif st.session_state.get('heat_level', 0) < 30:
                resposta_ia = {"text": NaturalResponses.get_low_heat_response(), "cta": {"show": False}}
                time.sleep(random.uniform(1.8, 2.5))
                
            # Se o nível de calor justificar um CTA
            elif HeatLevelSystem.should_show_cta():
                resposta_ia = CTAEngine.generate_strong_cta_response(user_msg)
                resposta_ia["text"] += " " + NaturalResponses.get_follow_up_response()
                time.sleep(random.uniform(1.0, 1.8))
                
            # Processamento normal
            else:
                resposta_ia = ApiService.ask_gemini(user_msg, st.session_state.session_id, conn)
                response_time = ChatService.simulate_human_response_time(len(resposta_ia["text"]))
                time.sleep(response_time)
                
            st.session_state.messages.append({"role": "assistant", "content": json.dumps(resposta_ia)})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", json.dumps(resposta_ia))
            save_persistent_data()
            st.rerun()

# ======================
# APLICAÇÃO PRINCIPAL
# ======================
def main():
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = DatabaseService.init_db()
    conn = st.session_state.db_conn
    
    ChatService.initialize_session(conn)
    
    if not st.session_state.age_verified:
        UiService.age_verification()
        st.stop()
        
    UiService.setup_sidebar()
    
    if not st.session_state.connection_complete:
        UiService.show_call_effect()
        st.session_state.connection_complete = True
        save_persistent_data()
        st.rerun()
        
    if not st.session_state.chat_started and st.session_state.current_page == 'chat':
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'<div style="text-align: center; margin: 50px 0;"><img src="{Config.IMG_PROFILE}" width="150" style="border-radius: 50%; border: 5px solid #ff6b6b;"><h2 style="color: #7e5bef;">Pronto para se perder comigo, amor? 😉</h2></div>', unsafe_allow_html=True)
            if st.button("CONVERSAR COM NICOLE AGORA! 🔥", type="primary", use_container_width=True, key="start_chat_button"):
                st.session_state.update({'chat_started': True, 'current_page': 'chat', 'audio_sent': False})
                save_persistent_data()
                st.rerun()
        st.stop()

    page_map = {
        "home": NewPages.show_home_page,
        "gallery": UiService.show_gallery_page,
        "offers": NewPages.show_offers_page,
        "chat": UiService.enhanced_chat_ui,
    }

    # Para a página de chat, precisamos passar a conexão com o banco de dados
    if st.session_state.current_page == "chat":
        UiService.enhanced_chat_ui(conn)
    else:
        # Para outras páginas, chame a função sem argumentos
        page_function = page_map.get(st.session_state.current_page, NewPages.show_home_page)
        page_function()

    save_persistent_data()

if __name__ == "__main__":
    main()
