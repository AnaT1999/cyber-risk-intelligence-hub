import streamlit as st
import time
from utils.ui_components import apply_custom_theme, render_hero_section, render_footer, HERO_IMAGES

st.set_page_config(
    page_title="Cyber Risk Intelligence Hub",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

render_hero_section(
    title="Cyber Risk Intelligence Hub",
    subtitle="Motor Estocástico e Avaliação Contínua de Risco Cibernético de Nova Geração",
    image_url=HERO_IMAGES["ai_brain"]
)

# --- MEMÓRIA DE SESSÃO ---
if "dashboards_criados" not in st.session_state:
    st.session_state.dashboards_criados = False

if "dashboards_importados" not in st.session_state:
    st.session_state.dashboards_importados = None

# --- BARRA DE STATUS RAPIDA ---
col_status, col_empty = st.columns([2.5, 7.5])
with col_status:
    if st.button(":material/sync: Verificação de Integridade do Motor", use_container_width=True):
        with st.spinner("A calibrar redes de risco e motor matemático..."):
            time.sleep(1.5)
        st.success("Status: Online e a aguardar instruções.")

st.markdown("---")

# --- CONTEÚDO PRINCIPAL ---
colA, colB = st.columns([1.7, 1])

with colA:
    st.markdown("### A Mudança de Paradigma")
    st.write("""
    Esta plataforma transcende as avaliações qualitativas tradicionais de cibersegurança. 
    Implementamos uma arquitetura analítica profunda baseada em **Cálculo Estocástico, Teoria de Redes** e **Modelos Financeiros**, traduzindo vulnerabilidades técnicas em exposição financeira e operacional rigorosa.
    """)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- CARTÃO 1 ---
    with st.container(border=True):
        st.markdown("#### :material/analytics: 1. Dinâmica Estocástica e Perdas Extremas")
        st.write("""
        Utilizado no **Simulador de Cenários**, o motor abandona a ideia de que o risco é um valor estático. A cibersegurança é modelada como um ativo financeiro sujeito a choques constantes (Zero-Days).
        """)
        st.write("**Modelação no Tempo Contínuo (Lema de Itô):** Incorpora a degradação das defesas (obsolescência) e a volatilidade do mercado cibernético.")
        st.latex(r"dX_t = \mu(X_t, t)dt + \sigma(X_t, t)dW_t")
        
        st.write("**Value at Risk (VaR):** Define o limiar financeiro máximo de perda esperada para um dado nível de confiança $\\alpha$ ,que pode ser por exemplo 95%. É a fronteira matemática onde o risco diário acaba e o desastre começa.")
        st.latex(r"P(L \le VaR_\alpha) = \alpha")

        st.write("**Exposição de Cauda Pesada (Conditional VaR):** Os ciberataques não seguem uma distribuição normal, são eventos *Black Swan*. O CVaR calcula a média do desastre catastrófico (o pior cenário possível além do VaR).")
        st.latex(r"CVaR_\alpha = \mathbb{E}[L \mid L > VaR_\alpha]")
        
        st.write("**Equação de Fokker-Planck:** Enquanto Itô traça o caminho individual do risco (Monte Carlo), Fokker-Planck mapeia como a incerteza e a densidade de probabilidade se difundem e evoluem no tempo.")
        st.latex(r"\frac{\partial p}{\partial t} = -\frac{\partial}{\partial x}(\mu p) + \frac{1}{2}\frac{\partial^2}{\partial x^2}(\sigma^2 p)")

    # --- CARTÃO 2 ---
    with st.container(border=True):
        st.markdown("#### :material/network_check: 2. Propagação de Ameaças em Rede")
        st.write("""
        Aplicado na simulação de **Contágio Sistémico**. Prova matematicamente a importância da segmentação de rede (Zero Trust), demonstrando como um sensor desprotegido compromete a Administração.
        """)
        st.write("**Matriz de Risco com Decaimento de Hawkes:** Modelamos os ataques não como eventos isolados, mas como processos em cascata. O risco propaga-se dependendo do tempo de resposta (*Dwell Time*) da equipa de SOC.")
        st.latex(r"R_{t+1}(i) = R_t(i) + \sum_{j} (R_t(j) W_{ji} e^{-\beta t} (1-R_t(i)))")
        
        st.write("**Variância de Portefólio (Markowitz) e Cópulas:** A correlação de falhas prova que o risco sistémico de uma rede corporativa não é a mera soma aritmética das suas partes, mas sim uma rede de contágio complexa e não-linear.")
        st.latex(r"\sigma_p^2 = \sum w_i^2 \sigma_i^2 + \sum_{i \neq j} w_i w_j \sigma_i \sigma_j \rho_{ij}")

    # --- CARTÃO 3 ---
    with st.container(border=True):
        st.markdown("#### :material/shield: 3. Modelos de Auditoria Específicos")
        st.write("""
        Motores de cálculo em tempo real utilizados nos nossos **Formulários de Risco e Ingestão de Dados**, projetados para as ameaças emergentes do século XXI.
        """)
        st.write("**Índice de Desinformação Sintética (DRI):** Avalia o risco de imagem gerado por Deepfakes (IA). Aplica um amortecimento logarítmico ao alcance mediático, cruzando-o com o sentimento social e a velocidade de desmentido.")
        st.latex(r"DRI = \ln(reach) \cdot velocity \cdot (1.5 - sentiment) \cdot AI_{prob}")
        
        st.write("**Risco Pós-Quântico (PQR):** Mede a vulnerabilidade da criptografia clássica face aos futuros computadores quânticos. Penaliza arquiteturas sujeitas à tática de espionagem *Harvest Now, Decrypt Later*.")
        st.latex(r"PQR = \alpha C + \beta V - \gamma M")
        
        st.write("**Divergência de Kullback-Leibler (DKL):** Base matemática para que os nossos motores detetem anomalias em tráfego de rede ou campanhas de desinformação, medindo a entropia entre o comportamento orgânico ($P$) e o sintético ($Q$).")
        st.latex(r"D_{KL}(P||Q) = \sum P(x) \log\left(\frac{P(x)}{Q(x)}\right)")

with colB:
    st.markdown("### O Contexto do Projeto")
    st.write("""
    Desenvolvido no âmbito da disciplina de **Avaliação do Risco em Cibersegurança**, este Hub foi desenhado para colmatar a maior falha do mercado atual, **a barreira de comunicação entre a engenharia e a gestão**. 
    
    Ao traduzir CVEs, <i>exploits</i> e falhas criptográficas em **Euros, probabilidades e taxas de retorno (ROSI)**, permitimos que os conselhos de administração (C-Level) tomem decisões baseadas em dados rigorosos.
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown("### Frameworks e Normativos")
    st.write("A matemática do nosso motor é alimentada e calibrada pelos standards mais exigentes da indústria global:")
    st.success("**Compliance Global:** ISO/IEC 27005 & NIST CSF")
    st.warning("**Cálculo Financeiro:** Modelo FAIR (Factor Analysis of Information Risk)")
    st.error("**Threat Intelligence:** MITRE ATT&CK & CISA KEV")
    st.info("**Feed de Dados Live:** AlienVault OTX & NIST NVD")

    st.markdown("---")

    st.markdown("### Meta-Risco Agregado")
    st.write("A verdadeira inteligência executiva reside na consolidação. O motor processa os três pilares anteriores num Score de Decisão Único para a Administração:")
    st.latex(r"MR = w_1 CVaR + w_2 Sistémico + w_3 Incerteza")

    st.markdown("---")

    st.markdown("### Como Navegar")
    st.write("""
    Utilize o **menu lateral** para iniciar a sua jornada pelo Hub:
    - :material/bar_chart: **Dashboards Estáticos:** Análise histórica e dados globais.
    - :material/shield: **Formulários de Risco:** Triagem multivetorial.
    - :material/lightbulb: **Simulador de Cenários:** Predição Monte Carlo e ROSI.
    - :material/download: **Ingestão de Dados:** Importação JSON, Excel ou PDF.
    - :material/radar: **Threat Intel Live:** API de ameaças em tempo real.
    """)

render_footer()