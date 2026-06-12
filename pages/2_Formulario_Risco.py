import streamlit as st
import pandas as pd
import json
import numpy as np
import math
from datetime import datetime
from fpdf import FPDF
from utils.risk_calculators import calculate_fair_ale, calculate_iso_risk, calculate_advanced_pqr, calculate_dri, calculate_var_cvar
import zipfile
import io

st.markdown("## :shield: Avaliação Unificada de Risco Corporativo (NIST & FAIR)")
st.write("Preencha o formulário detalhado abaixo para quantificar a postura de cibersegurança da sua organização. Este questionário cruza dados financeiros, organizacionais e de infraestrutura técnica.")

st.markdown("---")

# --- FORMULÁRIO UNIFICADO  ---
with st.form("form_risco_global_avancado"):
    
    # --- BLOCO 1: CONTEXTO DE NEGÓCIO E ATIVOS (FAIR & ISO) ---
    st.markdown("### :material/business: Bloco 1: Contexto de Negócio e Ativos")
    st.write("Nesta secção, identificamos a dimensão financeira e a importância dos dados que a sua organização manuseia no dia a dia.")
    
    col1, col2 = st.columns(2)
    with col1:
        revenue = st.number_input(
            "1. Faturação / Orçamento Anual da Organização (€):",
            min_value=10000, max_value=1000000000, value=1000000, step=50000,
            help="Este valor serve de base para calcular o impacto financeiro real em caso de paragem de sistemas ou multas."
        )
        
        asset_value_text = st.selectbox(
            "2. Qual é a importância deste ativo/sistema para a operação?",
            ["Baixa (Impacto mínimo se parar)", "Moderada (Causa lentidão, mas o negócio continua)", "Elevada (Perdas financeiras imediatas)", "Crítica (O negócio para completamente)"],
            help="Mede o impacto operacional direto caso o sistema seja atacado ou fique offline."
        )
        
    with col2:
        i_dados_text = st.selectbox(
            "3. Que tipo de dados estão guardados ou são processados neste sistema?",
            ["Dados Públicos (Sem qualquer sensibilidade)", "Dados Internos (Documentos e emails normais da empresa)", "Dados Pessoais Regulados (RGPD, dados de clientes ou funcionários)", "Dados Altamente Confidenciais (Propriedade Intelectual ou Segredos comerciais)"],
            help="Alimenta o cálculo de impactos secundários, como custos com reputação e sanções legais."
        )
        
        exposicao_text = st.selectbox(
            "4. Qual é o nível de exposição à rede deste sistema?",
            ["Isolado (Sem qualquer ligação à Internet)", "Interno (Apenas acessível dentro do escritório ou via VPN)", "DMZ (Zona semi-protegida)", "Internet-facing (Público na Web e exposto diretamente)"],
            help="Determina a facilidade com que um atacante externo consegue descobrir o sistema."
        )

    st.markdown("---")
    
    # --- BLOCO 2: INFRAESTRUTURA, AMEAÇAS E MATURIDADE (NIST & ISO) ---
    st.markdown("### :material/router: Bloco 2: Infraestrutura, Ameaças e Maturidade")
    st.write("Avaliação da segurança dos dispositivos físicos (IoT), frequência de ataques e resiliência das defesas atuais.")
    
    col3, col4 = st.columns(2)
    with col3:
        iot_exposure_text = st.selectbox(
            "5. Nível de Exposição de Dispositivos IoT na Rede:",
            ["Baixa (Totalmente isolados e protegidos)", "Moderada (Em redes separadas, mas comunicam com servidores)", "Alta (Ligados na mesma rede dos computadores normais)", "Crítica (Acessíveis a partir de fora sem segurança)"],
            help="Avalia se um atacante pode usar uma câmara de segurança ou sensor IoT para infetar o resto da empresa."
        )
        
        tef_text = st.selectbox(
            "6. Frequência estimada de tentativas de ataque detetadas (Phishing, Scans):",
            ["Baixa (1 a 2 vezes por ano)", "Moderada (Tentativas mensais)", "Elevada (Várias vezes por semana)", "Crítica (Ataques e tentativas diárias)"],
            help="Estabelece a frequência com que os atacantes tentam forçar as vossas defesas."
        )
        
        f_adversary_text = st.selectbox(
            "7. Qual o perfil de atacante mais provável para o vosso setor?",
            ["Amadores / Erros acidentais internos", "Cibercriminosos genéricos (Ataques oportunos em massa)", "Ameaças internas maliciosas (Ex-funcionários)", "Grupos de Ransomware organizados / Estados-Nação (Alvo direcionado)"],
            help="Define o nível de sofisticação e recursos que o inimigo tem para vos atacar."
        )
        
    with col4:
        vuln_text = st.selectbox(
            "8. Estado de atualizações e falhas conhecidas (CVEs) nos sistemas:",
            ["Excelente (Sistemas totalmente atualizados e sem falhas)", "Moderado (Algumas falhas leves conhecidas - CVSS < 7)", "Elevado (Existem falhas graves não corrigidas - CVSS 7-9)", "Crítico (Existem falhas críticas públicas por corrigir - CVSS > 9)"],
            help="Mede se a empresa deixa 'portas abertas' conhecidas na internet por falta de manutenção."
        )
        
        nist_maturity_text = st.selectbox(
            "9. Nível de maturidade geral dos controlos de segurança (NIST Tiers):",
            ["Tier 1 - Parcial (Defesas reativas, sem processos formais)", "Tier 2 - Informado pelo Risco (A direção apoia, mas não há automação)", "Tier 3 - Repetível (Processos formais e equipas treinadas)", "Tier 4 - Adaptativo (Defesas proativas, automáticas e líderes de mercado)"],
            help="O nível de organização e preparação da equipa de segurança face a normas internacionais."
        )
        
        recover_text = st.selectbox(
            "10. Estado das cópias de segurança (Backups) e capacidade de recuperação:",
            ["Inexistentes ou nunca testadas", "Backups online normais (Podem ser encriptados por Ransomware)", "Backups offline periódicos (Seguros, mas perda de alguns dias de dados)", "Backups imutáveis offline com plano de recuperação testado com sucesso"],
            help="Determina se a empresa consegue recuperar os seus dados após um desastre cibernético."
        )

    st.markdown("---")
    
    # --- BLOCO 3: POSTURA CRIPTOGRÁFICA E RISCO PÓS-QUÂNTICO (PQR) ---
    st.markdown("### :material/hourglass_empty: Bloco 3: Postura Criptográfica e Risco Pós-Quântico")
    st.write("Avaliamos a longevidade dos vossos segredos e a vossa capacidade de resistir ao advento dos computadores quânticos.")
    
    col5, col6 = st.columns(2)
    with col5:
        i_longevity = st.slider(
            "11. Durante quantos anos estes dados precisam de se manter confidenciais? (D):", 
            min_value=1, max_value=25, value=10,
            help="Se os vossos dados forem roubados hoje, durante quantos anos o seu conteúdo ainda causará dano se for lido?"
        )
        
        crypto_alg_text = st.selectbox(
            "12. Algoritmo de Encriptação Primário Atual:",
            ["AES-256 (Resistente Quântico)", "RSA-4096 (Risco Médio)", "RSA-2048 (Risco Elevado)", "DES/3DES ou MD5 (Obsoleto/Crítico)"],
            help="Os algoritmos RSA e ECC atuais serão totalmente quebrados por computadores quânticos no futuro."
        )
        
        rsa_long_term_text = st.selectbox(
            "13. Há uso de criptografia assimétrica clássica (RSA/ECC) para dados de longa duração?",
            ["Não aplicável", "Apenas para sessões curtas de navegação", "Para proteger arquivos guardados em arquivo/backup", "Sim, para dados altamente críticos de longo prazo"],
            help="Identifica se dados históricos e confidenciais estão guardados com chaves fáceis de quebrar no futuro quântico."
        )
        
    with col6:
        p_harvest_text = st.selectbox(
            "14. Os vossos dados circulam por canais que podem estar a ser gravados hoje?",
            ["Isolado / Canais de fibra ultra-seguros", "Redes normais protegidas com chaves fortes (TLS)", "Canais corporativos via VPN clássica", "Canais públicos ou sem qualquer proteção quântica"],
            help="Alimenta o risco de 'Harvest Now, Decrypt Later' (Ataques onde os hackers gravam a vossa rede hoje para a decifrar daqui a uns anos)."
        )
        
        m_pqc_text = st.selectbox(
            "15. Existe um plano de migração ativa para criptografia Pós-Quântica (PQC)?",
            ["Sem qualquer plano ou orçamento", "Plano conceptual em discussão, sem prazos", "Plano definido com projetos piloto ativos", "Plano em execução total com substituição faseada de sistemas"],
            help="Avalia se a organização já está a testar a substituição de chaves antigas pelas novas cifras pós-quânticas."
        )
        
        m_qkd_text = st.selectbox(
            "16. Existe utilização ou plano de implementação de QKD (Quantum Key Distribution)?",
            ["Não aplicável ou sem orçamento disponível", "Orçamento limitado com projetos piloto em avaliação", "Infraestrutura dedicada já instalada em pontos críticos"],
            help="A distribuição quântica de chaves por laser/fibra zera o risco de interceção física de chaves criptográficas."
        )

    st.markdown("---")

    # --- BLOCO 4: DESINFORMAÇÃO SINTÉTICA E REPUTAÇÃO (DRI) ---
    st.markdown("### :material/campaign: Bloco 4: Desinformação Sintética e Reputação")
    st.write("Aparato de monitorização e velocidade de resposta contra ataques à imagem da empresa gerados por Inteligência Artificial (Deepfakes).")
    
    col7, col8 = st.columns(2)
    with col7:
        media_exposure = st.slider(
            "17. Dependência Reputacional e Exposição Mediática da Empresa (%):",
            min_value=1, max_value=100, value=75,
            help="Se uma notícia falsa ou vídeo falso (Deepfake) se espalhar, qual a probabilidade de causar pânico nos clientes?"
        )
        
    with col8:
        response_time = st.selectbox(
            "18. Tempo formal de reação e desmentido face a campanhas de desinformação:",
            ["< 1 Hora (Monitorização Ativa de Redes e Resposta Imediata)", "1 a 24 Horas (Reação rápida da equipa de RP)", "Dias (A análise passa por vários diretores antes de responder)", "Semanas / Inexistente (A empresa não tem plano de resposta a crises de imagem)"],
            help="Quanto mais tempo o mercado passar a acreditar numa mentira sintética, maior o dano financeiro catastrófico."
        )

    st.markdown("---")
    submitted = st.form_submit_button(":material/settings: Processar Avaliação Multivetorial", use_container_width=True)

