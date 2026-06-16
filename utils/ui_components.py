import streamlit as st
import base64
from pathlib import Path
from typing import Optional, List, Dict, Any
import requests
from io import BytesIO
from PIL import Image

# ============================================================
# CONFIGURAÇÃO GLOBAL DE TEMA
# ============================================================

# Paleta de Cores
COLORS = {
    "primary": "#1A1A2E",        # Dark navy background
    "secondary": "#16213E",      # Dark blue secondary
    "accent": "#0F3460",         # Deep blue accent
    "highlight": "#E94560",      # Vibrant red-pink
    "success": "#00B894",        # Soft green pastel
    "warning": "#FDCB6E",        # Soft yellow pastel
    "danger": "#FF7675",         # Soft red pastel
    "info": "#74B9FF",           # Soft blue pastel
    "text_primary": "#ECEFF1",   # Off-white
    "text_secondary": "#B0BEC5", # Blue-grey
    "text_muted": "#78909C",     # Muted blue-grey
    "border": "#2D3748",         # Subtle border
    "card_bg": "#1E2A4A",        # Card background
    "gradient_start": "#667eea", # Purple-blue
    "gradient_end": "#764ba2",   # Purple
}

# Imagens públicas
IMAGES = {
    "hero_clear": "https://images.unsplash.com/photo-1581089788214-316e6c08fa35?w=1920",  # Header 1
    "hero_bg": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1920",      # Cyber security abstract
    "card_security": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800",  # Security lock
    "card_data": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",      # Data visualization
    "card_network": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800",   # Network/server
    "card_shield": "https://images.unsplash.com/photo-1633265486501-0cf524a07213?w=800", # Shield/Protection
    "card_ai": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",     # AI abstract
    "card_analytics": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800", # Analytics dashboard
    "logo": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=400",        # Security logo
    "pattern_dots": "https://images.unsplash.com/photo-1557683316-973673baf926?w=200",   # Abstract dots
    "background_texture": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920", # Dark abstract
}

# Fontes do Google
GOOGLE_FONTS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap",
    "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap",
]

# ============================================================
# CSS GLOBAL
# ============================================================

