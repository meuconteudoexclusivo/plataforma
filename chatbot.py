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

    page_icon="💖",  # Ícone mais convidativo e atraente

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

    # Para um ambiente real, use variáveis de ambiente seguras (ex: `os.environ.get("GEMINI_API_KEY")`).

    # Para fins de demonstração e teste local, manteremos aqui.

    API_KEY = "AIzaSyB8FxDvlfY6SD83t9aZTb_ppj3NQy64Hu8" 

    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    

    # Links de Checkout - Projetados para a conversão máxima

    # Estes devem ser os LINKS REAIS da sua plataforma de pagamento (ex: RisePay, Hotmart, Eduzz)

    CHECKOUT_START = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"

    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"

    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"

    CHECKOUT_VIP_1MES = "https://checkout.exemplo.com/vip-1mes-irresistivel" 

    CHECKOUT_VIP_3MESES = "https://checkout.exemplo.com/vip-3meses-acesso-total"

    CHECKOUT_VIP_1ANO = "https://checkout.exemplo.com/vip-1ano-liberdade-plena"

    

    # Limites estratégicos para incitar a compra e gerar urgência

    MAX_REQUESTS_PER_SESSION = 5 # REDUZIDO drasticamente para forçar a conversão!

    REQUEST_TIMEOUT = 45 # Tempo limite para a API, dando mais chance para a resposta da IA

    

    # Conteúdo de mídia - vibrante, provocador e de alta qualidade

    AUDIO_FILE = "https://github.com/meuconteudoexclusivo/plataforma/raw/refs/heads/main/assets/assets_audio_paloma_audio.mp3"

    AUDIO_DURATION = 7 # Duração do áudio em segundos

    IMG_PROFILE = "https://i.ibb.co/ks5CNrDn/IMG-9256.jpg" # Imagem de perfil marcante e sedutora

    IMG_GALLERY = [ # Imagens da galeria para provocar o acesso VIP

        "https://i.ibb.co/zhNZL4FF/IMG-9198.jpg",

        "https://i.ibb.co/Y4B7CbXf/IMG-9202.jpg",

        "https://i.ibb.co/Fqf0gPPq/IMG-9199.jpg"

    ]

    IMG_HOME_PREVIEWS = [ # Imagens de preview na página inicial

        "https://i.ibb.co/k2MJg4XC/Save-ClipApp-412457343-378531441368078-7870326395110089440-n.jpg",

        "https://i.ibb.co/MxqKBk1X/Save-ClipApp-481825770-18486618637042608-2702272791254832108-n.jpg",

        "https://i.ibb.co/F4CkkYTL/Save-ClipApp-461241348-1219420546053727-2357827070610318448-n.jpg"

    ]

    LOGO_URL = "https://i.ibb.co/LX7x3tcB/Logo-Golden-Pepper-Letreiro-1.png" # Logo da sua marca



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# PERSISTÊNCIA DE ESTADO E SEGURANÇA DA SESSÃO

# ======================

