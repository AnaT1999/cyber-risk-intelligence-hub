import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from utils.risk_calculators import simulate_financial_monte_carlo, calculate_rosi, quantum_threat_curve, calculate_var_cvar, propagate_systemic_risk

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulador Preditivo", layout="wide", page_icon=":material/model_training:")

st.title(":material/model_training: Simulador Preditivo e Análise de Retorno (ROSI)")
st.markdown("Projete a exposição financeira da sua organização ao longo do tempo através de simulações estocásticas baseadas na maturidade atual da sua infraestrutura.")
st.divider()

# --- MEMÓRIA DINÂMICA E DADOS COMPLETOS ---
if 'ale_val' in st.session_state:
    ale_atual = st.session_state.get('ale_val', 50000.0)
    faturacao = st.session_state.get('revenue', 1000000.0)
    mat_nist = st.session_state.get('nist_mat', 1) 
    sensibilidade_dados = st.session_state.get('q_dados', 3) 

    # Buscar o nível de Exposição IoT (Q5) diretamente da Matriz
    dados_completos = st.session_state.get('dados_completos', {})
    iot_texto = dados_completos.get("Q5_IoT", "Moderada")
    if "Inexistente" in iot_texto: risco_inicial_iot = 0.05
    elif "Baixa" in iot_texto: risco_inicial_iot = 0.20
    elif "Moderada" in iot_texto: risco_inicial_iot = 0.50
    elif "Alta" in iot_texto: risco_inicial_iot = 0.80
    else: risco_inicial_iot = 1.0 # Crítica

    st.success(f":material/check_circle: **Auditoria Sincronizada com Sucesso:** Perda Média Inicial: **{ale_atual:,.0f} €** | Maturidade NIST: **Tier {mat_nist}** | Sensibilidade: **Nível {sensibilidade_dados}** | Exposição IoT: **{iot_texto.split(' ')[0]}**")
else:
    st.info(":material/info: **Modo de Demonstração Ativo:** Como não sincronizou o Formulário, pode definir o Risco Inicial base manualmente abaixo para testar o motor.")
    ale_atual = st.number_input("Defina a Perda Média Inicial (€) para simulação:", min_value=1000.0, value=50000.0, step=5000.0, help="Este campo só aparece em Modo de Demonstração.")
    
    # Variáveis Padrão
    faturacao = 1000000.0
    mat_nist = 1 
    sensibilidade_dados = 3
    iot_texto = "Moderada"
    risco_inicial_iot = 0.50

# --- CALIBRAÇÃO DINÂMICA DE RISCO ---
drift_dinamico = 0.20 - (mat_nist * 0.02)  
volatilidade_dinamica = 0.15 + (sensibilidade_dados * 0.01) 

# --- BLOCO 1: PAINEL DE COMANDO ESTRATÉGICO ---
st.markdown("### :material/tune: 1. Parâmetros de Simulação e Orçamento")
with st.container(border=True):
    col_anos, col_orcamento, col_eficacia, col_obsol = st.columns(4)
    with col_anos: anos_simulacao = st.slider("Horizonte (Anos)", 1, 10, 5)
    # CORREÇÃO: Removido o limite máximo escondido, usando declaração explícita de min_value e value.
    with col_orcamento: orcamento_defesa = st.number_input("Orçamento (€)", min_value=0.0, value=25000.0, step=5000.0)
    with col_eficacia: eficacia_solucao = st.slider("Eficácia Inicial (%)", 0, 100, 75)
    with col_obsol: obsolescencia = st.slider("Obsolescência Tecnológica", 0.0, 5.0, 1.5, step=0.5, format="%f%% ao ano")

# --- BLOCO 2: MOTOR MATEMÁTICO (Monte Carlo) ---
caminhos_asis = simulate_financial_monte_carlo(ale_initial=ale_atual, drift=drift_dinamico, volatility=volatilidade_dinamica, years=anos_simulacao, simulations=1000, taxa_obsolescencia=0.01)
p50_asis = np.percentile(caminhos_asis, 50, axis=1) 
p95_asis = np.percentile(caminhos_asis, 95, axis=1) 
p05_asis = np.percentile(caminhos_asis, 5, axis=1)  