def load_global_css() -> str:
    """
    Retorna o CSS global para ser injetado no início da app.
    """
    
    return f"""
    <style>
        /* ============ FONTES ============ */
        @import url('{GOOGLE_FONTS[0]}');
        @import url('{GOOGLE_FONTS[1]}');
        @import url('{GOOGLE_FONTS[2]}');
        
        /* ============ RESET & BASE ============ */
        * {{
            font-family: 'Inter', 'Space Grotesk', sans-serif;
        }}
        
        .stApp {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, {COLORS['accent']} 100%);
            background-attachment: fixed;
        }}
        
        /* ============ SCROLLBAR CUSTOM ============ */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['primary']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['highlight']};
        }}
        
        /* ============ TÍTULOS ============ */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['text_primary']} !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }}
        
        h1 {{
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['highlight']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.8rem !important;
            text-align: center;
            margin-bottom: 2rem !important;
            animation: slideDown 0.8s ease-out;
        }}
        
        h2 {{
            font-size: 2rem !important;
            border-left: 4px solid {COLORS['highlight']};
            padding-left: 1rem !important;
            margin: 1.5rem 0 !important;
        }}
        
        h3 {{
            font-size: 1.5rem !important;
            color: {COLORS['info']} !important;
        }}
        
        /* ============ PARÁGRAFOS & TEXTO ============ */
        p, li, span, div {{
            color: {COLORS['text_secondary']} !important;
            line-height: 1.7 !important;
        }}
        
        /* ============ LINKS ============ */
        a {{
            color: {COLORS['info']} !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
        }}
        a:hover {{
            color: {COLORS['highlight']} !important;
            text-decoration: underline !important;
        }}
        
        /* ============ MÉTRICAS ============ */
        [data-testid="stMetric"] {{
            background: {COLORS['card_bg']} !important;
            border: 1px solid {COLORS['border']} !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            transition: all 0.3s ease !important;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-5px) !important;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3) !important;
            border-color: {COLORS['gradient_start']} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_secondary']} !important;
            font-size: 0.9rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {COLORS['text_primary']} !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
        }}
        [data-testid="stMetricDelta"] {{
            font-weight: 600 !important;
        }}
        
        /* ============ DATAFRAME ============ */
        [data-testid="stDataFrame"] {{
            background: {COLORS['card_bg']} !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid {COLORS['border']} !important;
        }}
        [data-testid="stDataFrame"] th {{
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
        }}
        [data-testid="stDataFrame"] td {{
            background: {COLORS['card_bg']} !important;
            color: {COLORS['text_secondary']} !important;
            padding: 10px 16px !important;
            border-bottom: 1px solid {COLORS['border']} !important;
        }}
        [data-testid="stDataFrame"] tr:hover td {{
            background: rgba(102, 126, 234, 0.1) !important;
        }}
        
        /* ============ INPUTS & WIDGETS ============ */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea {{
            background: {COLORS['card_bg']} !important;
            border: 2px solid {COLORS['border']} !important;
            border-radius: 12px !important;
            color: {COLORS['text_primary']} !important;
            transition: all 0.3s ease !important;
        }}
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {COLORS['gradient_start']} !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        }}
        
        /* ============ SIDEBAR ============ */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%) !important;
            border-right: 1px solid {COLORS['border']} !important;
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {COLORS['text_primary']} !important;
        }}
        
        /* ============ EXPANDER ============ */
        .streamlit-expanderHeader {{
            background: {COLORS['card_bg']} !important;
            border-radius: 12px !important;
            border: 1px solid {COLORS['border']} !important;
            color: {COLORS['text_primary']} !important;
            font-weight: 600 !important;
        }}
        .streamlit-expanderContent {{
            background: {COLORS['card_bg']} !important;
            border-radius: 0 0 12px 12px !important;
            border: 1px solid {COLORS['border']} !important;
            border-top: none !important;
        }}
        
        /* ============ TOOLTIP ============ */
        .tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
        }}
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 200px;
            background: {COLORS['secondary']};
            color: {COLORS['text_primary']};
            text-align: center;
            border-radius: 8px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.85rem;
            border: 1px solid {COLORS['border']};
        }}
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
        
        /* ============ LOADING SPINNER ============ */
        .custom-spinner {{
            border: 4px solid {COLORS['border']};
            border-top: 4px solid {COLORS['gradient_start']};
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        /* ============ PROGRESS BAR ============ */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
            border-radius: 10px !important;
        }}
        
        /* ============ TABS ============ */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent !important;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS['card_bg']} !important;
            border-radius: 12px 12px 0 0 !important;
            color: {COLORS['text_secondary']} !important;
            border: 1px solid {COLORS['border']} !important;
            transition: all 0.3s ease !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
            color: white !important;
            border-color: transparent !important;
        }}
        
        /* ============ ANIMAÇÕES ============ */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-50px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(50px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        @keyframes glow {{
            0% {{ box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }}
            50% {{ box-shadow: 0 0 30px rgba(102, 126, 234, 0.8); }}
            100% {{ box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }}
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes shimmer {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .animate-fade-in {{
            animation: fadeIn 0.8s ease-out;
        }}
        .animate-slide-up {{
            animation: slideUp 0.8s ease-out;
        }}
        .animate-slide-left {{
            animation: slideInLeft 0.8s ease-out;
        }}
        .animate-slide-right {{
            animation: slideInRight 0.8s ease-out;
        }}
        .animate-pulse {{
            animation: pulse 2s infinite;
        }}
        .animate-glow {{
            animation: glow 2s infinite;
        }}
        .animate-float {{
            animation: float 3s ease-in-out infinite;
        }}
        
        /* ============ SHIMMER EFFECT ============ */
        .shimmer {{
            background: linear-gradient(
                90deg,
                {COLORS['card_bg']} 0%,
                rgba(102, 126, 234, 0.2) 50%,
                {COLORS['card_bg']} 100%
            );
            background-size: 200% 100%;
            animation: shimmer 2s infinite;
        }}

        /* ============ HERO SECTION (do app original) ============ */
        .hero-wrapper {{
            position: relative;
            width: 100%;
            padding: 3rem 2.5rem 2.5rem 2.5rem;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 2rem;
            border: 1px solid rgba(148,163,184,0.15);
            animation: fadeIn 1s ease-out;
            background-size: cover;
            background-position: center;
        }}
        .hero-wrapper::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 30% 40%, rgba(59,130,246,0.35), transparent 55%),
                        linear-gradient(135deg, rgba(26, 26, 46, 0.85) 0%, rgba(22, 33, 62, 0.92) 100%);
            backdrop-filter: blur(6px);
            z-index: 0;
        }}
        .hero-content {{
            position: relative;
            z-index: 1;
        }}
        .hero-title {{
            font-size: 3.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #93c5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -1.5px;
            margin-bottom: 0.5rem;
        }}
        .hero-subtitle {{
            font-size: 1.2rem;
            color: #bae6fd;
            font-weight: 400;
            margin-bottom: 1.8rem;
            opacity: 0.9;
        }}

        /* ============ CARDS  ============ */
        .card {{
            background: rgba(30, 42, 74, 0.8);  /* card_bg + transparência */
            backdrop-filter: blur(12px);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(148,163,184,0.25);
            margin-bottom: 1.8rem;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out both;
        }}
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #667eea, #764ba2);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .card:hover {{
            transform: translateY(-6px);
            box-shadow: 0 25px 40px -15px rgba(0,0,0,0.6);
            border-color: rgba(148,163,184,0.45);
        }}
        .card:hover::before {{
            opacity: 1;
        }}
        .card-title {{
            color: #f8fafc !important;
            font-weight: 700;
            font-size: 1.25rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .card p, .card span, .card div, .card label, .card li {{
            color: #e2e8f0 !important;
            line-height: 1.7;
        }}

        /* ============ BOTÕES GLOBAIS ============ */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            padding: 10px 24px;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            letter-spacing: 0.3px;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            filter: brightness(1.1);
        }}
        .stButton > button:active {{
            transform: translateY(0);
            filter: brightness(0.95);
        }}

                /* ============ HERO CLEAR ============ */
        .hero-clear {{
            position: relative;
            width: 100%;
            padding: 3rem 2.5rem 2.5rem 2.5rem;
            border-radius: 24px;
            overflow: hidden;
            margin-bottom: 2rem;
            border: 1px solid rgba(148,163,184,0.2);
            background-size: cover;
            background-position: center;
            animation: fadeIn 1s ease-out;
        }}
        .hero-clear::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.7) 0%, rgba(22, 33, 62, 0.8) 100%);
            z-index: 0;
        }}
        .hero-clear > .hero-content {{
            position: relative;
            z-index: 1;
        }}
    </style>
    """

