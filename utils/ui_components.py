import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# INJEÇÃO DA ANIMAÇÃO JAVASCRIPT (PARTÍCULAS)
# ==========================================
def inject_particle_background():
    """
    Injeta um script JavaScript no Document Object Model (DOM) global da página.
    Isto desenha a tua rede neural dinâmica no fundo, sem interferir com os botões.
    """
    js_code = """
    <script>
    const parentDoc = window.parent.document;
    const parentWin = window.parent;

    // Garante que o canvas só é criado uma vez (evita duplicações nos reloads do Streamlit)
    if (!parentDoc.getElementById('cyber-network-canvas')) {
        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'cyber-network-canvas';
        
        // CSS do Canvas para cobrir a janela toda e não bloquear cliques
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '0'; 
        canvas.style.pointerEvents = 'none';

        // Anexar o canvas ao container principal do Streamlit
        const stApp = parentDoc.querySelector('.stApp');
        if(stApp) {
            stApp.prepend(canvas);
        } else {
            parentDoc.body.appendChild(canvas);
        }

        const ctx = canvas.getContext('2d');
        const PARTICLE_COUNT = 70;
        const CONNECTION_DISTANCE = 130;
        const PARTICLE_SPEED_MAX = 0.25;
        const GLOW_CHANCE = 0.15;

        // Paleta de Cores adaptada para o teu Dashboard
        const COLORS = {
            nodeDefault: '#60a5fa',     // Azul claro (Normal)
            nodeRisk: '#ef4444',        // Vermelho (Risco)
            line: 'rgba(96, 165, 250, 0.15)',
            lineRisk: 'rgba(239, 68, 68, 0.3)',
            glowColor: 'rgba(96, 165, 250, 0.4)',
            glowRisk: 'rgba(239, 68, 68, 0.4)'
        };

        let particles = [];
        let width, height;

        function resize() {
            width = parentWin.innerWidth;
            height = parentWin.innerHeight;
            canvas.width = width;
            canvas.height = height;
        }

        parentWin.addEventListener('resize', () => {
            resize();
            initParticles();
        });
        resize();

        function createParticle() {
            const isRiskNode = Math.random() < 0.2; // 20% das partículas são nós de risco (vermelhos)
            return {
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * PARTICLE_SPEED_MAX,
                vy: (Math.random() - 0.5) * PARTICLE_SPEED_MAX,
                radius: isRiskNode ? (Math.random() * 1.8 + 1.8) : (Math.random() * 1.5 + 1.2),
                isRisk: isRiskNode,
                color: isRiskNode ? COLORS.nodeRisk : COLORS.nodeDefault,
                glow: isRiskNode ? true : (Math.random() < GLOW_CHANCE),
                phase: Math.random() * Math.PI * 2
            };
        }

        function initParticles() {
            particles = [];
            for (let i = 0; i < PARTICLE_COUNT; i++) {
                particles.push(createParticle());
            }
        }

        function update() {
            for (let p of particles) {
                p.vx += (Math.random() - 0.5) * 0.02;
                p.vy += (Math.random() - 0.5) * 0.02;

                const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
                if (speed > PARTICLE_SPEED_MAX) {
                    p.vx = (p.vx / speed) * PARTICLE_SPEED_MAX;
                    p.vy = (p.vy / speed) * PARTICLE_SPEED_MAX;
                }

                p.x += p.vx;
                p.y += p.vy;

                if (p.x < -10) p.x = width + 10;
                if (p.x > width + 10) p.x = -10;
                if (p.y < -10) p.y = height + 10;
                if (p.y > height + 10) p.y = -10;
            }
        }

        function draw() {
            // O clearRect limpa o canvas mas MATÉM-O TRANSPARENTE, deixando ver o Gradiente CSS
            ctx.clearRect(0, 0, width, height);

            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const a = particles[i];
                    const b = particles[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < CONNECTION_DISTANCE) {
                        const opacity = (1 - dist / CONNECTION_DISTANCE) * 0.5;
                        const bothRisk = a.isRisk && b.isRisk;
                        const oneRisk = a.isRisk || b.isRisk;

                        let lineColor = bothRisk ? `rgba(239, 68, 68, ${opacity * 0.8})` : 
                                        oneRisk  ? `rgba(168, 85, 247, ${opacity * 0.6})` : 
                                                   `rgba(96, 165, 250, ${opacity * 0.4})`;

                        ctx.beginPath();
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.strokeStyle = lineColor;
                        ctx.lineWidth = 0.8;
                        ctx.stroke();
                    }
                }
            }

            const time = Date.now() * 0.001;
            for (let p of particles) {
                ctx.save();
                ctx.translate(p.x, p.y);

                if (p.glow) {
                    const pulse = 0.6 + 0.4 * Math.sin(time * 1.5 + p.phase);
                    const glowRadius = p.radius * 3.5;
                    const gradient = ctx.createRadialGradient(0, 0, p.radius * 0.5, 0, 0, glowRadius);
                    gradient.addColorStop(0, p.isRisk ? COLORS.glowRisk : COLORS.glowColor);
                    gradient.addColorStop(1, 'transparent');
                    ctx.fillStyle = gradient;
                    ctx.globalAlpha = pulse * 0.7;
                    ctx.beginPath();
                    ctx.arc(0, 0, glowRadius, 0, Math.PI * 2);
                    ctx.fill();
                }

                ctx.globalAlpha = 0.9;
                ctx.beginPath();
                ctx.arc(0, 0, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();

                ctx.globalAlpha = 0.6;
                ctx.beginPath();
                ctx.arc(0, 0, p.radius * 0.5, 0, Math.PI * 2);
                ctx.fillStyle = '#ffffff';
                ctx.fill();

                ctx.restore();
            }
        }

        function animate() {
            update();
            draw();
            parentWin.requestAnimationFrame(animate);
        }

        initParticles();
        animate();
    }
    </script>
    """
    components.html(js_code, height=0, width=0)

