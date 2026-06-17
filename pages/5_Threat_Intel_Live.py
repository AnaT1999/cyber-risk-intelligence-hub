import streamlit as st
import pandas as pd
from utils.api_helpers import fetch_live_threat_intel
from utils.live_dashboards import plot_top_threats_bar, plot_cvss_vs_ia_scatter, plot_threat_distribution_donut

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Threat Intel Live", layout="wide", page_icon=":material/radar:")

st.title(":material/radar: Threat Intelligence & Previsão em Tempo Real")
st.markdown("O nosso motor **XGBoost Otimizado** analisa dezenas de vulnerabilidades em tempo real cruzando dados da **NIST NVD**. A IA destaca o que é verdadeiramente crítico (prioridade de Patching), reduzindo a fadiga de falsos alarmes em mais de 75%.")
st.divider()

# --- BOTÃO DE SINCRONIZAÇÃO E LÓGICA DE CHAMADA ---
col_sync, col_status = st.columns([1, 3])
with col_sync:
    if st.button(":material/sync: Varrer API ao Vivo", use_container_width=True, type="primary"):
        st.session_state['recarregar_api'] = True

if 'resultados_api' not in st.session_state or st.session_state.get('recarregar_api', False):
    with st.spinner("A comunicar com a base de dados do Governo Americano (NIST) e a processar vetores através do motor de Machine Learning..."):
        resposta = fetch_live_threat_intel()
        st.session_state['resultados_api'] = resposta
        st.session_state['recarregar_api'] = False

# --- APRESENTAÇÃO DOS RESULTADOS ---
resultado = st.session_state['resultados_api']

if "erro" in resultado:
    st.error(f"**Falha de Conexão:** {resultado['erro']}")
    st.info("Sugestão: A API da NIST pode estar a bloquear o acesso temporariamente (Erro 503). Tente novamente em alguns minutos.")

else:
    # Converter o dicionário de volta para Pandas DataFrame para facilitar os gráficos
    df_live = pd.DataFrame(resultado["dados"])
    
    # Métricas Globais (Cards)
    total_cves = len(df_live)
    criticos_ia = len(df_live[df_live['probabilidade_ia'] >= 70])
    rede_expostos = len(df_live[df_live['attack_vector'] == 'NETWORK'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Vulnerabilidades Analisadas (Hoje)", f"{total_cves}")
    with col2:
        st.metric("Ameaças Críticas (Probabilidade > 70%)", f"{criticos_ia}", delta=f"Foco imediato", delta_color="inverse")
    with col3:
        st.metric("Exposição Crítica via Rede (Network)", f"{rede_expostos}")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- SECÇÃO DE DASHBOARDS (live_dashboards.py) ---
    st.markdown("### :material/monitoring: Radares de Risco (Motor XGBoost)")
    
    col_graf1, col_graf2 = st.columns([2, 1])
    with col_graf1:
        with st.container(border=True):
            st.plotly_chart(plot_cvss_vs_ia_scatter(df_live), use_container_width=True)
    with col_graf2:
        with st.container(border=True):
            st.plotly_chart(plot_threat_distribution_donut(df_live), use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(plot_top_threats_bar(df_live), use_container_width=True)

    # --- TABELA DE DETALHES ---
    st.markdown("### :material/table_rows: Triage Prioritária (Lista Detalhada)")
    st.info("Abaixo encontra as vulnerabilidades extraídas, ordenadas pela probabilidade prevista pela IA de serem exploradas por atacantes cibernéticos.")
    
    # Formatar a tabela 
    df_visual = df_live.copy()
    df_visual['probabilidade_ia'] = df_visual['probabilidade_ia'].apply(lambda x: f"{x:.2f}%")
    df_visual.rename(columns={
        'cve_id': 'Código CVE',
        'descricao': 'Descrição da Ameaça',
        'base_score': 'CVSS Base',
        'attack_vector': 'Vetor de Ataque',
        'probabilidade_ia': 'Risco Previsão IA'
    }, inplace=True)
    
    st.dataframe(
        df_visual,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Descrição da Ameaça": st.column_config.TextColumn(width="large"),
            "Risco Previsão IA": st.column_config.TextColumn(help="Probabilidade calculada pelo modelo preditivo")
        }
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Módulo de Threat Intelligence Alimentado por Machine Learning | © 2026")