# ============================================================
# CUSTOM CARDS
# ============================================================

def card_container(
    title: str,
    content: str,
    icon: str = ":material/security:",
    image_url: Optional[str] = None,
    accent_color: str = COLORS['gradient_start'],
    animation: str = "fade-in"
) -> str:
    """
    Cria um card estilizado com ícone, imagem e animação.
    
    Args:
        title: Título do card
        content: Conteúdo HTML do card
        icon: Ícone do Streamlit (formato :material/...:)
        image_url: URL da imagem de fundo (opcional)
        accent_color: Cor de destaque do card
        animation: Tipo de animação (fade-in, slide-up, etc.)
    """
    image_html = ""
    if image_url:
        image_html = f"""
        <div class="card-image" style="background-image: url('{image_url}'); 
             height: 160px; background-size: cover; background-position: center;
             border-radius: 16px 16px 0 0; position: relative; overflow: hidden;">
            <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 0%, {COLORS['card_bg']} 100%);"></div>
        </div>
        """
    
    html = f"""
    <div class="custom-card animate-{animation}" style="
        background: {COLORS['card_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1rem 0;
        position: relative;
    " onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 25px 50px rgba(0,0,0,0.4)'; this.style.borderColor='{accent_color}';"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'; this.style.borderColor='{COLORS['border']}';">
        {image_html}
        <div style="padding: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 2rem;">{icon}</span>
                <h3 style="margin: 0; color: {COLORS['text_primary']}; font-size: 1.3rem;">{title}</h3>
            </div>
            <div style="color: {COLORS['text_secondary']}; line-height: 1.7;">
                {content}
            </div>
        </div>
        <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; 
             background: linear-gradient(180deg, {accent_color}, transparent);"></div>
    </div>
    """
    return html

