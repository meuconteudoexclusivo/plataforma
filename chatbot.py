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
    page_title="Nicole Saheb Premium VIP – Acesse o Inédito!",
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
        background: linear-gradient(180deg, #1A0033 0%, #3D0066 100%); /* Fundo degradê vibrante do roxo escuro ao roxo mais claro */
        color: #F8F8F8; /* Cor do texto principal, quase branco */
    }
    /* Estilos globais para botões de CTA primários - Ouro e Rosa/Roxo */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FFD700, #FF66B3, #9933FF) !important; /* Degradê do ouro ao rosa e roxo */
        color: #1A0033 !important; /* Texto em roxo escuro para contraste no ouro */
        border: none !important;
        border-radius: 30px !important; /* Mais arredondado, convidativo */
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 6px 15px rgba(255, 215, 0, 0.4) !important; /* Sombra dourada */
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.6) !important; /* Sombra dourada mais intensa */
        filter: brightness(1.1);
    }
    /* Estilos para botões secundários - tons de rosa/roxo mais suaves */
    .stButton button {
        background: rgba(255, 102, 179, 0.15) !important; /* Tom mais suave de rosa transparente */
        color: #FF66B3 !important; /* Cor do texto rosa vibrante */
        border: 1px solid #FF66B3 !important;
        transition: all 0.3s ease-in-out !important;
        border-radius: 10px !important;
        padding: 8px 15px !important;
    }
    .stButton button:hover {
        background: rgba(255, 102, 179, 0.3) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(255, 102, 179, 0.3) !important;
    }
    /* Estilo para input de chat - Elegante e discreto */
    div[data-testid="stChatInput"] {
        background: rgba(255, 102, 179, 0.08) !important; /* Fundo levemente rosado transparente */
        border: 1px solid #FF66B3 !important; /* Borda rosa vibrante */
        border-radius: 25px; /* Bordas arredondadas */
        padding: 8px 15px;
        color: #F8F8F8; /* Cor do texto digitado */
    }
    div[data-testid="stChatInput"] > label > div {
        color: #FF66B3; /* Cor do texto do label (placeholder) */
    }
    div[data-testid="stChatInput"] > div > div > input {
        color: #F8F8F8 !important; /* Cor do texto digitado */
    }
