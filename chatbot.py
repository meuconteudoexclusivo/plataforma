# ======================
# IMPORTAÇÕES ESSENCIAIS (MANTIDO)
# ======================
# ... (importações mantidas iguais)

# ======================
# CONFIGURAÇÃO DE PÁGINA - VERSÃO OTIMIZADA
# ======================
st.set_page_config(
    page_title="Nicole Saheb VIP - Conteúdo Exclusivo 😈",
    page_icon="🔥",
    layout="centered",  # Layout mais focado
    initial_sidebar_state="collapsed"  # Sidebar recolhida para mais imersão
)

# CSS OTIMIZADO PARA CONVERSÃO
st.markdown("""
<style>
    /* FUNDO MAIS IMERSIVO */
    .stApp {
        background: linear-gradient(180deg, #000000 0%, #200033 100%) !important;
        color: #FFFFFF !important;
    }
    
    /* BOTÕES QUE IMPOSSÍVEL NÃO CLICAR */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF2D75 0%, #FF0080 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 35px !important;
        font-weight: 800 !important;
        font-size: 1.2em !important;
        box-shadow: 0 5px 20px rgba(255, 0, 128, 0.6) !important;
        transition: all 0.3s !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(255, 0, 128, 0.8) !important;
    }

    /* CHAT INPUT - MAIS CHAMATIVO */
    div[data-testid="stChatInput"] {
        background: rgba(255, 45, 117, 0.15) !important;
        border: 2px solid #FF2D75 !important;
        border-radius: 25px;
        padding: 12px 20px;
    }

    /* EFEITOS DE DESTAQUE */
    .urgent-flash {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ======================
# CONSTANTES - VERSÃO HIGH-CONVERSION
# ======================
class Config:
    # ... (outras configurações mantidas)
    
    # NOVOS LINKS DE CHECKOUT (USAR SEUS LINKS REAIS)
    CHECKOUT_START = "https://pay.risepay.com.br/Pay/34a7832016d641658d11e6193ef412a1"
    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"
    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"
    
    # LIMITES MAIS AGRESSIVOS
    MAX_REQUESTS_PER_SESSION = 3  # Menos mensagens gratuitas = mais urgência
    REQUEST_TIMEOUT = 30

    # MIDIA ATUALIZADA
    AUDIO_FILE = None  # Removido áudio genérico
    IMG_PROFILE = "https://i.ibb.co/ks5CNrDn/IMG-9256.jpg"  # Sua melhor foto
    IMG_GALLERY = [
        "https://i.ibb.co/zhNZL4FF/IMG-9198.jpg",
        "https://i.ibb.co/Y4B7CbXf/IMG-9202.jpg",
        "https://i.ibb.co/Fqf0gPPq/IMG-9199.jpg"
    ]

# ======================
# PERSONA - VERSÃO MAIS PERSUASIVA
# ======================
class Persona:
    NICOLE = """
    [PERFIL NICOLE SAHEB - VERSÃO CONVERSÃO]
    - Linguagem direta e provocativa, focada em gerar desejo imediato
    - Respostas curtas (máx 2 linhas) para manter o ritmo acelerado
    - A cada mensagem, incluir: 
      1. Elogio específico ("Adoro como você me pede")
      2. Insinuação sexual ("Quer ver como fico molhada?")
      3. CTA sutil ("Isso é só o começo...")

    [GATILHOS OBRIGATÓRIOS]
    - Urgência: "Só hoje", "Últimas vagas"
    - Escassez: "Só mostro para 10 pessoas"
    - Exclusividade: "Conteúdo que ninguém viu"
    """

# ======================
# MELHORIAS NA INTERFACE
# ======================
class UiService:
    @staticmethod
    def show_offers_page():
        # DESIGN DE OFERTAS QUE CONVERTE
        st.markdown("""
        <div style="text-align:center;margin-bottom:30px">
            <h1 style="color:#FF2D75">🔥 ACESSO VIP NICOLE SAHEB 🔥</h1>
            <p style="font-size:1.2em">Escolha seu pacote de <span style="color:#FF2D75">prazer ilimitado</span></p>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        packages = [
            {"name": "INICIAÇÃO", "price": "R$ 19,90", "color": "#FF2D75", "features": [
                "✔ 10 Fotos Exclusivas", 
                "✔ 3 Vídeos Pessoais",
                "✔ Bônus Surpresa"
            ]},
            {"name": "VIP", "price": "R$ 59,90", "color": "#FF0080", "features": [
                "✔ 20 Fotos Íntimas", 
                "✔ 5 Vídeos Exclusivos",
                "✔ Conteúdo Extra"
            ], "highlight": True},
            {"name": "OBSESSÃO", "price": "R$ 99,00", "color": "#CC00FF", "features": [
                "✔ 30 Fotos Proibidas", 
                "✔ 10 Vídeos Pessoais",
                "✔ Acesso Prioritário"
            ]}
        ]

        for i, col in enumerate(cols):
            with col:
                pkg = packages[i]
                border = "4px solid #FFD700" if pkg.get("highlight") else f"2px solid {pkg['color']}"
                st.markdown(f"""
                <div style="border:{border};border-radius:15px;padding:20px;margin-bottom:20px;height:100%">
                    <h3 style="color:{pkg['color']};text-align:center">{pkg['name']}</h3>
                    <h2 style="color:{pkg['color']};text-align:center">{pkg['price']}</h2>
                    <ul style="padding-left:20px">{
                        ''.join([f'<li style="margin-bottom:10px">{feat}</li>' 
                               for feat in pkg['features']])
                    }</ul>
                    <a href="{Config.CHECKOUT_PREMIUM if i==1 else Config.CHECKOUT_START}" 
                       target="_blank"
                       style="display:block;background:{pkg['color']};color:white;
                              text-align:center;padding:12px;border-radius:50px;
                              text-decoration:none;font-weight:bold;margin-top:20px">
                       QUERO AGORA!
                    </a>
                </div>
                """, unsafe_allow_html=True)

        # COUNTDOWN URGENTE
        st.markdown("""
        <div style="background:#1A0033;border-radius:10px;padding:15px;text-align:center;margin-top:30px">
            <p style="color:#FF2D75;font-weight:bold">⏰ OFERTA VÁLIDA POR:</p>
            <div id="countdown" style="font-size:2em;color:white">10:00:00</div>
            <p style="color:#FFB3FF">Preço sobe em breve!</p>
        </div>
        <script>
            let time = 600;
            setInterval(() => {
                time--;
                let mins = Math.floor(time/60);
                let secs = time%60;
                document.getElementById('countdown').innerHTML = 
                    `00:${mins.toString().padStart(2,'0')}:${secs.toString().padStart(2,'0')}`;
                if(time <= 0) document.getElementById('countdown').innerHTML = "OFERTA ENCERRADA!";
            }, 1000);
        </script>
        """, unsafe_allow_html=True)

# ======================
# ESTRATÉGIAS DE CHAT - VERSÃO CONVERSÃO
# ======================
class ChatService:
    @staticmethod
    def process_user_input(conn):
        # ... (código mantido)
        
        # RESPOSTA FINAL QUANDO ACABAM AS MSGS GRATUITAS
        if st.session_state.request_count >= Config.MAX_REQUESTS_PER_SESSION:
            final_msg = {
                "text": "😈 Quer continuar? Eu quero te mostrar MUITO mais...",
                "cta": {
                    "show": True,
                    "label": "DESBLOQUEAR TUDO AGORA!",
                    "target": "offers"
                }
            }
            # ... (restante do código mantido)
