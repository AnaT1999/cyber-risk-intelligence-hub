import plotly.express as px
import pandas as pd

def plot_top_threats_bar(df):
    """Cria um gráfico de barras horizontal com o Top 10 das piores ameaças."""
    # Pegar apenas no Top 10 para o gráfico não ficar confuso
    top10 = df.head(10).copy()
    
    # Inverter a ordem para o pior ficar no topo do gráfico
    top10 = top10.iloc[::-1]
    
    fig = px.bar(
        top10, 
        x='probabilidade_ia', 
        y='cve_id', 
        orientation='h',
        title="Top 10 Ameaças Iminentes (IA Score)",
        labels={'probabilidade_ia': 'Probabilidade de Exploração (%)', 'cve_id': 'Vulnerabilidade (CVE)'},
        color='probabilidade_ia',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis=dict(range=[0, 100]),
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0') # Cor de texto clara para dark mode
    )
    return fig


def plot_cvss_vs_ia_scatter(df):
    """Cria um gráfico de dispersão: Nota Tradicional (CVSS) vs Probabilidade Real (IA)."""
    fig = px.scatter(
        df, 
        x='base_score', 
        y='probabilidade_ia', 
        color='attack_vector',
        hover_name='cve_id',
        size_max=15,
        title="Matriz de Risco: CVSS Tradicional vs Previsão IA",
        labels={
            'base_score': 'Severidade CVSS (0-10)', 
            'probabilidade_ia': 'Probabilidade IA (%)',
            'attack_vector': 'Vetor de Ataque'
        },
        template='plotly_dark'
    )
    
    # Linhas de quadrante para destacar a "Zona de Perigo" (Canto Superior Direito)
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Alta Probabilidade (>70%)")
    fig.add_vline(x=7.0, line_dash="dash", line_color="orange", annotation_text="Alto CVSS (>7.0)")
    
    fig.update_traces(marker=dict(size=10, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def plot_threat_distribution_donut(df):
    """Cria um gráfico Donut com a distribuição dos níveis de perigo."""
    
    # Criar categorias baseadas na probabilidade da IA
    def categorizar_risco(prob):
        if prob >= 70: return 'Crítico (Ação Imediata)'
        elif prob >= 40: return 'Elevado (Monitorizar)'
        else: return 'Baixo/Moderado'

    df['Nível de Risco'] = df['probabilidade_ia'].apply(categorizar_risco)
    contagem = df['Nível de Risco'].value_counts().reset_index()
    contagem.columns = ['Nível de Risco', 'Quantidade']
    
    # Cores para cada categoria
    cores = {
        'Crítico (Ação Imediata)': '#ef4444', # Vermelho
        'Elevado (Monitorizar)': '#f59e0b',   # Laranja
        'Baixo/Moderado': '#3b82f6'           # Azul
    }

    fig = px.pie(
        contagem, 
        values='Quantidade', 
        names='Nível de Risco', 
        hole=0.6,
        title="Distribuição do Risco no Lote Atual",
        color='Nível de Risco',
        color_discrete_map=cores
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0')
    )
    return fig