# ==========================================
# GESTOR DE TEMA (MODO ESCURO + GRADIENTE ANIMADO)
# ==========================================
def apply_custom_theme():
    """
    Injeta o CSS dinâmico fixado num Dark Mode elegante e de alto contraste.
    Chama também a rede neural de partículas no fundo.
    """
    # 1. Acionar as Partículas em Javascript
    inject_particle_background()

    text_color = "#f8fafc" 
    text_muted = "#94a3b8"
    card_bg = "rgba(15, 23, 42, 0.65)"
    card_border = "rgba(56, 189, 248, 0.15)"
    sidebar_bg = "rgba(2, 6, 23, 0.85)" # Ligeiramente translúcido para ver as partículas a passar

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    /* ANIMAÇÃO CSS DO GRADIENTE DE FUNDO (Mais rápida e 3 cores) */
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    .stApp {{
        /* Gradiente contínuo: Azul Noite -> Azul Ciano -> Roxo Tecnológico -> Azul Noite */
        background: linear-gradient(-45deg, #020617, #0284c7, #4c1d95, #020617) !important;
        background-size: 300% 300% !important;
        animation: gradientShift 10s ease infinite !important;
        background-attachment: fixed !important;
    }}

    /* GARANTIR COR DO TEXTO E FONTES (Protegendo Ícones) */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, label {{
        font-family: 'Inter', sans-serif;
        color: {text_color} !important;
    }}
    
    .material-symbols-rounded, .material-symbols-outlined, .stIcon {{
        font-family: 'Material Symbols Rounded' !important;
    }}

    [data-testid="stButton"] button p, [data-testid="stDownloadButton"] button p, [data-testid="stPageLink"] a p {{
        color: inherit !important;
    }}

    [data-testid="stMetricLabel"] div {{
        color: {text_muted} !important;
    }}

    /* Elevar o conteúdo para garantir que as partículas ficam por trás dos botões */
    .block-container {{
        position: relative;
        z-index: 1;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid {card_border};
        z-index: 2;
    }}
    
    [data-testid="stSidebarNav"] a:hover {{
        background: linear-gradient(90deg, rgba(59,130,246,0.15), transparent) !important;
        border-left: 4px solid #3b82f6 !important;
        transition: all 0.3s ease;
        padding-left: 1rem;
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }}
    .glass-card h3 {{
        margin-top: 0;
        font-family: 'Space Grotesk', sans-serif !important;
        color: {text_color} !important;
    }}
    .glass-card p {{
        color: {text_muted} !important;
        font-size: 0.95rem;
    }}

    [data-testid="stButton"] button {{
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        border-color: {card_border} !important;
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: {text_color} !important;
    }}
    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px rgba(59, 130, 246, 0.25) !important;
        border-color: #3b82f6 !important;
        color: #60a5fa !important;
    }}

    [data-testid="stDownloadButton"] button {{
        background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
        border: none !important;
        color: white !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 10px rgba(91, 33, 182, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stDownloadButton"] button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(91, 33, 182, 0.5) !important;
        color: white !important;
    }}

    [data-testid="stPageLink"] a {{
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        border: none !important;
        color: white !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stPageLink"] a:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 25px rgba(37, 99, 235, 0.4) !important;
        color: white !important;
    }}

    .custom-footer {{
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid {card_border};
        color: {text_muted} !important;
        font-size: 0.9rem;
    }}
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# COMPONENTES VISUAIS REUTILIZÁVEIS
# ==========================================

def render_hero_section(title, subtitle, image_url, gradient_start="rgba(15, 23, 42, 0.85)", gradient_end="rgba(30, 58, 138, 0.6)"):
    hero_title_color = "#ffffff"
    hero_sub_color = "#93c5fd"

    html_code = f"""
    <div style="
        background-image: linear-gradient(135deg, {gradient_start}, {gradient_end}), url('{image_url}');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        z-index: 2;
    ">
        <h1 style="color: #ffffff !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 3.5rem !important; font-weight: 800; margin: 0; padding-bottom: 1rem; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">
            {title}
        </h1>
        <p style="color: #93c5fd !important; font-family: 'Inter', sans-serif !important; font-size: 1.25rem; font-weight: 400; margin: 0 auto; max-width: 800px; text-shadow: 0 1px 5px rgba(0,0,0,0.5);">
            {subtitle}
        </p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_glass_card(title, content, icon="🛡️"):
    html_code = f"""
    <div class="glass-card">
        <h3><span style="font-size: 1.5rem; margin-right: 8px;">{icon}</span>{title}</h3>
        <p>{content}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_footer():
    st.markdown(f"""
    <div class="custom-footer">
        <b>Cyber Risk Intelligence Hub</b> <br>
        Desenvolvido no âmbito da disciplina de Avaliação do Risco em Cibersegurança | © 2026
    </div>
    """, unsafe_allow_html=True)

HERO_IMAGES = {
    "dashboard": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop", 
    "network": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=2070&auto=format&fit=crop",  
    "ai_brain": "https://thfvnext.bing.com/th/id/OIP.hMzf3Wdt9or-3p1qDj0gSgHaEJ?w=297&h=180&c=7&r=0&o=7&cb=thfvnextfalcon2&dpr=1.1&pid=1.7&rm=300", 
    "matrix": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=2070&auto=format&fit=crop"    
}