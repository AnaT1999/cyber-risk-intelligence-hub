import streamlit as st

st.set_page_config(page_title="Cyber Risk Intelligence Hub", page_icon=":shield:", layout="wide")

if "dashboards_criados" not in st.session_state:
    st.session_state.dashboards_criados = False

if "dashboards_importados" not in st.session_state:
    st.session_state.dashboards_importados = None

st.title("Cyber Risk Intelligence Hub :shield:")

st.markdown("""
### Bem-vindo ao Centro de Avaliação e Mitigação de Risco.

Esta plataforma web modular avançada está desenhada para centralizar, modelar, analisar e mitigar riscos cibernéticos emergentes.

Utilize o menu de navegação lateral para aceder aos quatro pilares críticos do sistema:

* **1. Dashboard Estático:** Análise e cálculo do índice de risco de campanhas de desinformação sintética.
* **2. Formulário de Risco:** Avaliação e auditoria de vetores criptográficos vulneráveis incluindo Risco Pós-Quânticos.
* **3. Threat Intel Live:** Triagem automática de criticidade de vulnerabilidades em tempo real.
* **4. Ingestão de Dados:** Motor dinâmico para upload estruturado de ficheiros JSON e CSV.

---
""")
st.success("Status do Sistema: Online e a aguardar instruções.")