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
# CONFIGURAÇÃO DE PÁGINA INFANTIL
# ======================
st.set_page_config(
    page_title="Nicole Saheb Premium VIP – Acesso Restrito!",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos com tema infantil
st.markdown("""
<style>
    /* Esconde elementos padrão */
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
    
    /* Tema infantil */
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #FF9EC4 0%, #FFD6E0 100%) !important;
        color: #FF1493 !important;
    }
    
    /* Botões principais */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FFDE7D, #FF9F1C, #FF85A1) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 6px 15px rgba(255, 158, 157, 0.4) !important;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(255, 158, 157, 0.6) !important;
        filter: brightness(1.1);
    }
    
    /* Botões secundários */
    .stButton button {
        background: rgba(255, 182, 193, 0.3) !important;
        color: #FF69B4 !important;
        border: 1px solid #FF69B4 !important;
        transition: all 0.3s ease-in-out !important;
        border-radius: 10px !important;
        padding: 8px 15px !important;
    }
    .stButton button:hover {
        background: rgba(255, 182, 193, 0.5) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(255, 182, 193, 0.3) !important;
    }
    
    /* Input de chat */
    div[data-testid="stChatInput"] {
        background: rgba(255, 215, 230, 0.5) !important;
        border: 1px solid #FF85A1 !important;
        border-radius: 25px;
        padding: 8px 15px;
        color: #FF1493 !important;
    }
    div[data-testid="stChatInput"] > label > div {
        color: #FF69B4 !important;
    }
    div[data-testid="stChatInput"] > div > div > input {
        color: #FF1493 !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# CONSTANTES E CONFIGURAÇÕES
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

    MAX_REQUESTS_PER_SESSION = 5
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

# ======================
# PERSISTÊNCIA DE ESTADO
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
    """Gera ou recupera um ID de usuário único"""
    if 'user_id' not in st.session_state:
        user_id = st.query_params.get('uid', [None])[0]
        if not user_id:
            user_id = str(uuid.uuid4())
            st.query_params['uid'] = user_id
        st.session_state.user_id = user_id
    return st.session_state.user_id

def load_persistent_data():
    """Carrega dados persistentes do usuário"""
    user_id = get_user_id()
    db = PersistentState()
    saved_data = db.load_state(user_id) or {}
    for key, value in saved_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_persistent_data():
    """Salva dados importantes do estado da sessão"""
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

# ======================
# MODELOS DE DADOS
# ======================
class Persona:
    NICOLE = """
    [PERFIL NICOLE SAHEB]
    - Personalidade cativante e interativa
    - Linguagem envolvente e acolhedora
    - Respostas divertidas e curiosas
    - Uso de emojis coloridos (🌈, 🎨, 🧸)
    
    [EXEMPLOS DE RESPOSTAS]
    1. Resposta inicial:
    ```json
    {
      "text": "Olá amiguinho! Que alegria te ver aqui! O que vamos explorar hoje? 🌈",
      "cta": {"show": false}
    }
    ```
    2. Quando elogiam:
    ```json
    {
      "text": "Você é tão gentil! Isso me lembra uma surpresa especial que tenho guardada... 🎁",
      "cta": {"show": false}
    }
    """
    
class CTAEngine:
    @staticmethod
    def should_show_cta(conversation_history: list) -> bool:
        """Decide quando mostrar chamada para ação"""
        if len(conversation_history) < 3:
            return False
            
        last_msgs = " ".join([m["content"].lower() for m in conversation_history[-3:]])
        
        triggers = [
            "quero ver", "como funciona", "mostra mais",
            "surpresa", "especial", "diversão"
        ]
        
        return any(trigger in last_msgs for trigger in triggers)

    @staticmethod
    def generate_strong_cta_response(user_input: str) -> dict:
        """Gera resposta com CTA"""
        return {
            "text": "Tenho um mundo de cores e diversão esperando por você! Quer dar uma espiadinha? 🎨",
            "cta": {
                "show": True,
                "label": "Ver Mundo Colorido 🌈",
                "target": "offers"
            }
        }

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
            st.error(f"Erro ao salvar mensagem: {e}.")

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
        time.sleep(random.uniform(1.0, 2.5))
        status_container = st.empty()
        UiService.show_status_effect(status_container, "viewed")
        UiService.show_status_effect(status_container, "typing")
        
        conversation_history = ChatService.format_conversation_history(st.session_state.messages)
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "role": "user",
                "parts": [{"text": f"{Persona.NICOLE}\n\nHistórico:\n{conversation_history}\n\nÚltima mensagem: '{prompt}'\n\nResponda em JSON."}]
            }],
            "generationConfig": {"temperature": 0.9, "topP": 0.8, "topK": 40}
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
                return CTAEngine.generate_strong_cta_response(prompt)
                
        except requests.exceptions.RequestException as e:
            return {"text": "Estou organizando minhas tintas coloridas... Volto já! 🎨", "cta": {"show": False}}

# ======================
# SERVIÇOS DE INTERFACE
# ======================
class UiService:
    @staticmethod
    def get_chat_audio_player():
        return f"""
        <div style="background: linear-gradient(45deg, #FF85A1, #FF9F1C); border-radius: 18px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 10px rgba(255, 140, 157, 0.3);">
            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);">
                <source src="{Config.AUDIO_FILE}" type="audio/mp3">
            </audio>
        </div>
        """

    @staticmethod
    def show_call_effect():
        call_container = st.empty()
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #FF9EC4, #FFD6E0); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(255, 158, 157, 0.5); border: 3px solid #FF85A1; text-align: center; color: #FF1493; animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);">
            <div style="font-size: 3.5rem; color: #FF9F1C;">🌈</div>
            <h3 style="color: #FF1493; margin-bottom: 10px; font-size: 1.8em;">Conectando...</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                <div style="width: 12px; height: 12px; background: #FFDE7D; border-radius: 50%; box-shadow: 0 0 8px #FFDE7D;"></div>
                <span style="font-size: 1.1rem; font-weight: bold;">Nicole Online - Pronta para diversão!</span>
            </div>
        </div>
        <style> @keyframes pulse-ring { 0% { transform: scale(0.9); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.8; } } </style>
        """, unsafe_allow_html=True)
        time.sleep(2)
        call_container.empty()

    @staticmethod
    def show_status_effect(container, status_type):
        status_messages = {
            "viewed": "Nicole viu 👀", 
            "typing": "Digitando..."
        }
        message = status_messages[status_type]
        dots = ""
        start_time = time.time()
        duration = 1.2 if status_type == "viewed" else 2.5
        
        while time.time() - start_time < duration:
            if status_type == "typing":
                dots = "." * (int((time.time() - start_time) * 3) % 4)
            container.markdown(
                f'<div style="color: #FF69B4; font-size: 0.9em; padding: 4px 12px; border-radius: 15px; background: rgba(255, 182, 193, 0.2); display: inline-block; margin-left: 15px; font-style: italic;">{message}{dots}</div>', 
                unsafe_allow_html=True
            )
            time.sleep(0.2)
        container.empty()

    @staticmethod
    def age_verification():
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 15px; background: rgba(255, 215, 230, 0.7); margin: 20px auto; max-width: 500px;">
            <div style="font-size: 3rem;">🧸</div>
            <h1 style="color: #FF1493;">Bem-vindo ao Mundo Colorido!</h1>
            <p style="color: #FF69B4;">Este é um espaço de diversão e aprendizado.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Quero Entrar no Mundo Colorido! 🌈", key="age_confirm_button", use_container_width=True, type="primary"):
                st.session_state.age_verified = True
                save_persistent_data()
                st.rerun()

    @staticmethod
    def setup_sidebar():
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{Config.LOGO_URL}" style="max-width: 200px; border-radius: 15px;">
                <h3 style="color: #FF1493; margin-top: 10px;">Mundo Colorido</h3>
                <p style="color: #FF69B4;">Sua aventura diária!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            menu_options = {
                "Início": "home",
                "Galeria": "gallery", 
                "Chat": "chat",
                "Atividades": "offers"
            }
            
            for option, page in menu_options.items():
                if st.button(option, use_container_width=True, key=f"menu_{page}"):
                    if st.session_state.current_page != page:
                        st.session_state.current_page = page
                        save_persistent_data()
                        st.rerun()
            
            st.markdown("---")
            
            st.markdown(f"""
            <div style="background: rgba(255, 182, 193, 0.3); padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px solid #FF69B4;">
                <p style="margin:0; color: #FF1493;">Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p>
                <progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px; accent-color: #FF85A1;"></progress>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Ver Atividades Especiais! 🎨", use_container_width=True, type="primary", key="sidebar_cta_button"):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()

    @staticmethod
    def show_gallery_page():
        st.markdown('<h2 style="color: #FF1493;">Minha Galeria Colorida 🎨</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #FF69B4;">Descubra todas as cores que preparamos para você!</p>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div style="position: relative; border-radius: 15px; overflow: hidden; margin-bottom: 15px;">
                    <img src="{Config.IMG_GALLERY[idx]}" style="width:100%; filter: brightness(0.8);">
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; font-size: 1.3em; text-shadow: 0 0 8px #FF1493;">
                        🎨 Descubra Mais 🎨
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("Liberar Galeria Completa! 🔓", key="vip_button_gallery", use_container_width=True, type="primary"):
            st.session_state.current_page = "offers"
            st.rerun()

    @staticmethod
    def enhanced_chat_ui(conn):
        st.markdown('<h2 style="text-align: center; color: #FF1493;">Chat Colorido com Nicole 🌈</h2>', unsafe_allow_html=True)
        ChatService.process_user_input(conn)
        save_persistent_data()

# ======================
# PÁGINAS DA APLICAÇÃO
# ======================
class NewPages:
    @staticmethod
    def show_home_page():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF9EC4, #FFD6E0); padding: 40px 20px; text-align: center; border-radius: 20px; color: #FF1493; margin-bottom: 30px; border: 3px solid #FF85A1;">
            <h1 style="font-size: 2.5em; margin-bottom: 10px;">Bem-vindo ao Mundo Colorido! 🌈</h1>
            <p style="font-size: 1.2em;">Descubra um universo de diversão e criatividade.</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for col, img in zip(cols, Config.IMG_HOME_PREVIEWS):
            with col:
                st.image(img, use_container_width=True, caption="Surpresas esperando por você!")
        
        if st.button("Começar Aventura Colorida 🎨", use_container_width=True, type="primary", key="home_chat_button"):
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

    @staticmethod
    def show_offers_page():
        st.markdown('<h2 style="color: #FF1493;">Atividades Especiais! 🎁</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #FF69B4;">Escolha sua próxima aventura colorida:</p>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        packages = [
            {"name": "Iniciante 🌟", "price": "R$ 9,90", "color": "#FFDE7D", "link": Config.CHECKOUT_START, "features": ["10 Atividades", "3 Surpresas"]},
            {"name": "Intermediário 🎨", "price": "R$ 39,90", "color": "#FF9F1C", "link": Config.CHECKOUT_PREMIUM, "features": ["20 Atividades", "5 Surpresas", "Bônus"]},
            {"name": "Avançado 🌈", "price": "R$ 69,00", "color": "#FF85A1", "link": Config.CHECKOUT_EXTREME, "features": ["30 Atividades", "10 Surpresas", "Acesso Antecipado"]}
        ]

        for i, col in enumerate(cols):
            with col:
                pkg = packages[i]
                st.markdown(f"""
                <div style="border: 2px solid {pkg['color']}; border-radius: 15px; padding: 15px; margin-bottom: 20px; background: rgba(255, 255, 255, 0.7);">
                    <div style="text-align: center;">
                        <h3 style="color: {pkg['color']}; margin-bottom: 5px;">{pkg['name']}</h3>
                        <div style="font-size: 1.5em; font-weight: bold; color: {pkg['color']}; margin-bottom: 15px;">{pkg['price']}</div>
                    </div>
                    <ul style="padding-left: 20px; color: #FF1493;">
                        {''.join([f'<li style="margin-bottom: 8px;">✔️ {feat}</li>' for feat in pkg['features']])}
                    </ul>
                    <a href="{pkg['link']}" target="_blank" style="display: block; text-align: center; background: {pkg['color']}; color: white; padding: 10px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 15px;">
                        Eu Quero!
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(255, 182, 193, 0.3); padding: 15px; border-radius: 15px; text-align: center; margin-top: 20px; border: 1px solid #FF69B4;">
            <h3 style="color: #FF1493;">⏰ Oferta por Tempo Limitado!</h3>
            <div id="countdown" style="font-size: 1.5em; font-weight: bold; color: #FF1493;">24:00:00</div>
        </div>
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
        """, unsafe_allow_html=True)

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
        
        defaults = {
            'age_verified': False,
            'connection_complete': False,
            'chat_started': False,
            'audio_sent': False,
            'current_page': 'home',
            'last_cta_time': 0
        }
        
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
                content = "[áudio divertido]"
            elif content.startswith('{"text"'):
                try:
                    content = json.loads(content).get("text", content)
                except:
                    pass
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)

    @staticmethod
    def display_chat_history():
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧒"):
                    st.markdown(msg["content"])
            elif msg["content"] == "[ÁUDIO]":
                with st.chat_message("assistant", avatar="🌈"):
                    st.markdown(UiService.get_chat_audio_player(), unsafe_allow_html=True)
            else:
                try:
                    content_data = json.loads(msg["content"])
                    with st.chat_message("assistant", avatar="🌈"):
                        st.markdown(content_data.get("text", ""))
                        if content_data.get("cta", {}).get("show", False):
                            button_key = f"cta_button_{idx}"
                            if st.button(content_data["cta"]["label"], key=button_key, use_container_width=True):
                                st.session_state.current_page = content_data["cta"]["target"]
                                save_persistent_data()
                                st.rerun()
                except (json.JSONDecodeError, TypeError):
                    with st.chat_message("assistant", avatar="🌈"):
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

        user_input = st.chat_input("Me diga o que você gostaria de fazer hoje... 🎨", key="chat_input_main")
        
        if user_input:
            cleaned_input = ChatService.validate_input(user_input)
            st.session_state.messages.append({"role": "user", "content": cleaned_input})
            DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "user", cleaned_input)
            st.session_state.request_count += 1
            save_persistent_data()
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            if st.session_state.request_count > Config.MAX_REQUESTS_PER_SESSION:
                final_offer = {
                    "text": "Nossa diversão gratuita acabou por hoje! Quer continuar explorando? 🎁",
                    "cta": {
                        "show": True,
                        "label": "Ver Atividades Especiais! 🌈",
                        "target": "offers"
                    }
                }
                st.session_state.messages.append({"role": "assistant", "content": json.dumps(final_offer)})
                DatabaseService.save_message(conn, get_user_id(), st.session_state.session_id, "assistant", json.dumps(final_offer))
                save_persistent_data()
                st.rerun()
                return

            resposta_ia = ApiService.ask_gemini(st.session_state.messages[-1]["content"], st.session_state.session_id, conn)
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
            st.markdown(f"""
            <div style="text-align: center; margin: 50px 0;">
                <img src="{Config.IMG_PROFILE}" width="150" style="border-radius: 50%; border: 5px solid #FF85A1;">
                <h2 style="color: #FF1493;">Pronto para uma conversa colorida? 🌈</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("COMEÇAR CONVERSA DIVERTIDA! 🎨", type="primary", use_container_width=True, key="start_chat_button"):
                st.session_state.update({
                    'chat_started': True,
                    'current_page': 'chat',
                    'audio_sent': False
                })
                save_persistent_data()
                st.rerun()
        st.stop()

    page_map = {
        "home": NewPages.show_home_page,
        "gallery": UiService.show_gallery_page,
        "offers": NewPages.show_offers_page,
        "chat": UiService.enhanced_chat_ui,
    }

    if st.session_state.current_page == "chat":
        UiService.enhanced_chat_ui(conn)
    else:
        page_function = page_map.get(st.session_state.current_page, NewPages.show_home_page)
        page_function()

    save_persistent_data()

if __name__ == "__main__":
    main()
