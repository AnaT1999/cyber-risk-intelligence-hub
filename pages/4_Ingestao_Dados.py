import streamlit as st
from utils.parser_json import parse_json_risk
from utils.parser_excel import parse_excel_risk
from utils.parser_pdf import parse_pdf_risk

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ingestão de Dados", layout="wide", page_icon=":material/cloud_upload:")

st.title(":material/cloud_upload: Ingestão Automática de Telemetria e Relatórios")
st.markdown("Faça o upload de auditorias anteriores (JSON, Excel ou PDF). O motor de mineração de dados irá extrair automaticamente as palavras-chave e métricas quantitativas para alimentar o simulador preditivo.")
st.divider()

# --- INTERFACE DE UPLOAD ---
st.markdown("### :material/upload_file: Selecione o Ficheiro de Auditoria")
ficheiro_carregado = st.file_uploader("Arraste ou selecione um ficheiro .json, .xlsx ou .pdf", type=["json", "xlsx", "pdf"])

if ficheiro_carregado is not None:
    nome_ficheiro = ficheiro_carregado.name
    dados_extraidos = None
    
    with st.spinner(":material/loading: O motor de inteligência do Hub está a analisar o documento..."):
        if nome_ficheiro.endswith(".json"): 
            dados_extraidos = parse_json_risk(ficheiro_carregado)
        elif nome_ficheiro.endswith(".xlsx"): 
            dados_extraidos = parse_excel_risk(ficheiro_carregado)
        elif nome_ficheiro.endswith(".pdf"): 
            dados_extraidos = parse_pdf_risk(ficheiro_carregado)
            
    # Se houver um erro grave 
    if dados_extraidos and "erro" in dados_extraidos:
        st.error(f":material/cancel: **Erro de Ingestão:** {dados_extraidos['erro']}")
        
    elif dados_extraidos:
        # --- GRAVAÇÃO DOS DADOS (SESSION STATE) ---
        st.session_state['ale_val'] = dados_extraidos["ale_val"]
        st.session_state['revenue'] = dados_extraidos["revenue"]
        st.session_state['nist_mat'] = dados_extraidos["nist_mat"]
        st.session_state['q_dados'] = dados_extraidos["q_dados"]
        st.session_state['dados_completos'] = dados_extraidos.get("dados_completos", {})
        
        # --- EXIBIÇÃO DE ALERTAS  ---
        if dados_extraidos.get("alertas"):
            st.error(":material/error: **Aviso de Integridade:** O documento submetido não contém o formato de auditoria esperado ou faltam-lhe campos essenciais. Foram injetados valores genéricos de salvaguarda:")
            # Imprime todas as falhas que os parsers detetaram
            for alerta in dados_extraidos["alertas"]:
                st.warning(f":material/warning: {alerta}")
        else:
            st.success(f":material/check_circle: **Ficheiro Ingerido com Sucesso e 100% de Integridade!** Fonte detetada: **{dados_extraidos['origem']}**")
        
        # Painel Executivo do que foi minerado do documento
        st.markdown("#### :material/analytics: Métricas Carregadas para a Simulação:")
        
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Perda Média (ALE)", f"{dados_extraidos['ale_val']:,.0f} €")
            with col2: st.metric("Faturação da Empresa", f"{dados_extraidos['revenue']:,.0f} €")
            with col3: st.metric("Maturidade NIST", f"Tier {dados_extraidos['nist_mat']}")
            with col4: st.metric("Sensibilidade de Dados", f"Nível {dados_extraidos['q_dados']}/5")
        
        # --- PORTAL DE REDIRECIONAMENTO COM DESIGN EM BLOCO AZUL ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <style>
        [data-testid="stPageLink"] a { background-color: #1e3a8a !important; border: 1px solid #3b82f6 !important; color: #eff6ff !important; padding: 20px !important; border-radius: 12px !important; text-align: center !important; font-size: 1.25rem !important; font-weight: 600 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important; transition: all 0.3s ease-in-out !important; display: flex !important; justify-content: center !important; text-decoration: none !important; }
        [data-testid="stPageLink"] a:hover { background-color: #1e40af !important; border-color: #60a5fa !important; transform: translateY(-3px) !important; box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important; }
        [data-testid="stPageLink"] a p { font-size: 1.15rem !important; margin: 0 !important; }
        </style>
        """, unsafe_allow_html=True)

        st.page_link(page="pages/3_Simulador_Cenarios.py", label="Injetar Dados Ingeridos no Simulador Preditivo e Correr Monte Carlo", icon=":material/arrow_forward:", use_container_width=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Desenvolvido no âmbito da disciplina de Avaliação do Risco em Cibersegurança | © 2026")