ale_mitigado = ale_atual * (1.0 - (eficacia_solucao / 100.0))
drift_tobe_base = drift_dinamico * (1.0 - (eficacia_solucao / 100.0) * 0.7)
vol_tobe = volatilidade_dinamica * (1.0 - (eficacia_solucao / 100.0) * 0.4)
caminhos_tobe = simulate_financial_monte_carlo(ale_initial=ale_mitigado, drift=drift_tobe_base, volatility=vol_tobe, years=anos_simulacao, simulations=1000, taxa_obsolescencia=(obsolescencia/100.0))
p50_tobe = np.percentile(caminhos_tobe, 50, axis=1)
p95_tobe = np.percentile(caminhos_tobe, 95, axis=1)
p05_tobe = np.percentile(caminhos_tobe, 5, axis=1)

rosi_calculado = calculate_rosi(np.sum(p50_asis), np.sum(p50_tobe), orcamento_defesa)
var_asis, _ = calculate_var_cvar(caminhos_asis[-1, :])
var_tobe, _ = calculate_var_cvar(caminhos_tobe[-1, :])
estabilidade = (1.0 - (float(np.std(caminhos_tobe[-1, :])) / max(1e-6, float(np.std(caminhos_asis[-1, :]))))) * 100
rrr = (np.sum(p50_tobe) / max(1e-6, np.sum(p50_asis))) * 100

# --- BLOCO 3: VISUALIZAÇÃO SIDE-BY-SIDE ---
st.markdown("<br> <h3>:material/assessment: 2. Projeção de Exposição Financeira (As-Is vs. To-Be) </h3>", unsafe_allow_html=True)
col_grafico, gap, col_kpis = st.columns([2.5, 0.1, 1.2]) 