# ============================================================
# BOTÕES CUSTOMIZADOS
# ============================================================

def custom_button(
    label: str,
    key: str,
    button_type: str = "primary",
    icon: str = "",
    width: str = "auto",
    disabled: bool = False,
    use_container_width: bool = False
) -> bool:
    """
    Cria um botão estilizado com vários tipos.
    
    Args:
        label: Texto do botão
        key: Chave única do Streamlit
        button_type: Tipo (primary, secondary, success, danger, warning, gradient)
        icon: Ícone opcional
        width: Largura CSS (ex: "100%", "200px")
        disabled: Desabilitado
        use_container_width: Largura total do container
    """
    button_styles = {
        "primary": f"""
            background: {COLORS['highlight']};
            color: white;
            border: none;
        """,
        "secondary": f"""
            background: transparent;
            color: {COLORS['info']};
            border: 2px solid {COLORS['info']};
        """,
        "success": f"""
            background: {COLORS['success']};
            color: {COLORS['primary']};
            border: none;
        """,
        "danger": f"""
            background: {COLORS['danger']};
            color: white;
            border: none;
        """,
        "warning": f"""
            background: {COLORS['warning']};
            color: {COLORS['primary']};
            border: none;
        """,
        "gradient": f"""
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
            color: white;
            border: none;
        """,
    }
    
    style = button_styles.get(button_type, button_styles["primary"])
    
    css = f"""
    <style>
        div[data-testid="stButton"] > button#{key} {{
            {style}
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            width: {width};
            text-transform: none;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }}
        div[data-testid="stButton"] > button#{key}:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            filter: brightness(1.1);
        }}
        div[data-testid="stButton"] > button#{key}:active {{
            transform: translateY(-1px);
            filter: brightness(0.9);
        }}
        div[data-testid="stButton"] > button#{key}:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }}
        div[data-testid="stButton"] > button#{key}::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}
        div[data-testid="stButton"] > button#{key}:active::after {{
            width: 300px;
            height: 300px;
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
    
    button_label = f"{icon} {label}" if icon else label
    
    return st.button(
        button_label,
        key=key,
        disabled=disabled,
        use_container_width=use_container_width
    )

# ============================================================
# BADGES E TAGS
# ============================================================

def status_badge(
    text: str,
    badge_type: str = "info",
    size: str = "md"
) -> str:
    """
    Cria um badge de status colorido.
    
    Args:
        text: Texto do badge
        badge_type: info, success, warning, danger, gradient
        size: sm, md, lg
    """
    colors = {
        "info": COLORS['info'],
        "success": COLORS['success'],
        "warning": COLORS['warning'],
        "danger": COLORS['danger'],
        "gradient": f"linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']})",
    }
    
    sizes = {
        "sm": "font-size: 0.75rem; padding: 4px 10px;",
        "md": "font-size: 0.85rem; padding: 6px 16px;",
        "lg": "font-size: 1rem; padding: 8px 20px;",
    }
    
    bg = colors.get(badge_type, colors['info'])
    text_color = COLORS['primary'] if badge_type in ['success', 'warning'] else 'white'
    
    return f"""
    <span style="
        background: {bg};
        color: {text_color};
        border-radius: 50px;
        {sizes.get(size, sizes['md'])}
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
    ">{text}</span>
    """

# ============================================================
# ALERTAS E NOTIFICAÇÕES
# ============================================================

def alert_box(
    message: str,
    alert_type: str = "info",
    icon: str = ":material/info:",
    dismissible: bool = False
) -> str:
    """
    Cria uma caixa de alerta estilizada.
    
    Args:
        message: Mensagem do alerta
        alert_type: info, success, warning, error
        icon: Ícone do alerta
        dismissible: Se pode ser fechado
    """
    alert_colors = {
        "info": (COLORS['info'], "rgba(116, 185, 255, 0.1)"),
        "success": (COLORS['success'], "rgba(0, 184, 148, 0.1)"),
        "warning": (COLORS['warning'], "rgba(253, 203, 110, 0.1)"),
        "error": (COLORS['danger'], "rgba(255, 118, 117, 0.1)"),
    }
    
    border_color, bg_color = alert_colors.get(alert_type, alert_colors['info'])
    
    dismiss_script = """
    <script>
        document.querySelector('.alert-dismiss').addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    </script>
    """ if dismissible else ""
    
    dismiss_btn = """
    <button class="alert-dismiss" style="
        background: transparent;
        border: none;
        color: inherit;
        cursor: pointer;
        font-size: 1.2rem;
        padding: 0;
        margin-left: auto;
        opacity: 0.7;
        transition: opacity 0.3s;
    " onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'">✕</button>
    """ if dismissible else ""
    
    return f"""
    <div style="
        background: {bg_color};
        border-left: 4px solid {border_color};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
        animation: slideDown 0.5s ease-out;
    ">
        <span style="font-size: 1.5rem;">{icon}</span>
        <span style="color: {COLORS['text_primary']}; flex: 1;">{message}</span>
        {dismiss_btn}
    </div>
    {dismiss_script}
    """

# ============================================================
# LOADING / SKELETON
# ============================================================

def skeleton_loader(lines: int = 3, width: str = "100%") -> str:
    """
    Cria um skeleton loader para placeholder de carregamento.
    
    Args:
        lines: Número de linhas
        width: Largura do skeleton
    """
    html = '<div style="padding: 1rem;">'
    for i in range(lines):
        random_width = f"{70 + (i * 10) % 30}%"
        html += f"""
        <div class="shimmer" style="
            height: 16px;
            width: {random_width};
            border-radius: 8px;
            margin-bottom: 12px;
        "></div>
        """
    html += '</div>'
    return html

# ============================================================
# TOOLTIP HELPER
# ============================================================

def tooltip(text: str, tooltip_text: str) -> str:
    """Cria um texto com tooltip ao passar o mouse."""
    return f"""
    <div class="tooltip">
        {text}
        <span class="tooltiptext">{tooltip_text}</span>
    </div>
    """

# ============================================================
# SEÇÃO HERO
# ============================================================

def hero_section(
    title: str,
    subtitle: str,
    background_image: str = IMAGES['hero_bg'],
    cta_text: Optional[str] = None,
    cta_url: Optional[str] = None
) -> str:
    """
    Cria uma seção hero com imagem de fundo.
    
    Args:
        title: Título principal
        subtitle: Subtítulo
        background_image: URL da imagem de fundo
        cta_text: Texto do botão de call-to-action
        cta_url: URL do CTA
    """
    cta_html = ""
    if cta_text:
        cta_html = f"""
        <a href="{cta_url or '#'}" style="
            display: inline-block;
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
            color: white;
            padding: 14px 32px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            margin-top: 1.5rem;
        " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 15px 35px rgba(102, 126, 234, 0.4)';"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            {cta_text} →
        </a>
        """
    
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.85) 0%, rgba(22, 33, 62, 0.9) 100%),
                    url('{background_image}');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        padding: 4rem 3rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid {COLORS['border']};
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {COLORS['gradient_start']}, {COLORS['highlight']}, {COLORS['gradient_end']});
        "></div>
        <h1 style="
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, white, {COLORS['info']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">{title}</h1>
        <p style="
            color: {COLORS['text_secondary']};
            font-size: 1.2rem;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.8;
        ">{subtitle}</p>
        {cta_html}
    </div>
    """

