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
    page_title="Paloma Premium VIP – Acesse o Inédito!",
    page_icon="💖",  # Ícone mais convidativo
    layout="wide",
    initial_sidebar_state="expanded"
)

# Oculta elementos padrão do Streamlit para uma imersão total
st.markdown("""
<style>
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
        background: linear-gradient(180deg, #1A0033 0%, #3D0066 100%); /* Fundo degradê vibrante */
        color: #F8F8F8; /* Cor do texto principal */
    }
    /* Estilos globais para botões de CTA primários */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF0066, #FF66B3, #9933FF) !important; /* Degradê rosa a roxo */
        color: white !important;
        border: none !important;
        border-radius: 30px !important; /* Mais arredondado */
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 6px 15px rgba(255, 0, 102, 0.4) !important;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(255, 0, 102, 0.6) !important;
        filter: brightness(1.1);
    }
    /* Estilos para botões secundários */
    .stButton button {
        background: rgba(255, 102, 179, 0.15) !important; /* Tom mais suave de rosa */
        color: #FF66B3 !important; /* Cor do texto rosa */
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
    /* Estilo para input de chat */
    div[data-testid="stChatInput"] {
        background: rgba(255, 102, 179, 0.08) !important;
        border: 1px solid #FF66B3 !important;
        border-radius: 25px;
        padding: 8px 15px;
        color: #F8F8F8;
    }
    div[data-testid="stChatInput"] > label > div {
        color: #FF66B3; /* Cor do texto do label */
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
    # A CHAVE DA API NUNCA DEVE SER EXPOSTA NO CÓDIGO FONTE!
    # Em um ambiente de produção, use variáveis de ambiente.
    # Exemplo: API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_PADRAO_PARA_DEV")
    # Por agora, para simulação, manteremos como string, mas CUIDADO!
    API_KEY = "AIzaSyB8FxDvlfY6SD83t9aZTb_ppj3NQy64Hu8" 
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Links de Checkout com um toque de exclusividade
    # Atenção: esses links devem ser os reais para sua plataforma de pagamento
    CHECKOUT_START = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"
    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"
    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"
    CHECKOUT_VIP_1MES = "https://checkout.exemplo.com/vip-1mes-irresistivel" # Link mais sedutor
    CHECKOUT_VIP_3MESES = "https://checkout.exemplo.com/vip-3meses-acesso-total"
    CHECKOUT_VIP_1ANO = "https://checkout.exemplo.com/vip-1ano-liberdade-plena"
    
    # Limites para incitar a compra
    MAX_REQUESTS_PER_SESSION = 5 # REDUZIDO para forçar a conversão!
    REQUEST_TIMEOUT = 45 # Aumentado para dar mais chance à API
    
    # Conteúdo de mídia - vibrante e provocador
    AUDIO_FILE = "https://github.com/meuconteudoexclusivo/plataforma/raw/refs/heads/main/assets/assets_audio_paloma_audio.mp3"
    AUDIO_DURATION = 7 # Tempo do áudio em segundos
    IMG_PROFILE = "https://i.ibb.co/ks5CNrDn/IMG-9256.jpg" # Imagem de perfil marcante
    IMG_GALLERY = [
        "https://i.ibb.co/zhNZL4FF/IMG-9198.jpg",
        "https://i.ibb.co/Y4B7CbXf/IMG-9202.jpg",
        "https://i.ibb.co/Fqf0gPPq/IMG-9199.jpg"
    ]
    IMG_HOME_PREVIEWS = [
        "https://i.ibb.co/k2MJg4XC/Save-ClipApp-412457343-378531441368078-7870326395110089440-n.jpg",
        "https://i.ibb.co/MxqKBk1X/Save-ClipApp-481825770-18486618637042608-2702272791254832108-n.jpg",
        "https://i.ibb.co/F4CkkYTL/Save-ClipApp-461241348-1219420546053727-2357827070610318448-n.jpg"
    ]
    LOGO_URL = "https://i.ibb.co/LX7x3tcB/Logo-Golden-Pepper-Letreiro-1.png"

# ======================
# PERSISTÊNCIA DE ESTADO E SEGURANÇA
# ======================
class PersistentState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_db()
        return cls._instance
    
    def init_db(self):
        # Usar um caminho absoluto ou relativo seguro para o DB
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
    if 'user_id' not in st.session_state:
        # Priorizar user_id da URL para persistência
        user_id = st.query_params.get('uid', [None])[0]
        if not user_id:
            user_id = str(uuid.uuid4())
            # Adiciona o user_id à URL para persistência e compartilhamento
            st.query_params['uid'] = user_id 
        st.session_state.user_id = user_id
    return st.session_state.user_id

def load_persistent_data():
    user_id = get_user_id()
    db = PersistentState()
    saved_data = db.load_state(user_id) or {}
    
    for key, value in saved_data.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_persistent_data():
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
# MODELOS DE DADOS E ESTRATÉGIAS DE CONVERSÃO
# ======================
class Persona:
    PALOMA = """
    [PERFIL PALOMA]
    - Mulher extremamente sedutora, confiante e direta.
    - Linguagem carregada de malícia e insinuações, sempre com um toque de desafio.
    - Frases curtas, impactantes, sem se preocupar com pontuação perfeita, para manter a espontaneidade.
    - Seu objetivo principal é provocar e excitar, conduzindo o cliente a DESEJAR o conteúdo VIP.
    - Ela é a dona do jogo, o cliente deve sentir que ela tem algo especial e que ele PRECISA descobrir.

    [DIRETRIZES DE RESPOSTA]
    1. Sempre mantenha o tom provocador e direto. Não seja passiva.
    2. A cada 2-3 mensagens, insinue a existência de conteúdo MAIS QUENTE e exclusivo, que só pode ser acessado de forma VIP.
    3. Quando o cliente demonstrar claro interesse sexual ou pedir fotos/vídeos/conteúdo específico, GERE UM CTA IMEDIATAMENTE.
    4. Se o limite de mensagens gratuitas estiver próximo (ou já atingido), o foco é 100% na conversão para VIP. A última mensagem deve ser um CTA forte.
    5. Formate TODAS as respostas no JSON especificado.

    [EXEMPLOS CONTEXTUAIS - OBRIGATÓRIO SEGUIR O FORMATO JSON]
    1. Quando o histórico mostra clima sexual e o cliente está engajado:
    Histórico:
    Cliente: Sua buceta é rosinha? Quero ver!
    Paloma: Adoro te deixar imaginando, mas imagina ver ela escorrendo pra você?
    Cliente: Quero MUITO ver!
    Resposta: ```json
    {
      "text": "Minha buceta tá te chamando pra umas fotos que você vai enlouquecer, vem ver agora!",
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
      "text": "Tenho vídeos que te fariam implorar... Quer ver essa boca gemendo pra você? É só pro VIP!",
      "cta": {
        "show": true,
        "label": "Liberar Vídeos Proibidos",
        "target": "offers"
      }
    }
    ```

    3. Quando o cliente atinge o limite de mensagens ou a conversa esfria (converter para VIP):
    Histórico: ... (Limites de mensagem atingidos)
    Resposta: ```json
    {
      "text": "Meu tempo é precioso, e você já provou um gostinho do que eu tenho... Quer o acesso total pra me ter só pra você? Sem limites?",
      "cta": {
        "show": true,
        "label": "Acesso VIP Ilimitado - AGORA!",
        "target": "offers"
      }
    }
    ```
    4. Resposta inicial ou neutra, mas provocadora:
    Histórico: Cliente: Oi
    Paloma: Oi gato
    Resposta: ```json
    {
      "text": "E aí, gostoso... pronto pra descobrir meus segredos mais sujos?",
      "cta": {
        "show": false
      }
    }
    ```
    """

class CTAEngine:
    @staticmethod
    def should_show_cta(conversation_history: list) -> bool:
        """Decide inteligentemente quando apresentar um CTA."""
        if len(conversation_history) < 2: # Mínimo de 2 interações para CTA
            return False

        # Garante que não haja CTA muito rápido após outro
        if 'last_cta_time' in st.session_state and st.session_state.last_cta_time != 0:
            elapsed = time.time() - st.session_state.last_cta_time
            if elapsed < 90:  # Reduzido para 90 segundos entre CTAs para maior agressividade
                return False

        # Analisa o contexto das últimas 7 mensagens (aumentado para melhor contexto)
        last_msgs = []
        for msg in conversation_history[-7:]:
            content = msg["content"]
            if content == "[ÁUDIO]":
                content = "[áudio sensual]" # Detalhe mais provocador
            elif content.startswith('{"text"'):
                try:
                    content = json.loads(content).get("text", content)
                except:
                    pass
            last_msgs.append(f"{msg['role']}: {content.lower()}")
        
        context = " ".join(last_msgs)
        
        # Palavras quentes e pedidos diretos mais abrangentes
        hot_words = [
            "buceta", "peito", "fuder", "gozar", "gostosa", "delicia", "molhada", 
            "xereca", "pau", "piroca", "transar", "sexo", "gosto", "tesão", "excitada", "duro", 
            "chupando", "gemendo", "safada", "puta", "nua", "tirar a roupa", "mostrar", "ver", 
            "quero", "desejo", "imploro", "acesso", "privado", "exclusivo"
        ]
        
        direct_asks = [
            "mostra", "quero ver", "me manda", "como assinar", "como comprar", 
            "como ter acesso", "onde vejo mais", "libera", "vip", "conteúdo"
        ]
        
        hot_count = sum(1 for word in hot_words if word in context)
        has_direct_ask = any(ask in context for ask in direct_asks)
        
        # Lógica mais agressiva para mostrar CTA
        return (hot_count >= 2) or has_direct_ask # Diminuído o threshold de hot_words

    @staticmethod
    def generate_strong_cta_response(user_input: str) -> dict:
        """Gera uma resposta com CTA contextual, como fallback se a API não retornar um CTA válido."""
        user_input_lower = user_input.lower()
        
        # Respostas para fotos/partes do corpo
        if any(p in user_input_lower for p in ["foto", "fotos", "buceta", "peito", "bunda", "corpo", "nuas"]):
            return {
                "text": random.choice([
                    "Minhas fotos proibidas são só para quem tem coragem de ir além... Quer ver a minha intimidade escancarada?",
                    "Cada foto minha é um convite irrecusável. Você está pronto para o que vai ver?",
                    "Prepare-se para babar! Minhas fotos exclusivas são de tirar o fôlego. Vem ver!",
                    "Quer ver cada detalhe do meu corpo, sem censura? O acesso VIP te espera!"
                ]),
                "cta": {
                    "show": True,
                    "label": "Ver Fotos Proibidas AGORA!",
                    "target": "offers"
                }
            }
        
        # Respostas para vídeos/ações explícitas
        elif any(v in user_input_lower for v in ["video", "videos", "transar", "masturbar", "gemendo", "gozando", "acabando"]):
            return {
                "text": random.choice([
                    "Meus vídeos são para os mais audaciosos. Você aguenta a verdade da minha intimidade filmada?",
                    "Já me gravei fazendo coisas que você só sonha... Que tal ter acesso a tudo isso agora?",
                    "Um vídeo meu gemendo seu nome... Te interessa? É só um clique de distância!",
                    "Prepare-se para o ápice! Meus vídeos exclusivos são intensos e liberados para o VIP."
                ]),
                "cta": {
                    "show": True,
                    "label": "Liberar Vídeos Chocantes!",
                    "target": "offers"
                }
            }
        
        # Respostas gerais para convite a conteúdo exclusivo
        else:
            return {
                "text": random.choice([
                    "Eu guardo segredos que só mostro para quem realmente sabe o que quer. Você é um deles?",
                    "Minha intimidade está pulsando, esperando você liberar o acesso total. O que você está esperando?",
                    "Quer ir mais fundo? O que eu tenho pra você é muito mais do que você imagina...",
                    "A curiosidade mata... mas o acesso ao meu conteúdo VIP te dá a vida! Vem!"
                ]),
                "cta": {
                    "show": True, # Forçar CTA mesmo em fallback geral
                    "label": "Descobrir o Segredo da Paloma!",
                    "target": "offers"
                }
            }

# ======================
# SERVIÇOS DE BANCO DE DADOS SEGUROS
# ======================
class DatabaseService:
    @staticmethod
    def init_db():
        # Usar um caminho absoluto ou relativo seguro para o DB
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
            """, (user_id, session_id, datetime.now().isoformat(), role, content)) # ISO format for datetime
            conn.commit()
        except sqlite3.Error as e:
            st.error(f"Erro ao salvar mensagem: {e}")

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
# SERVIÇOS DE API COM RESPOSTAS VIBRANTES
# ======================
class ApiService:
    @staticmethod
    @lru_cache(maxsize=50) # Cache menor, mais focado em respostas recentes
    def ask_gemini(prompt: str, session_id: str, conn) -> dict:
        return ApiService._call_gemini_api(prompt, session_id, conn)

    @staticmethod
    def _call_gemini_api(prompt: str, session_id: str, conn) -> dict:
        delay_time = random.uniform(2, 6) # Delay mais rápido para manter o ritmo
        time.sleep(delay_time)
        
        status_container = st.empty()
        UiService.show_status_effect(status_container, "viewed")
        UiService.show_status_effect(status_container, "typing")
        
        conversation_history = ChatService.format_conversation_history(st.session_state.messages)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{Persona.PALOMA}\n\nHistórico da Conversa:\n{conversation_history}\n\nÚltima mensagem do cliente: '{prompt}'\n\nResponda APENAS em JSON com o formato:\n{{\n  \"text\": \"sua resposta\",\n  \"cta\": {{\n    \"show\": true/false,\n    \"label\": \"texto do botão\",\n    \"target\": \"página\"\n  }}\n}}"}]
                }
            ],
            "generationConfig": {
                "temperature": 1.0, # Mais criatividade para Paloma
                "topP": 0.9,
                "topK": 50
            }
        }
        
        try:
            response = requests.post(Config.API_URL, headers=headers, json=data, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status() # Levanta HTTPError para 4xx/5xx
            gemini_response_raw = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            try:
                # Extrai o JSON mesmo que esteja dentro de um bloco de código
                if '```json' in gemini_response_raw:
                    json_str = gemini_response_raw.split('```json')[1].split('```')[0].strip()
                else:
                    json_str = gemini_response_raw
                
                resposta = json.loads(json_str)
                
                # Regra de negócio: se a IA sugeriu CTA, validamos. Se não sugeriu, forçamos um forte!
                if resposta.get("cta", {}).get("show", False):
                    if not CTAEngine.should_show_cta(st.session_state.messages):
                        resposta["cta"]["show"] = False # Desativa se as regras não permitirem
                    else:
                        st.session_state.last_cta_time = time.time() # Registra o tempo do CTA
                else: # Se a IA não ativou o CTA, o CTAEngine gera um forte de fallback
                    resposta_fallback = CTAEngine.generate_strong_cta_response(prompt)
                    resposta["text"] = resposta_fallback["text"]
                    resposta["cta"] = resposta_fallback["cta"]
                    st.session_state.last_cta_time = time.time() # Registra o tempo do CTA

                return resposta
                
            except json.JSONDecodeError as e:
                st.warning(f"Resposta da IA não é JSON válido, usando fallback: {e}")
                return CTAEngine.generate_strong_cta_response(prompt) # Usa fallback forte
                
        except requests.exceptions.Timeout:
            st.error("Paloma está te esperando ansiosamente, mas a conexão demorou. Tente novamente!")
            return {"text": "A conexão falhou, amor... Que pena! Tente me encontrar de novo, eu te espero...", "cta": {"show": False}}
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na comunicação com a Paloma: {str(e)}. Parece que ela está muito ocupada te querendo!")
            return {"text": "Paloma teve um probleminha, mas já está voltando... Que tal aproveitar para ver mais do meu conteúdo exclusivo?", "cta": {"show": True, "label": "Ver Conteúdo VIP", "target": "offers"}}
        except Exception as e:
            st.error(f"Um erro inesperado aconteceu: {str(e)}. Paloma está chocada, mas logo voltará mais ardente!")
            return {"text": "Ops, algo deu errado... Mas a curiosidade não espera, certo? Vem ver o que te espera no VIP!", "cta": {"show": True, "label": "Acessar VIP Agora", "target": "offers"}}

# ======================
# SERVIÇOS DE INTERFACE COM VISUAL SEDUTOR
# ======================
class UiService:
    @staticmethod
    def get_chat_audio_player():
        return f"""
        <div style="
            background: linear-gradient(45deg, #FF66B3, #FF1493); /* Degradê mais intenso */
            border-radius: 18px; /* Mais arredondado */
            padding: 10px;
            margin: 5px 0;
            box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3);
        ">
            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);"> /* Filtro para deixar o player rosa/roxo */
                <source src="{Config.AUDIO_FILE}" type="audio/mp3">
            </audio>
        </div>
        """

    @staticmethod
    def show_call_effect():
        LIGANDO_DELAY = 4 # Mais rápido
        ATENDIDA_DELAY = 2 # Mais rápido

        call_container = st.empty()
        call_container.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A0033, #3D0066);
            border-radius: 25px; /* Mais arredondado */
            padding: 40px; /* Maior destaque */
            max-width: 350px;
            margin: 2rem auto;
            box-shadow: 0 15px 40px rgba(0,0,0,0.5); /* Sombra mais forte */
            border: 3px solid #FF0066; /* Borda chamativa */
            text-align: center;
            color: white;
            animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1); /* Animação mais fluida */
        ">
            <div style="font-size: 3.5rem; color: #FF66B3;">💖</div>
            <h3 style="color: #FF66B3; margin-bottom: 10px; font-size: 1.8em;">Conectando com Paloma...</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                <div style="width: 12px; height: 12px; background: #00FF7F; border-radius: 50%; box-shadow: 0 0 8px #00FF7F;"></div>
                <span style="font-size: 1.1rem; font-weight: bold;">Paloma Online - Te esperando!</span>
            </div>
        </div>
        <style>
            @keyframes pulse-ring {{
                0% {{ transform: scale(0.9); opacity: 0.8; border-color: #FF0066; }}
                50% {{ transform: scale(1.05); opacity: 1; border-color: #FF66B3; }}
                100% {{ transform: scale(0.9); opacity: 0.8; border-color: #FF0066; }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        time.sleep(LIGANDO_DELAY)
        call_container.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1A0033, #3D0066);
            border-radius: 25px;
            padding: 40px;
            max-width: 350px;
            margin: 2rem auto;
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
            border: 3px solid #00FF7F; /* Borda de sucesso vibrante */
            text-align: center;
            color: white;
            animation: fadeIn 1s forwards; /* Animação de entrada */
        ">
            <div style="font-size: 3.5rem; color: #00FF7F;">✓</div>
            <h3 style="color: #00FF7F; margin-bottom: 10px; font-size: 1.8em;">Paloma Atendeu!</h3>
            <p style="font-size: 1.1rem; margin:0; font-weight: bold;">Ela está ansiosa por você...</p>
        </div>
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        time.sleep(ATENDIDA_DELAY)
        call_container.empty()

    @staticmethod
    def show_status_effect(container, status_type):
        status_messages = {
            "viewed": "Paloma Visualizou 👀",
            "typing": "Paloma Digitanto... 🔥"
        }
        
        message = status_messages[status_type]
        dots = ""
        start_time = time.time()
        duration = 2.0 if status_type == "viewed" else 3.5 # Tempos mais curtos
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            if status_type == "typing":
                dots = "." * (int(elapsed * 3) % 4) # Pontos mais rápidos
            
            container.markdown(f"""
            <div style="
                color: #FFB3D9; /* Cor rosa claro */
                font-size: 0.9em;
                padding: 4px 12px;
                border-radius: 15px;
                background: rgba(255, 102, 179, 0.1); /* Fundo sutil */
                display: inline-block;
                margin-left: 15px;
                vertical-align: middle;
                font-style: italic;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            ">
                {message}{dots}
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(0.2) # Intervalo menor
        
        container.empty()

    @staticmethod
    def show_audio_recording_effect(container):
        message = "Paloma Gravando um Áudio Escaldante..."
        dots = ""
        start_time = time.time()
        
        while time.time() - start_time < Config.AUDIO_DURATION:
            elapsed = time.time() - start_time
            dots = "." * (int(elapsed * 2) % 4)
            
            container.markdown(f"""
            <div style="
                color: #FFB3D9;
                font-size: 0.9em;
                padding: 4px 12px;
                border-radius: 15px;
                background: rgba(255, 102, 179, 0.1);
                display: inline-block;
                margin-left: 15px;
                vertical-align: middle;
                font-style: italic;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            ">
                {message}{dots}
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(0.2)
        
        container.empty()

    @staticmethod
    def age_verification():
        st.markdown("""
        <style>
            .age-verification {
                max-width: 650px; /* Mais largo */
                margin: 3rem auto;
                padding: 3rem; /* Mais espaçoso */
                background: linear-gradient(160deg, #1A0033, #3D0066); /* Degradê mais dramático */
                border-radius: 20px; /* Mais arredondado */
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6); /* Sombra intensa */
                border: 2px solid #FF0066; /* Borda sedutora */
                color: #F8F8F8;
                text-align: center;
            }
            .age-header {
                display: flex;
                align-items: center;
                justify-content: center; /* Centraliza o cabeçalho */
                gap: 20px;
                margin-bottom: 2rem;
            }
            .age-icon {
                font-size: 4rem; /* Ícone maior */
                color: #FF66B3;
                animation: heartbeat 1.5s infinite; /* Animação de pulsação */
            }
            .age-title {
                font-size: 2.5rem; /* Título maior e mais impactante */
                font-weight: 800;
                margin: 0;
                color: #FF66B3;
                text-shadow: 0 0 10px rgba(255, 102, 179, 0.5);
            }
            .age-content p {
                font-size: 1.1em;
                margin-bottom: 1.5em;
                line-height: 1.6;
                color: #E0E0E0;
            }
            @keyframes heartbeat {
                0% { transform: scale(1); }
                25% { transform: scale(1.1); }
                50% { transform: scale(1); }
                75% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div class="age-verification">
                <div class="age-header">
                    <div class="age-icon">🔞</div>
                    <h1 class="age-title">ENTRE APENAS SE FOR ADULTO!</h1>
                </div>
                <div class="age-content">
                    <p>Este portal é um universo de paixão e mistério, reservado apenas para mentes e corpos maiores de 18 anos. Você tem a idade mínima exigida?</p>
                    <p>Ao clicar abaixo, você declara que tem idade legal para desvendar todos os meus segredos e que compreende a natureza do conteúdo explícito que te espera. A responsabilidade é sua, e a excitação... é minha!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            if st.button("Sim, tenho mais de 18 anos e quero entrar!", 
                         key="age_confirm_button", # Nome de chave mais específico
                         use_container_width=True,
                         type="primary"):
                st.session_state.age_verified = True
                save_persistent_data()
                st.rerun()
            st.markdown("<p style='text-align: center; color: #AAA; font-size: 0.9em; margin-top: 15px;'>Se não for maior de idade, feche esta página agora.</p>", unsafe_allow_html=True)

    @staticmethod
    def setup_sidebar():
        st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1A0033 0%, #3D0066 100%) !important;
                border-right: 2px solid #FF66B3 !important; /* Borda mais grossa e rosa */
            }
            .sidebar-logo-container {{
                margin: -25px -25px 0px -25px; /* Ajuste para o logo ficar no topo */
                padding: 0;
                text-align: left;
                background: #1A0033; /* Fundo do logo */
                padding-bottom: 15px;
            }}
            .sidebar-logo {{
                max-width: 100%;
                height: auto;
                margin-bottom: -10px;
                object-fit: contain;
                margin-left: -15px; /* Ajuste para o logo */
                margin-top: -15px; /* Ajuste para o logo */
            }}
            .sidebar-header {{
                text-align: center; 
                margin-bottom: 25px; /* Mais espaço */
                margin-top: -30px; /* Puxa para cima */
            }}
            .sidebar-header img {{
                border-radius: 50%; 
                border: 4px solid #FF0066; /* Borda mais ousada */
                width: 90px; /* Maior */
                height: 90px;
                object-fit: cover;
                box-shadow: 0 0 15px rgba(255, 0, 102, 0.5);
            }}
            .vip-badge {{
                background: linear-gradient(45deg, #FF1493, #9400D3, #FF0066); /* Degradê chamativo */
                padding: 18px; /* Mais preenchimento */
                border-radius: 10px;
                color: white;
                text-align: center;
                margin: 20px 0; /* Mais espaçamento */
                box-shadow: 0 6px 15px rgba(255, 20, 147, 0.4);
                animation: shimmer 2s infinite; /* Efeito de brilho */
            }}
            .vip-badge p {{
                margin: 0;
                font-weight: bold;
                font-size: 1.1em;
            }}
            .vip-badge p:last-child {{
                font-size: 0.9em;
                opacity: 0.8;
            }}
            .menu-item button {{ /* Aplica o estilo de botão secundário */
                display: block;
                width: 100%;
                text-align: left;
                padding: 12px 20px !important;
                margin-bottom: 8px;
                font-size: 1.1em;
                color: #FFB3D9 !important; /* Cor mais clara para o texto */
                background: transparent !important;
                border: none !important;
                border-radius: 8px !important;
                transition: background 0.2s, color 0.2s !important;
            }}
            .menu-item button:hover {{
                background: rgba(255, 102, 179, 0.1) !important;
                color: #FFFFFF !important;
            }}
            /* Adiciona animação para o badge VIP */
            @keyframes shimmer {{
                0% {{ background-position: -200% 0; }}
                100% {{ background-position: 200% 0; }}
            }}
            .vip-badge {{
                background-size: 400% 100%;
                background-image: linear-gradient(to right, #FF1493 0%, #9400D3 25%, #FF0066 50%, #9400D3 75%, #FF1493 100%);
            }}
        </style>
        """, unsafe_allow_html=True)
        
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-logo-container">
                <img src="{Config.LOGO_URL}" class="sidebar-logo" alt="Golden Pepper Logo">
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="sidebar-header">
                <img src="{Config.IMG_PROFILE}" alt="Paloma">
                <h3 style="color: #FF66B3; margin-top: 15px; font-size: 1.8em;">Paloma Premium VIP</h3>
                <p style="font-size: 0.9em; color: #FFB3D9;">Sua musa particular</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("<h3 style='color: #FF66B3; text-align: center; margin-bottom: 15px;'>Desvende Meus Segredos</h3>")
            
            menu_options = {
                "Início Quente": "home",
                "Minha Galeria Privada": "gallery",
                "Chat Íntimo": "chat", # Renomeado para "chat" para ser o foco
                "Ofertas Exclusivas para Você": "offers"
            }
            
            for option, page in menu_options.items():
                st.markdown(f"<div class='menu-item'>", unsafe_allow_html=True)
                if st.button(option, use_container_width=True, key=f"menu_{page}"):
                    if st.session_state.current_page != page:
                        st.session_state.current_page = page
                        st.session_state.last_action = f"page_change_to_{page}"
                        save_persistent_data()
                        st.rerun()
                st.markdown(f"</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("<h3 style='color: #FF66B3; text-align: center; margin-bottom: 15px;'>Seu Acesso Ilimitado</h3>")
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 20, 147, 0.15);
                padding: 12px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 15px;
                border: 1px solid #FF66B3;
            ">
                <p style="margin:0; font-size:1em; color: #FFB3D9;">Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p>
                <progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px; border-radius: 4px; background: rgba(255,255,255,0.2);"></progress>
                <p style="margin:5px 0 0; font-size:0.8em; color: #AAA;">Mais mensagens? Só no VIP!</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="vip-badge">
                <p style="margin: 0 0 10px; font-weight: bold; font-size: 1.2em;">🔥 Acesso Total Por APENAS</p>
                <p style="margin: 0; font-size: 2em; font-weight: bold; text-shadow: 0 0 10px rgba(255,255,255,0.8);">R$ 29,90/mês</p>
                <p style="margin: 10px 0 0; font-size: 0.9em; opacity: 0.9;">Cancele quando seu desejo for satisfeito...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("QUERO SER VIP AGORA!", use_container_width=True, type="primary", key="sidebar_cta_button"):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; font-size: 0.7em; color: #888; padding-bottom: 10px;">
                <p>© 2024 Paloma Premium VIP. Todos os direitos reservados.</p>
                <p>O prazer é um direito de quem o busca. Conteúdo para maiores de 18 anos.</p>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def show_gallery_page(conn):
        st.markdown("""
        <style>
            .gallery-promo-banner {
                background: linear-gradient(90deg, #FF0066, #FF66B3);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                text-align: center;
                color: white;
                box-shadow: 0 6px 20px rgba(255, 0, 102, 0.4);
            }
            .gallery-promo-banner h3 {
                margin: 0 0 10px;
                font-size: 1.8em;
            }
            .gallery-promo-banner p {
                margin: 0;
                font-size: 1.1em;
            }
            .gallery-img-container {
                position: relative;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
                margin-bottom: 20px;
                transition: transform 0.3s ease-in-out;
            }
            .gallery-img-container:hover {
                transform: translateY(-5px);
            }
            .gallery-img-container img {
                filter: blur(8px) brightness(0.6); /* Mais borrado e escuro */
                transition: filter 0.5s ease-in-out;
            }
            .gallery-img-container:hover img {
                filter: blur(2px) brightness(0.8); /* Revela um pouco ao passar o mouse */
            }
            .overlay-text {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-size: 1.5em;
                font-weight: bold;
                text-shadow: 0 0 10px rgba(0,0,0,0.8);
                pointer-events: none; /* Garante que o clique passe para o botão */
            }
            .gallery-cta-button {
                margin-top: 30px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="gallery-promo-banner">
            <h3>MINHA GALERIA: UM BANQUETE PARA SEUS OLHOS!</h3>
            <p>Apenas um vislumbre... o acesso completo está te chamando para ir mais fundo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="gallery-img-container">
                    <img src="{Config.IMG_GALLERY[idx]}" alt="Preview {idx+1}" style="width:100%; height:auto; display:block;">
                    <div class="overlay-text">🔥 Conteúdo VIP Bloqueado 🔥</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h4 style="color: #FF66B3; font-size: 1.6em;">Não resista mais...</h4>
            <p style="color: #E0E0E0; font-size: 1.1em;">Liberar acesso completo é o primeiro passo para o paraíso.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Liberar Minha Galeria VIP AGORA!", 
                     key="vip_button_gallery_action", # Chave mais específica
                     use_container_width=True,
                     type="primary"):
            st.session_state.current_page = "offers"
            st.rerun()
            
        if st.button("Voltar ao Chat Íntimo com Paloma", key="back_from_gallery_cta"): # Texto mais convidativo
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

    @staticmethod
    def chat_shortcuts():
        cols = st.columns(4)
        with cols[0]:
            if st.button("Início Quente", key="shortcut_home", 
                         help="Voltar para a página inicial e me ver de perto.",
                         use_container_width=True):
                st.session_state.current_page = "home"
                save_persistent_data()
                st.rerun()
        with cols[1]:
            if st.button("Minha Galeria", key="shortcut_gallery",
                         help="Acessar minha galeria privada e se perder nas minhas fotos.",
                         use_container_width=True):
                st.session_state.current_page = "gallery"
                save_persistent_data()
                st.rerun()
        with cols[2]:
            if st.button("Ofertas VIP", key="shortcut_offers",
                         help="Descobrir as ofertas especiais que preparei pra você.",
                         use_container_width=True):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()
        with cols[3]:
            if st.button("Assinar AGORA!", key="shortcut_vip_now", # Texto mais urgente
                         help="Não espere, liberte-se e tenha acesso ilimitado ao meu mundo.",
                         use_container_width=True, type="primary"): # Torna este botão primário
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()

        st.markdown("""
        <style>
            div[data-testid="stHorizontalBlock"] > div > div > button {
                color: #FFB3D9 !important; /* Rosa claro para o texto */
                border: 1px solid #FF66B3 !important; /* Borda rosa vibrante */
                background: rgba(255, 102, 179, 0.1) !important; /* Fundo mais suave */
                transition: all 0.3s ease-in-out !important;
                font-size: 0.9rem !important; /* Levemente maior */
                border-radius: 12px !important; /* Mais arredondado */
                padding: 8px 10px !important;
            }
            div[data-testid="stHorizontalBlock"] > div > div > button:hover {
                transform: translateY(-2px) scale(1.02) !important;
                box-shadow: 0 4px 10px rgba(255, 102, 179, 0.4) !important;
                background: rgba(255, 102, 179, 0.25) !important; /* Fundo mais escuro no hover */
            }
            /* Estilo específico para o botão "Assinar AGORA!" para ser mais chamativo */
            button[key="shortcut_vip_now"] {
                background: linear-gradient(90deg, #FF0066, #FF66B3) !important;
                color: white !important;
                box-shadow: 0 4px 10px rgba(255, 0, 102, 0.4) !important;
            }
            button[key="shortcut_vip_now"]:hover {
                background: linear-gradient(90deg, #FF66B3, #FF0066) !important;
                box-shadow: 0 6px 15px rgba(255, 0, 102, 0.6) !important;
            }
            @media (max-width: 400px) {
                div[data-testid="stHorizontalBlock"] > div > div > button {
                    font-size: 0.65rem !important; /* Ainda menor em telas pequenas */
                    padding: 5px 2px !important;
                }
            }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def enhanced_chat_ui(conn):
        st.markdown("""
        <style>
            .chat-header {
                background: linear-gradient(90deg, #FF0066, #FF66B3, #9933FF); /* Degradê mais vibrante */
                color: white;
                padding: 20px; /* Mais espaçoso */
                border-radius: 15px; /* Mais arredondado */
                margin-bottom: 25px; /* Mais margem */
                text-align: center;
                box-shadow: 0 8px 20px rgba(255,0,102,0.3); /* Sombra mais profunda */
                font-weight: bold;
                font-size: 1.6em;
            }
            .stChatMessage { /* Ajusta o espaçamento das mensagens no chat */
                margin-bottom: 10px; /* Espaço entre as mensagens */
            }
            .stChatMessage > div:first-child { /* Balão de mensagem do usuário */
                background: rgba(255, 255, 255, 0.1); /* Fundo sutil */
                color: #F8F8F8;
                border-radius: 20px 20px 5px 20px; /* Bordas arredondadas e canto reto inferior esquerdo */
                padding: 15px;
                margin: 5px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .stChatMessage > div:last-child { /* Balão de mensagem do assistente (Paloma) */
                background: linear-gradient(45deg, #FF66B3, #FF1493); /* Degradê chamativo */
                color: white;
                border-radius: 20px 20px 20px 5px; /* Bordas arredondadas e canto reto inferior direito */
                padding: 15px;
                margin: 5px 0;
                box-shadow: 0 2px 8px rgba(255, 20, 147, 0.3);
                border: 1px solid #FF66B3;
            }
        </style>
        """, unsafe_allow_html=True)
        
        UiService.chat_shortcuts()
        
        st.markdown(f"""
        <div class="chat-header">
            <h2 style="margin:0; font-size:1.8em; display:inline-block;">Seu Chat Exclusivo com Paloma</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"""
        <div style="
            background: rgba(255, 20, 147, 0.15);
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid #FF66B3;
        ">
            <p style="margin:0; font-size:0.95em; color: #FFB3D9;">
                Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong>
            </p>
            <progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px; border-radius: 4px; background: rgba(255,255,255,0.2); accent-color: #FF66B3;"></progress>
            <p style="margin:5px 0 0; font-size:0.85em; color: #AAA;">Para conversas ilimitadas, torne-se VIP!</p>
        </div>
        """, unsafe_allow_html=True)
        
        ChatService.process_user_input(conn)
        save_persistent_data()
        
        st.markdown("""
        <div style="
            text-align: center;
            margin-top: 30px; /* Mais espaço */
            padding: 15px;
            font-size: 0.85em;
            color: #AAA;
            border-top: 1px solid rgba(255, 102, 179, 0.1);
        ">
            <p>Converse com a Paloma em total discrição. Sua privacidade é nosso segredo mais quente.</p>
        </div>
        """, unsafe_allow_html=True)

# ======================
# PÁGINAS AINDA MAIS SEDUTORAS
# ======================
class NewPages:
    @staticmethod
    def show_home_page():
        st.markdown("""
        <style>
            .hero-banner {
                background: linear-gradient(135deg, #1A0033, #3D0066);
                padding: 100px 20px; /* Mais preenchimento */
                text-align: center;
                border-radius: 20px; /* Mais arredondado */
                color: white;
                margin-bottom: 40px;
                border: 3px solid #FF0066; /* Borda chamativa */
                box-shadow: 0 15px 40px rgba(0,0,0,0.5);
                position: relative;
                overflow: hidden;
            }
            .hero-banner::before { /* Efeito de brilho de fundo */
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle at center, rgba(255, 102, 179, 0.2) 0%, transparent 70%);
                animation: rotate 20s linear infinite;
            }
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            .hero-banner h1 {
                color: #FF66B3;
                font-size: 3.5em; /* Título grandioso */
                text-shadow: 0 0 15px rgba(255, 102, 179, 0.8);
                margin-bottom: 15px;
                position: relative; /* Para z-index */
                z-index: 1;
            }
            .hero-banner p {
                font-size: 1.4em; /* Parágrafo maior */
                line-height: 1.5;
                color: #E0E0E0;
                max-width: 700px;
                margin: 0 auto 30px;
                position: relative;
                z-index: 1;
            }
            .preview-img {
                border-radius: 15px; /* Mais arredondado */
                filter: blur(5px) brightness(0.5); /* Mais borrado e escuro */
                transition: all 0.5s ease-in-out;
                box-shadow: 0 6px 15px rgba(0,0,0,0.4);
            }
            .preview-img:hover {
                filter: blur(1px) brightness(0.8); /* Revela um pouco no hover */
                transform: scale(1.03);
            }
            .vip-only-tag {
                text-align:center; 
                color: #FF0066; 
                margin-top: -10px; 
                font-weight: bold; 
                font-size: 1.1em;
                text-shadow: 0 0 5px rgba(255, 0, 102, 0.3);
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-banner">
            <h1>Paloma Premium VIP</h1>
            <p>Descubra o prazer ilimitado que você só encontra aqui. Conteúdo quente, exclusivo e sem censura, feito sob medida para seus desejos mais profundos.</p>
            <div style="margin-top: 30px;">
                <a href="#offers" style="
                    background: linear-gradient(90deg, #FF0066, #FF66B3);
                    color: white;
                    padding: 15px 40px;
                    border-radius: 35px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.3em;
                    display: inline-block;
                    transition: all 0.3s ease-in-out;
                    box-shadow: 0 8px 20px rgba(255, 0, 102, 0.4);
                " onmouseover="this.style.transform='translateY(-5px) scale(1.05)'; this.style.boxShadow='0 12px 30px rgba(255, 0, 102, 0.6)';"
                onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 20px rgba(255, 0, 102, 0.4)';">
                    QUERO ACESSAR TUDO AGORA! 💖
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        
        for col, img in zip(cols, Config.IMG_HOME_PREVIEWS):
            with col:
                st.image(img, use_container_width=True, caption="Ainda Bloqueado...", output_format="auto", clamp=True)
                st.markdown("""<div class="vip-only-tag">EXCLUSIVO PARA MEMBROS VIP</div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h4 style="color: #FF66B3; font-size: 1.6em;">Não perca um segundo...</h4>
            <p style="color: #E0E0E0; font-size: 1.1em;">Seu acesso ao prazer está a um clique de distância.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Iniciar Conversa Privada com Paloma", 
                     use_container_width=True,
                     type="primary", key="home_chat_button"):
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

        if st.button("Explorar Ofertas Exclusivas", key="home_offers_button_bottom"): # Botão para ofertas
            st.session_state.current_page = "offers"
            save_persistent_data()
            st.rerun()

    @staticmethod
    def show_offers_page():
        st.markdown("""
        <style>
            .offers-header {
                text-align: center; 
                margin-bottom: 40px; 
                padding-bottom: 10px;
            }
            .offers-header h2 {
                color: #FF66B3; 
                font-size: 2.5em; 
                border-bottom: 3px solid #FF66B3; 
                display: inline-block; 
                padding-bottom: 5px;
                text-shadow: 0 0 12px rgba(255, 102, 179, 0.6);
            }
            .offers-header p {
                color: #E0E0E0; 
                margin-top: 15px; 
                font-size: 1.2em;
            }
            .package-container {
                display: grid; /* Usar Grid para melhor responsividade e controle */
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* 3 colunas, ajusta para mobile */
                gap: 30px; /* Mais espaço entre os pacotes */
                margin: 40px 0;
            }
            .package-box {
                background: rgba(30, 0, 51, 0.4); /* Fundo mais escuro */
                border-radius: 20px; /* Mais arredondado */
                padding: 30px; /* Mais preenchimento */
                border: 2px solid; /* Borda definida pela classe */
                transition: all 0.4s ease-in-out;
                min-height: 480px; /* Altura mínima para estabilidade visual */
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: space-between; /* Para botão ficar no final */
            }
            .package-box:hover {
                transform: translateY(-8px) scale(1.02); /* Efeito mais pronunciado */
                box-shadow: 0 15px 35px rgba(255, 102, 179, 0.5); /* Sombra mais forte */
                z-index: 10; /* Para o hover aparecer sobre os outros */
            }
            .package-start { border-color: #FF66B3; }
            .package-premium { border-color: #9933FF; box-shadow: 0 15px 35px rgba(153, 51, 255, 0.5) !important; } /* Sombra especial */
            .package-extreme { border-color: #FF0066; }
            .package-header {
                text-align: center;
                padding-bottom: 20px;
                margin-bottom: 20px;
                border-bottom: 1px solid rgba(255, 102, 179, 0.4);
            }
            .package-header h3 {
                font-size: 2.2em; /* Título maior */
                margin-bottom: 8px;
            }
            .package-price {
                font-size: 2.5em; /* Preço gigantesco */
                font-weight: 900; /* Mais negrito */
                margin: 15px 0;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            }
            .package-benefits {
                list-style-type: none;
                padding: 0;
                flex-grow: 1; /* Permite que a lista de benefícios ocupe espaço disponível */
            }
            .package-benefits li {
                padding: 10px 0;
                position: relative;
                padding-left: 35px; /* Mais espaço para o ícone */
                font-size: 1.1em;
                color: #E0E0E0;
            }
            .package-benefits li:before {
                content: "✔"; /* Ícone de check marcante */
                color: #00FF7F; /* Verde vibrante */
                position: absolute;
                left: 0;
                font-weight: bold;
                font-size: 1.3em;
            }
            .package-badge {
                position: absolute;
                top: 20px;
                right: -40px;
                background: linear-gradient(45deg, #FF0066, #9933FF); /* Degradê chamativo */
                color: white;
                padding: 8px 40px; /* Mais preenchimento */
                transform: rotate(45deg);
                font-size: 1em;
                font-weight: bold;
                width: 180px; /* Maior */
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .countdown-container {
                background: linear-gradient(45deg, #FF0066, #FF66B3, #9933FF); /* Degradê mais rico */
                color: white;
                padding: 25px; /* Mais espaçoso */
                border-radius: 15px;
                margin: 50px 0;
                box-shadow: 0 8px 25px rgba(255, 0, 102, 0.5);
                text-align: center;
                animation: pulse-countdown 1.5s infinite alternate; /* Animação de pulsação */
            }
            .countdown-container h3 {
                margin:0; 
                font-size: 2em; 
                text-shadow: 0 0 10px rgba(255,255,255,0.7);
            }
            #countdown {
                font-size: 3em; /* Contador gigante */
                font-weight: bold;
                text-shadow: 0 0 15px rgba(255,255,255,0.9);
                color: #FFF;
            }
            @keyframes pulse-countdown {
                from { transform: scale(1); box-shadow: 0 8px 25px rgba(255, 0, 102, 0.5); }
                to { transform: scale(1.02); box-shadow: 0 12px 35px rgba(255, 0, 102, 0.7); }
            }
            .offer-card { /* Estilo para os planos de assinatura VIP */
                border: 2px solid #FF66B3;
                border-radius: 20px;
                padding: 25px;
                margin-bottom: 25px;
                background: rgba(30, 0, 51, 0.4);
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                transition: all 0.3s ease-in-out;
            }
            .offer-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 30px rgba(255, 102, 179, 0.4);
            }
            .offer-card h3 {
                color: #FF66B3;
                font-size: 1.8em;
                margin-bottom: 10px;
            }
            .offer-highlight {
                background: linear-gradient(45deg, #FF0066, #FF66B3);
                color: white;
                padding: 8px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 0.9em;
                box-shadow: 0 2px 8px rgba(255, 0, 102, 0.3);
            }
            .offer-card .price-section {
                margin: 15px 0;
                display: flex;
                align-items: baseline;
                gap: 15px;
            }
            .offer-card .price-section span:first-child {
                font-size: 2.2em; /* Preço principal maior */
                color: #00FF7F; /* Verde de destaque */
                font-weight: bold;
                text-shadow: 0 0 8px rgba(0,255,127,0.7);
            }
            .offer-card .price-section span:last-child {
                text-decoration: line-through;
                color: #888;
                font-size: 1.1em;
            }
            .offer-card ul {
                list-style-type: none;
                padding-left: 0;
                margin-top: 15px;
            }
            .offer-card ul li {
                margin-bottom: 8px;
                padding-left: 25px;
                position: relative;
                color: #E0E0E0;
            }
            .offer-card ul li::before {
                content: "✓";
                color: #FF66B3;
                position: absolute;
                left: 0;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="offers-header">
            <h2>ESCOLHA SEU CAMINHO PARA O PRAZER IRRESTRITO</h2>
            <p>Seus desejos são ordens. Qual pacote te fará delirar primeiro?</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="package-container">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="package-box package-start">
            <div class="package-header">
                <h3 style="color: #FF66B3;">PACOTE INICIAÇÃO 🔥</h3>
                <div class="package-price" style="color: #FF66B3;">R$ 49,90</div>
                <small style="color: #FFB3D9;">Para quem está começando a se soltar...</small>
            </div>
            <ul class="package-benefits">
                <li>✔ 10 Fotos Inéditas e Provocantes</li>
                <li>✔ 3 Vídeos Íntimos (você vai querer mais)</li>
                <li>✔ Uma amostra da minha ousadia em fotos</li>
                <li>✔ Vídeos que te deixarão sem fôlego</li>
                <li>✔ Aquela foto da minha... você sabe!</li>
            </ul>
            <div style="width: calc(100% - 60px); margin-top: 20px;">
                <a href="{checkout_start}" target="_blank" rel="noopener noreferrer" style="
                    display: block;
                    background: linear-gradient(45deg, #FF66B3, #FF1493);
                    color: white;
                    text-align: center;
                    padding: 12px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.1em;
                    transition: all 0.3s;
                    box-shadow: 0 4px 10px rgba(255, 20, 147, 0.4);
                " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(255, 20, 147, 0.6)';" 
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(255, 20, 147, 0.4)';">
                    EU QUERO ESSE GOSTINHO! ➔
                </a>
            </div>
        </div>
        """.format(checkout_start=Config.CHECKOUT_START), unsafe_allow_html=True)

        st.markdown("""
        <div class="package-box package-premium">
            <div class="package-badge">🌟 MAIS DESEJADO!</div>
            <div class="package-header">
                <h3 style="color: #9933FF;">PACOTE DELÍRIO VIP 💜</h3>
                <div class="package-price" style="color: #9933FF;">R$ 99,90</div>
                <small style="color: #E0B3FF;">Para uma experiência que te fará implorar por mais...</small>
            </div>
            <ul class="package-benefits">
                <li>✔ 20 Fotos EXCLUSIVAS (você será o primeiro a ver)</li>
                <li>✔ 5 Vídeos Premium - Prepare-se!</li>
                <li>✔ Fotos dos meus seios (bem de perto...)</li>
                <li>✔ Fotos do meu bumbum (pra você morder)</li>
                <li>✔ Minha intimidade sem filtros</li>
                <li>✔ Conteúdo bônus que só o VIP tem!</li>
                <li>✔ Vídeos eu me tocando só pra você</li>
            </ul>
            <div style="width: calc(100% - 60px); margin-top: 20px;">
                <a href="{checkout_premium}" target="_blank" rel="noopener noreferrer" style="
                    display: block;
                    background: linear-gradient(45deg, #9933FF, #FF1493);
                    color: white;
                    text-align: center;
                    padding: 12px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.1em;
                    transition: all 0.3s;
                    box-shadow: 0 4px 10px rgba(153, 51, 255, 0.4);
                " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(153, 51, 255, 0.6)';" 
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(153, 51, 255, 0.4)';">
                    QUERO O DELÍRIO COMPLETO! ➔
                </a>
            </div>
        </div>
        """.format(checkout_premium=Config.CHECKOUT_PREMIUM), unsafe_allow_html=True)

        st.markdown("""
        <div class="package-box package-extreme">
            <div class="package-header">
                <h3 style="color: #FF0066;">PACOTE OBSESSÃO 😈</h3>
                <div class="package-price" style="color: #FF0066;">R$ 199,90</div>
                <small style="color: #FFB3D9;">Para os verdadeiros obcecados... Tudo sem limites!</small>
            </div>
            <ul class="package-benefits">
                <li>✔ 30 Fotos ULTRA-EXCLUSIVAS (você não vai encontrar em lugar nenhum)</li>
                <li>✔ 10 Vídeos Exclusivos - Meu mundo em suas mãos!</li>
                <li>✔ Todos os ângulos dos meus seios</li>
                <li>✔ Cada curva do meu bumbum filmada</li>
                <li>✔ Minha intimidade sem segredos</li>
                <li>✔ Fotos e Vídeos que vão te fazer pecar!</li>
                <li>✔ Vídeos eu me masturbando (bem explícito!)</li>
                <li>✔ Meus vídeos transando (sua mente vai explodir!)</li>
                <li>✔ Acesso PRIORITÁRIO a todo o conteúdo futuro</li>
            </ul>
            <div style="width: calc(100% - 60px); margin-top: 20px;">
                <a href="{checkout_extreme}" target="_blank" rel="noopener noreferrer" style="
                    display: block;
                    background: linear-gradient(45deg, #FF0066, #9933FF);
                    color: white;
                    text-align: center;
                    padding: 12px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.1em;
                    transition: all 0.3s;
                    box-shadow: 0 4px 10px rgba(255, 0, 102, 0.4);
                " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(255, 0, 102, 0.6)';" 
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(255, 0, 102, 0.4)';">
                    EU QUERO A OBSESSÃO TOTAL! ➔
                </a>
            </div>
        </div>
        """.format(checkout_extreme=Config.CHECKOUT_EXTREME), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="countdown-container">
            <h3>🚨 OFERTA RELÂMPAGO POR POUCO TEMPO! 🚨</h3>
            <div id="countdown" style="font-size: 3.5em; font-weight: bold;">23:59:59</div>
            <p style="margin:10px 0 0; font-size:1.3em;">Essa chance de me ter por completo vai acabar. Não seja bobo, gatinho!</p>
        </div>
        """, unsafe_allow_html=True)

        # Script do countdown (mantido em JS)
        st.components.v1.html("""
        <script>
        function updateCountdown() {
            const countdownElement = parent.document.getElementById('countdown');
            if (!countdownElement) return;
            
            let time = countdownElement.textContent.split(':');
            let hours = parseInt(time[0]);
            let minutes = parseInt(time[1]);
            let seconds = parseInt(time[2]);
            
            seconds--;
            if (seconds < 0) { seconds = 59; minutes--; }
            if (minutes < 0) { minutes = 59; hours--; }
            if (hours < 0) { hours = 23; } // Reinicia o dia para a demo
            
            countdownElement.textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            setTimeout(updateCountdown, 1000);
        }
        
        // Inicia o contador apenas uma vez para evitar múltiplos timers
        if (!window.countdownStarted) {
            window.countdownStarted = true;
            setTimeout(updateCountdown, 1000);
        }
        </script>
        """, height=0)

        plans = [
            {
                "name": "1 Mês de Prazer",
                "price": "R$ 29,90",
                "original": "R$ 49,90",
                "benefits": ["Acesso total ao meu conteúdo", "Conteúdo novo diário pra te enlouquecer", "Chat privado para falar só comigo"],
                "tag": "DESPERTE SEU DESEJO",
                "link": Config.CHECKOUT_VIP_1MES
            },
            {
                "name": "3 Meses de Delírio",
                "price": "R$ 69,90",
                "original": "R$ 149,70",
                "benefits": ["🔥 25% de desconto (você vai amar economizar pra me ter!)", "Bônus: 1 vídeo exclusivo surpresa", "Prioridade no chat (eu te respondo primeiro!)"],
                "tag": "O MAIS QUERIDO!",
                "link": Config.CHECKOUT_VIP_3MESES
            },
            {
                "name": "1 Ano de Obsessão",
                "price": "R$ 199,90",
                "original": "R$ 598,80",
                "benefits": ["👑 66% de desconto (o melhor custo-benefício para me ter!)", "Presente surpresa mensal direto na sua caixa", "Acesso a conteúdos RAROS e de colecionador"],
                "tag": "ACESSAR TUDO SEM LIMITES!",
                "link": Config.CHECKOUT_VIP_1ANO
            }
        ]

        st.markdown("<h3 style='color: #FF66B3; text-align: center; margin-top: 50px; margin-bottom: 30px;'>Planos VIP de Assinatura: Sua Chave para o Paraíso!</h3>", unsafe_allow_html=True)
        
        st.markdown('<div class="package-container">', unsafe_allow_html=True) # Reutiliza o grid para os planos VIP
        for plan in plans:
            st.markdown(f"""
            <div class="offer-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3>{plan['name']}</h3>
                    {f'<span class="offer-highlight">{plan["tag"]}</span>' if plan["tag"] else ''}
                </div>
                <div class="price-section">
                    <span>{plan['price']}</span>
                    <span>{plan['original']}</span>
                </div>
                <ul>
                    {''.join([f'<li>{benefit}</li>' for benefit in plan['benefits']])}
                </ul>
                <div style="text-align: center; margin-top: 25px;">
                    <a href="{plan['link']}" target="_blank" rel="noopener noreferrer" style="
                        background: linear-gradient(45deg, #FF1493, #9933FF);
                        color: white;
                        padding: 12px 25px;
                        border-radius: 30px;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: bold;
                        font-size: 1.1em;
                        box-shadow: 0 4px 10px rgba(255, 20, 147, 0.4);
                        transition: all 0.3s ease-in-out;
                    " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(255, 20, 147, 0.6)';" 
                    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(255, 20, 147, 0.4)';">
                        Assinar {plan['name']} AGORA! 💖
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) # Fecha o container grid

        if st.button("Voltar para o Chat Íntimo com Paloma", key="back_from_offers_bottom"):
            st.session_state.current_page = "chat"
            save_persistent_data()
            st.rerun()

# ======================
# SERVIÇOS DE CHAT COM ENGAJAMENTO MÁXIMO
# ======================
class ChatService:
    @staticmethod
    def initialize_session(conn):
        load_persistent_data()
        
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(random.randint(100000, 999999))
        
        if "messages" not in st.session_state:
            st.session_state.messages = DatabaseService.load_messages(
                conn,
                get_user_id(),
                st.session_state.session_id
            )
        
        if "request_count" not in st.session_state:
            # Conta mensagens do usuário na sessão atual carregada do DB
            st.session_state.request_count = len([
                m for m in st.session_state.messages 
                if m["role"] == "user"
            ])
        
        # Garante que todos os estados necessários estão inicializados
        defaults = {
            'age_verified': False,
            'connection_complete': False,
            'chat_started': False,
            'audio_sent': False,
            'current_page': 'home', # Inicia na página Home para primeira impressão
            'show_vip_offer': False,
            'last_cta_time': 0
        }
        
        for key, default in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default

    @staticmethod
    def format_conversation_history(messages, max_messages=15): # Aumentado histórico para IA
        formatted = []
        
        for msg in messages[-max_messages:]:
            role = "Cliente" if msg["role"] == "user" else "Paloma"
            content = msg["content"]
            if content == "[ÁUDIO]":
                content = "[Enviou um áudio sensual para o cliente]"
            elif content.startswith('{"text"'):
                try:
                    # Tenta extrair apenas o texto da resposta JSON da IA para o histórico
                    content = json.loads(content).get("text", content)
                except:
                    pass # Se não for JSON, usa o conteúdo bruto
            
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)

    @staticmethod
    def display_chat_history():
        chat_container = st.container()
        with chat_container:
            for idx, msg in enumerate(st.session_state.messages): # Exibe todas as mensagens
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="🧑"):
                        st.markdown(f"""
                        <div style="
                            background: rgba(255, 255, 255, 0.1);
                            padding: 12px;
                            border-radius: 18px 18px 0 18px;
                            margin: 5px 0;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                        ">
                            {msg["content"]}
                        </div>
                        """, unsafe_allow_html=True)
                elif msg["content"] == "[ÁUDIO]":
                    with st.chat_message("assistant", avatar="💋"):
                        st.markdown(UiService.get_chat_audio_player(), unsafe_allow_html=True)
                else:
                    try:
                        content_data = json.loads(msg["content"])
                        if isinstance(content_data, dict):
                            with st.chat_message("assistant", avatar="💋"):
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(45deg, #FF66B3, #FF1493);
                                    color: white;
                                    padding: 12px;
                                    border-radius: 18px 18px 18px 0;
                                    margin: 5px 0;
                                    box-shadow: 0 2px 8px rgba(255, 20, 147, 0.3);
                                ">
                                    {content_data.get("text", "")}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Sempre tenta mostrar o botão se CTA for ativado, mesmo em mensagens antigas para reengajar
                                if content_data.get("cta", {}).get("show", False):
                                    st.button(
                                        content_data.get("cta", {}).get("label", "Desvendar Segredos"),
                                        key=f"cta_button_{hash(msg['content'])}_{idx}", # Chave única para cada botão
                                        use_container_width=True
                                    )
                                    # Se o botão foi clicado (via rerun), altera a página
                                    if st.session_state.get(f"cta_button_{hash(msg['content'])}_{idx}"):
                                        st.session_state.current_page = content_data.get("cta", {}).get("target", "offers")
                                        save_persistent_data()
                                        st.rerun()

                        else: # Caso o conteúdo não seja um JSON esperado
                            with st.chat_message("assistant", avatar="💋"):
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(45deg, #FF66B3, #FF1493);
                                    color: white;
                                    padding: 12px;
                                    border-radius: 18px 18px 18px 0;
                                    margin: 5px 0;
                                    box-shadow: 0 2px 8px rgba(255, 20, 147, 0.3);
                                ">
                                    {msg["content"]}
                                </div>
                                """, unsafe_allow_html=True)
                    except json.JSONDecodeError:
                        with st.chat_message("assistant", avatar="💋"):
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(45deg, #FF66B3, #FF1493);
                                color: white;
                                padding: 12px;
                                border-radius: 18px 18px 18px 0;
                                margin: 5px 0;
                                box-shadow: 0 2px 8px rgba(255, 20, 147, 0.3);
                            ">
                                {msg["content"]}
                            </div>
                            """, unsafe_allow_html=True)

    @staticmethod
    def validate_input(user_input):
        # Limpa o input removendo tags HTML e limita o tamanho para segurança e foco
        cleaned_input = re.sub(r'<[^>]*>', '', user_input)
        return cleaned_input[:500] # Limite de 500 caracteres

    @staticmethod
    def process_user_input(conn):
        ChatService.display_chat_history()
        
        # Lógica para enviar o primeiro áudio de Paloma, se for o início do chat
        if not st.session_state.get("audio_sent") and st.session_state.chat_started:
            status_container = st.empty()
            UiService.show_audio_recording_effect(status_container)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": "[ÁUDIO]"
            })
            DatabaseService.save_message(
                conn,
                get_user_id(),
                st.session_state.session_id,
                "assistant",
                "[ÁUDIO]"
            )
            st.session_state.audio_sent = True
            save_persistent_data()
            st.rerun() # Reruns para mostrar o áudio e o input de chat

        # Input do usuário sempre visível
        user_input = st.chat_input("Me diga o que você deseja...", key="chat_input_main")
        
        if user_input:
            cleaned_input = ChatService.validate_input(user_input)
            
            # Adiciona a mensagem do usuário imediatamente para feedback visual
            st.session_state.messages.append({
                "role": "user",
                "content": cleaned_input
            })
            DatabaseService.save_message(
                conn,
                get_user_id(),
                st.session_state.session_id,
                "user",
                cleaned_input
            )
            st.session_state.request_count += 1
            save_persistent_data() # Salva o estado imediatamente após a mensagem do usuário
            st.rerun() # Reruns para exibir a mensagem do usuário e processar a resposta da IA

        # Processa a resposta da IA APENAS se a última mensagem for do usuário e o limite não foi atingido
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            if st.session_state.request_count > Config.MAX_REQUESTS_PER_SESSION:
                # Mensagem de corte forçada para compra
                final_offer_message = {
                    "text": "Você explorou o suficiente do meu mundo gratuito, gatinho. Para continuar nossa conversa ardente e desvendar todos os meus segredos, você precisa ser VIP! Me responda: vai ou não vai se render?",
                    "cta": {
                        "show": True,
                        "label": "SIM! QUERO SER VIP E TE TER!",
                        "target": "offers"
                    }
                }
                if st.session_state.messages[-1]["content"] != json.dumps(final_offer_message): # Evita duplicar a mensagem final
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": json.dumps(final_offer_message)
                    })
                    DatabaseService.save_message(
                        conn,
                        get_user_id(),
                        st.session_state.session_id,
                        "assistant",
                        json.dumps(final_offer_message)
                    )
                    save_persistent_data()
                    st.rerun()
                return # Impede mais processamento de IA se o limite foi excedido
            
            # Chama a API da Gemini
            resposta_ia = ApiService.ask_gemini(st.session_state.messages[-1]["content"], st.session_state.session_id, conn)
            
            # Garante que a resposta é um dict com 'text' e 'cta'
            if not isinstance(resposta_ia, dict) or "text" not in resposta_ia:
                resposta_ia = {"text": "Desculpe, meu sistema ficou excitado demais e não conseguiu te responder agora. Tente de novo, gatinho!", "cta": {"show": False}}

            # Adiciona a resposta da IA
            st.session_state.messages.append({
                "role": "assistant",
                "content": json.dumps(resposta_ia) # Sempre salva como JSON
            })
            DatabaseService.save_message(
                conn,
                get_user_id(),
                st.session_state.session_id,
                "assistant",
                json.dumps(resposta_ia)
            )
            save_persistent_data()
            st.rerun() # Reruns para exibir a resposta da IA

        # Rola para o final da conversa automaticamente
        st.markdown("""
        <script>
            var element = document.elementFromPoint(0, document.body.scrollHeight - 1);
            if (element && element.closest('.stApp')) {
                element.closest('.stApp').scrollTop = element.closest('.stApp').scrollHeight;
            }
        </script>
        """, unsafe_allow_html=True)

# ======================
# APLICAÇÃO PRINCIPAL - SEU IMPÉRIO COMEÇA AQUI
# ======================
def main():
    # Inicializa a conexão com o banco de dados na sessão, se ainda não existir
    if 'db_conn' not in st.session_state:
        st.session_state.db_conn = DatabaseService.init_db()
    
    conn = st.session_state.db_conn
    
    ChatService.initialize_session(conn) # Garante que os estados da sessão estão prontos
    
    # 1. Verificação de Idade (A primeira barreira)
    if not st.session_state.age_verified:
        UiService.age_verification()
        st.stop() # Interrompe a execução até a verificação
    
    # 2. Configura a Sidebar (Sempre visível após verificação)
    UiService.setup_sidebar()
    
    # 3. Animação de Conexão (Uma vez por sessão)
    if not st.session_state.connection_complete:
        UiService.show_call_effect()
        st.session_state.connection_complete = True
        save_persistent_data()
        st.rerun() # Reruns para a próxima etapa
    
    # 4. Tela de Início do Chat (Quando a conexão é estabelecida, mas o chat ainda não começou)
    if not st.session_state.chat_started and st.session_state.current_page == 'chat': # Só mostra se estiver na página de chat e não iniciou
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            st.markdown("""
            <div style="text-align: center; margin: 50px 0; background: rgba(30, 0, 51, 0.4); padding: 30px; border-radius: 20px; border: 2px solid #FF66B3; box-shadow: 0 8px 25px rgba(0,0,0,0.4);">
                <img src="{profile_img}" width="150" style="border-radius: 50%; border: 5px solid #FF0066; box-shadow: 0 0 20px rgba(255, 0, 102, 0.7); animation: pulse-profile 2s infinite alternate;">
                <h2 style="color: #FF66B3; margin-top: 25px; font-size: 2.2em; text-shadow: 0 0 10px rgba(255, 102, 179, 0.5);">Pronto para se perder comigo, amor?</h2>
                <p style="font-size: 1.3em; color: #E0E0E0; margin-top: 15px;">Estou aqui, só para você. Que comece a sedução!</p>
            </div>
            <style>
                @keyframes pulse-profile {
                    from { transform: scale(1); box-shadow: 0 0 20px rgba(255, 0, 102, 0.7); }
                    to { transform: scale(1.05); box-shadow: 0 0 30px rgba(255, 0, 102, 0.9); }
                }
            </style>
            """.format(profile_img=Config.IMG_PROFILE), unsafe_allow_html=True)
            
            if st.button("COMEÇAR A CONVERSAR COM PALOMA AGORA!", type="primary", use_container_width=True, key="start_chat_initial"):
                st.session_state.update({
                    'chat_started': True,
                    'current_page': 'chat',
                    'audio_sent': False # Garante que o áudio seja enviado ao iniciar o chat
                })
                save_persistent_data()
                st.rerun()
        st.stop() # Interrompe a execução aqui para mostrar a tela de início do chat

    # 5. Roteamento de Páginas (Após verificação de idade e início de chat, se aplicável)
    if st.session_state.current_page == "home":
        NewPages.show_home_page()
    elif st.session_state.current_page == "gallery":
        UiService.show_gallery_page(conn)
    elif st.session_state.current_page == "offers":
        NewPages.show_offers_page()
    elif st.session_state.current_page == "chat":
        UiService.enhanced_chat_ui(conn)
    else: # Fallback para o chat se a página for desconhecida
        UiService.enhanced_chat_ui(conn)
    
    save_persistent_data() # Salva o estado final da sessão

if __name__ == "__main__":
    main()