with col_grafico:
    fig = go.Figure()
    anos_x = np.arange(anos_simulacao + 1)
    
    fig.add_trace(go.Scatter(x=anos_x, y=p95_asis, mode='lines', line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=anos_x, y=p05_asis, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(239, 68, 68, 0.12)', name='Incerteza Atual (5% a 95%)'))
    fig.add_trace(go.Scatter(x=anos_x, y=p50_asis, mode='lines+markers', name='Trajetória Mediana (As-Is)', line=dict(color='rgb(220, 38, 38)', width=3)))

    fig.add_trace(go.Scatter(x=anos_x, y=p95_tobe, mode='lines', line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=anos_x, y=p05_tobe, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(16, 185, 129, 0.18)', name='Incerteza Mitigada (5% a 95%)'))
    fig.add_trace(go.Scatter(x=anos_x, y=p50_tobe, mode='lines+markers', name='Trajetória Mediana (To-Be)', line=dict(color='rgb(5, 150, 105)', width=3)))

    fig.update_layout(
        title="Nuvem de Simulação Monte Carlo (Trajetórias de Prejuízo)",
        xaxis_title="Projeção (Anos)", yaxis_title="Perda Média Esperada (€)", hovermode="x unified",
        legend=dict(font=dict(color="#000000", size=11), bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="rgba(0,0,0,0.15)", borderwidth=1, yanchor="top", y=1, xanchor="left", x=1.02),
        plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=120, t=60, b=0)
    )
    fig.update_xaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', dtick=1)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', tickprefix="€ ", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

with col_kpis:
    st.markdown("#### Justificação de Orçamento")
    risco_evitado = np.sum(p50_asis) - np.sum(p50_tobe)
    
    with st.container(border=True):
        st.metric("Dinheiro Salvo (Prejuízo Evitado)", f"€ {risco_evitado:,.0f}", f"Acumulado em {anos_simulacao} anos", "normal")
        st.metric("Custo da Solução", f"€ -{orcamento_defesa:,.0f}", "Orçamento Inicial", "inverse")
    
    cor_bg = '#dCFce7' if rosi_calculado > 0 else '#fee2e2'
    cor_border = '#10B981' if rosi_calculado > 0 else '#EF4444'
    cor_texto = '#047857' if rosi_calculado > 0 else '#b91c1c'
    
    st.markdown(f"""
    <div style="background-color: {cor_bg}; padding: 20px; border-radius: 12px; border: 2px solid {cor_border}; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
        <h4 style="color: {cor_texto}; margin: 0; text-align: center; text-transform: uppercase; font-size: 0.9rem;">Taxa de Retorno (ROSI)</h4>
        <h1 style="color: {cor_texto}; margin: 5px 0 0 0; text-align: center; font-size: 3rem; font-weight: 800;">{"+" if rosi_calculado > 0 else ""}{rosi_calculado:,.0f}%</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# --- BLOCO 4:  CURVA LEC (LOSS EXCEEDANCE CURVE) ---
st.markdown("### :material/show_chart: 3. Curva de Excedência de Perda (LEC - Probabilidade Catastrófica)")
st.markdown("A **Curva LEC** (Loss Exceedance Curve) reflete o padrão das seguradoras: Qual a probabilidade exata da sua empresa sofrer uma perda superior a *X* Euros num único ano? Quanto mais a curva desce para a esquerda, mais segura está a organização.")

# Cálculo matemático da Curva LEC baseada nos resultados finais do Monte Carlo
perdas_finais_asis = np.sort(caminhos_asis[-1, :])[::-1] # Ordenar do pior cenário para o melhor
perdas_finais_tobe = np.sort(caminhos_tobe[-1, :])[::-1]
probabilidades_lec = (np.arange(1, 1001) / 1000.0) * 100.0 # 0.1% a 100%

fig_lec = go.Figure()
fig_lec.add_trace(go.Scatter(x=perdas_finais_asis, y=probabilidades_lec, mode='lines', name='Risco Atual (As-Is)', line=dict(color='rgb(220, 38, 38)', width=3), fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)'))
fig_lec.add_trace(go.Scatter(x=perdas_finais_tobe, y=probabilidades_lec, mode='lines', name='Risco Mitigado (To-Be)', line=dict(color='rgb(5, 150, 105)', width=3), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.2)'))

fig_lec.update_layout(
    xaxis_title="Perda Financeira Potencial (€)",
    yaxis_title="Probabilidade de Exceder este Valor (%)",
    hovermode="x unified",
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig_lec.update_xaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', tickprefix="€ ", tickformat=",.0f")
fig_lec.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', range=[0, 100])

st.plotly_chart(fig_lec, use_container_width=True)
st.markdown("---")

# --- BLOCO 5: CONTÁGIO IoT (PROCESSO DE HAWKES) ---
st.markdown("### :material/hub: 4. Simulação de Contágio Sistémico (O Vírus IoT)")

# 1. Buscar a lentidão de resposta da empresa à Matriz do Formulário (Q18)
tempo_resposta = dados_completos.get("Q18_Resposta", "Dias")
if "Minutos" in tempo_resposta: 
    dias_contagio = 1  
elif "Horas" in tempo_resposta: 
    dias_contagio = 3  # Dwell time curto
elif "Dias" in tempo_resposta: 
    dias_contagio = 15 # Dwell time médio de Ransomware
else: 
    dias_contagio = 45 # Semanas/Meses

st.markdown(f"Usando o **Processo de Hawkes** e a sua Exposição IoT atual (***{iot_texto.split(' ')[0]}***), este modelo simula como um vírus numa câmara ou sensor compromete progressivamente a rede corporativa inteira nos **{dias_contagio} dias** que a sua equipa demora, em média, a responder a um incidente crítico.")

col_hwk_grafico, col_hwk_texto = st.columns([2.5, 1])

# Lógica de Rede e Hawkes
nos_rede = ['Dispositivos IoT', 'Sistemas IT Básicos', 'Base de Dados de Operações', 'Servidores Financeiros', 'Computadores da Administração']
risco_inicial = np.array([risco_inicial_iot, 0.05, 0.05, 0.02, 0.01])

# Matriz de Adjacência As-Is (Rede Plana / Flat Network - muito comum e perigosa)
matriz_asis = np.array([
    [0.0, 0.5, 0.3, 0.1, 0.1],
    [0.5, 0.0, 0.6, 0.4, 0.3],
    [0.3, 0.6, 0.0, 0.5, 0.2],
    [0.1, 0.4, 0.5, 0.0, 0.6],
    [0.1, 0.3, 0.2, 0.6, 0.0]
])

# Matriz de Adjacência To-Be (Segmentação de Rede / Zero Trust baseada na eficácia da solução)
matriz_tobe = matriz_asis * (1.0 - (eficacia_solucao / 100.0))

# Propagar risco com base no tempo de resposta (Dwell Time)
risco_final_asis = propagate_systemic_risk(matriz_asis, risco_inicial, iterations=dias_contagio, hawkes_decay_rate=0.05)
risco_final_tobe = propagate_systemic_risk(matriz_tobe, risco_inicial, iterations=dias_contagio, hawkes_decay_rate=0.05)

with col_hwk_grafico:
    fig_hawkes = go.Figure()
    fig_hawkes.add_trace(go.Bar(x=nos_rede, y=risco_final_asis * 100, name='Infeção As-Is (Rede Plana)', marker_color='rgb(220, 38, 38)'))
    fig_hawkes.add_trace(go.Bar(x=nos_rede, y=risco_final_tobe * 100, name='Infeção To-Be (Rede Segmentada)', marker_color='rgb(5, 150, 105)'))
    
    fig_hawkes.update_layout(
        barmode='group',
        yaxis_title="Nível de Infeção do Departamento (%)",
        xaxis_title="Departamentos da Empresa",
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_hawkes.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', range=[0, 100])
    st.plotly_chart(fig_hawkes, use_container_width=True)

with col_hwk_texto:
    st.info("**O Efeito Bola de Neve (Hawkes):** Na Cibersegurança, os ataques não são eventos isolados. Se o seu IoT for infetado hoje, a probabilidade de o Departamento Financeiro cair amanhã aumenta exponencialmente devido à conectividade da rede.")
    st.success(f"**Vantagem da Mitigação:** A sua solução não se limitou a baixar o risco do IoT; ao aplicar eficácia de **{eficacia_solucao}%**, atuou como 'Quebra-Fogo' (Segmentação de Rede), protegendo a Administração de contágio direto.")

st.markdown("---")

# --- BLOCO 6: DASHBOARD DE DESEMPENHO  ---
st.markdown("### :material/speed: 5. Dashboard de Desempenho Operacional")
col_g1, col_g2, col_g3 = st.columns(3)

if rrr <= 30: bg_rrr, font_rrr, bar_rrr = "#ecfdf5", "#064e3b", "#10b981" 
elif rrr <= 70: bg_rrr, font_rrr, bar_rrr = "#fffbeb", "#78350f", "#f59e0b" 
else: bg_rrr, font_rrr, bar_rrr = "#fef2f2", "#7f1d1d", "#ef4444" 

if estabilidade >= 70: bg_est, font_est, bar_est = "#ecfdf5", "#064e3b", "#10b981" 
elif estabilidade >= 30: bg_est, font_est, bar_est = "#fffbeb", "#78350f", "#f59e0b" 
else: bg_est, font_est, bar_est = "#fef2f2", "#7f1d1d", "#ef4444" 

if var_tobe < var_asis: bg_var, font_var = "#ecfdf5", "#064e3b" 
else: bg_var, font_var = "#fef2f2", "#7f1d1d" 

with col_g1:
    fig_rrr = go.Figure(go.Indicator(mode = "gauge+number", value = min(100, max(0, rrr)), number = {'suffix': "%", 'font': {'size': 40, 'color': font_rrr}}, title = {'text': f"Risco Residual (RRR)<br><span style='font-size:0.8em;color:{font_rrr}'>Percentagem não mitigada</span>", 'font': {'size': 18, 'color': font_rrr}}, gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': font_rrr}, 'bar': {'color': bar_rrr, 'thickness': 0.2}, 'bgcolor': "rgba(255,255,255,0.5)", 'steps': [{'range': [0, 30], 'color': "rgba(16, 185, 129, 0.2)"}, {'range': [30, 70], 'color': "rgba(245, 158, 11, 0.2)"}, {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.2)"}]}))
    fig_rrr.update_layout(height=340, margin=dict(l=30, r=30, t=100, b=30), paper_bgcolor=bg_rrr)
    st.plotly_chart(fig_rrr, use_container_width=True)

with col_g2:
    fig_est = go.Figure(go.Indicator(mode = "gauge+number", value = min(100, max(0, estabilidade)), number = {'suffix': "%", 'font': {'size': 40, 'color': font_est}}, title = {'text': f"Ganho de Estabilidade<br><span style='font-size:0.8em;color:{font_est}'>Redução da Volatilidade</span>", 'font': {'size': 18, 'color': font_est}}, gauge = {'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': font_est}, 'bar': {'color': bar_est, 'thickness': 0.2}, 'bgcolor': "rgba(255,255,255,0.5)", 'steps': [{'range': [0, 30], 'color': "rgba(239, 68, 68, 0.2)"}, {'range': [30, 70], 'color': "rgba(245, 158, 11, 0.2)"}, {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}]}))
    fig_est.update_layout(height=340, margin=dict(l=30, r=30, t=100, b=30), paper_bgcolor=bg_est)
    st.plotly_chart(fig_est, use_container_width=True)

with col_g3:
    fig_var = go.Figure(go.Indicator(mode = "number+delta", value = var_tobe, number = {'prefix': "€", 'valueformat': ",.0f", 'font': {'size': 35, 'color': font_var}}, delta = {'reference': var_asis, 'relative': False, 'valueformat': ",.0f", 'position': "bottom", 'font': {'size': 20}}, title = {'text': f"Value at Risk (VaR 95%)<br><span style='font-size:0.8em;color:{font_var}'>Pior Cenário no Ano {anos_simulacao}</span>", 'font': {'size': 18, 'color': font_var}}))
    fig_var.update_layout(height=340, margin=dict(l=30, r=30, t=100, b=30), paper_bgcolor=bg_var)
    st.plotly_chart(fig_var, use_container_width=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- BLOCO 7: O Diagrama de Mosca E Tabela ---
st.markdown("### :material/timer: 6. Cronograma Quântico e Histórico Financeiro")
col_q_grafico, col_tab = st.columns([2, 1.5])

with col_q_grafico:
    prob_quantica = quantum_threat_curve(anos_simulacao, sensibilidade_dados)
    ale_q_total = float(np.sum(p50_asis * (np.array(prob_quantica) / 100.0)))
    fig_q = go.Figure()
    fig_q.add_trace(go.Scatter(x=np.arange(anos_simulacao + 1), y=prob_quantica, mode='lines+markers', line=dict(color='rgb(139, 92, 246)', width=4), fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.1)', name="Probabilidade de Quebra"))
    fig_q.update_layout(title=f"Exposição Quântica Acumulada: € {ale_q_total:,.0f}", xaxis_title="Projeção (Anos a partir de Hoje)", yaxis_title="Probabilidade (%)", yaxis=dict(range=[0, 100]), plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=50, b=0))
    fig_q.update_xaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', dtick=1)
    fig_q.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)')
    st.plotly_chart(fig_q, use_container_width=True)

with col_tab:
    anos_list = np.arange(anos_simulacao + 1)
    df_table = pd.DataFrame({"Período": [f"Ano {ano}" if ano > 0 else "Ano Inicial" for ano in anos_list], "As-Is (€)": [f"{val:,.0f} €" for val in p50_asis], "To-Be (€)": [f"{val:,.0f} €" for val in p50_tobe], "Poupança": [f"{val_asis - val_tobe:,.0f} €" for val_asis, val_tobe in zip(p50_asis, p50_tobe)]})
    st.dataframe(df_table, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Desenvolvido no âmbito da disciplina de Avaliação do Risco em Cibersegurança | © 2026")