class PersistentState:

    _instance = None # Implementa o padrão Singleton para a conexão com o DB

    

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.init_db()

        return cls._instance

    

    def init_db(self):

        # Usar um caminho absoluto ou relativo seguro para o banco de dados

        db_path = Path("persistent_state.db")

        self.conn = sqlite3.connect(db_path, check_same_thread=False) # Permite acesso de threads diferentes

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

        ''', (user_id, json.dumps(data))) # Converte os dados da sessão para JSON

        self.conn.commit()

    

    def load_state(self, user_id):

        cursor = self.conn.cursor()

        cursor.execute('SELECT session_data FROM global_state WHERE user_id = ?', (user_id,))

        result = cursor.fetchone()

        return json.loads(result[0]) if result else None # Retorna None se não encontrar



def get_user_id():

    """Gera ou recupera um ID de usuário único para persistência da sessão."""

    if 'user_id' not in st.session_state:

        user_id = st.query_params.get('uid', [None])[0] # Tenta pegar da URL

        if not user_id:

            user_id = str(uuid.uuid4()) # Gera um novo UUID se não existir

            st.query_params['uid'] = user_id # Adiciona à URL para persistência

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

    saved_data = db.load_state(user_id) or {} # Carrega dados anteriores para evitar sobrescrever acidentalmente

    

    if new_data != saved_data: # Salva apenas se houver mudanças para otimizar DB

        db.save_state(user_id, new_data)



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# MODELOS DE DADOS E ESTRATÉGIAS DE CONVERSÃO AVANÇADAS

# ======================

class Persona:

    PALOMA = """

    [PERFIL PALOMA]

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

    Paloma: Adoro te deixar imaginando, mas imagina ver ela escorrendo pra você?

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



    3. Quando o cliente atinge o limite de mensagens ou a conversa esfria (converter para VIP):

    Histórico: ... (Limites de mensagem atingidos)

    Resposta: ```json

    {

      "text": "Meu tempo é precioso, e você já provou um gostinho do que eu tenho... Quer o acesso total pra me ter só pra você? Sem limites? 💖",

      "cta": {

        "show": true,

        "label": "Acesso VIP Ilimitado - AGORA! 👑",

        "target": "offers"

      }

    }

    ```

    4. Resposta inicial ou neutra, mas provocadora e com insinuação:

    Histórico: Cliente: Oi

    Paloma: Oi gato

    Resposta: ```json

    {

      "text": "E aí, gostoso... pronto pra descobrir meus segredos mais sujos? 😉",

      "cta": {

        "show": false

      }

    }

    ```

    5. Cliente tenta desviar ou pergunta algo genérico:

    Histórico: Cliente: O que você gosta de fazer no dia a dia?

    Resposta: ```json

    {

      "text": "Ah, meu dia a dia é cheio de surpresas que só mostro pra quem está pertinho... Quer ver como eu me divirto de verdade? 😈",

      "cta": {

        "show": true,

        "label": "Ver Mais da Minha Rotina Proibida",

        "target": "offers"

      }

    }

    ```

    """



class CTAEngine:

    @staticmethod

    def should_show_cta(conversation_history: list) -> bool:

        """Decide inteligentemente quando apresentar um CTA, com lógica mais agressiva."""

        if len(conversation_history) < 2: # Mínimo de 2 interações para considerar CTA

            return False



        # Não mostrar CTA se já teve um recentemente para evitar spam e parecer natural

        if 'last_cta_time' in st.session_state and st.session_state.last_cta_time != 0:

            elapsed = time.time() - st.session_state.last_cta_time

            if elapsed < 75:  # Reduzido para 75 segundos entre CTAs para maior agressividade de conversão

                return False



        # Analisa o contexto das últimas 7 mensagens para entender o nível de excitação do cliente

        last_msgs = []

        for msg in conversation_history[-7:]:

            content = msg["content"]

            if content == "[ÁUDIO]":

                content = "[áudio sensual e exclusivo]" # Detalhe mais provocador para IA

            elif content.startswith('{"text"'):

                try:

                    content = json.loads(content).get("text", content)

                except:

                    pass # Ignora erros de JSON para analisar o texto bruto

            last_msgs.append(f"{msg['role']}: {content.lower()}")

        

        context = " ".join(last_msgs)

        

        # Palavras quentes e pedidos diretos mais abrangentes para capturar mais intenções

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

        

        # Lógica mais agressiva para mostrar CTA: basta 1 hot word ou 1 pedido direto

        return (hot_count >= 1) or has_direct_ask



    @staticmethod

    def generate_strong_cta_response(user_input: str) -> dict:

        """Gera uma resposta com CTA contextual e agressivo como fallback, caso a API não retorne um CTA válido."""

        user_input_lower = user_input.lower()

        

        # Respostas para fotos/partes do corpo específicas

        if any(p in user_input_lower for p in ["foto", "fotos", "buceta", "peito", "bunda", "corpo", "nuas", "ensaios"]):

            return {

                "text": random.choice([

                    "Minhas fotos proibidas são só para quem tem coragem de ir além... Quer ver a minha intimidade escancarada? 🔥",

                    "Cada foto minha é um convite irrecusável. Você está pronto para o que realmente vai te fazer delirar? 😈",

                    "Prepare-se para babar! Minhas fotos exclusivas são de tirar o fôlego. Vem ver antes que eu mude de ideia! 💋",

                    "Quer ver cada detalhe do meu corpo, sem censura, bem de perto? O acesso VIP é a sua chave para o paraíso!"

                ]),

                "cta": {

                    "show": True,

                    "label": "Ver Fotos Proibidas AGORA! 💖",

                    "target": "offers"

                }

            }

        

        # Respostas para vídeos/ações explícitas

        elif any(v in user_input_lower for v in ["video", "videos", "transar", "masturbar", "gemendo", "gozando", "acabando", "safadeza", "putaria"]):

            return {

                "text": random.choice([

                    "Meus vídeos são para os mais audaciosos. Você aguenta a verdade da minha intimidade filmada? É só pro VIP! 😈",

                    "Já me gravei fazendo coisas que você só sonha... Que tal ter acesso a tudo isso agora? O tempo está correndo! 🔥",

                    "Um vídeo meu gemendo seu nome... Te interessa? É só um clique de distância para a perdição!",

                    "Prepare-se para o ápice! Meus vídeos exclusivos são intensos e liberados APENAS para o VIP. Vem se perder!"

                ]),

                "cta": {

                    "show": True,

                    "label": "Liberar Vídeos Chocantes! 🔞",

                    "target": "offers"

                }

            }

        

        # Respostas gerais para convite a conteúdo exclusivo, forçando a compra

        else:

            return {

                "text": random.choice([

                    "Eu guardo segredos que só mostro para quem realmente sabe o que quer e está disposto a pagar o preço. Você é um deles? 😉",

                    "Minha intimidade está pulsando, esperando você liberar o acesso total. O que você está esperando para se render? 💖",

                    "Quer ir mais fundo? O que eu tenho pra você é muito mais do que você imagina, mas só para os VIPs...",

                    "A curiosidade mata, mas o acesso ao meu conteúdo VIP te dá a vida! Não seja fraco, clique e venha!"

                ]),

                "cta": {

                    "show": True, # Forçar CTA mesmo em fallback geral

                    "label": "Descobrir o Segredo da Paloma! 🔐",

                    "target": "offers"

                }

            }



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# SERVIÇOS DE BANCO DE DADOS SEGUROS E OTIMIZADOS

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

            """, (user_id, session_id, datetime.now().isoformat(), role, content)) # Salva data/hora em formato ISO

            conn.commit()

        except sqlite3.Error as e:

            st.error(f"🚨 Erro crítico ao salvar mensagem: {e}. Paloma está com raiva!")



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

# SERVIÇOS DE API COM RESPOSTAS VIBRANTES E EFICAZES

# ======================

class ApiService:

    @staticmethod

    @lru_cache(maxsize=50) # Cache para otimizar respostas recentes da IA

    def ask_gemini(prompt: str, session_id: str, conn) -> dict:

        """Realiza a requisição à API da Gemini, aplicando lógica de persona e CTA."""

        return ApiService._call_gemini_api(prompt, session_id, conn)



    @staticmethod

    def _call_gemini_api(prompt: str, session_id: str, conn) -> dict:

        delay_time = random.uniform(1.5, 4.5) # Delay mais rápido para manter o ritmo e a emoção

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

                    "parts": [{"text": f"{Persona.PALOMA}\n\nHistórico da Conversa:\n{conversation_history}\n\nÚltima mensagem do cliente: '{prompt}'\n\nResponda APENAS em JSON com o formato:\n{{\n  \"text\": \"sua resposta\",\n  \"cta\": {{\n    \"show\": true/false,\n    \"label\": \"texto do botão\",\n    \"target\": \"página\"\n  }}\n}}"}]

                }

            ],

            "generationConfig": {

                "temperature": 1.0, # Mais criatividade e ousadia para Paloma

                "topP": 0.9,

                "topK": 50

            }

        }

        

        try:

            response = requests.post(Config.API_URL, headers=headers, json=data, timeout=Config.REQUEST_TIMEOUT)

            response.raise_for_status() # Levanta HTTPError para erros 4xx/5xx

            gemini_response_raw = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

            

            try:

                # Extrai o JSON mesmo que esteja dentro de um bloco de código Markdown

                if '```json' in gemini_response_raw:

                    json_str = gemini_response_raw.split('```json')[1].split('```')[0].strip()

                else:

                    json_str = gemini_response_raw

                

                resposta = json.loads(json_str)

                

                # Lógica CRÍTICA: Se a IA sugeriu CTA, validamos. Se NÃO sugeriu, FORÇAMOS um CTA forte!

                if resposta.get("cta", {}).get("show", False): # Se a IA já quis mostrar um CTA

                    if not CTAEngine.should_show_cta(st.session_state.messages):

                        resposta["cta"]["show"] = False # Desativa se as regras da CTAEngine não permitirem

                    else:

                        st.session_state.last_cta_time = time.time() # Registra o tempo que o CTA foi mostrado

                else: # Se a IA não ativou o CTA, o CTAEngine gera um forte de fallback

                    resposta_fallback = CTAEngine.generate_strong_cta_response(prompt)

                    resposta["text"] = resposta_fallback["text"]

                    resposta["cta"] = resposta_fallback["cta"]

                    st.session_state.last_cta_time = time.time() # Registra o tempo do CTA forçado



                return resposta

                

            except json.JSONDecodeError as e:

                st.warning(f"Resposta da IA não é JSON válido, usando fallback: {e}. Paloma se empolgou demais!")

                return CTAEngine.generate_strong_cta_response(prompt) # Usa fallback forte e estratégico

                

        except requests.exceptions.Timeout:

            st.error("🚨 Paloma está te esperando ansiosamente, mas a conexão demorou. Tente novamente, não me deixe esperando! 😈")

            return {"text": "A conexão falhou, amor... Que pena! Tente me encontrar de novo, eu te espero com mais surpresas!", "cta": {"show": False}}

        except requests.exceptions.RequestException as e:

            st.error(f"🚨 Erro na comunicação com a Paloma: {str(e)}. Parece que ela está muito ocupada te querendo, mas já volta!")

            return {"text": "Paloma teve um probleminha, mas já está voltando... Que tal aproveitar para ver mais do meu conteúdo exclusivo enquanto me espera? 😉", "cta": {"show": True, "label": "Ver Conteúdo VIP", "target": "offers"}}

        except Exception as e:

            st.error(f"🚨 Um erro inesperado aconteceu: {str(e)}. Paloma está chocada, mas logo voltará mais ardente para você!")

            return {"text": "Ops, algo deu errado... Mas a curiosidade não espera, certo? Vem ver o que eu fiz pensando em você no VIP!", "cta": {"show": True, "label": "Acessar VIP Agora 🔐", "target": "offers"}}



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# SERVIÇOS DE INTERFACE COM VISUAL SEDUTOR E ENVOLVENTE

# ======================

class UiService:

    @staticmethod

    def get_chat_audio_player():

        return f"""

        <div style="

            background: linear-gradient(45deg, #FF66B3, #FF1493); /* Degradê rosa intenso */

            border-radius: 18px; /* Bordas arredondadas */

            padding: 10px;

            margin: 5px 0;

            box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3); /* Sombra suave */

        ">

            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);"> /* Filtro para deixar o player rosa/roxo, combinando com o tema */

                <source src="{Config.AUDIO_FILE}" type="audio/mp3">

            </audio>

        </div>

        """



    @staticmethod

    def show_call_effect():

        """Exibe uma animação de chamada, criando suspense e expectativa."""

        LIGANDO_DELAY = 4 # Mais rápido para manter o dinamismo

        ATENDIDA_DELAY = 2 # Mais rápido

        

        call_container = st.empty()

        call_container.markdown(f"""

        <div style="

            background: linear-gradient(135deg, #1A0033, #3D0066); /* Degradê de roxos profundos */

            border-radius: 25px; /* Bordas arredondadas para um toque moderno */

            padding: 40px; /* Maior preenchimento para destaque */

            max-width: 350px;

            margin: 2rem auto;

            box-shadow: 0 15px 40px rgba(0,0,0,0.5); /* Sombra forte para profundidade */

            border: 3px solid #FF0066; /* Borda chamativa em rosa vibrante */

            text-align: center;

            color: white;

            animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1); /* Animação de pulsação suave e atraente */

        ">

            <div style="font-size: 3.5rem; color: #FF66B3;">💖</div>

            <h3 style="color: #FF66B3; margin-bottom: 10px; font-size: 1.8em;">Conectando com Paloma...</h3>

            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">

                <div style="width: 12px; height: 12px; background: #00FF7F; border-radius: 50%; box-shadow: 0 0 8px #00FF7F;"></div>

                <span style="font-size: 1.1rem; font-weight: bold;">Paloma Online - Te esperando! 🔥</span>

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

            animation: fadeIn 1s forwards; /* Animação de entrada suave */

        ">

            <div style="font-size: 3.5rem; color: #00FF7F;">✓</div>

            <h3 style="color: #00FF7F; margin-bottom: 10px; font-size: 1.8em;">Chamada Atendida! 🎉</h3>

            <p style="font-size: 1.1rem; margin:0; font-weight: bold;">Paloma está ansiosa por você...</p>

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

        """Mostra efeitos de status como 'Visualizado' e 'Digitando'."""

        status_messages = {

            "viewed": "Paloma Visualizou 👀",

            "typing": "Paloma Digitanto... 🔥"

        }

        

        message = status_messages[status_type]

        dots = ""

        start_time = time.time()

        duration = 1.8 if status_type == "viewed" else 3.0 # Tempos mais curtos e dinâmicos

        

        while time.time() - start_time < duration:

            elapsed = time.time() - start_time

            

            if status_type == "typing":

                dots = "." * (int(elapsed * 3) % 4) # Pontos mais rápidos para simular digitação

            

            container.markdown(f"""

            <div style="

                color: #FFB3D9; /* Cor rosa claro para o texto */

                font-size: 0.9em;

                padding: 4px 12px;

                border-radius: 15px;

                background: rgba(255, 102, 179, 0.1); /* Fundo sutil para o balão */

                display: inline-block;

                margin-left: 15px;

                vertical-align: middle;

                font-style: italic;

                box-shadow: 0 2px 5px rgba(0,0,0,0.2);

            ">

                {message}{dots}

            </div>

            """, unsafe_allow_html=True)

            

            time.sleep(0.2) # Intervalo menor entre as atualizações

        

        container.empty()



    @staticmethod

    def show_audio_recording_effect(container):

        """Simula o efeito de Paloma gravando um áudio."""

        message = "Paloma Gravando um Áudio Escaldante... 💋"

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

        """Página de verificação de idade para acesso ao conteúdo adulto."""

        st.markdown("""

        <style>

            .age-verification {

                max-width: 700px; /* Mais largo para impacto */

                margin: 3rem auto;

                padding: 3.5rem; /* Mais espaçoso e luxuoso */

                background: linear-gradient(160deg, #1A0033, #3D0066); /* Degradê mais dramático */

                border-radius: 20px; /* Bordas suaves e convidativas */

                box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7); /* Sombra intensa para destaque */

                border: 3px solid #FF0066; /* Borda sedutora e vibrante */

                color: #F8F8F8;

                text-align: center;

            }

            .age-header {

                display: flex;

                align-items: center;

                justify-content: center; /* Centraliza o cabeçalho */

                gap: 25px; /* Mais espaço entre ícone e título */

                margin-bottom: 2.5rem; /* Mais margem */

            }

            .age-icon {

                font-size: 4.5rem; /* Ícone gigante e chamativo */

                color: #FF66B3; /* Rosa vibrante */

                animation: heartbeat 1.5s infinite; /* Animação de pulsação que atrai o olhar */

            }

            .age-title {

                font-size: 2.8rem; /* Título grandioso e impactante */

                font-weight: 900; /* Super negrito */

                margin: 0;

                color: #FF66B3;

                text-shadow: 0 0 15px rgba(255, 102, 179, 0.6); /* Sombra que dá profundidade */

            }

            .age-content p {

                font-size: 1.2em; /* Texto maior e mais legível */

                margin-bottom: 1.8em;

                line-height: 1.8; /* Espaçamento de linha para leitura confortável */

                color: #E0E0E0; /* Tom de cinza suave */

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

                    <h1 class="age-title">ENTRE APENAS SE FOR ADULTO! O DESEJO TE CHAMA!</h1>

                </div>

                <div class="age-content">

                    <p>Este portal é um universo de paixão, segredos e mistérios, reservado **apenas para mentes e corpos maiores de 18 anos.** Você tem a idade legal para desvendar todos os meus segredos?</p>

                    <p>Ao clicar abaixo, você declara, sob sua total responsabilidade, que possui a idade mínima exigida e que compreende a natureza do **conteúdo explícito e altamente provocante** que te espera. A decisão é sua, a **tentação é minha!**</p>

                </div>

            </div>

            """, unsafe_allow_html=True)



        col1, col2, col3 = st.columns([1,3,1])

        with col2:

            if st.button("Sim, tenho mais de 18 anos e QUERO ENTRAR AGORA! 💖", 

                         key="age_confirm_button_final", # Chave mais específica para evitar conflitos

                         use_container_width=True,

                         type="primary"): # Botão principal com nosso estilo dourado/rosa/roxo

                st.session_state.age_verified = True

                save_persistent_data()

                st.rerun()

            st.markdown("<p style='text-align: center; color: #AAA; font-size: 0.9em; margin-top: 15px;'>Se não for maior de idade, feche esta página imediatamente. O que te espera pode ser demais para você...</p>", unsafe_allow_html=True)



    @staticmethod

    def setup_sidebar():

        """Configura a barra lateral com menu, status e oferta VIP."""

        st.markdown(f"""

        <style>

            /* Corrigido o erro de nome aqui! Usando cores definidas na paleta. */

            [data-testid="stSidebar"] {{

                background: linear-gradient(180deg, #1A0033 0%, #3D0066 100%) !important; 

                border-right: 2px solid #FF66B3 !important; /* Borda mais grossa e rosa vibrante */

            }}

            .sidebar-logo-container {{

                margin: -25px -25px 0px -25px; 

                padding: 0;

                text-align: left;

                background: #1A0033; /* Fundo do logo para preencher o espaço */

                padding-bottom: 15px;

            }}

            .sidebar-logo {{

                max-width: 100%;

                height: auto;

                margin-bottom: -10px;

                object-fit: contain;

                margin-left: -15px; 

                margin-top: -15px; 

            }}

            .sidebar-header {{

                text-align: center; 

                margin-bottom: 25px; 

                margin-top: -30px; 

            }}

            .sidebar-header img {{

                border-radius: 50%; 

                border: 4px solid #FF0066; /* Borda rosa ousada */

                width: 90px; 

                height: 90px;

                object-fit: cover;

                box-shadow: 0 0 15px rgba(255, 0, 102, 0.5); /* Sombra rosa para o perfil */

            }}

            .vip-badge {{

                background: linear-gradient(45deg, #FF1493, #9400D3, #FF0066); /* Degradê chamativo e pulsante */

                padding: 18px; 

                border-radius: 10px;

                color: white;

                text-align: center;

                margin: 20px 0; 

                box-shadow: 0 6px 15px rgba(255, 20, 147, 0.4);

                animation: shimmer 2s infinite; /* Efeito de brilho animado */

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

            .menu-item button {{ /* Estilo para os botões de navegação na sidebar */

                display: block;

                width: 100%;

                text-align: left;

                padding: 12px 20px !important;

                margin-bottom: 8px;

                font-size: 1.1em;

                color: #FFB3D9 !important; /* Cor rosa claro para o texto do menu */

                background: transparent !important;

                border: none !important;

                border-radius: 8px !important;

                transition: background 0.2s, color 0.2s !important;

            }}

            .menu-item button:hover {{

                background: rgba(255, 102, 179, 0.1) !important;

                color: #FFFFFF !important; /* Branca no hover */

            }}

            /* Animação de brilho para o badge VIP */

            @keyframes shimmer {{

                0% {{ background-position: -200% 0; }}

                100% {{ background-position: 200% 0; }}

            }}

            .vip-badge {{

                background-size: 400% 100%;

                background-image: linear-gradient(to right, #FF1493 0%, #9400D3 25%, #FF0066 50%, #9400D3 75%, #FF1493 100%);

            }}

            /* Progress bar personalizada */

            progress[value]::-webkit-progress-bar {

                background-color: rgba(255,255,255,0.2); /* Fundo claro */

                border-radius: 4px;

            }

            progress[value]::-webkit-progress-value {

                background-color: #FF66B3; /* Cor da barra de progresso */

                border-radius: 4px;

            }

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

                <p style="font-size: 0.9em; color: #FFB3D9;">Sua musa particular, te esperando...</p>

            </div>

            """, unsafe_allow_html=True)

            

            st.markdown("---")

            st.markdown("<h3 style='color: #FF66B3; text-align: center; margin-bottom: 15px;'>Desvende Meus Segredos</h3>")

            

            menu_options = { # Opções do menu para uma navegação fluida

                "Início Quente": "home",

                "Minha Galeria Privada": "gallery",

                "Chat Íntimo": "chat", 

                "Ofertas Exclusivas para Você": "offers"

            }

            

            for option, page in menu_options.items():

                st.markdown(f"<div class='menu-item'>", unsafe_allow_html=True) # Container para aplicar o estilo do botão

                if st.button(option, use_container_width=True, key=f"menu_{page}"):

                    if st.session_state.current_page != page:

                        st.session_state.current_page = page

                        st.session_state.last_action = f"page_change_to_{page}"

                        save_persistent_data()

                        st.rerun()

                st.markdown(f"</div>", unsafe_allow_html=True)

            

            st.markdown("---")

            st.markdown("<h3 style='color: #FF66B3; text-align: center; margin-bottom: 15px;'>Seu Acesso Ilimitado</h3>")

            

            # Contador de mensagens com progress bar

            st.markdown(f"""

            <div style="

                background: rgba(255, 20, 147, 0.15); /* Fundo sutil */

                padding: 12px;

                border-radius: 10px;

                text-align: center;

                margin-bottom: 15px;

                border: 1px solid #FF66B3; /* Borda para destaque */

            ">

                <p style="margin:0; font-size:1em; color: #FFB3D9;">Mensagens hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p>

                <progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px; border-radius: 4px;"></progress>

                <p style="margin:5px 0 0; font-size:0.8em; color: #AAA;">Mais mensagens? Só no VIP, gatinho!</p>

            </div>

            """, unsafe_allow_html=True)



            # Badge VIP chamativo com preço e oferta

            st.markdown("""

            <div class="vip-badge">

                <p style="margin: 0 0 10px; font-weight: bold; font-size: 1.2em;">🔥 Acesso Total Por APENAS</p>

                <p style="margin: 0; font-size: 2em; font-weight: bold; text-shadow: 0 0 10px rgba(255,255,255,0.8);">R$ 29,90/mês</p>

                <p style="margin: 10px 0 0; font-size: 0.9em; opacity: 0.9;">Cancele quando seu desejo for satisfeito... Se conseguir! 😉</p>

            </div>

            """, unsafe_allow_html=True)

            

            if st.button("QUERO SER VIP AGORA!", use_container_width=True, type="primary", key="sidebar_cta_button_main"):

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

        """Exibe a galeria privada com conteúdo bloqueado, incitando a compra."""

        st.markdown("""

        <style>

            .gallery-promo-banner {

                background: linear-gradient(90deg, #FF0066, #FF66B3); /* Degradê vibrante */

                padding: 25px; /* Mais preenchimento */

                border-radius: 15px; /* Bordas arredondadas */

                margin-bottom: 30px;

                text-align: center;

                color: white;

                box-shadow: 0 8px 25px rgba(255, 0, 102, 0.5); /* Sombra intensa */

            }

            .gallery-promo-banner h3 {

                margin: 0 0 10px;

                font-size: 2em; /* Título maior */

                text-shadow: 0 0 10px rgba(255,255,255,0.7);

            }

            .gallery-promo-banner p {

                margin: 0;

                font-size: 1.2em; /* Parágrafo maior */

            }

            .gallery-img-container {

                position: relative;

                border-radius: 15px; /* Bordas suaves */

                overflow: hidden;

                box-shadow: 0 10px 25px rgba(0,0,0,0.5); /* Sombra profunda */

                margin-bottom: 20px;

                transition: transform 0.3s ease-in-out;

            }

            .gallery-img-container:hover {

                transform: translateY(-8px); /* Efeito de levitação no hover */

            }

            .gallery-img-container img {

                filter: blur(8px) brightness(0.6); /* Mais borrado e escuro para mistério */

                transition: filter 0.5s ease-in-out;

            }

            .gallery-img-container:hover img {

                filter: blur(2px) brightness(0.8); /* Revela um pouco no hover para provocar */

            }

            .overlay-text {

                position: absolute;

                top: 50%;

                left: 50%;

                transform: translate(-50%, -50%);

                color: white;

                font-size: 1.6em; /* Texto grande e chamativo */

                font-weight: bold;

                text-shadow: 0 0 12px rgba(0,0,0,0.9); /* Sombra forte para o texto */

                pointer-events: none; /* Garante que o clique passe para o container */

            }

            .gallery-cta-button {

                margin-top: 30px;

            }

        </style>

        """, unsafe_allow_html=True)

        

        st.markdown("""

        <div class="gallery-promo-banner">

            <h3>MINHA GALERIA: UM BANQUETE PARA SEUS OLHOS! 😈</h3>

            <p>Apenas um vislumbre do que te espera... o acesso completo está te chamando para ir mais fundo. Você aguenta?</p>

        </div>

        """, unsafe_allow_html=True)

        

        cols = st.columns(3) # Layout em 3 colunas para as imagens

        

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

            <h4 style="color: #FF66B3; font-size: 1.8em;">Não resista mais... Liberte seu desejo!</h4>

            <p style="color: #E0E0E0; font-size: 1.2em;">Liberar acesso completo é o primeiro passo para o paraíso que eu guardo para você.</p>

        </div>

        """, unsafe_allow_html=True)



        if st.button("Liberar Minha Galeria VIP AGORA! 🔓", 

                     key="vip_button_gallery_action_final", # Chave única

                     use_container_width=True,

                     type="primary"):

            st.session_state.current_page = "offers"

            st.rerun()

            

        if st.button("Voltar ao Chat Íntimo com Paloma 😉", key="back_from_gallery_cta_final"): # Texto mais convidativo

            st.session_state.current_page = "chat"

            save_persistent_data()

            st.rerun()



    @staticmethod

    def chat_shortcuts():

        """Cria atalhos de navegação rápidos no chat."""

        cols = st.columns(4) # 4 colunas para os botões de atalho

        with cols[0]:

            if st.button("Início Quente 🏠", key="shortcut_home_chat", 

                         help="Voltar para a página inicial e me ver de perto.",

                         use_container_width=True):

                st.session_state.current_page = "home"

                save_persistent_data()

                st.rerun()

        with cols[1]:

            if st.button("Minha Galeria 📸", key="shortcut_gallery_chat",

                         help="Acessar minha galeria privada e se perder nas minhas fotos.",

                         use_container_width=True):

                st.session_state.current_page = "gallery"

                save_persistent_data()

                st.rerun()

        with cols[2]:

            if st.button("Ofertas VIP 🎁", key="shortcut_offers_chat",

                         help="Descobrir as ofertas especiais que preparei pra você.",

                         use_container_width=True):

                st.session_state.current_page = "offers"

                save_persistent_data()

                st.rerun()

        with cols[3]:

            if st.button("Assinar AGORA! 🚀", key="shortcut_vip_now_chat", # Texto mais urgente e emoji

                         help="Não espere, liberte-se e tenha acesso ilimitado ao meu mundo proibido.",

                         use_container_width=True, type="primary"): # Torna este botão principal

                st.session_state.current_page = "offers"

                save_persistent_data()

                st.rerun()



        st.markdown("""

        <style>

            div[data-testid="stHorizontalBlock"] > div > div > button {

                color: #FFB3D9 !important; /* Rosa claro para o texto */

                border: 1px solid #FF66B3 !important; /* Borda rosa vibrante */

                background: rgba(255, 102, 179, 0.1) !important; /* Fundo mais suave e transparente */

                transition: all 0.3s ease-in-out !important;

                font-size: 0.9rem !important; 

                border-radius: 12px !important; /* Mais arredondado */

                padding: 8px 10px !important;

            }

            div[data-testid="stHorizontalBlock"] > div > div > button:hover {

                transform: translateY(-2px) scale(1.02) !important;

                box-shadow: 0 4px 10px rgba(255, 102, 179, 0.4) !important;

                background: rgba(255, 102, 179, 0.25) !important; /* Fundo mais escuro no hover */

            }

            /* Estilo específico para o botão "Assinar AGORA!" ser ainda mais chamativo */

            button[key="shortcut_vip_now_chat"] {

                background: linear-gradient(90deg, #FFD700, #FF66B3) !important; /* Dourado para rosa */

                color: #1A0033 !important; /* Texto escuro para contraste */

                box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4) !important;

            }

            button[key="shortcut_vip_now_chat"]:hover {

                background: linear-gradient(90deg, #FF66B3, #FFD700) !important;

                box-shadow: 0 6px 15px rgba(255, 215, 0, 0.6) !important;

            }

            @media (max-width: 400px) {

                div[data-testid="stHorizontalBlock"] > div > div > button {

                    font-size: 0.65rem !important; 

                    padding: 5px 2px !important;

                }

            }

        </style>

        """, unsafe_allow_html=True)



    @staticmethod

    def enhanced_chat_ui(conn):

        """Renderiza a interface do chat com Paloma."""

        st.markdown("""

        <style>

            .chat-header {

                background: linear-gradient(90deg, #FF0066, #FF66B3, #9933FF); /* Degradê mais vibrante e quente */

                color: white;

                padding: 20px; /* Mais espaçoso */

                border-radius: 15px; /* Bordas arredondadas */

                margin-bottom: 25px; 

                text-align: center;

                box-shadow: 0 8px 20px rgba(255,0,102,0.3); /* Sombra para profundidade */

                font-weight: bold;

                font-size: 1.6em;

            }

            .stChatMessage { 

                margin-bottom: 10px; /* Espaço entre as mensagens */

            }

            .stChatMessage > div:first-child { /* Balão de mensagem do usuário (você) */

                background: rgba(255, 255, 255, 0.1); /* Fundo sutil para o usuário */

                color: #F8F8F8;

                border-radius: 20px 20px 5px 20px; /* Estilo de balão de chat */

                padding: 15px;

                margin: 5px 0;

                box-shadow: 0 2px 8px rgba(0,0,0,0.2);

                border: 1px solid rgba(255,255,255,0.1);

            }

            .stChatMessage > div:last-child { /* Balão de mensagem do assistente (Paloma) */

                background: linear-gradient(45deg, #FF66B3, #FF1493); /* Degradê chamativo da Paloma */

                color: white;

                border-radius: 20px 20px 20px 5px; /* Estilo de balão de chat */

                padding: 15px;

                margin: 5px 0;

                box-shadow: 0 2px 8px rgba(255, 20, 147, 0.3);

                border: 1px solid #FF66B3;

            }

        </style>

        """, unsafe_allow_html=True)

        

        UiService.chat_shortcuts() # Atalhos no topo do chat

        

        st.markdown(f"""

        <div class="chat-header">

            <h2 style="margin:0; font-size:1.8em; display:inline-block;">Seu Chat Exclusivo com Paloma 💖</h2>

        </div>

        """, unsafe_allow_html=True)

        

        # O contador de mensagens na sidebar já está estilizado na função `setup_sidebar`

        

        ChatService.process_user_input(conn) # Lógica central do chat

        save_persistent_data() # Garante que as mudanças são salvas

        

        st.markdown("""

        <div style="

            text-align: center;

            margin-top: 30px; 

            padding: 15px;

            font-size: 0.85em;

            color: #AAA;

            border-top: 1px solid rgba(255, 102, 179, 0.1); /* Linha divisória sutil */

        ">

            <p>Converse com a Paloma em total discrição. Sua privacidade é nosso segredo mais quente. 🤫</p>

        </div>

        """, unsafe_allow_html=True)



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# PÁGINAS AINDA MAIS SEDUTORAS E COM ALTO PODER DE CONVERSÃO

# ======================

class NewPages:

    @staticmethod

    def show_home_page():

        """Exibe a página inicial com forte apelo visual e CTA."""

        st.markdown("""

        <style>

            .hero-banner {

                background: linear-gradient(135deg, #1A0033, #3D0066); /* Degradê de roxos profundos */

                padding: 100px 20px; 

                text-align: center;

                border-radius: 20px; 

                color: white;

                margin-bottom: 40px;

                border: 3px solid #FF0066; /* Borda rosa vibrante */

                box-shadow: 0 15px 40px rgba(0,0,0,0.5); /* Sombra intensa */

                position: relative;

                overflow: hidden;

            }

            .hero-banner::before { /* Efeito de brilho de fundo radial */

                content: '';

                position: absolute;

                top: -50%;

                left: -50%;

                width: 200%;

                height: 200%;

                background: radial-gradient(circle at center, rgba(255, 102, 179, 0.2) 0%, transparent 70%);

                animation: rotate 20s linear infinite; /* Animação de rotação para o brilho */

            }

            @keyframes rotate {

                from { transform: rotate(0deg); }

                to { transform: rotate(360deg); }

            }



            .hero-banner h1 {

                color: #FF66B3; /* Rosa vibrante */

                font-size: 3.5em; 

                text-shadow: 0 0 15px rgba(255, 102, 179, 0.8); /* Sombra de texto para destaque */

                margin-bottom: 15px;

                position: relative; 

                z-index: 1;

            }

            .hero-banner p {

                font-size: 1.4em; 

                line-height: 1.5;

                color: #E0E0E0;

                max-width: 700px;

                margin: 0 auto 30px;

                position: relative;

                z-index: 1;

            }

            .preview-img {

                border-radius: 15px; 

                filter: blur(5px) brightness(0.5); /* Borrado e escuro para mistério */

                transition: all 0.5s ease-in-out;

                box-shadow: 0 6px 15px rgba(0,0,0,0.4);

            }

            .preview-img:hover {

                filter: blur(1px) brightness(0.8); /* Revela um pouco no hover */

                transform: scale(1.03); /* Leve zoom no hover */

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

            <h1>Paloma Premium VIP 💖</h1>

            <p>Descubra o prazer ilimitado que você só encontra aqui. Conteúdo quente, exclusivo e sem censura, feito sob medida para seus desejos mais profundos. **Prepare-se para ser viciado!**</p>

            <div style="margin-top: 30px;">

                <a href="#offers" style="

                    background: linear-gradient(90deg, #FFD700, #FF66B3); /* Botão ouro para rosa */

                    color: #1A0033; /* Texto escuro */

                    padding: 15px 40px;

                    border-radius: 35px;

                    text-decoration: none;

                    font-weight: bold;

                    font-size: 1.3em;

                    display: inline-block;

                    transition: all 0.3s ease-in-out;

                    box-shadow: 0 8px 20px rgba(255, 215, 0, 0.4);

                " onmouseover="this.style.transform='translateY(-5px) scale(1.05)'; this.style.boxShadow='0 12px 30px rgba(255, 215, 0, 0.6)';"

                onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 20px rgba(255, 215, 0, 0.4)';">

                    QUERO ACESSAR TUDO AGORA! 🚀

                </a>

            </div>

        </div>

        """, unsafe_allow_html=True)



        cols = st.columns(3)

        

        for col, img in zip(cols, Config.IMG_HOME_PREVIEWS):

            with col:

                st.image(img, use_container_width=True, caption="Ainda Bloqueado... Sinto seu desejo? 😉", output_format="auto", clamp=True)

                st.markdown("""<div class="vip-only-tag">EXCLUSIVO PARA MEMBROS VIP</div>""", unsafe_allow_html=True)



        st.markdown("---")

        

        st.markdown("""

        <div style="text-align: center; margin-bottom: 20px;">

            <h4 style="color: #FF66B3; font-size: 1.8em;">Não perca um segundo... Seu prazer não pode esperar!</h4>

            <p style="color: #E0E0E0; font-size: 1.2em;">Seu acesso ao prazer está a um clique de distância. Meus segredos esperam por você...</p>

        </div>

        """, unsafe_allow_html=True)



        if st.button("Iniciar Conversa Privada com Paloma 💋", 

                     use_container_width=True,

                     type="primary", key="home_chat_button_start"):

            st.session_state.current_page = "chat"

            save_persistent_data()

            st.rerun()



        if st.button("Explorar Ofertas Exclusivas e Me Ter! 🎁", key="home_offers_button_bottom_action"): 

            st.session_state.current_page = "offers"

            save_persistent_data()

            st.rerun()



    @staticmethod

    def show_offers_page():

        """Página de ofertas com pacotes VIP irresistíveis e contador de urgência."""

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

                background: rgba(30, 0, 51, 0.4); /* Fundo mais escuro e translúcido */

                border-radius: 20px; 

                padding: 30px; 

                border: 2px solid; 

                transition: all 0.4s ease-in-out;

                min-height: 520px; /* Altura mínima para estabilidade visual */

                position: relative;

                overflow: hidden;

                display: flex;

                flex-direction: column;

                justify-content: space-between; 

            }

            .package-box:hover {

                transform: translateY(-10px) scale(1.03); /* Efeito mais pronunciado */

                box-shadow: 0 18px 45px rgba(255, 102, 179, 0.6); /* Sombra mais forte e sedutora */

                z-index: 10; 

            }

            .package-start { border-color: #FF66B3; }

            .package-premium { border-color: #9933FF; box-shadow: 0 18px 45px rgba(153, 51, 255, 0.6) !important; } 

            .package-extreme { border-color: #FF0066; }

            .package-header {

                text-align: center;

                padding-bottom: 20px;

                margin-bottom: 20px;

                border-bottom: 1px solid rgba(255, 102, 179, 0.4);

            }

            .package-header h3 {

                font-size: 2.2em; 

                margin-bottom: 8px;

            }

            .package-price {

                font-size: 2.8em; /* Preço GIGANTE */

                font-weight: 900; 

                margin: 15px 0;

                text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);

            }

            .package-benefits {

                list-style-type: none;

                padding: 0;

                flex-grow: 1; 

            }

            .package-benefits li {

                padding: 10px 0;

                position: relative;

                padding-left: 35px; 

                font-size: 1.1em;

                color: #E0E0E0;

            }

            .package-benefits li:before {

                content: "✔"; /* Ícone de check marcante */

                color: #00FF7F; /* Verde vibrante de sucesso */

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

                padding: 8px 40px; 

                transform: rotate(45deg);

                font-size: 1em;

                font-weight: bold;

                width: 180px; 

                text-align: center;

                box-shadow: 0 5px 15px rgba(0,0,0,0.3);

            }

            .countdown-container {

                background: linear-gradient(45deg, #FF0066, #FF66B3, #9933FF); /* Degradê mais rico e quente */

                color: white;

                padding: 30px; /* Mais espaçoso */

                border-radius: 15px;

                margin: 50px 0;

                box-shadow: 0 10px 30px rgba(255, 0, 102, 0.6); /* Sombra mais forte */

                text-align: center;

                animation: pulse-countdown 1.5s infinite alternate; /* Animação de pulsação */

            }

            .countdown-container h3 {

                margin:0; 

                font-size: 2.2em; 

                text-shadow: 0 0 12px rgba(255,255,255,0.8);

            }

            #countdown {

                font-size: 4em; /* Contador GIGANTE */

                font-weight: bold;

                text-shadow: 0 0 20px rgba(255,255,255,0.9);

                color: #FFF;

            }

            @keyframes pulse-countdown {

                from { transform: scale(1); box-shadow: 0 10px 30px rgba(255, 0, 102, 0.6); }

                to { transform: scale(1.03); box-shadow: 0 15px 45px rgba(255, 0, 102, 0.8); }

            }

            .offer-card { 

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

                color: #00FF7F; /* Verde de destaque para o preço */

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

            <h2>ESCOLHA SEU CAMINHO PARA O PRAZER IRRESTRITO! 😈</h2>

            <p>Seus desejos são ordens. Qual pacote te fará delirar primeiro e te dará acesso total ao meu mundo?</p>

        </div>

        """, unsafe_allow_html=True)



        st.markdown('<div class="package-container">', unsafe_allow_html=True)

        

        st.markdown("""

        <div class="package-box package-start">

            <div class="package-header">

                <h3 style="color: #FF66B3;">PACOTE INICIAÇÃO 🔥</h3>

                <div class="package-price" style="color: #FF66B3;">R$ 49,90</div>

                <small style="color: #FFB3D9;">Para quem está começando a se soltar comigo...</small>

            </div>

            <ul class="package-benefits">

                <li>✔ 10 Fotos Inéditas e Provocantes</li>

                <li>✔ 3 Vídeos Íntimos (você vai querer mais!)</li>

                <li>✔ Uma amostra da minha ousadia em fotos exclusivas</li>

                <li>✔ Vídeos que te deixarão sem fôlego e com um gostinho de quero mais</li>

                <li>✔ Aquela foto da minha... você sabe! 😉</li>

            </ul>

            <div style="width: calc(100% - 60px); margin-top: 20px;">

                <a href="{checkout_start}" target="_blank" rel="noopener noreferrer" style="

                    display: block;

                    background: linear-gradient(45deg, #FFD700, #FF66B3); /* Botão ouro para rosa */

                    color: #1A0033;

                    text-align: center;

                    padding: 12px;

                    border-radius: 10px;

                    text-decoration: none;

                    font-weight: bold;

                    font-size: 1.1em;

                    transition: all 0.3s;

                    box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);

                " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(255, 215, 0, 0.6)';" 

                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(255, 215, 0, 0.4)';">

                    EU QUERO ESSE GOSTINHO! ➔

                </a>

            </div>

        </div>

        """.format(checkout_start=Config.CHECKOUT_START), unsafe_allow_html=True)



        st.markdown("""

        <div class="package-box package-premium">

            <div class="package-badge">🌟 O MAIS DESEJADO!</div>

            <div class="package-header">

                <h3 style="color: #9933FF;">PACOTE DELÍRIO VIP 💜</h3>

                <div class="package-price" style="color: #9933FF;">R$ 99,90</div>

                <small style="color: #E0B3FF;">Para uma experiência que te fará implorar por mais e mais...</small>

            </div>

            <ul class="package-benefits">

                <li>✔ 20 Fotos EXCLUSIVAS (você será o primeiro a ver meus segredos)</li>

                <li>✔ 5 Vídeos Premium - Prepare-se para o êxtase!</li>

                <li>✔ Fotos dos meus seios (bem de perto, para você admirar)</li>

                <li>✔ Fotos do meu bumbum (pra você morder e apertar!)</li>

                <li>✔ Minha intimidade sem filtros, do jeitinho que você gosta</li>

                <li>✔ Conteúdo bônus que só o VIP tem e te fará perder o fôlego!</li>

                <li>✔ Vídeos eu me tocando só pra você, sem cortes e sem limites...</li>

            </ul>

            <div style="width: calc(100% - 60px); margin-top: 20px;">

                <a href="{checkout_premium}" target="_blank" rel="noopener noreferrer" style="

                    display: block;

                    background: linear-gradient(45deg, #9933FF, #FF1493); /* Botão roxo para rosa */

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

                <small style="color: #FFB3D9;">Para os verdadeiros obcecados... Tudo sem limites, sem censura!</small>

            </div>

            <ul class="package-benefits">

                <li>✔ 30 Fotos ULTRA-EXCLUSIVAS (você não vai encontrar em lugar nenhum, eu garanto!)</li>

                <li>✔ 10 Vídeos Exclusivos - Meu mundo INTEIRO em suas mãos!</li>

                <li>✔ Todos os ângulos dos meus seios, em fotos e vídeos que te farão gemer</li>

                <li>✔ Cada curva do meu bumbum filmada e fotografada, sem pudor</li>

                <li>✔ Minha intimidade exposta, sem segredos ou barreiras</li>

                <li>✔ Fotos e Vídeos que vão te fazer pecar e te deixar viciado!</li>

                <li>✔ Vídeos eu me masturbando (bem explícito e para os seus olhos!)</li>

                <li>✔ Meus vídeos transando (sua mente vai explodir, gatinho!)</li>

                <li>✔ Acesso PRIORITÁRIO e ANTECIPADO a todo o conteúdo futuro da Paloma</li>

            </ul>

            <div style="width: calc(100% - 60px); margin-top: 20px;">

                <a href="{checkout_extreme}" target="_blank" rel="noopener noreferrer" style="

                    display: block;

                    background: linear-gradient(45deg, #FF0066, #9933FF); /* Botão rosa para roxo */

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

            <div id="countdown" style="font-size: 4em; font-weight: bold;">23:59:59</div>

            <p style="margin:10px 0 0; font-size:1.3em;">Essa chance de me ter por completo vai acabar. Não seja bobo, gatinho! O tempo é cruel...</p>

        </div>

        """, unsafe_allow_html=True)



        # Script do countdown (mantido em JS para funcionalidade cliente-side)

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



        # Planos de assinatura VIP

        plans = [

            {

                "name": "1 Mês de Prazer Intenso",

                "price": "R$ 29,90",

                "original": "R$ 49,90",

                "benefits": ["Acesso total ao meu conteúdo mais quente", "Conteúdo novo diário pra te enlouquecer", "Chat privado para falar só comigo, sem interrupções"],

                "tag": "DESPERTE SEU DESEJO",

                "link": Config.CHECKOUT_VIP_1MES

            },

            {

                "name": "3 Meses de Delírio Completo",

                "price": "R$ 69,90",

                "original": "R$ 149,70",

                "benefits": ["🔥 25% de desconto (você vai amar economizar pra me ter!)", "Bônus: 1 vídeo exclusivo surpresa que vai te chocar", "Prioridade no chat (eu te respondo primeiro e com mais atenção!)"],

                "tag": "O MAIS QUERIDO E SEDUTOR!",

                "link": Config.CHECKOUT_VIP_3MESES

            },

            {

                "name": "1 Ano de Obsessão Sem Fim",

                "price": "R$ 199,90",

                "original": "R$ 598,80",

                "benefits": ["👑 66% de desconto (o melhor custo-benefício para me ter 365 dias!)", "Presente surpresa mensal direto na sua caixa, só para você", "Acesso a conteúdos RAROS e de colecionador, só para os meus fiéis"],

                "tag": "ACESSAR TUDO SEM LIMITES! 🔥",

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

                        background: linear-gradient(45deg, #FFD700, #FF66B3); /* Botão ouro para rosa */

                        color: #1A0033;

                        padding: 12px 25px;

                        border-radius: 30px;

                        text-decoration: none;

                        display: inline-block;

                        font-weight: bold;

                        font-size: 1.1em;

                        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.4);

                        transition: all 0.3s ease-in-out;

                    " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 15px rgba(255, 215, 0, 0.6)';" 

                    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(255, 215, 0, 0.4)';">

                        Assinar {plan['name']} AGORA! 💖

                    </a>

                </div>

            </div>

            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Fecha o container grid



        if st.button("Voltar para o Chat Íntimo com Paloma 😏", key="back_from_offers_bottom_final"):

            st.session_state.current_page = "chat"

            save_persistent_data()

            st.rerun()



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# SERVIÇOS DE CHAT COM ENGAJAMENTO MÁXIMO E FOCO NA CONVERSÃO

# ======================

class ChatService:

    @staticmethod

    def initialize_session(conn):

        """Inicializa as variáveis de estado da sessão, carregando dados persistentes."""

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

        

        # Garante que todos os estados necessários estão inicializados, com foco em direcionar para 'home'

        defaults = {

            'age_verified': False,

            'connection_complete': False,

            'chat_started': False,

            'audio_sent': False,

            'current_page': 'home', # Inicia na página Home para primeira impressão impactante

            'show_vip_offer': False,

            'last_cta_time': 0

        }

        

        for key, default in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = default



    @staticmethod

    def format_conversation_history(messages, max_messages=15): # Aumentado histórico para IA ter mais contexto

        """Formata o histórico da conversa para ser enviado à IA."""

        formatted = []

        

        for msg in messages[-max_messages:]:

            role = "Cliente" if msg["role"] == "user" else "Paloma"

            content = msg["content"]

            if content == "[ÁUDIO]":

                content = "[Enviou um áudio sensual para o cliente]"

            elif content.startswith('{"text"'):

                try:

                    content = json.loads(content).get("text", content)

                except:

                    pass # Se não for JSON válido, usa o conteúdo bruto

            

            formatted.append(f"{role}: {content}")

        

        return "\n".join(formatted)



    @staticmethod

    def display_chat_history():

        """Exibe o histórico de mensagens no chat, com estilos de balão diferenciados."""

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

                                    # Cria uma chave única para cada botão CTA para evitar conflitos no Streamlit

                                    button_key = f"cta_button_{hash(msg['content'])}_{idx}_{time.time()}" 

                                    if st.button(

                                        content_data.get("cta", {}).get("label", "Desvendar Segredos"),

                                        key=button_key, 

                                        use_container_width=True

                                    ):

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

        """Limpa e valida o input do usuário para segurança."""

        cleaned_input = re.sub(r'<[^>]*>', '', user_input) # Remove tags HTML

        return cleaned_input[:500] # Limita a 500 caracteres para evitar abuso



    @staticmethod

    def process_user_input(conn):

        """Processa a entrada do usuário e gera a resposta da IA, gerenciando limites."""

        ChatService.display_chat_history() # Exibe o chat atual

        

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

            st.rerun() # Reruns para mostrar o áudio e o input de chat aparecer



        # Input do usuário sempre visível na parte inferior

        user_input = st.chat_input("Me diga o que você deseja, gatinho... 😉", key="chat_input_main")

        

        if user_input: # Se o usuário digitou algo

            cleaned_input = ChatService.validate_input(user_input)

            

            # Adiciona a mensagem do usuário imediatamente para feedback visual instantâneo

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

            st.rerun() # Reruns para exibir a mensagem do usuário e então processar a IA



        # Processa a resposta da IA APENAS se a última mensagem for do usuário e o limite não foi atingido

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

            if st.session_state.request_count > Config.MAX_REQUESTS_PER_SESSION:

                # Mensagem de corte forçada para compra, de forma sedutora

                final_offer_message = {

                    "text": "Você explorou o suficiente do meu mundo gratuito, gatinho. Para continuar nossa conversa ardente e desvendar todos os meus segredos, você precisa ser VIP! Me responda: vai ou não vai se render aos meus encantos? 😈",

                    "cta": {

                        "show": True,

                        "label": "SIM! QUERO SER VIP E TE TER! 💖",

                        "target": "offers"

                    }

                }

                # Evita duplicar a mensagem de limite se ela já foi a última

                if st.session_state.messages[-1]["content"] != json.dumps(final_offer_message): 

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

            

            # Chama a API da Gemini para obter a resposta da Paloma

            resposta_ia = ApiService.ask_gemini(st.session_state.messages[-1]["content"], st.session_state.session_id, conn)

            

            # Garante que a resposta é um dict com 'text' e 'cta' para consistência

            if not isinstance(resposta_ia, dict) or "text" not in resposta_ia:

                resposta_ia = {"text": "Desculpe, meu sistema ficou excitado demais e não conseguiu te responder agora. Tente de novo, gatinho!", "cta": {"show": False}}



            # Adiciona a resposta da IA ao histórico e salva

            st.session_state.messages.append({

                "role": "assistant",

                "content": json.dumps(resposta_ia) 

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



        # Rola para o final da conversa automaticamente para a melhor UX

        st.markdown("""

        <script>

            var element = document.elementFromPoint(0, document.body.scrollHeight - 1);

            if (element && element.closest('.stApp')) {

                element.closest('.stApp').scrollTop = element.closest('.stApp').scrollHeight;

            }

        </script>

        """, unsafe_allow_html=True)



# ----------------------------------------------------------------------------------------------------------------------



# ======================

# APLICAÇÃO PRINCIPAL - SEU IMPÉRIO COMEÇA AQUI!

# ======================

def main():

    # Inicializa a conexão com o banco de dados na sessão, para ser acessível globalmente

    if 'db_conn' not in st.session_state:

        st.session_state.db_conn = DatabaseService.init_db()

    

    conn = st.session_state.db_conn

    

    ChatService.initialize_session(conn) # Garante que os estados da sessão estão prontos e carregados

    

    # 1. Verificação de Idade: O primeiro e crucial passo para o acesso.

    if not st.session_state.age_verified:

        UiService.age_verification()

        st.stop() # Interrompe a execução até a verificação ser concluída

    

    # 2. Configura a Sidebar: Sempre visível após a verificação de idade para navegação.

    UiService.setup_sidebar()

    

    # 3. Animação de Conexão: Cria uma experiência de "chamada" uma vez por sessão.

    if not st.session_state.connection_complete:

        UiService.show_call_effect()

        st.session_state.connection_complete = True

        save_persistent_data()

        st.rerun() # Reruns para a próxima etapa, já com a conexão completa

    

    # 4. Tela de Início do Chat: Apresenta a Paloma e convida para a conversa íntima.

    # Esta tela aparece apenas se o chat ainda não foi iniciado e o usuário está na página 'chat'

    if not st.session_state.chat_started and st.session_state.current_page == 'chat': 

        col1, col2, col3 = st.columns([1,3,1])

        with col2:

            st.markdown("""

            <div style="text-align: center; margin: 50px 0; background: rgba(30, 0, 51, 0.4); padding: 30px; border-radius: 20px; border: 2px solid #FF66B3; box-shadow: 0 8px 25px rgba(0,0,0,0.4);">

                <img src="{profile_img}" width="150" style="border-radius: 50%; border: 5px solid #FF0066; box-shadow: 0 0 20px rgba(255, 0, 102, 0.7); animation: pulse-profile 2s infinite alternate;">

                <h2 style="color: #FF66B3; margin-top: 25px; font-size: 2.2em; text-shadow: 0 0 10px rgba(255, 102, 179, 0.5);">Pronto para se perder comigo, amor? 😉</h2>

                <p style="font-size: 1.3em; color: #E0E0E0; margin-top: 15px;">Estou aqui, só para você. Que comece a sedução!</p>

            </div>

            <style>

                @keyframes pulse-profile {

                    from { transform: scale(1); box-shadow: 0 0 20px rgba(255, 0, 102, 0.7); }

                    to { transform: scale(1.05); box-shadow: 0 0 30px rgba(255, 0, 102, 0.9); }

                }

            </style>

            """.format(profile_img=Config.IMG_PROFILE), unsafe_allow_html=True)

            

            if st.button("COMEÇAR A CONVERSAR COM PALOMA AGORA! 🔥", type="primary", use_container_width=True, key="start_chat_initial_button"):

                st.session_state.update({

                    'chat_started': True,

                    'current_page': 'chat',

                    'audio_sent': False # Garante que o áudio seja enviado ao iniciar o chat

                })

                save_persistent_data()

                st.rerun()

        st.stop() # Interrompe a execução aqui para mostrar a tela de início do chat



    # 5. Roteamento de Páginas: Direciona o usuário para a página apropriada com base no estado.

    if st.session_state.current_page == "home":

        NewPages.show_home_page()

    elif st.session_state.current_page == "gallery":

        UiService.show_gallery_page(conn)

    elif st.session_state.current_page == "offers":

        NewPages.show_offers_page()

    elif st.session_state.current_page == "chat":

        UiService.enhanced_chat_ui(conn)

    else: # Fallback para o chat se a página for desconhecida ou não especificada

        UiService.enhanced_chat_ui(conn)

    

    save_persistent_data() # Salva o estado final da sessão após qualquer interação



if __name__ == "__main__":

    main()