# --- PROCESSAMENTO EXECUTIVO ---
if submitted:
    st.markdown("## :material/analytics: Relatório Oficial de Avaliação de Risco")
    
    # Mapeamento ultra-seguro (procura apenas palavras-chave imutáveis)
    map_asset = {"Baixa": 1, "Moderada": 2, "Elevada": 3, "Crítica": 5}
    asset_val = next(v for k, v in map_asset.items() if k in asset_value_text)
    
    map_dados = {"Públicos": 1, "Internos": 2, "Pessoais": 3, "Confidenciais": 5}
    i_dados = next(v for k, v in map_dados.items() if k in i_dados_text)
    
    map_exposicao = {"Isolado": 1, "Interno": 2, "DMZ": 3, "Internet-facing": 5}
    exposicao_val = next(v for k, v in map_exposicao.items() if k in exposicao_text)
    
    map_iot = {"Baixa": 1, "Moderada": 2, "Alta": 3, "Crítica": 4}
    iot_val = next(v for k, v in map_iot.items() if k in iot_exposure_text)
    
    map_tef = {"Baixa": 1, "Moderada": 5, "Elevada": 10, "Crítica": 20}
    tef_score = next(v for k, v in map_tef.items() if k in tef_text)
    
    map_adversary = {"Amadores": 1, "Cibercriminosos": 2, "internas": 3, "Ransomware": 5}
    f_adversary = next(v for k, v in map_adversary.items() if k in f_adversary_text)
    
    map_vuln = {"Excelente": 1, "Moderado": 2, "Elevado": 4, "Crítico": 5}
    vuln_score = next(v for k, v in map_vuln.items() if k in vuln_text)
    
    map_nist = {"Tier 1": 1, "Tier 2": 2, "Tier 3": 3, "Tier 4": 5}
    nist_maturity = next(v for k, v in map_nist.items() if k in nist_maturity_text)
    
    map_recover = {"Inexistentes": 1, "online": 2, "offline periódicos": 3, "imutáveis": 5}
    recover_score = next(v for k, v in map_recover.items() if k in recover_text)
    
    map_crypto = {"AES-256": 1, "RSA-4096": 2, "RSA-2048": 4, "DES/3DES": 5}
    p_quantum = next(v for k, v in map_crypto.items() if k in crypto_alg_text)
    
    # AQUI ESTAVA O ERRO PRINCIPAL. Palavras-chave corrigidas:
    map_rsa_long = {"Não aplicável": 1, "sessões curtas": 2, "arquivos guardados": 4, "dados altamente críticos": 5}
    rsa_long_val = next(v for k, v in map_rsa_long.items() if k in rsa_long_term_text)
    
    map_harvest = {"Isolado": 1, "Redes normais": 2, "Canais corporativos": 3, "Canais públicos": 5}
    p_harvest = next(v for k, v in map_harvest.items() if k in p_harvest_text)
    
    # AQUI ESTAVA OUTRO POTENCIAL ERRO CORRIGIDO:
    map_mpqc = {"Sem qualquer": 1, "conceptual": 2, "piloto": 4, "execução": 5}
    m_pqc = next(v for k, v in map_mpqc.items() if k in m_pqc_text)
    
    map_mqkd = {"Não aplicável": 1, "Orçamento limitado": 2, "Infraestrutura dedicada": 5}
    m_qkd = next(v for k, v in map_mqkd.items() if k in m_qkd_text)
    
    map_response = {"< 1 Hora": 0.5, "1 a 24 Horas": 1.5, "Dias": 3.0, "Semanas": 5.0}
    velocity_val = next(v for k, v in map_response.items() if k in response_time)

    # --- EXECUÇÃO DOS CÁLCULOS MATEMÁTICOS ---
    # 1. FAIR Financeiro
    lef_annual, lm_total, ale_val = calculate_fair_ale(revenue, float(tef_score), float(vuln_score), float(nist_maturity), float(i_dados))
    
    # 2. ISO 27005 (Módulo IoT expandido com variáveis de infraestrutura)
    risco_iso_base = calculate_iso_risk(asset_val, iot_val, vuln_score, nist_maturity)
    
    # 3. PQR Estocástico Avançado
    r_futuro, r_hndl, r_residual = calculate_advanced_pqr(i_longevity, i_dados, p_quantum, p_harvest, f_adversary, m_pqc, m_qkd)
    
    # 4. DRI Desinformação
    reach_simulated = int(media_exposure * 10000) # Simula mais impacto
    # Removemos o cálculo complexo antigo do DRI que limitava a 10% e criamos uma percentagem direta
    risco_dri_perc = min(100.0, (media_exposure) * (velocity_val / 1.5))

    # 5. Cálculo do VaR e CVaR de cauda pesada (Black Swan Financeiro)
    # Geramos uma simulação rápida de perdas para alimentar a função de cauda
    np.random.seed(42)
    simulated_losses = np.random.lognormal(mean=math.log(max(1.0, ale_val)), sigma=0.7, size=1000)
    simulated_losses = np.clip(simulated_losses, 0.0, lm_total * 10.0) 
    var_95, cvar_95 = calculate_var_cvar(simulated_losses, confidence_level=0.95)

    # Score de Postura Qualitativa Global (Mapeado de 0 a 100)
    risco_global_score = (risco_iso_base * 0.25) + (r_residual * 0.40) + (risco_dri_perc * 0.35)

    def calc_level(score):
        if score < 30: return "Baixo", ":material/check_circle:"     
        if score < 60: return "Moderado", ":material/remove_circle:"          
        if score < 80: return "Elevado", ":material/error:"       
        return "Crítico", ":material/dangerous:"                    

    nv_global, cor_global = calc_level(risco_global_score)

    # Painel Executivo Principal
    st.info(f"**Score Global de Postura de Risco:** {risco_global_score:.1f}/100 ({nv_global}) {cor_global}")
    
    colA, colB, colC = st.columns(3)
    colA.metric("Risco de Infraestrutura (ISO)", f"{risco_iso_base:.1f}%", f"Estado: {calc_level(risco_iso_base)[0]}", delta_color="off")
    colB.metric("Risco Quântico Residual", f"{r_residual:.1f}%", f"Estado: {calc_level(r_residual)[0]}", delta_color="off")
    colC.metric("Risco Reputacional (DRI)", f"{risco_dri_perc:.1f}%", f"Estado: {calc_level(risco_dri_perc)[0]}", delta_color="off")

    # --- NOVO BLOCO QUANTITATIVO FINANCEIRO (FAIR & VaR/CVaR) ---
    st.markdown("### :material/monetization_on: Exposição Financeira Anualizada (Modelo FAIR & Cauda Pesada)")
    st.write("Abaixo encontra a tradução exata dos riscos técnicos em valores monetários reais, essencial para discussão em conselhos de administração.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f1.metric("Perda Anual Esperada (ALE)", f"{ale_val:,.2f} €", "Média Normal", delta_color="off")
    col_f2.metric("Value at Risk (VaR 95%)", f"{var_95:,.2f} €", "Pior Cenário (95%)", delta_color="inverse")
    col_f3.metric("Conditional VaR (CVaR)", f"{cvar_95:,.2f} €", "Média do Desastre Catastrófico", delta_color="inverse")

    # --- RECOMENDAÇÕES DINÂMICAS ---
    st.markdown("### :material/lightbulb: Inteligência Acionável")
    
    if risco_iso_base >= 60:
        st.error("**Fator Ciber-Físico (IoT):** A sua infraestrutura IoT está exposta e sem monitorização contínua. Isole imediatamente estes sensores em VLANs dedicadas sem comunicação direta com a rede corporativa principal.")
    if r_residual >= 50:
        st.error(f"**Vulnerabilidade Quântica Grave:** Os seus dados corporativos sofrem de elevado risco de interceção e gravação no modelo 'Harvest Now, Decrypt Later'. Inicie a transição das vossas chaves assimétricas para cifras híbridas NIST PQC.")
    if p_quantum >= 4:
        st.warning("**Uso de Criptografia Obsoleta:** Detetámos chaves RSA-2048 ou cifras clássicas legadas que já são vulneráveis a ataques clássicos otimizados. Evolua a infraestrutura interna para AES-256 de forma urgente.")
    if risco_dri_perc >= 50:
        st.warning("**Inércia Reputacional:** A sua organização demora mais de 1 hora a reagir a crises mediáticas. Campanhas de desinformação baseadas em IA (Deepfakes) propagam-se de forma exponencial. Recomenda-se a contratação de ferramentas OSINT de deteção precoce.")
    if recover_score == 1 or recover_score == 2:
        st.error("**Vulnerabilidade Crítica de Recuperação:** A sua política de backups está desatualizada ou vulnerável a Ransomware. Implemente cópias de segurança imutáveis offline de forma a mitigar a cauda pesada de prejuízos calculada no CVaR.")

    st.markdown("---")
    
    # Dicionário com todos os textos e números estruturados para o motor de design
    dados_para_pdf = {
        "Orcamento_Empresa": revenue,
        "Score_Global": risco_global_score,
        "Nivel_Global": nv_global,
        "IoT_ISO_Risco": risco_iso_base,
        "Nivel_IoT": calc_level(risco_iso_base)[0],
        "PQR_Residual": r_residual,
        "Nivel_PQR": calc_level(r_residual)[0],
        "DRI_Risco": risco_dri_perc,
        "Nivel_DRI": calc_level(risco_dri_perc)[0],
        "FAIR_ALE": ale_val,
        "VaR_95": var_95,
        "CVaR_Pior_Cenario": cvar_95,
        "Q1_Receita": revenue,
        "Q2_Ativo": asset_value_text,
        "Q3_Dados": i_dados_text,
        "Q4_Exposicao_Rede": exposicao_text,
        "Q5_IoT": iot_exposure_text,
        "Q6_TEF": tef_text,
        "Q7_Adversario": f_adversary_text,
        "Q8_CVE": vuln_text,
        "Q9_NIST": nist_maturity_text,
        "Q10_Backups": recover_text,
        "Q11_Vida_Util": i_longevity,
        "Q12_Cripto": crypto_alg_text,
        "Q13_RSA_Longo": rsa_long_term_text,
        "Q14_Canais": p_harvest_text,
        "Q15_PQC": m_pqc_text,
        "Q16_QKD": m_qkd_text,
        "Q17_Media": media_exposure,
        "Q18_Resposta": response_time
    }

    # --- EXPORTAÇÕES ---
    st.markdown("#### :material/cloud_download: Exportar Relatório Oficial e Matrizes de Dados")
    
    # 1. Gerar os bytes de todos os ficheiros antecipadamente
    from utils.report_generator import generate_pdf
    from utils.excel_generator import generate_excel
    
    pdf_bytes = generate_pdf(dados_para_pdf)
    excel_bytes = generate_excel(dados_para_pdf)
    json_str = json.dumps(dados_para_pdf, indent=4)
    
    # 2. Layout dos 3 botões individuais
    col_pdf, col_excel, col_json = st.columns(3)
    
    with col_pdf:
        st.download_button(label=":material/picture_as_pdf: Relatório Executivo (PDF)", data=pdf_bytes, file_name="relatorio_risco_executivo.pdf", mime="application/pdf", use_container_width=True)
        
    with col_excel:
        st.download_button(
            label=":material/table_chart: Matriz Estruturada (EXCEL)", 
            data=excel_bytes, 
            file_name="matriz_risco_detalhada.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
            use_container_width=True
        )

    with col_json:
        st.download_button(label=":material/data_object: Telemetria Pura (JSON)", data=json_str, file_name="telemetria_risco.json", mime="application/json", use_container_width=True)
    
    # 3. Criar o pacote ZIP com os 3 ficheiros
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("relatorio_risco_executivo.pdf", pdf_bytes)
        zip_file.writestr("matriz_risco_detalhada.xlsx", excel_bytes)
        zip_file.writestr("telemetria_risco.json", json_str)
        
    # 4. O Botão Estável de Download Múltiplo
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label=":material/folder_zip: Descarregar Pacote Completo de Auditoria (ZIP)", 
        data=zip_buffer.getvalue(), 
        file_name="pacote_auditoria_risco.zip", 
        mime="application/zip", 
        use_container_width=True
    )