# ============================================================
# GRID DE CARDS
# ============================================================

def card_grid(cards: List[Dict[str, Any]], columns: int = 3) -> None:
    """
    Cria uma grid de cards.
    
    Args:
        cards: Lista de dicionários com 'title', 'content', 'icon', 'image'
        columns: Número de colunas
    """
    cols = st.columns(columns)
    
    for i, card in enumerate(cards):
        with cols[i % columns]:
            html = card_container(
                title=card.get('title', ''),
                content=card.get('content', ''),
                icon=card.get('icon', ':material/info:'),
                image_url=card.get('image'),
                accent_color=card.get('accent', COLORS['gradient_start']),
                animation=card.get('animation', f"slide-up")
            )
            st.markdown(html, unsafe_allow_html=True)

# ============================================================
# LINHA DO TEMPO
# ============================================================

def timeline_item(
    period: str,
    title: str,
    description: str,
    is_last: bool = False,
    status: str = "completed"
) -> str:
    """
    Cria um item de linha do tempo.
    
    Args:
        period: Período (ex: "Jan 2024")
        title: Título do evento
        description: Descrição
        is_last: Se é o último item
        status: completed, current, upcoming
    """
    status_colors = {
        "completed": COLORS['success'],
        "current": COLORS['gradient_start'],
        "upcoming": COLORS['text_muted'],
    }
    
    color = status_colors.get(status, COLORS['text_muted'])
    
    connector = "" if is_last else f"""
    <div style="
        position: absolute;
        left: 12px;
        top: 32px;
        bottom: -24px;
        width: 2px;
        background: {COLORS['border']};
    "></div>
    """
    
    return f"""
    <div style="
        position: relative;
        padding-left: 40px;
        margin-bottom: 24px;
    ">
        {connector}
        <div style="
            position: absolute;
            left: 0;
            top: 4px;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: {color};
            border: 3px solid {COLORS['card_bg']};
            box-shadow: 0 0 0 3px {color}33;
        "></div>
        <div style="
            background: {COLORS['card_bg']};
            border-radius: 12px;
            padding: 1rem 1.5rem;
            border: 1px solid {COLORS['border']};
        ">
            <div style="color: {COLORS['text_muted']}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                {period}
            </div>
            <h4 style="color: {COLORS['text_primary']}; margin: 0 0 8px 0;">{title}</h4>
            <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">{description}</p>
        </div>
    </div>
    """

