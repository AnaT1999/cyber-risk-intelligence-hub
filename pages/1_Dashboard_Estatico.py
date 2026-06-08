import streamlit as st
import pandas as pd
import os
import plotly.express as px
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
        ["Tráfego IoT (Risco Sistémico)", "Anomalias de Rede (UNSW-NB15)", "Contexto Tático (MITRE ATT&CK)", "Correlação de Ameaças"]
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

            # 4. DASHBOARD INTERATIVO (PLOTLY SEGUIDO)
            st.markdown("### Análise Visual Dinâmica (Plotly)")
            
            # --- GRUPO 1: LADO A LADO ---
            colA, colB = st.columns(2)
            with colA:
                # Gráfico 1: Gráfico Circular (Donut) usando 'class_label'
                if 'class_label' in df_iot.columns:
                    label_counts = df_iot['class_label'].value_counts().reset_index()
                    label_counts.columns = ['Tipo', 'Contagem']
                    fig_pie = px.pie(label_counts, names='Tipo', values='Contagem', 
                                     title='Distribuição de Tráfego (Risco)',
                                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'class_label' não encontrada.")
            
            with colB:
                # Gráfico 2: Barras dos ataques usando 'attack_type'
                if 'attack_type' in df_iot.columns:
                    top_attacks = df_iot['attack_type'].value_counts().head(10).reset_index()
                    top_attacks.columns = ['Ataque', 'Ocorrências']
                    fig_bar = px.bar(top_attacks, x='Ataque', y='Ocorrências', 
                                     title='Top Vetores de Ataque',
                                     text_auto='.2s', color='Ocorrências', color_continuous_scale='Reds')
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'attack_type' não encontrada.")

            st.markdown("---")

            # --- GRUPO 2: EM BAIXO (BOXPLOT) ---
            st.markdown("#### Análise Distributiva por Dispositivo")
            if 'device_type' in df_iot.columns and 'payload_entropy' in df_iot.columns:
                df_sample = df_iot.sample(n=min(10000, len(df_iot)), random_state=42)
                fig_box = px.box(df_sample, x='device_type', y='payload_entropy', color='class_label',
                                 title='Entropia Informacional por Dispositivo (Amostra 10k)',
                                 points='outliers')
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.error("Erro: Faltam as colunas 'device_type' ou 'payload_entropy'.")
                
            st.markdown("---")
                
            # --- GRUPO 3: EM BAIXO (SCATTER 3D COM HEIGHT EXPANDIDO) ---
            st.markdown("#### Espaço Estocástico Tridimensional")
            st.write("Mapeamento multidimensional de anomalias com base no tamanho do pacote, volume enviado e entropia.")
            
            colunas_3d = ['packet_size', 'bytes_sent', 'payload_entropy', 'class_label']
            if all(col in df_iot.columns for col in colunas_3d):
                df_3d = df_iot.dropna(subset=['packet_size', 'bytes_sent', 'payload_entropy']).sample(n=min(2000, len(df_iot)), random_state=42)
                fig_3d = px.scatter_3d(df_3d, x='packet_size', y='bytes_sent', z='payload_entropy',
                                       color='class_label', size_max=10, opacity=0.7,
                                       title='Dispersão Estocástica de Pacotes IoT',
                                       color_discrete_sequence=px.colors.qualitative.Set1)
                
                # REQUISITO FUNDAMENTAL: Altura aumentada para 800px para evitar cortes na ampliação
                fig_3d.update_layout(
                    height=800,
                    paper_bgcolor="rgba(0,0,0,0)", 
                    scene=dict(bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig_3d, use_container_width=True)
            else:
                st.error(f"Erro: Faltam colunas para o 3D. Necessárias: {colunas_3d}")

            # --- GRUPO 4: INTELIGÊNCIA TÁTICA E CIBER-FÍSICA  ---
            st.markdown("---")
            st.markdown("#### Inteligência Avançada (Ameaças Ciber-Físicas e Exfiltração)")
            
            colC, colD = st.columns(2)
            
            with colC:
                # 1. Mapa de Calor (Força Bruta e Reconhecimento)
                if all(col in df_iot.columns for col in ['device_type', 'attack_type', 'failed_auth_attempts']):
                    #  histfunc='sum' para somar todas as tentativas falhadas por tipo de dispositivo
                    fig_heat = px.density_heatmap(df_iot, x='attack_type', y='device_type', z='failed_auth_attempts',
                                                  histfunc='sum', title='Intensidade de Força Bruta por Dispositivo',
                                                  color_continuous_scale='Inferno')
                    st.plotly_chart(fig_heat, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o Mapa de Calor.")
            
            with colD:
                # 2. Exaustão de Recursos (DDoS / Botnets)
                if all(col in df_iot.columns for col in ['request_rate', 'cpu_usage', 'class_label']):
                    df_ddos = df_iot.sample(n=min(5000, len(df_iot)), random_state=42)
                    fig_ddos = px.scatter(df_ddos, x='request_rate', y='cpu_usage', color='class_label',
                                          title='Exaustão de Recursos (Assinatura Botnet/DDoS)',
                                          opacity=0.6, color_discrete_sequence=px.colors.qualitative.Set1)
                    st.plotly_chart(fig_ddos, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico de Exaustão.")

            colE, colF = st.columns(2)
            
            with colE:
                # 3. Violino (Impacto Ciber-Físico / Temperatura)
                if all(col in df_iot.columns for col in ['attack_type', 'temperature', 'class_label']):
                    df_temp = df_iot.sample(n=min(5000, len(df_iot)), random_state=42)
                    fig_violin = px.violin(df_temp, x='attack_type', y='temperature', color='class_label',
                                           box=True, points=False, # points=False para manter o gráfico leve
                                           title='Impacto Físico: Desvio de Temperatura do Hardware')
                    st.plotly_chart(fig_violin, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o gráfico de Temperatura.")

            with colF:
                # 4. Bolhas de Exfiltração de Dados
                if all(col in df_iot.columns for col in ['bytes_received', 'bytes_sent', 'connection_duration', 'class_label']):
                    # Evitar erros com durações a zeros ou negativas no tamanho da bolha
                    df_exfil = df_iot[df_iot['connection_duration'] > 0].sample(n=min(2000, len(df_iot)), random_state=42)
                    fig_bubble = px.scatter(df_exfil, x='bytes_received', y='bytes_sent',
                                            size='connection_duration', color='class_label',
                                            title='Deteção de Exfiltração de Dados (Volume vs Duração)',
                                            size_max=30, opacity=0.7,
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
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
            # O ficheiro original não tem nomes de colunas. Vamos forçar as 49 variáveis oficiais:
            colunas_oficiais = [
                'srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes',
                'sttl', 'dttl', 'sloss', 'dloss', 'service', 'sload', 'dload', 'spkts', 'dpkts',
                'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len',
                'sjit', 'djit', 'stime', 'ltime', 'sintpkt', 'dintpkt', 'tcprtt', 'synack', 'ackdat',
                'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd',
                'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm',
                'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'label'
            ]
            
            # Aplicar as colunas (se o ficheiro tiver as 49 colunas esperadas)
            if len(df_net.columns) == 49:
                df_net.columns = colunas_oficiais
                
            # --- LIMPEZA DE DADOS EM TEMPO REAL ---
            # 1. O UNSW-NB15 deixa a categoria vazia/nula quando o tráfego é normal.
            if 'attack_cat' in df_net.columns:
                df_net['attack_cat'] = df_net['attack_cat'].fillna('Normal').replace(r'^\s*$', 'Normal', regex=True)
                # Opcional: Limpar espaços em branco à volta dos nomes dos ataques
                df_net['attack_cat'] = df_net['attack_cat'].str.strip()

            # 2. Garantir que a coluna 'label' é um número inteiro (0 ou 1) para evitar erros nas cores
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
            
            # 4. DASHBOARD INTERATIVO (PLOTLY)
            st.markdown("### Análise Visual Dinâmica (Plotly)")
            
            # --- GRUPO 1: LADO A LADO ---
            colA, colB = st.columns(2)
            with colA:
                # Gráfico 1: Gráfico Circular (Donut) usando 'label' (0 = Normal, 1 = Ataque)
                if 'label' in df_net.columns:
                    label_counts = df_net['label'].value_counts().reset_index()
                    label_counts.columns = ['Malignidade', 'Contagem']
                    # Mapear para texto corporativo
                    label_counts['Malignidade'] = label_counts['Malignidade'].map({0: 'Tráfego Normal', 1: 'Ataque Registado'})
                    fig_pie = px.pie(label_counts, names='Malignidade', values='Contagem', 
                                     title='Distribuição de Tráfego (Taxa de Infeção)',
                                     hole=0.4, color_discrete_sequence=['#3b82f6', '#ef4444']) # Azul e Vermelho
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.error("Erro: Coluna 'label' não encontrada.")
            
            with colB:
                # Gráfico 2: Barras dos ataques usando 'attack_cat'
                if 'attack_cat' in df_net.columns:
                    # Filtrar 'Normal' para vermos apenas a taxonomia de ataques
                    df_attacks = df_net[df_net['attack_cat'] != 'Normal']
                    if not df_attacks.empty:
                        top_attacks = df_attacks['attack_cat'].value_counts().head(10).reset_index()
                        top_attacks.columns = ['Categoria', 'Ocorrências']
                        fig_bar = px.bar(top_attacks, x='Categoria', y='Ocorrências', 
                                         title='Classificação Tática de Intrusões',
                                         text_auto='.2s', color='Ocorrências', color_continuous_scale='Reds')
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.info("A amostra atual não contém tráfego malicioso classificado.")
                else:
                    st.error("Erro: Coluna 'attack_cat' não encontrada.")

            st.markdown("---")

            # --- GRUPO 2: EM BAIXO (BOXPLOT DE DURAÇÃO) ---
            st.markdown("#### Comportamento de Protocolos de Rede")
            if 'proto' in df_net.columns and 'dur' in df_net.columns and 'label' in df_net.columns:
                # Focar apenas nos 10 protocolos principais para legibilidade
                top_protos = df_net['proto'].value_counts().nlargest(10).index
                df_sample = df_net[df_net['proto'].isin(top_protos)].sample(n=min(10000, len(df_net)), random_state=42)
                df_sample['Status'] = df_sample['label'].map({0: 'Normal', 1: 'Ataque'})
                
                # Usar Escala Logarítmica (log_y=True) porque a duração varia de milissegundos a horas
                fig_box = px.box(df_sample, x='proto', y='dur', color='Status',
                                 title='Duração da Conexão por Protocolo (Escala Logarítmica)',
                                 points=False, log_y=True, color_discrete_map={'Normal': '#3b82f6', 'Ataque': '#ef4444'})
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
                
                fig_3d = px.scatter_3d(df_3d, x='sbytes', y='dbytes', z='dur',
                                       color='Status', size_max=10, opacity=0.7,
                                       title='Dispersão de Fluxo de Rede',
                                       color_discrete_map={'Normal': '#3b82f6', 'Ataque': '#ef4444'})
                
                fig_3d.update_layout(
                    height=800,
                    paper_bgcolor="rgba(0,0,0,0)", 
                    scene=dict(bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig_3d, use_container_width=True)
            else:
                st.error(f"Erro: Faltam colunas para o 3D. Necessárias: {colunas_3d}")

            st.markdown("---")
            
            # --- GRUPO 4: INTELIGÊNCIA AVANÇADA ---
            st.markdown("#### Inteligência Tática de Exploração")
            
            colC, colD = st.columns(2)
            
            with colC:
                # 1. Mapa de Calor (Serviço Alvo vs Categoria de Ataque)
                if all(col in df_net.columns for col in ['service', 'attack_cat']):
                    df_heat = df_net[df_net['attack_cat'] != 'Normal']
                    # Remover o traço '-' que o UNSW usa para serviços desconhecidos
                    df_heat = df_heat[df_heat['service'] != '-'] 
                    
                    fig_heat = px.density_heatmap(df_heat, x='attack_cat', y='service',
                                                  title='Matriz de Exploração (Serviço vs Tipo de Intrusão)',
                                                  color_continuous_scale='Plasma')
                    st.plotly_chart(fig_heat, use_container_width=True)
                else:
                    st.warning("Variáveis insuficientes para o Mapa de Calor.")
            
            with colD:
                # 2. Anomalias de Roteamento (Time To Live)
                if all(col in df_net.columns for col in ['sttl', 'dttl', 'label']):
                    df_ttl = df_net.sample(n=min(5000, len(df_net)), random_state=42)
                    df_ttl['Status'] = df_ttl['label'].map({0: 'Normal', 1: 'Ataque'})
                    
                    fig_ttl = px.scatter(df_ttl, x='sttl', y='dttl', color='Status',
                                         title='Anomalias de Roteamento (Time To Live - Source vs Dest)',
                                         opacity=0.5, color_discrete_map={'Normal': '#3b82f6', 'Ataque': '#ef4444'})
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
                # O MITRE guarda a informação dentro do array 'objects'
                for obj in stix_data.get('objects', []):
                    # attack-pattern = Técnica no MITRE
                    if obj.get('type') == 'attack-pattern':
                        name = obj.get('name')
                        
                        # Extrair o ID oficial (ex: T1566)
                        ext_refs = obj.get('external_references', [])
                        mitre_id = next((ref['external_id'] for ref in ext_refs if ref.get('source_name') == 'mitre-attack'), "N/A")
                        
                        # Extrair a Tática (Kill Chain Phase)
                        phases = obj.get('kill_chain_phases', [])
                        for phase in phases:
                            if phase.get('kill_chain_name') == 'mitre-attack':
                                # Limpar o nome da tática (ex: "initial-access" -> "Initial Access")
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
            
            # 4. DASHBOARD INTERATIVO (PLOTLY)
            st.markdown("### Mapeamento Visual da Matriz")
            
            colA, colB = st.columns([1, 1.5])
            
            with colA:
                # Gráfico 1: Barras Horizontais (Concentração de Técnicas por Tática)
                tactic_counts = df_mitre['Tática'].value_counts().reset_index()
                tactic_counts.columns = ['Tática', 'Volume de Técnicas']
                
                fig_bar = px.bar(tactic_counts, x='Volume de Técnicas', y='Tática', orientation='h',
                                 title='Densidade de Ataque por Fase (Kill Chain)',
                                 color='Volume de Técnicas', color_continuous_scale='Purples')
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with colB:
                # Gráfico 2: Treemap (O mapa tático perfeito para o MITRE)
                # Adicionar uma coluna raiz para o Treemap
                df_mitre['Framework'] = 'MITRE ATT&CK'
                fig_tree = px.treemap(df_mitre, path=['Framework', 'Tática', 'Técnica'],
                                      title='Matriz Tática Hierárquica (Treemap)',
                                      color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_tree.update_traces(root_color="lightgrey")
                fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))
                st.plotly_chart(fig_tree, use_container_width=True)

                st.markdown("---")
            
            # --- MOTOR DE PESQUISA THREAT INTEL ---
            st.markdown("#### Motor de Pesquisa de Inteligência (Threat Intel Lookup)")
            st.write("Utilize os filtros abaixo para consultar a base de dados oficial do MITRE ATT&CK e mapear ameaças específicas.")
            
            # Criar os controlos de pesquisa
            col_search, col_filter = st.columns([1, 1])
            
            with col_search:
                # Pesquisa por texto livre (Nome ou ID)
                texto_pesquisa = st.text_input("Pesquisar por ID ou Nome da Técnica (ex: Phishing, T1566, Bypass):", "")
                
            with col_filter:
                # Filtro por Tática (Dropdown múltiplo)
                todas_taticas = sorted(df_mitre['Tática'].unique())
                taticas_selecionadas = st.multiselect(" Filtrar por Fase de Ataque (Tática):", todas_taticas)
                
            # Lógica de filtragem do DataFrame
            df_pesquisa = df_mitre.copy()
            
            if texto_pesquisa:
                # Filtrar ignorando maiúsculas e minúsculas
                filtro_texto = df_pesquisa['Técnica'].str.contains(texto_pesquisa, case=False, na=False) | \
                               df_pesquisa['ID'].str.contains(texto_pesquisa, case=False, na=False)
                df_pesquisa = df_pesquisa[filtro_texto]
                
            if taticas_selecionadas:
                df_pesquisa = df_pesquisa[df_pesquisa['Tática'].isin(taticas_selecionadas)]
                
            # Apresentar resultados dinâmicos
            st.success(f"Foram encontradas **{len(df_pesquisa)}** técnicas que correspondem à sua pesquisa.")
            st.dataframe(df_pesquisa[['ID', 'Tática', 'Técnica']], use_container_width=True, hide_index=True)