import streamlit as st
import pandas as pd
import os
import plotly.express as px
from utils.visuals import plot_donut_chart, plot_bar_chart, plot_3d_scatter, plot_boxplot, plot_heatmap, plot_scatter, plot_violin
import json

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

st.markdown('<h1 class="header-title"> Dashboard Estático de Inteligência</h1>', unsafe_allow_html=True)
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
        [
            "Tráfego IoT (Risco Sistémico)", 
            "Anomalias de Rede (UNSW-NB15)", 
            "Contexto Tático (MITRE ATT&CK)", 
            "Gestão de Vulnerabilidades (CVE / CISA / EPSS)"
        ]
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
        st.markdown("### Análise de Tráfego e Comportamento IoT")
        
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
            
            # 3. Tabela Interativa de Dados
            st.write("**Pré-visualização Interativa dos Dados:**")
            st.dataframe(df_iot.head(1000), use_container_width=True)
            
            # --- LIMPEZA DE DADOS EM TEMPO REAL ---
            df_iot.columns = df_iot.columns.str.strip()
            
            colunas_numericas = ['orig_bytes', 'duration', 'orig_ip_bytes', 'id.resp_p']
            for col in colunas_numericas:
                if col in df_iot.columns:
                    df_iot[col] = pd.to_numeric(df_iot[col].replace('-', pd.NA), errors='coerce')

            # 4. DASHBOARD INTERATIVO (ATOMIZADO)
            st.markdown("### Análise Visual Dinâmica (Plotly)")
            
            # --- GRUPO 1: LADO A LADO ---
            colA, colB = st.columns(2)
            with colA:
                # Gráfico 1: Gráfico Circular (Donut) usando 'class_label'
                if 'class_label' in df_iot.columns:
                    label_counts = df_iot['class_label'].value_counts().reset_index()
                    label_counts.columns = ['Tipo', 'Contagem']
                    fig_pie = plot_donut_chart(label_counts, 'Tipo', 'Contagem', 'Distribuição de Tráfego (Risco)')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'class_label' não encontrada.")
            
            with colB:
                # Gráfico 2: Barras dos ataques usando 'attack_type'
                if 'attack_type' in df_iot.columns:
                    top_attacks = df_iot['attack_type'].value_counts().head(10).reset_index()
                    top_attacks.columns = ['Ataque', 'Ocorrências']
                    fig_bar = plot_bar_chart(top_attacks, 'Ataque', 'Ocorrências', 'Top Vetores de Ataque', colorscale='Reds')
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'attack_type' não encontrada.")

            st.markdown("---")

            # --- GRUPO 2: EM BAIXO (BOXPLOT) ---
            st.markdown("#### Análise Distributiva por Dispositivo")
            if 'device_type' in df_iot.columns and 'payload_entropy' in df_iot.columns:
                df_sample = df_iot.sample(n=min(10000, len(df_iot)), random_state=42)
                fig_box = plot_boxplot(df_sample, 'device_type', 'payload_entropy', 'class_label', 'Entropia Informacional por Dispositivo (Amostra 10k)')
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.error("Erro: Faltam as colunas 'device_type' ou 'payload_entropy'.")
                
            st.markdown("---")
                
            # --- GRUPO 3: EM BAIXO (SCATTER 3D) ---
            st.markdown("#### Espaço Estocástico Tridimensional")
            st.write("Mapeamento multidimensional de anomalias com base no tamanho do pacote, volume enviado e entropia.")
            
            colunas_3d = ['packet_size', 'bytes_sent', 'payload_entropy', 'class_label']
            if all(col in df_iot.columns for col in colunas_3d):
                df_3d = df_iot.dropna(subset=['packet_size', 'bytes_sent', 'payload_entropy']).sample(n=min(2000, len(df_iot)), random_state=42)
                fig_3d = plot_3d_scatter(df_3d, 'packet_size', 'bytes_sent', 'payload_entropy', 'class_label', 'Dispersão Estocástica de Pacotes IoT')
                st.plotly_chart(fig_3d, use_container_width=True)
            else:
                st.error(f"Erro: Faltam colunas para o 3D. Necessárias: {colunas_3d}")

            # --- GRUPO 4: INTELIGÊNCIA TÁTICA E CIBER-FÍSICA (ATOMIZADO) ---
            st.markdown("---")
            st.markdown("#### 🚨 Inteligência Avançada (Ameaças Ciber-Físicas e Exfiltração)")
            
            colC, colD = st.columns(2)
            
            with colC:
                # 1. Mapa de Calor (Força Bruta)
                if all(col in df_iot.columns for col in ['device_type', 'attack_type', 'failed_auth_attempts']):
                    # CHAMADA À FÁBRICA
                    fig_heat = plot_heatmap(df_iot, 'attack_type', 'device_type', 'Intensidade de Força Bruta por Dispositivo', 
                                            z_col='failed_auth_attempts', histfunc='sum', colorscale='Inferno')
                    st.plotly_chart(fig_heat, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o Mapa de Calor.")
            
            with colD:
                # 2. Exaustão de Recursos (Scatter)
                if all(col in df_iot.columns for col in ['request_rate', 'cpu_usage', 'class_label']):
                    df_ddos = df_iot.sample(n=min(5000, len(df_iot)), random_state=42)
                    fig_ddos = plot_scatter(df_ddos, 'request_rate', 'cpu_usage', 'class_label', 
                                            'Exaustão de Recursos (Assinatura Botnet/DDoS)', opacity=0.6, colors=px.colors.qualitative.Set1)
                    st.plotly_chart(fig_ddos, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico de Exaustão.")

            colE, colF = st.columns(2)
            
            with colE:
                # 3. Violino (Temperatura)
                if all(col in df_iot.columns for col in ['attack_type', 'temperature', 'class_label']):
                    df_temp = df_iot.sample(n=min(5000, len(df_iot)), random_state=42)
                    fig_violin = plot_violin(df_temp, 'attack_type', 'temperature', 'class_label', 'Impacto Físico: Desvio de Temperatura do Hardware')
                    st.plotly_chart(fig_violin, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico de Temperatura.")

            with colF:
                # 4. Bolhas de Exfiltração (Scatter com Tamanho)
                if all(col in df_iot.columns for col in ['bytes_received', 'bytes_sent', 'connection_duration', 'class_label']):
                    df_exfil = df_iot[df_iot['connection_duration'] > 0].sample(n=min(2000, len(df_iot)), random_state=42)
                    fig_bubble = plot_scatter(df_exfil, 'bytes_received', 'bytes_sent', 'class_label', 'Deteção de Exfiltração de Dados (Volume vs Duração)', size_col='connection_duration', opacity=0.7, colors=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig_bubble, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico de Exfiltração.")
                    
    elif dataset_escolhido == "Anomalias de Rede (UNSW-NB15)":
        st.markdown("### Análise de Anomalias de Rede (UNSW-NB15)")
        
        # 1. Carregar o dataset físico
        caminho_net = "data/raw/network/UNSW-NB15_1.csv"
        df_net = load_local_csv(caminho_net)
        
        if df_net is not None:
            # --- CORREÇÃO DE CABEÇALHO (INJEÇÃO DO DICIONÁRIO OFICIAL UNSW-NB15) ---
            colunas_oficiais = [
                'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes',
                'sttl', 'dttl', 'sloss', 'dloss', 'service', 'sload', 'dload', 'spkts', 'dpkts',
                'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len',
                'sjit', 'djit', 'stime', 'ltime', 'sintpkt', 'dintpkt', 'tcprtt', 'synack', 'ackdat',
                'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd',
                'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm',
                'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'label'
            ]
            
            if len(df_net.columns) == 49:
                df_net.columns = colunas_oficiais
                
            # --- LIMPEZA DE DADOS EM TEMPO REAL ---
            if 'attack_cat' in df_net.columns:
                df_net['attack_cat'] = df_net['attack_cat'].fillna('Normal').replace(r'^\s*$', 'Normal', regex=True)
                df_net['attack_cat'] = df_net['attack_cat'].str.strip()

            if 'label' in df_net.columns:
                df_net['label'] = pd.to_numeric(df_net['label'], errors='coerce').fillna(0).astype(int)

            # 2. Top KPIs (Métricas Resumo)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Fluxos", f"{len(df_net):,}")
            col2.metric("Vetorizações de Rede", len(df_net.columns))
            col3.metric("Status do Motor", "Online", delta="Ativo")
            
            st.markdown("---")
            
            # 3. Tabela Interativa de Dados
            st.write("**Pré-visualização Interativa dos Dados:**")
            st.dataframe(df_net.head(1000), use_container_width=True)
            
            # 4. DASHBOARD INTERATIVO
            st.markdown("### Análise Visual Dinâmica (Plotly)")
            
            colA, colB = st.columns(2)
            with colA:
                # Gráfico Circular 
                if 'label' in df_net.columns:
                    label_counts = df_net['label'].value_counts().reset_index()
                    label_counts.columns = ['Malignidade', 'Contagem']
                    label_counts['Malignidade'] = label_counts['Malignidade'].map({0: 'Tráfego Normal', 1: 'Ataque Registado'})
                    
                    fig_pie = plot_donut_chart(label_counts, 'Malignidade', 'Contagem', 'Distribuição de Tráfego (Taxa de Infeção)', colors=['#3b82f6', '#ef4444'])
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'label' não encontrada.")
            
            with colB:
                # Gráfico 2: Barras dos ataques usando 'attack_cat'
                if 'attack_cat' in df_net.columns:
                    df_attacks = df_net[df_net['attack_cat'] != 'Normal']
                    if not df_attacks.empty:
                        top_attacks = df_attacks['attack_cat'].value_counts().head(10).reset_index()
                        top_attacks.columns = ['Categoria', 'Ocorrências']
                        
                        fig_bar = plot_bar_chart(top_attacks, 'Categoria', 'Ocorrências', 'Classificação Tática de Intrusões', colorscale='Reds')
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.info("A amostra atual não contém tráfego malicioso classificado.")
                else:
                    st.error("Erro: Coluna 'attack_cat' não encontrada.")

            st.markdown("---")

            # --- GRUPO 2: EM BAIXO (BOXPLOT DE DURAÇÃO) ---
            st.markdown("#### Comportamento de Protocolos de Rede")
            if 'proto' in df_net.columns and 'dur' in df_net.columns and 'label' in df_net.columns:
                top_protos = df_net['proto'].value_counts().nlargest(10).index
                df_sample = df_net[df_net['proto'].isin(top_protos)].sample(n=min(10000, len(df_net)), random_state=42)
                df_sample['Status'] = df_sample['label'].map({0: 'Normal', 1: 'Ataque'})
                
                fig_box = plot_boxplot(df_sample, 'proto', 'dur', 'Status', 'Duração da Conexão por Protocolo (Escala Logarítmica)', log_y=True)
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.error("Erro: Faltam as colunas 'proto', 'dur' ou 'label'.")
                
            st.markdown("---")
                
            # --- GRUPO 3: ESPAÇO ESTOCÁSTICO 3D ---
            st.markdown("#### Espaço Tridimensional de Exfiltração")
            st.write("Mapeamento estocástico cruzando Bytes Enviados (Source), Bytes Recebidos (Destination) e Tempo (Duração).")
            
            colunas_3d = ['sbytes', 'dbytes', 'dur', 'label']
            if all(col in df_net.columns for col in colunas_3d):
                df_3d = df_net.dropna(subset=['sbytes', 'dbytes', 'dur']).sample(n=min(2000, len(df_net)), random_state=42)
                df_3d['Status'] = df_3d['label'].map({0: 'Normal', 1: 'Ataque'})

                fig_3d = plot_3d_scatter(df_3d, 'sbytes', 'dbytes', 'dur', 'Status', 'Dispersão de Fluxo de Rede')
                st.plotly_chart(fig_3d, use_container_width=True)
            else:
                st.error(f"Erro: Faltam colunas para o 3D. Necessárias: {colunas_3d}")

            st.markdown("---")
            
            # --- GRUPO 4: INTELIGÊNCIA AVANÇADA (ATOMIZADO) ---
            st.markdown("#### Inteligência Tática de Exploração")
            
            colC, colD = st.columns(2)
            
            with colC:
                # 1. Mapa de Calor (Serviço vs Ataque)
                if all(col in df_net.columns for col in ['service', 'attack_cat']):
                    df_heat = df_net[df_net['attack_cat'] != 'Normal']
                    df_heat = df_heat[df_heat['service'] != '-'] 
                    fig_heat = plot_heatmap(df_heat, 'attack_cat', 'service', 'Matriz de Exploração (Serviço vs Tipo de Intrusão)', colorscale='Plasma')
                    st.plotly_chart(fig_heat, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o Mapa de Calor.")
            
            with colD:
                # 2. Anomalias de Roteamento (Scatter TTL)
                if all(col in df_net.columns for col in ['sttl', 'dttl', 'label']):
                    df_ttl = df_net.sample(n=min(5000, len(df_net)), random_state=42)
                    df_ttl['Status'] = df_ttl['label'].map({0: 'Normal', 1: 'Ataque'})
                    mapa_cores_net = {'Normal': '#3b82f6', 'Ataque': '#ef4444'}
                    fig_ttl = plot_scatter(df_ttl, 'sttl', 'dttl', 'Status', 'Anomalias de Roteamento (Time To Live - Source vs Dest)', opacity=0.5, color_map=mapa_cores_net)
                    st.plotly_chart(fig_ttl, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico TTL.")

    elif dataset_escolhido == "Contexto Tático (MITRE ATT&CK)":
        st.markdown("### Inteligência Tática (Framework MITRE ATT&CK)")
        st.write("Mapeamento do comportamento adversarial estruturado em Táticas (Objetivos) e Técnicas (Métodos).")
        
        # --- FUNÇÃO EXCLUSIVA PARA LER O STIX JSON DO MITRE ---
        @st.cache_data
        def load_mitre_stix(caminho):
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    stix_data = json.load(f)
                    
                techniques_list = []
                for obj in stix_data.get('objects', []):
                    if obj.get('type') == 'attack-pattern':
                        name = obj.get('name')
                        ext_refs = obj.get('external_references', [])
                        mitre_id = next((ref['external_id'] for ref in ext_refs if ref.get('source_name') == 'mitre-attack'), "N/A")
                        
                        phases = obj.get('kill_chain_phases', [])
                        for phase in phases:
                            if phase.get('kill_chain_name') == 'mitre-attack':
                                tactic = phase.get('phase_name').replace('-', ' ').title()
                                techniques_list.append({
                                    'ID': mitre_id,
                                    'Tática': tactic,
                                    'Técnica': name
                                })
                return pd.DataFrame(techniques_list)
            except Exception as e:
                st.error(f"O ficheiro foi encontrado, mas o Python detetou este erro ao abri-lo: {e}")
                return None

        # 1. Carregar o dataset físico
        caminho_mitre = "data/raw/threat_intel/enterprise-attack.json"
        df_mitre = load_mitre_stix(caminho_mitre)
        
        if df_mitre is not None and not df_mitre.empty:
            # 2. Top KPIs
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Técnicas e Subtécnicas", f"{df_mitre['Técnica'].nunique():,}")
            col2.metric("Fases da Kill Chain (Táticas)", df_mitre['Tática'].nunique())
            col3.metric("Framework Version", "Enterprise STIX 2.1")
            
            st.markdown("---")
            
            # 3. Tabela de Dicionário Tático
            st.write("**Catálogo de Ameaças Adversariais:**")
            st.dataframe(df_mitre, use_container_width=True)
            
            # 4. DASHBOARD INTERATIVO 
            st.markdown("### Mapeamento Visual da Matriz")
            
            colA, colB = st.columns([1, 1.5])
            
            with colA:
                # Gráfico 1: Barras Horizontais
                tactic_counts = df_mitre['Tática'].value_counts().reset_index()
                tactic_counts.columns = ['Tática', 'Volume de Técnicas']

                fig_bar = plot_bar_chart(tactic_counts, 'Volume de Técnicas', 'Tática', 'Densidade de Ataque por Fase (Kill Chain)', colorscale='Purples', horizontal=True)
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with colB:
                # Gráfico 2: Treemap (Mantido Nativo)
                df_mitre['Framework'] = 'MITRE ATT&CK'
                fig_tree = px.treemap(df_mitre, path=['Framework', 'Tática', 'Técnica'], title='Matriz Tática Hierárquica (Treemap)', color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_tree.update_traces(root_color="lightgrey")
                fig_tree.update_layout(margin=dict(t=50, l=25, r=25, b=25))
                st.plotly_chart(fig_tree, use_container_width=True)

            st.markdown("---")
            
            # --- MOTOR DE PESQUISA THREAT INTEL ---
            st.markdown("#### Motor de Pesquisa de Inteligência (Threat Intel Lookup)")
            st.write("Utilize os filtros abaixo para consultar a base de dados oficial do MITRE ATT&CK e mapear ameaças específicas.")
            
            col_search, col_filter = st.columns([1, 1])
            
            with col_search:
                texto_pesquisa = st.text_input("Pesquisar por ID ou Nome da Técnica (ex: Phishing, T1566, Bypass):", "")
                
            with col_filter:
                todas_taticas = sorted(df_mitre['Tática'].unique())
                taticas_selecionadas = st.multiselect("Filtrar por Fase de Ataque (Tática):", todas_taticas)
                
            df_pesquisa = df_mitre.copy()
            
            if texto_pesquisa:
                filtro_texto = df_pesquisa['Técnica'].str.contains(texto_pesquisa, case=False, na=False) | \
                               df_pesquisa['ID'].str.contains(texto_pesquisa, case=False, na=False)
                df_pesquisa = df_pesquisa[filtro_texto]
                
            if taticas_selecionadas:
                df_pesquisa = df_pesquisa[df_pesquisa['Tática'].isin(taticas_selecionadas)]
                
            st.success(f"Foram encontradas **{len(df_pesquisa)}** técnicas que correspondem à sua pesquisa.")
            st.dataframe(df_pesquisa[['ID', 'Tática', 'Técnica']], use_container_width=True, hide_index=True)
    
    elif dataset_escolhido == "Gestão de Vulnerabilidades (CVE / CISA / EPSS)":
        st.markdown("### Gestão de Vulnerabilidades Baseada em Risco (RBVM)")
        st.write("Correlação tática: Severidade Teórica (CVSS) vs. Probabilidade Real de Exploração (EPSS) e Catálogo CISA KEV.")
        
        # 1. Carregar os dois datasets
        caminho_corpus = "data/raw/threat_intel/cve_corpus.csv"
        caminho_enriched = "data/raw/threat_intel/cve_cisa_epss_enriched_dataset.csv"
        
        df_corpus = load_local_csv(caminho_corpus)
        df_enriched = load_local_csv(caminho_enriched)
        
        if df_corpus is not None and df_enriched is not None:
            
            # Vamos usar o 'cve_id' que é a chave primária oficial em ambos os ficheiros da Kaggle
            if 'cve_id' in df_corpus.columns and 'cve_id' in df_enriched.columns:
                # O merge 'inner' junta os dados garantindo que temos a descrição (corpus) e os scores (enriched) unificados
                df_vun = pd.merge(df_corpus, df_enriched, on='cve_id', how='inner', suffixes=('', '_dup'))
                # Limpar colunas duplicadas geradas pela junção
                df_vun = df_vun.loc[:, ~df_vun.columns.str.endswith('_dup')]
            else:
                # Caso os nomes sejam diferentes, assume o enriched que já costuma ter a maioria dos dados
                df_vun = df_enriched

            # Converter a coluna KEV (Known Exploited) para formato de texto limpo para o Plotly
            if 'cisa_kev' in df_vun.columns:
                df_vun['cisa_kev'] = df_vun['cisa_kev'].astype(str).str.lower().replace(
                    {'1.0':'Sim', '1':'Sim', 'true':'Sim', '0.0':'Não', '0':'Não', 'false':'Não'}
                )
                df_vun['cisa_kev'] = df_vun['cisa_kev'].fillna('Não')
            
            # 2. Top KPIs (Métricas Resumo)
            col1, col2, col3 = st.columns(3)
            col1.metric("CVEs Analisados e Correlacionados", f"{len(df_vun):,}")
            
            num_kev = len(df_vun[df_vun['cisa_kev'] == 'Sim']) if 'cisa_kev' in df_vun.columns else "N/A"
            col2.metric("Ameaças Críticas Ativas (CISA KEV)", f"{num_kev:,}")
            
            if 'base_score' in df_vun.columns:
                media_cvss = df_vun['base_score'].mean()
                col3.metric("Severidade Técnica Média (CVSS)", f"{media_cvss:.1f} / 10")
            else:
                col3.metric("Severidade Média", "N/A")
            
            st.markdown("---")
            
            # 3. Tabela Interativa Unificada
            st.write("**Matriz Unificada de Inteligência (Corpus + EPSS):**")
            st.dataframe(df_vun.head(1000), use_container_width=True)
            
            # 4. DASHBOARD INTERATIVO (ATOMIZADO)
            st.markdown("### Matriz de Priorização de Decisão Executiva")
            
            colA, colB = st.columns(2)
            
            with colA:
                # Gráfico 1: Dispersão CVSS vs EPSS (Mantido Nativo)
                if 'base_score' in df_vun.columns and 'epss_score' in df_vun.columns:
                    df_sample_normal = df_vun[df_vun['cisa_kev'] == 'Não'].sample(n=min(2000, len(df_vun)), random_state=42)
                    df_sample_kev = df_vun[df_vun['cisa_kev'] == 'Sim']
                    df_plot = pd.concat([df_sample_normal, df_sample_kev])
                    
                    fig_scatter = px.scatter(df_plot, x='base_score', y='epss_score', color='cisa_kev', title="Decisão de Risco: Severidade Teórica vs Probabilidade Real", labels={'base_score': 'CVSS Base Score', 'epss_score': 'EPSS Score (%)', 'cisa_kev': 'Catálogo KEV'}, opacity=0.7, color_discrete_map={'Sim': '#ef4444', 'Não': '#3b82f6'}, hover_data=['cve_id'])
                    
                    fig_scatter.update_layout(yaxis_tickformat='.1%')
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    st.error("Colunas 'base_score' ou 'epss_score' em falta para a matriz de dispersão.")
            
            with colB:
                # Gráfico 2: Histograma da Complexidade de Ataque cruzado com KEV (Mantido Nativo)
                if 'attack_complexity' in df_vun.columns and 'cisa_kev' in df_vun.columns:
                    df_vun['attack_complexity'] = df_vun['attack_complexity'].str.upper()
                    fig_bar = px.histogram(df_vun, x='attack_complexity', color='cisa_kev', barmode='group', title="Complexidade da Invasão vs Exploração Ativa no Mundo Real", labels={'attack_complexity': 'Nível de Complexidade', 'count': 'Volume de CVEs', 'cisa_kev': 'CISA KEV'}, color_discrete_map={'Sim': '#ef4444', 'Não': '#3b82f6'})
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.error("Coluna 'attack_complexity' em falta.")
            
            st.markdown("---")
            
            colC, colD = st.columns(2)
            
            with colC:
                # Gráfico 3: Gráfico Circular dos Vetores de Ataque
                if 'attack_vector' in df_vun.columns:
                    df_kev_only = df_vun[df_vun['cisa_kev'] == 'Sim']
                    if not df_kev_only.empty:
                        vetor_counts = df_kev_only['attack_vector'].str.upper().value_counts().reset_index()
                        vetor_counts.columns = ['Vetor', 'Total']
                        fig_pie = plot_donut_chart(vetor_counts, 'Vetor', 'Total', 'Vetores de Entrada Exclusivos das Ameaças Ativas')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("Aguardando carregamento de vulnerabilidades ativas.")
            
            with colD:
                # Gráfico 4: Boxplot de Dispersão do EPSS por Gravidade Oficial
                if 'base_severity' in df_vun.columns and 'epss_score' in df_vun.columns:
                    df_box = df_vun.sample(n=min(5000, len(df_vun)), random_state=42)
                    df_box['base_severity'] = df_box['base_severity'].str.upper().str.strip()
                    ordem_sev = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
                    mapa_cores = {'LOW': '#22c55e', 'MEDIUM': '#eab308', 'HIGH': '#f97316', 'CRITICAL': '#ef4444'}
                    fig_box = plot_boxplot(df_box, 'base_severity', 'epss_score', 'base_severity', 'A Incoerência do Risco: EPSS Score dentro das Severidades Oficiais', category_orders={'base_severity': ordem_sev}, color_map=mapa_cores, y_tickformat='.1%')
                    st.plotly_chart(fig_box, use_container_width=True)