# ============================================================
# DIVIDER DECORATIVO
# ============================================================

def decorative_divider(style: str = "gradient") -> str:
    """Cria um divisor decorativo."""
    styles = {
        "gradient": f"""
            height: 3px;
            background: linear-gradient(90deg, transparent, {COLORS['gradient_start']}, {COLORS['gradient_end']}, transparent);
            border: none;
            margin: 2rem 0;
        """,
        "dots": f"""
            height: 4px;
            background: radial-gradient(circle, {COLORS['gradient_start']} 2px, transparent 2px);
            background-size: 16px 4px;
            border: none;
            margin: 2rem 0;
        """,
    }
    return f'<hr style="{styles.get(style, styles["gradient"])}">'

# ============================================================
# FOOTER
# ============================================================

def app_footer(
    text: str = "",
    links: Optional[Dict[str, str]] = None
) -> str:
    """Cria um footer estilizado."""
    links_html = ""
    if links:
        links_html = " | ".join([
            f'<a href="{url}" style="color: {COLORS["text_muted"]}; text-decoration: none;">{name}</a>'
            for name, url in links.items()
        ])
    
    return f"""
    <div style="
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid {COLORS['border']};
        color: {COLORS['text_muted']};
        font-size: 0.85rem;
    ">
        <p>{text or '© 2024 Cyber Security Simulator. Todos os direitos reservados.'}</p>
        {f'<p>{links_html}</p>' if links_html else ''}
    </div>
    """

# ============================================================
# INFORMAÇÃO DE CARREGAMENTO
# ============================================================

def img_to_base64(url: str) -> str:
    """Converte imagem URL para base64 (útil para embutir)."""
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return ""

# ============================================================
# INICIALIZADOR
# ============================================================

def init_ui() -> None:
    """
    Inicializa todos os componentes de UI.
    Chama esta função no início da tua app Streamlit.
    
    Exemplo:
        from ui_components import init_ui
        init_ui()
    """
    st.markdown(load_global_css(), unsafe_allow_html=True)
    
    # Esconde elementos padrão do Streamlit (opcional)
    hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)