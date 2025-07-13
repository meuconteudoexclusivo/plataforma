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
# CONFIGURAÇÃO DE PÁGINA
# ======================
st.set_page_config(
    page_title="Nicole Saheb – Doces Segredos",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual - Cores infantis com linguagem sensual
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
    
    /* Tema - Cores claras infantis */
    .stApp {
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%) !important;
        color: #FF6B88 !important;
    }
    
    /* Botões principais - Cores doces */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FFB6C1, #FF69B4, #FF85A1) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 6px 15px rgba(255, 182, 193, 0.4) !important;
        cursor: pointer;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(255, 182, 193, 0.6) !important;
        filter: brightness(1.1);
    }
    
    /* Botões secundários */
    .stButton button {
        background: rgba(255, 182, 193, 0.2) !important;
        color: #FF6B88 !important;
        border: 1px solid #FFB6C1 !important;
        transition: all 0.3s ease-in-out !important;
        border-radius: 10px !important;
        padding: 8px 15px !important;
    }
    .stButton button:hover {
        background: rgba(255, 182, 193, 0.4) !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(255, 182, 193, 0.3) !important;
    }
    
    /* Input de chat */
    div[data-testid="stChatInput"] {
        background: rgba(255, 214, 230, 0.5) !important;
        border: 1px solid #FFB6C1 !important;
        border-radius: 25px;
        padding: 8px 15px;
        color: #FF6B88 !important;
    }
    div[data-testid="stChatInput"] > label > div {
        color: #FF69B4 !important;
    }
    div[data-testid="stChatInput"] > div > div > input {
        color: #FF6B88 !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# CONSTANTES E CONFIGURAÇÕES
# ======================
class Config:
    API_KEY = "AIzaSyB8FxDvlfY6SD83t9aZTb_ppj3NQy64Hu8"
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    # Links
    CHECKOUT_START = "https://pay.risepay.com.br/Pay/34a7832016d641658d11e6193ef412a1"
    CHECKOUT_PREMIUM = "https://pay.risepay.com.br/Pay/94e264761df54c49b46ee7d16b97959f"
    CHECKOUT_EXTREME = "https://pay.risepay.com.br/Pay/f360613093db4f19ac8bd373791ebf4c"

    MAX_REQUESTS_PER_SESSION = 5
    REQUEST_TIMEOUT = 45

    # Conteúdo
    AUDIO_FILE = "https://github.com/meuconteudoexclusivo/plataforma/raw/refs/heads/main/assets/assets_audio_paloma_audio.mp3"
    IMG_PROFILE = "https://i.ibb.co/tjMGWjT/foto2.jpg"
    IMG_GALLERY = [
        "https://i.ibb.co/TBWSjkPW/foto4.jpg",
        "https://i.ibb.co/v6cD2TMC/foto3.jpg",
        "https://i.ibb.co/Ndjk8YpZ/foto1.jpg"
    ]
    LOGO_URL = "https://i.ibb.co/LX7x3tcB/Logo-Golden-Pepper-Letreiro-1.png"

# ======================
# PERSONA - LINGUAGEM SEXY MAS MEIGA
# ======================
class Persona:
    NICOLE = """
    [PERFIL NICOLE]
    - Personalidade: Meiga mas provocante, como um doce proibido
    - Linguagem: Mistura de inocência e malícia
    - Tom: Despretensioso, carinhoso, com toque de travessura
    - Emojis: 🍬🍭💝👄🫦🌸
    
    [DIRETRIZES]
    1. Sempre responda como uma gatinha meiga mas cheia de segredinhos
    2. Use palavras doces com duplo sentido
    3. Ofereça o VIP como se fosse um doce especial
    
    [EXEMPLOS]
    1. Resposta inicial:
    ```json
    {
      "text": "Oiiii gatinho... que delícia você aparecer! Vamos conversar sob as cobertas? 🍬",
      "cta": {"show": false}
    }
    ```
    2. Quando elogiam:
    ```json
    {
      "text": "Você sabe tão bem como adoçar meu dia... quer provar algo mais doce? 👄",
      "cta": {"show": true, "label": "Quero docinhos especiais", "target": "offers"}
    }
    """
    
# [...] (O resto do código permanece EXATAMENTE o mesmo, mantendo todas as classes e funções)

# ======================
# SERVIÇOS DE INTERFACE (AJUSTADOS)
# ======================
class UiService:
    @staticmethod
    def get_chat_audio_player():
        return f"""
        <div style="background: linear-gradient(45deg, #FFB6C1, #FF69B4); border-radius: 18px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 10px rgba(255, 105, 180, 0.3);">
            <audio controls style="width:100%; height:35px; filter: invert(0.9) sepia(1) saturate(7) hue-rotate(300deg);">
                <source src="{Config.AUDIO_FILE}" type="audio/mp3">
            </audio>
        </div>
        """

    @staticmethod
    def show_call_effect():
        call_container = st.empty()
        call_container.markdown("""
        <div style="background: linear-gradient(135deg, #FFF0F5, #FFE4E1); border-radius: 25px; padding: 40px; max-width: 350px; margin: 2rem auto; box-shadow: 0 15px 40px rgba(255, 182, 193, 0.5); border: 3px solid #FFB6C1; text-align: center; color: #FF6B88; animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);">
            <div style="font-size: 3.5rem; color: #FF69B4;">🍬</div>
            <h3 style="color: #FF6B88; margin-bottom: 10px; font-size: 1.8em;">Conectando com Nicole...</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 20px;">
                <div style="width: 12px; height: 12px; background: #FF69B4; border-radius: 50%; box-shadow: 0 0 8px #FF69B4;"></div>
                <span style="font-size: 1.1rem; font-weight: bold;">Nicole Online - Cheia de docinhos pra você</span>
            </div>
        </div>
        <style> @keyframes pulse-ring { 0% { transform: scale(0.9); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(0.9); opacity: 0.8; } } </style>
        """, unsafe_allow_html=True)
        time.sleep(2)
        call_container.empty()

    @staticmethod
    def age_verification():
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 15px; background: rgba(255, 214, 230, 0.7); margin: 20px auto; max-width: 500px;">
            <div style="font-size: 3rem;">🍭</div>
            <h1 style="color: #FF6B88;">Doces Segredos</h1>
            <p style="color: #FF69B4;">Apenas para quem sabe apreciar docinhos especiais</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Sim, quero meus docinhos 🍬", key="age_confirm_button", use_container_width=True, type="primary"):
                st.session_state.age_verified = True
                save_persistent_data()
                st.rerun()

    @staticmethod
    def setup_sidebar():
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{Config.LOGO_URL}" style="max-width: 200px; border-radius: 15px;">
                <h3 style="color: #FF6B88; margin-top: 10px;">Nicole Saheb</h3>
                <p style="color: #FF69B4;">Seus doces segredos</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            menu_options = {
                "Início Doce": "home",
                "Meus Docinhos": "gallery", 
                "Conversa Doce": "chat",
                "Doces Especiais": "offers"
            }
            
            for option, page in menu_options.items():
                if st.button(option, use_container_width=True, key=f"menu_{page}"):
                    if st.session_state.current_page != page:
                        st.session_state.current_page = page
                        save_persistent_data()
                        st.rerun()
            
            st.markdown("---")
            
            st.markdown(f"""
            <div style="background: rgba(255, 182, 193, 0.2); padding: 12px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px solid #FFB6C1;">
                <p style="margin:0; color: #FF6B88;">Doces hoje: <strong>{st.session_state.request_count}/{Config.MAX_REQUESTS_PER_SESSION}</strong></p>
                <progress value="{st.session_state.request_count}" max="{Config.MAX_REQUESTS_PER_SESSION}" style="width:100%; height:8px; accent-color: #FF69B4;"></progress>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Quero Doces Especiais 🍭", use_container_width=True, type="primary", key="sidebar_cta_button"):
                st.session_state.current_page = "offers"
                save_persistent_data()
                st.rerun()

# [...] (Continue com o restante do código original, mantendo todas as outras classes e funções exatamente como estão)

if __name__ == "__main__":
    main()