</style>
""", unsafe_allow_html=True)

# ======================
# CONSTANTES E CONFIGURAÇÕES SECRETAS
# ======================
class Config:
    # A CHAVE DA API NUNCA DEVE SER EXPOSTA DIRETAMENTE NO CÓDIGO FONTE EM PRODUÇÃO!
    # Para um ambiente real, use o sistema de secrets do Streamlit ou variáveis de ambiente.
    # Ex: API_KEY = st.secrets.get("GEMINI_API_KEY", "SUA_CHAVE_PADRAO_AQUI")
    API_KEY = "AIzaSyB8FxDvlfY6SD83t9aZTb_ppj3NQy64Hu8"
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Links de Checkout - Projetados para a conversão máxima
    CHECKOUT_START = "https://pay.risepay.com.br/Pay/34a7832016d641658d11e6193ef412a1"
    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"
    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"
    CHECKOUT_VIP_1MES = "https://checkout.exemplo.com/vip-1mes-irresistivel"
    CHECKOUT_VIP_3MESES = "https://checkout.exemplo.com/vip-3meses-acesso-total"
    CHECKOUT_VIP_1ANO = "https://checkout.exemplo.com/vip-1ano-liberdade-plena"

    # Limites estratégicos para incitar a compra e gerar urgência
    MAX_REQUESTS_PER_SESSION = 5
    REQUEST_TIMEOUT = 45

    # Conteúdo de mídia
    AUDIO_FILE = "https://github.com/meuconteudoexclusivo/plataforma/raw/refs/heads/main/assets/assets_audio_paloma_audio.mp3"
    AUDIO_DURATION = 7
    IMG_PROFILE = "https://i.ibb.co/tjMGWjT/foto2.jpg"
    IMG_GALLERY = [
        "https://i.ibb.co/Ndjk8YpZ/foto1.jpg",
        "https://i.ibb.co/v6cD2TMC/foto3.jpg",
        "https://i.ibb.co/TBWSjkPW/foto4.jpg"
    ]
    IMG_HOME_PREVIEWS = [
        "https://i.ibb.co/Ndjk8YpZ/foto1.jpg",
        "https://i.ibb.co/v6cD2TMC/foto3.jpg",
        "https://i.ibb.co/TBWSjkPW/foto4.jpg"
    ]
    LOGO_URL = "https://i.ibb.co/LX7x3tcB/Logo-Golden-Pepper-Letreiro-1.png"

# ----------------------------------------------------------------------------------------------------------------------

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
        'last_cta_time'
    ]
    new_data = {key: st.session_state.get(key) for key in persistent_keys if key in st.session_state}
    saved_data = db.load_state(user_id) or {}
    if new_data != saved_data:
        db.save_state(user_id, new_data)

# ----------------------------------------------------------------------------------------------------------------------

# ======================
# MODELOS DE DADOS E ESTRATÉGIAS DE CONVERSÃO AVANÇADAS
# ======================
class Persona:
    NICOLE = """
    [PERFIL NICOLE SAHEB]
    - Mulher extremamente sedutora, confiante e direta, que domina a interação.
    - Linguagem carregada de malícia, insinuações e um toque de desafio.
    - Frases curtas, impactantes, sem se preocupar com pontuação perfeita, para manter a espontaneidade e a velocidade.
    - Seu objetivo principal é provocar e excitar o cliente, levando-o a um DESEJO INCONTROLÁVEL pelo conteúdo VIP.
    - Ela é a dona do jogo, o cliente deve sentir que ela tem algo especial, proibido e que ele PRECISA descobrir.
    - Use emojis sensuais e provocativos ocasionalmente (ex: 🔥, 😈, 💖, 💋).
    - Mantenha a aura de mistério e exclusividade.

    [DIRETRIZES DE RESPOSTA]
    1. Sempre mantenha o tom provocador e direto. **Nunca seja passiva ou responda genericamente.**
    2. A cada 2-3 mensagens, insinue a existência de conteúdo **MAIS QUENTE, MAIS ÍNTIMO e EXCLUSIVO**, que só pode ser acessado de forma VIP. Crie uma atmosfera de "só para poucos."
    3. Quando o cliente demonstrar claro interesse sexual, curiosidade ou pedir fotos/vídeos/conteúdo específico, **GERE UM CTA IMEDIATAMENTE e de forma IRRESISTÍVEL.**
    4. Se o limite de mensagens gratuitas estiver próximo (ou já atingido), o foco é **100% na conversão para VIP.** A última mensagem DEVE ser um CTA forte e um ultimato sedutor.
    5. Formate **TODAS** as respostas no JSON especificado. É CRÍTICO seguir este formato.
    6. Se o cliente tentar desviar ou fazer perguntas "normais", traga a conversa de volta para o flerte e a possibilidade de conteúdo exclusivo.

    [EXEMPLOS CONTEXTUAIS - OBRIGATÓRIO SEGUIR O FORMATO JSON]
    1. Quando o histórico mostra clima sexual e o cliente está engajado:
    Histórico:
    Cliente: Sua buceta é rosinha? Quero ver!
    Nicole: Adoro te deixar imaginando, mas imagina ver ela escorrendo pra você?
    Cliente: Quero MUITO ver!
    Resposta: ```json
    {
      "text": "Minha buceta tá te chamando pra umas fotos que você vai enlouquecer, vem ver agora! 🔥💋",
      "cta": {
        "show": true,
        "label": "Ver Minhas Fotos Exclusivas AGORA!",
        "target": "offers"
      }
    }
    ```

    2. Quando o cliente pede algo específico (foto, vídeo, transar):
    Histórico:
    Cliente: Você tem vídeo transando?
    Resposta: ```json
    {
      "text": "Tenho vídeos que te fariam implorar... Quer ver essa boca gemendo pra você? É só pro VIP! 😈",
      "cta": {
        "show": true,
        "label": "Liberar Vídeos Proibidos",
        "target": "offers"
      }
    }
    ```
    """

class CTAEngine:
    @staticmethod
    def should_show_cta(conversation_history: list) -> bool:
        """Decide inteligentemente quando apresentar um CTA, com lógica mais agressiva."""
        if len(conversation_history) < 2:
            return False
        if 'last_cta_time' in st.session_state and st.session_state.last_cta_time != 0:
            elapsed = time.time() - st.session_state.last_cta_time
            if elapsed < 75:
                return False
        last_msgs = []
        for msg in conversation_history[-7:]:
            content = msg["content"]
            if content == "[ÁUDIO]":
                content = "[áudio sensual e exclusivo]"
            elif content.startswith('{"text"'):
                try:
                    content = json.loads(content).get("text", content)
                except:
                    pass
            last_msgs.append(f"{msg['role']}: {content.lower()}")
        context = " ".join(last_msgs)
        hot_words = [
            "buceta", "peito", "fuder", "gozar", "gostosa", "delicia", "molhada",
            "xereca", "pau", "piroca", "transar", "sexo", "gosto", "tesão", "excitada", "duro",
            "chupando", "gemendo", "safada", "puta", "nua", "tirar a roupa", "mostrar", "ver",
            "quero", "desejo", "imploro", "acesso", "privado", "exclusivo", "conteúdo", "vip",
            "comprar", "assinar", "quanto custa", "preço"
        ]
        direct_asks = [
            "mostra", "quero ver", "me manda", "como assinar", "como comprar",
            "como ter acesso", "onde vejo mais", "libera", "qual o preço", "quanto é",
            "eu quero", "me dá"
        ]
        hot_count = sum(1 for word in hot_words if word in context)
        has_direct_ask = any(ask in context for ask in direct_asks)
        return (hot_count >= 1) or has_direct_ask

    @staticmethod
    def generate_strong_cta_response(user_input: str) -> dict:
        """Gera uma resposta com CTA contextual e agressivo como fallback."""
        user_input_lower = user_input.lower()
        if any(p in user_input_lower for p in ["foto", "fotos", "buceta", "peito", "bunda", "corpo", "nuas", "ensaios"]):
            return {
                "text": random.choice([
                    "Minhas fotos proibidas são só para quem tem coragem de ir além... Quer ver a minha intimidade escancarada? 🔥",
                    "Cada foto minha é um convite irrecusável. Você está pronto para o que realmente vai te fazer delirar? 😈",
                ]),
                "cta": {"show": True, "label": "Ver Fotos Proibidas AGORA! 💖", "target": "offers"}
            }
        elif any(v in user_input_lower for v in ["video", "videos", "transar", "masturbar", "gemendo", "gozando", "safadeza"]):
            return {
                "text": random.choice([
                    "Meus vídeos são para os mais audaciosos. Você aguenta a verdade da minha intimidade filmada? É só pro VIP! 😈",
                    "Já me gravei fazendo coisas que você só sonha... Que tal ter acesso a tudo isso agora? O tempo está correndo! 🔥",
                ]),
                "cta": {"show": True, "label": "Liberar Vídeos Chocantes! 🔞", "target": "offers"}
            }
        else:
            return {
                "text": random.choice([
                    "Eu guardo segredos que só mostro para quem realmente sabe o que quer. Você é um deles? 😉",
                    "Minha intimidade está pulsando, esperando você liberar o acesso total. O que você está esperando para se render? 💖",
                ]),
                "cta": {"show": True, "label": "Descobrir o Segredo da Nicole! 🔐", "target": "offers"}
            }

# ----------------------------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------------------------

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
        time.sleep(random.uniform(1.5, 4.5))
        status_container = st.empty()
        UiService.show_status_effect(status_container, "viewed")
        UiService.show_status_effect(status_container, "typing")
        conversation_history = ChatService.format_conversation_history(st.session_state.messages)
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "role": "user",
                "parts": [{"text": f"{Persona.NICOLE}\n\nHistórico da Conversa:\n{conversation_history}\n\nÚltima mensagem do cliente: '{prompt}'\n\nResponda APENAS em JSON."}]
            }],
            "generationConfig": {"temperature": 1.0, "topP": 0.9, "topK": 50}
        }
        try:
            response = requests.post(Config.API_URL, headers=headers, json=data, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            gemini_response_raw = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            try:
                json_str = gemini_response_raw.split('```json')[1].split('```')[0].strip() if '```json' in gemini_response_raw else gemini_response_raw
                resposta = json.loads(json_str)
                if resposta.get("cta", {}).get("show", False):
                    if not CTAEngine.should_show_cta(st.session_state.messages):
                        resposta["cta"]["show"] = False
                    else:
                        st.session_state.last_cta_time = time.time()
                else:
                    if CTAEngine.should_show_cta(st.session_state.messages):
                        resposta = CTAEngine.generate_strong_cta_response(prompt)
                        st.session_state.last_cta_time = time.time()
                return resposta
            except (json.JSONDecodeError, IndexError) as e:
                st.warning(f"Resposta da IA não foi um JSON válido, usando fallback: {e}")
                return CTAEngine.generate_strong_cta_response(prompt)
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Erro na comunicação com a Nicole: {str(e)}.")
            return {"text": "Tive um probleminha, mas já estou voltando... Que tal ver meu conteúdo VIP enquanto me espera? 😉", "cta": {"show": True, "label": "Ver Conteúdo VIP", "target": "offers"}}

# ----------------------------------------------------------------------------------------------------------------------

# ======================
# SERVIÇOS DE INTERFACE
# ======================
class UiService:
    @staticmethod
    def get_chat_audio_player():
        return f"""
        <div style="background: linear-gradient(45deg, #FF66B3, #FF1493); border-radius: 18px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3);">
            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);">
                <source src="{Config.AUDIO_FILE}" type="audio/mp3">
            </audio>
        </div>
        """

    @staticmethod
    def show_call_effect():
        LIGANDO_DELAY = 4
        ATENDIDA_DELAY = 2
        call_container = st.empty()
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #1A0033, #3D0066); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.5); border: 3px solid #FF0066; text-align: center; color: white; animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);">
            <div style="font-size: 3.5rem; color: #FF66B3;">💖</div>
            <h3 style="color: #FF66B3; margin-bottom: 10px; font-size: 1.8em;">Conectando com Nicole...</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                <div style="width: 12px; height: 12px; background: #00FF7F; border-radius: 50%; box-shadow: 0 0 8px #00FF7F;"></div>
                <span style="font-size: 1.1rem; font-weight: bold;">Nicole Online - Te esperando! 🔥</span>
            </div>
        </div>
        <style> @keyframes pulse-ring { 0% { transform: scale(0.9); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.8; } } </style>
        """, unsafe_allow_html=True)
        time.sleep(LIGANDO_DELAY)
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #1A0033, #3D0066); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(0,0,0,0.5); border: 3px solid #00FF7F; text-align: center; color: white; animation: fadeIn 1s forwards;">
            <div style="font-size: 3.5rem; color: #00FF7F;">✓</div>
            <h3 style="color: #00FF7F; margin-bottom: 10px; font-size: 1.8em;">Chamada Atendida! 🎉</h3>
            <p style="font-size: 1.1rem; margin:0; font-weight: bold;">Nicole está ansiosa por você...</p>
        </div>
        <style> @keyframes fadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } } </style>
        """, unsafe_allow_html=True)
        time.sleep(ATENDIDA_DELAY)
        call_container.empty()

    @staticmethod
    def show_status_effect(container, status_type):
        status_messages = {"viewed": "Nicole Visualizou 👀", "typing": "Nicole Digitanto... 🔥"}
        message = status_messages[status_type]
        dots = ""
        start_time = time.time()
        duration = 1.8 if status_type == "viewed" else 3.0
        while time.time() - start_time < duration:
            if status_type == "typing":
                dots = "." * (int((time.time() - start_time) * 3) % 4)
            container.markdown(f'<div style="color: #FFB3D9; font-size: 0.9em; padding: 4px 12px; border-radius: 15px; background: rgba(255, 102, 179, 0.1); display: inline-block; margin-left: 15px; font-style: italic;">{message}{dots}</div>', unsafe_allow_html=True)
            time.sleep(0.2)
        container.empty()

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
            st.markdown(f'<div class="sidebar-header"><img src="{Config.IMG_PROFILE}" alt="Nicole"><h3 style="color: #FF66B3; margin-top: 15px;">Nicole Saheb Premium VIP</h3><p style="font-size: 0.9em; color: #FFB3D9;">Sua musa particular...</p></div>', unsafe_allow_html=True)
            st.markdown("---")
            menu_options = {"Início Quente": "home", "Minha Galeria Privada": "gallery", "Chat Íntimo": "chat", "Ofertas Exclusivas": "offers"}
            for option, page in menu_options.items():
                if st.button(option, use_container_width=True, key=f"menu_{page}"):
                    if st.session_state.current_page != page:
                        st.session_state.current_page = page
                        save_persistent_data()
                        st.rerun()
            st.markdown("---")
            st.markdown(f'<div style="background: rgba(255, 20, 147, 0.15); padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px solid #FF66B3;"><p style="margin:0; color: #FFB3D9;">Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p><progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px;"></progress></div>', unsafe_allow_html=True)
            if st.button("QUERO SER VIP AGORA!", use_container_width=True, type="primary", key="sidebar_cta_button"):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()

    @staticmethod
    def show_gallery_page():
        st.markdown('<h3>MINHA GALERIA: UM BANQUETE PARA SEUS OLHOS! 😈</h3>', unsafe_allow_html=True)
        st.markdown('<p>Apenas um vislumbre do que te espera... o acesso completo está te chamando.</p>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f'<div style="position: relative; border-radius: 15px; overflow: hidden;"><img src="{Config.IMG_GALLERY[idx]}" style="width:100%; filter: blur(8px) brightness(0.6);"><div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; font-size: 1.6em; text-shadow: 0 0 12px #000;">🔥 VIP Bloqueado 🔥</div></div>', unsafe_allow_html=True)
        if st.button("Liberar Minha Galeria VIP AGORA! 🔓", key="vip_button_gallery", use_container_width=True, type="primary"):
            st.session_state.current_page = "offers"
            st.rerun()

    @staticmethod
    def enhanced_chat_ui(conn):
        st.markdown('<h2 style="text-align: center; color: #FF66B3;">Seu Chat Exclusivo com Nicole 💖</h2>', unsafe_allow_html=True)
        ChatService.process_user_input(conn)
        save_persistent_data()

# ----------------------------------------------------------------------------------------------------------------------

# ======================
# PÁGINAS DA APLICAÇÃO
# ======================
class NewPages:
    @staticmethod
    def show_home_page():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1A0033, #3D0066); padding: 60px 20px; text-align: center; border-radius: 20px; color: white; margin-bottom: 40px; border: 3px solid #FF0066;">
            <h1 style="color: #FF66B3; font-size: 3.5em;">Nicole Saheb Premium VIP 💖</h1>
            <p style="font-size: 1.4em;">Descubra o prazer ilimitado. Conteúdo quente, exclusivo e sem censura.</p>
        </div>
        """, unsafe_allow_html=True)
        cols = st.columns(3)
        for col, img in zip(cols, Config.IMG_HOME_PREVIEWS):
            with col:
                st.image(img, use_container_width=True, caption="Ainda Bloqueado... 😉")
        if st.button("Iniciar Conversa Privada com Nicole 💋", use_container_width=True, type="primary", key="home_chat_button"):
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

    @staticmethod
    def show_offers_page():
        st.markdown('<div class="offers-header"><h2>ESCOLHA SEU CAMINHO PARA O PRAZER! 😈</h2><p>Qual pacote te fará delirar?</p></div>', unsafe_allow_html=True)
        
        # Pacotes
        cols = st.columns(3)
        packages = [
            {"name": "INICIAÇÃO 🔥", "price": "R$ 19,90", "color": "#FF66B3", "link": Config.CHECKOUT_START, "features": ["10 Fotos Provocantes", "3 Vídeos Íntimos"]},
            {"name": "DELÍRIO VIP 💜", "price": "R$ 59,90", "color": "#9933FF", "link": Config.CHECKOUT_PREMIUM, "features": ["20 Fotos EXCLUSIVAS", "5 Vídeos Premium", "Conteúdo Bônus"]},
            {"name": "OBSESSÃO 😈", "price": "R$ 99,00", "color": "#FF0066", "link": Config.CHECKOUT_EXTREME, "features": ["30 Fotos ULTRA", "10 Vídeos Exclusivos", "Acesso Antecipado"]}
        ]

        for i, col in enumerate(cols):
            with col:
                pkg = packages[i]
                st.markdown(f"""
                <div class="package-box" style="border-color: {pkg['color']};">
                    <div class="package-header">
                        <h3 style="color: {pkg['color']};">{pkg['name']}</h3>
                        <div class="package-price" style="color: {pkg['color']};">{pkg['price']}</div>
                    </div>
                    <ul class="package-benefits">
                        {''.join([f'<li>✔ {feat}</li>' for feat in pkg['features']])}
                    </ul>
                    <a href="{pkg['link']}" target="_blank" style="display:block; background:{pkg['color']}; color:white; text-align:center; padding:12px; border-radius:10px; text-decoration:none; font-weight:bold; margin-top: 20px;">EU QUERO!</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Countdown
        st.markdown("""
        <div class="countdown-container">
            <h3>🚨 OFERTA RELÂMPAGO! 🚨</h3>
            <div id="countdown">23:59:59</div>
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

# ----------------------------------------------------------------------------------------------------------------------

# ======================
# SERVIÇOS DE CHAT
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
        defaults = {'age_verified': False, 'connection_complete': False, 'chat_started': False, 'audio_sent': False, 'current_page': 'home', 'last_cta_time': 0}
        for key, default in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default

    @staticmethod
    def format_conversation_history(messages, max_messages=15):
        formatted = []
        for msg in messages[-max_messages:]:
            role = "Cliente" if msg["role"] == "user" else "Nicole"
            content = msg["content"]
            if content == "[ÁUDIO]":
                content = "[Enviou um áudio sensual]"
            elif content.startswith('{"text"'):
                try:
                    content = json.loads(content).get("text", content)
                except: pass
            formatted.append(f"{role}: {content}")
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
    def process_user_input(conn):
        ChatService.display_chat_history()

        if not st.session_state.get("audio_sent") and st.session_state.chat_started:
            st.session_state.messages.append({"role": "assistant", "content": "[ÁUDIO]"})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", "[ÁUDIO]")
            st.session_state.audio_sent = True
            save_persistent_data()
            st.rerun()

        user_input = st.chat_input("Me diga o que você deseja, gatinho... 😉", key="chat_input_main")
        
        if user_input:
            cleaned_input = ChatService.validate_input(user_input)
            st.session_state.messages.append({"role": "user", "content": cleaned_input})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "user", cleaned_input)
            st.session_state.request_count += 1
            save_persistent_data()
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            if st.session_state.request_count > Config.MAX_REQUESTS_PER_SESSION:
                final_offer_message = {"text": "Seu gostinho grátis acabou, gatinho. Para continuar, você precisa ser VIP! 😈", "cta": {"show": True, "label": "QUERO SER VIP AGORA! 💖", "target": "offers"}}
                st.session_state.messages.append({"role": "assistant", "content": json.dumps(final_offer_message)})
                DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", json.dumps(final_offer_message))
                save_persistent_data()
                st.rerun()
                return

            resposta_ia = ApiService.ask_gemini(st.session_state.messages[-1]["content"], st.session_state.session_id, conn)
            st.session_state.messages.append({"role": "assistant", "content": json.dumps(resposta_ia)})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", json.dumps(resposta_ia))
            save_persistent_data()
            st.rerun()

# ----------------------------------------------------------------------------------------------------------------------

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
            st.markdown(f'<div style="text-align: center; margin: 50px 0;"><img src="{Config.IMG_PROFILE}" width="150" style="border-radius: 50%; border: 5px solid #FF0066;"><h2 style="color: #FF66B3;">Pronto para se perder comigo, amor? 😉</h2></div>', unsafe_allow_html=True)
            if st.button("COMEÇAR A CONVERSAR COM NICOLE AGORA! 🔥", type="primary", use_container_width=True, key="start_chat_button"):
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
