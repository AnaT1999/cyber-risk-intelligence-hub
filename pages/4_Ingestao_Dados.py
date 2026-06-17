import streamlit as st
from utils.parser_json import parse_json_risk
from utils.parser_excel import parse_excel_risk
from utils.parser_pdf import parse_pdf_risk

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ingestão de Dados", layout="wide", page_icon=":material/cloud_upload:")

st.title(":material/cloud_upload: Ingestão Automática de Telemetria")
st.markdown("Faça o upload de auditorias anteriores (JSON, Excel ou PDF). O motor de mineração irá extrair automaticamente as métricas para alimentar o simulador preditivo.")
st.divider()

# --- INTERFACE DE UPLOAD ---
st.markdown("### :material/upload_file: Selecione o Ficheiro de Auditoria")
ficheiro_carregado = st.file_uploader("Arraste ou selecione um ficheiro .json, .xlsx ou .pdf", type=["json", "xlsx", "pdf"])

if ficheiro_carregado is not None:
    nome_ficheiro = ficheiro_carregado.name
    
    # 1. PROCESSAMENTO ÚNICO E LIMPEZA DE CACHE
    if 'ficheiro_atual' not in st.session_state or st.session_state['ficheiro_atual'] != nome_ficheiro:
        
        # ---> A Vassoura Digital: Limpa os dados do ficheiro anterior <---
        chaves_para_limpar = ['ale_val', 'revenue', 'nist_mat', 'q_dados', 'dados_completos']
        for chave in chaves_para_limpar:
            if chave in st.session_state:
                del st.session_state[chave]
                
        with st.spinner(":material/loading: O motor de inteligência do Hub está a analisar o documento..."):
            if nome_ficheiro.endswith(".json"): 
                dados_extraidos = parse_json_risk(ficheiro_carregado)
            elif nome_ficheiro.endswith(".xlsx"): 
                dados_extraidos = parse_excel_risk(ficheiro_carregado)
            elif nome_ficheiro.endswith(".pdf"): 
                dados_extraidos = parse_pdf_risk(ficheiro_carregado)
            
            # Guardar os resultados na memória
            st.session_state['temp_dados'] = dados_extraidos
            st.session_state['ficheiro_atual'] = nome_ficheiro
            st.session_state['dados_confirmados'] = False 
            
            # Lógica Inteligente para o Painel de Edição
            if dados_extraidos and dados_extraidos.get("alertas"):
                st.session_state['mostrar_edicao'] = True
            else:
                st.session_state['mostrar_edicao'] = False

    # Recuperar os dados da memória
    dados_extraidos = st.session_state.get('temp_dados', {})

    # Se houver um erro grave (formatação corrompida)
    if "erro" in dados_extraidos:
        st.error(f":material/cancel: **Erro de Ingestão:** {dados_extraidos['erro']}")
        
    else:
        # --- EXIBIÇÃO DE ALERTAS E FEEDBACK ---
        if not st.session_state.get('dados_confirmados', False):
            if dados_extraidos.get("alertas"):
                st.warning(":material/warning: **Aviso de Integridade:** Faltam campos essenciais no documento. Injetámos placeholders, mas **deve corrigi-los manualmente abaixo**.")
                with st.expander("Ver detalhes do que falhou na leitura"):
                    for alerta in dados_extraidos["alertas"]:
                        st.markdown(f"- {alerta}")
            else:
                st.success(f":material/check_circle: **Ficheiro lido com 100% de precisão!** Fonte: **{dados_extraidos['origem']}**")

        # --- MODO 1: MOSTRAR DADOS ESTÁTICOS ---
        if not st.session_state.get('mostrar_edicao', False) or st.session_state.get('dados_confirmados', False):
            st.markdown("#### :material/analytics: Métricas Ingeridas")
            
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(4)
                
                # Lê os valores guardados OU os que vieram diretos do parser (agora sem conflitos)
                ale_display = st.session_state.get('ale_val', dados_extraidos['ale_val'])
                rev_display = st.session_state.get('revenue', dados_extraidos['revenue'])
                nist_display = st.session_state.get('nist_mat', dados_extraidos['nist_mat'])
                dados_display = st.session_state.get('q_dados', dados_extraidos['q_dados'])
                
                with col1: st.metric("Perda Média (ALE)", f"{ale_display:,.2f} €")
                with col2: st.metric("Faturação da Empresa", f"{rev_display:,.2f} €")
                with col3: st.metric("Maturidade NIST", f"Tier {nist_display}")
                with col4: st.metric("Sensibilidade de Dados", f"Nível {dados_display}/5")

            if not st.session_state.get('dados_confirmados', False):
                if st.button(":material/edit: Ajustar Valores Manualmente", use_container_width=False):
                    st.session_state['mostrar_edicao'] = True
                    st.rerun() 
            else:
                if st.button(":material/undo: Editar Valores Novamente", use_container_width=False):
                    st.session_state['dados_confirmados'] = False
                    st.session_state['mostrar_edicao'] = True
                    st.rerun()

        # --- MODO 2: PAINEL DE EDIÇÃO INTERATIVO ---
        if st.session_state.get('mostrar_edicao', False) and not st.session_state.get('dados_confirmados', False):
            st.markdown("#### :material/edit_document: Revisão e Validação de Dados")
            st.info("Verifique os valores extraídos pelo sistema e aplique as correções necessárias.")
            
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    novo_ale = st.number_input("Perda Média (ALE) - €", value=float(dados_extraidos['ale_val']), step=10000.0, format="%.2f")
                    novo_rev = st.number_input("Faturação da Empresa - €", value=float(dados_extraidos['revenue']), step=50000.0, format="%.2f")
                with col2:
                    novo_nist = st.slider("Maturidade NIST", min_value=1, max_value=4, value=int(dados_extraidos['nist_mat']), help="Tier 1 (Inicial) a Tier 4 (Adaptativo)")
                    novo_dados = st.slider("Sensibilidade de Dados", min_value=1, max_value=5, value=int(dados_extraidos['q_dados']), help="Nível 1 (Público) a Nível 5 (Crítico)")

            if st.button(":material/save: Confirmar Valores e Gravar", use_container_width=True, type="primary"):
                st.session_state['ale_val'] = novo_ale
                st.session_state['revenue'] = novo_rev
                st.session_state['nist_mat'] = novo_nist
                st.session_state['q_dados'] = novo_dados
                st.session_state['dados_completos'] = dados_extraidos.get("dados_completos", {})
                st.session_state['dados_confirmados'] = True
                st.success("Dados validados e injetados com sucesso! O Simulador está pronto.")
                st.rerun() 

        # --- PORTAL DE REDIRECIONAMENTO ---
        if st.session_state.get('dados_confirmados', False) or (not dados_extraidos.get("alertas") and not st.session_state.get('mostrar_edicao', False)):
            
            if not st.session_state.get('dados_confirmados', False):
                st.session_state['ale_val'] = dados_extraidos['ale_val']
                st.session_state['revenue'] = dados_extraidos['revenue']
                st.session_state['nist_mat'] = dados_extraidos['nist_mat']
                st.session_state['q_dados'] = dados_extraidos['q_dados']
                st.session_state['dados_completos'] = dados_extraidos.get("dados_completos", {})

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