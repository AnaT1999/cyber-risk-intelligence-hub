import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="Dashboard Estático", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    .stApp { background-color: #020617 !important; }
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(30,64,175,0.6);
    }
    .header-title { font-size: 2.5rem; font-weight: 800; color: #f8fafc; margin-bottom: 0px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="header-title"> Dashboard Estático de Inteligência</p>', unsafe_allow_html=True)
st.markdown("Analise o histórico de risco através de dados globais ou importe as suas próprias avaliações.")
st.divider()

#---------------------------------------------------------------
st.sidebar.header("Controlos do Dashboard")

# O "Interruptor" principal
modo_visualizacao = st.sidebar.radio(
    "Selecione o Modo de Visualização:",
    ["Dashboards de Raiz (Python)", "Dashboards Importados"]
)

st.sidebar.divider()

#---------------------------------------------------------------
if modo_visualizacao == "Dashboards Importados":
    st.subheader("Galeria de Dashboards Externos")
    st.write("Faça o upload de avaliações de risco geradas noutras plataformas (ex: PowerBI, Excel, Tableau) para centralizar a informação visual.")
    
    # Criar a área de Drag & Drop para Imagens
    uploaded_files = st.file_uploader(
        "Carregar imagens de dashboards", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    st.divider()
    
    # Lógica para mostrar as imagens carregadas
    if uploaded_files:
        st.success(f"{len(uploaded_files)} dashboard(s) carregado(s) com sucesso!")
        
        # Mostrar cada imagem carregada com o respetivo nome
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption=f"Ficheiro: {uploaded_file.name}", use_column_width=True)
            st.markdown("---")
    else:
        st.info("A aguardar upload... Utilize a área acima para arrastar e largar os seus prints ou imagens.")

elif modo_visualizacao == "Dashboards de Raiz (Python)":
    st.subheader("Motor Analítico: Dados Globais")
    st.write("Análise interativa em tempo real baseada no motor matemático e nos datasets estáticos locais.")
    
    # Menu colapsável para escolher o dataset
    dataset_escolhido = st.sidebar.selectbox(
        "Selecione o Contexto de Risco:",
        ["Tráfego IoT (Risco Sistémico)", "Anomalias de Rede (UNSW-NB15)", "Contexto Tático (MITRE ATT&CK)"]
    )
    
    st.divider()

    # --- FUNÇÃO PARA CARREGAR DADOS COM CACHE (Super Rápido) ---
    @st.cache_data
    def load_local_csv(caminho):
        try:
            return pd.read_csv(caminho)
        except Exception as e:
            st.error(f"Erro ao carregar ficheiro: Não foi possível encontrar '{caminho}'. Garante que o ficheiro está na pasta correta.")
            return None

    # --- LÓGICA DO DASHBOARD: IOT ---
    if dataset_escolhido == "Tráfego IoT (Risco Sistémico)":
        st.markdown("Análise de Tráfego e Comportamento IoT")
        
        # 1. Carregar o dataset físico
        caminho_iot = "data/raw/iot/iot_behavior.csv"
        df_iot = load_local_csv(caminho_iot)
        
        if df_iot is not None:
            # 2. Top KPIs (Métricas Resumo)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Registos", f"{len(df_iot):,}")
            col2.metric("Colunas Analisadas", len(df_iot.columns))
            col3.metric("Status do Motor", "Online", delta="Ativo")
            
            st.markdown("---")
            
            # 3. Tabela Interativa de Dados (Podes filtrar e ordenar)
            st.write("**Pré-visualização Interativa dos Dados:**")
            st.dataframe(df_iot.head(1000), use_container_width=True)
            
            # 4. Preparação para o Plotly
            st.info("**Aviso:** Os dados já estão vivos no sistema! Para gerarmos os gráficos Plotly exatos (Pizzas, Barras, Séries Temporais), precisamos de saber os nomes das colunas deste dataset.")

    elif dataset_escolhido == "Anomalias de Rede (UNSW-NB15)":
        st.warning("O módulo de visualização para o UNSW-NB15 será ativado em breve.")

    elif dataset_escolhido == "Contexto Tático (MITRE ATT&CK)":
        st.warning("O módulo de visualização para o MITRE ATT&CK será ativado em breve.")