import streamlit as st
import time

st.set_page_config(
    page_title="Cyber Risk Intelligence Hub",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
    background-color: #020617; /* preto azulado (slate-950) */
}

/* Removemos a imagem global da app */
.stApp {
    background-color: #020617 !important;
}

/* HEADER WRAPPER COM IMAGEM DE FUNDO */
.hero-wrapper {
    position: relative;
    width: 100%;
    padding: 2.5rem 2rem 2rem 2rem;
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    background: url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1920') no-repeat center center;
    background-size: cover;
}

.hero-wrapper::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top left, rgba(59,130,246,0.55), transparent 55%),
                rgba(15,23,42,0.80); /* overlay escuro por cima da imagem */
    backdrop-filter: blur(4px);
    z-index: 0;
}

/* Conteúdo dentro do header fica acima do overlay */
.hero-content {
    position: relative;
    z-index: 1;
}

/* HERO SECTION */
.hero-title {
    font-size: 3.1rem;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -1px;
    margin-bottom: -5px;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #93c5fd;
    font-weight: 400;
    margin-bottom: 1.5rem;
}

/* CARTÕES GLASSMORPHISM DARK */
.card {
    background: rgba(15, 23, 42, 0.9);
    padding: 1.8rem;
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,0.35);
    margin-bottom: 1.5rem;
    transition: 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 35px rgba(0,0,0,0.55);
}

.card-title {
    color: #f9fafb;
    font-weight: 700;
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.card p, .card span, .card div, .card label {
    color: #e5e7eb !important;
}

/* SIDEBAR DARK */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid rgba(30,64,175,0.6);
}

</style>
""", unsafe_allow_html=True)


if "dashboards_criados" not in st.session_state:
    st.session_state.dashboards_criados = False

if "dashboards_importados" not in st.session_state:
    st.session_state.dashboards_importados = None
# ============================
st.markdown('<div class="hero-wrapper"><div class="hero-content">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown('<h1 class="hero-title">Cyber Risk Intelligence Hub </h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="hero-subtitle">Motor Estocástico e Avaliação Contínua de Risco Cibernético</h3>', unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")
    if st.button("Check Status", use_container_width=True):
        with st.spinner("A verificar integridade do motor matemático..."):
            time.sleep(1)
        st.success("Status do Sistema: Online e a aguardar instruções.")

st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ============================
colA, colB = st.columns([1.7, 1])

with colA:

    st.markdown("### A Mudança de Paradigma")
    st.write("""
    Esta plataforma transcende as avaliações qualitativas tradicionais. Implementamos uma arquitetura analítica 
    baseada em **Cálculo Estocástico, Teoria de Redes** e **Modelos Financeiros de Cauda Pesada**.
    """)

    # --- CARTÃO 1 ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">1. Dinâmica Estocástica e Perdas Extremas</p>', unsafe_allow_html=True)
    st.write("Modelação no Tempo Contínuo (Lema de Itô):")
    st.latex(r"dX_t = \mu(X_t, t)dt + \sigma(X_t, t)dW_t")
    st.write("Cálculo de Exposição de Cauda Pesada (CVaR):")
    st.latex(r"CVaR_\alpha = \mathbb{E}[L \mid L > VaR_\alpha]")
    st.write("Equação de Fokker-Planck:")
    st.write("Enquanto Itô traça o caminho individual do risco, Fokker-Planck mapeia como a incerteza e a densidade de probabilidade se difundem no tempo.")
    st.latex(r"\frac{\partial p}{\partial t} = -\frac{\partial}{\partial x}(\mu p) + \frac{1}{2}\frac{\partial^2}{\partial x^2}(\sigma^2 p)")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CARTÃO 2 ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">2. Propagação de Ameaças em Rede</p>', unsafe_allow_html=True)
    st.write("Matriz de Risco Sistémico com Decaimento de Hawkes:")
    st.latex(r"R_{t+1}(i) = R_t(i) + \sum_{j} (R_t(j) W_{ji} e^{-\beta t} (1-R_t(i)))")
    st.write("Dependência Não-Linear via Cópulas:")
    st.latex(r"F(x,y) = C(F_1(x), F_2(y))")
    st.write("Variância de Portefólio (Markowitz):")
    st.write("A correlação de falhas prova que o risco sistémico de uma rede não é a mera soma das suas partes.")
    st.latex(r"\sigma_p^2 = \sum w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j \sigma_i \sigma_j \rho_{ij}")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- CARTÃO 3 ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">3. Modelos de Auditoria Específicos</p>', unsafe_allow_html=True)
    st.write("Índice de Desinformação Sintética (DRI):")
    st.latex(r"DRI = \ln(reach) \cdot velocity \cdot (1.5 - sentiment) \cdot AI_{prob}")
    st.write("Avaliação de Risco Pós-Quântico (PQR):")
    st.latex(r"PQR = \alpha C + \beta V - \gamma M")
    st.write("Divergência de Kullback-Leibler (DKL):")
    st.write("Para o motor de IA detetar Desinformação, medimos a entropia informacional entre o comportamento orgânico e sintético.")
    st.latex(r"D_{KL}(P||Q) = \sum P(x) \log\left(\frac{P(x)}{Q(x)}\right)")
    st.markdown('</div>', unsafe_allow_html=True)

with colB:

    st.markdown("### Pilares de Análise")
    st.success("**Pilar 1:** Avaliação de Risco Pós-Quântico (PQR)")
    st.warning("**Pilar 2:** Índice de Desinformação Sintética (DRI)")
    st.error("**Pilar 3:** Contágio Sistémico (Redes e IoT)")
    st.info("**Pilar 4:** Inteligência de Ameaças em Tempo Real")

    st.markdown("---")

    st.markdown("### Meta-Risco Agregado")
    st.write("O motor converte todas as variáveis no *Score Executivo Único*:")
    st.latex(r"MR = w_1 CVaR + w_2 Sistémico + w_3 Incerteza")

    st.markdown("---")

    st.markdown("### Como Navegar")
    st.write("""
    Utilize o **menu lateral** para explorar:
    - Dashboards Estáticos  
    - Formulários de Triagem  
    - Threat Intel Live  
    - Painel Executivo (MR)  
    """)

st.markdown("---")
st.caption("Desenvolvido no âmbito da disciplina de Avaliação do Risco em Cibersegurança | © 2026")
