import streamlit as st
import time
from utils.ui_components import init_ui, decorative_divider, app_footer, IMAGES, COLORS

# ============================================================
# INICIALIZAR UI (injeta CSS, remove branding do Streamlit)
# ============================================================
init_ui()

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Cyber Risk Intelligence Hub",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INICIALIZAÇÃO DE ESTADO 
# ============================================================
if "dashboards_criados" not in st.session_state:
    st.session_state.dashboards_criados = False

if "dashboards_importados" not in st.session_state:
    st.session_state.dashboards_importados = None

# ============================================================
# HEADER COM IMAGEM NÍTIDA
# ============================================================
st.markdown(
    f'<div class="hero-clear" style="background-image: url(\'{IMAGES["hero_clear"]}\');">'
    '<div class="hero-content">',
    unsafe_allow_html=True
)

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown('<h1 class="hero-title">Cyber Risk Intelligence Hub</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="hero-subtitle">Motor Estocástico e Avaliação Contínua de Risco Cibernético</h3>', unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")
    if st.button("Check Status", use_container_width=True):
        with st.spinner("A verificar integridade do motor matemático..."):
            time.sleep(1)
        st.success("Status do Sistema: Online e a aguardar instruções.")

st.markdown('</div></div>', unsafe_allow_html=True)

# Divisor decorativo
st.markdown(decorative_divider(), unsafe_allow_html=True)

# ============================================================
# COLUNAS PRINCIPAIS
# ============================================================
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

    st.markdown(decorative_divider(), unsafe_allow_html=True)

    st.markdown("### Meta-Risco Agregado")
    st.write("O motor converte todas as variáveis no *Score Executivo Único*:")
    st.latex(r"MR = w_1 CVaR + w_2 Sistémico + w_3 Incerteza")

    st.markdown(decorative_divider(), unsafe_allow_html=True)

    st.markdown("### Como Navegar")
    st.write("""
    Utilize o **menu lateral** para explorar:
    - Dashboards Estáticos  
    - Formulários de Triagem  
    - Threat Intel Live  
    - Painel Executivo (MR)  
    """)

# ============================================================
# FOOTER DECORATIVO
# ============================================================
st.markdown(decorative_divider(), unsafe_allow_html=True)
st.markdown(
    app_footer("Desenvolvido no âmbito da disciplina de Avaliação do Risco em Cibersegurança | © 2026"),
    unsafe_allow_html=True
)