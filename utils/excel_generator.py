import pandas as pd
import io

def generate_excel(data_dict: dict) -> bytes:
    # Cria um ficheiro Excel em memória (Buffer)
    output = io.BytesIO()
    
    # --- 1. Tabela de Resumo Executivo ---
    df_exec = pd.DataFrame({
        "Indicador Global": ["Score Global de Risco", "Nível de Gravidade", "Risco ISO 27005 (IoT/Infra)", "Risco Quântico Residual", "Risco Reputacional (DRI)"],
        "Resultado": [
            f"{data_dict['Score_Global']:.1f}%", 
            data_dict['Nivel_Global'], 
            f"{data_dict['IoT_ISO_Risco']:.1f}%", 
            f"{data_dict['PQR_Residual']:.1f}%", 
            f"{data_dict['DRI_Risco']:.1f}%"
        ]
    })
    
    # --- 2. Tabela Financeira (FAIR & Cauda Pesada) ---
    df_fin = pd.DataFrame({
        "Métrica Financeira": ["Perda Média Esperada (ALE)", "Value at Risk (VaR 95%)", "Conditional CVaR (Média do Pior Cenário)"],
        "Valor Exposto (€)": [
            data_dict['FAIR_ALE'], 
            data_dict['VaR_95'], 
            data_dict['CVaR_Pior_Cenario']
        ]
    })
    
    # --- 3. Tabela de Respostas do Utilizador (Telemetria) ---
    df_telemetria = pd.DataFrame({
        "Bloco de Auditoria": [
            "1. Negócio e Ativos", "1. Negócio e Ativos", "1. Negócio e Ativos", "1. Negócio e Ativos",
            "2. Infraestrutura e Ameaças", "2. Infraestrutura e Ameaças", "2. Infraestrutura e Ameaças", "2. Infraestrutura e Ameaças", "2. Infraestrutura e Ameaças", "2. Infraestrutura e Ameaças",
            "3. Risco Quântico (PQR)", "3. Risco Quântico (PQR)", "3. Risco Quântico (PQR)", "3. Risco Quântico (PQR)", "3. Risco Quântico (PQR)", "3. Risco Quântico (PQR)",
            "4. Desinformação (DRI)", "4. Desinformação (DRI)"
        ],
        "Parâmetro Inspecionado": [
            "1. Orçamento / Faturação Anual", "2. Criticidade do Ativo", "3. Tipo de Dados Processados", "4. Exposição à Rede",
            "5. Exposição IoT", "6. Frequência de Ataques", "7. Perfil do Adversário", "8. Vulnerabilidades (CVEs)", "9. Maturidade NIST", "10. Estado dos Backups",
            "11. Vida Útil dos Dados (Anos)", "12. Criptografia Primária", "13. Uso de Criptografia Legada", "14. Gravação de Canais (Harvesting)", "15. Migração PQC", "16. Implementação QKD",
            "17. Exposição Mediática (%)", "18. Velocidade de Resposta a Crises"
        ],
        "Resposta Registada": [
            f"{data_dict['Q1_Receita']:,.2f} €", data_dict['Q2_Ativo'], data_dict['Q3_Dados'], data_dict['Q4_Exposicao_Rede'],
            data_dict['Q5_IoT'], data_dict['Q6_TEF'], data_dict['Q7_Adversario'], data_dict['Q8_CVE'], data_dict['Q9_NIST'], data_dict['Q10_Backups'],
            data_dict['Q11_Vida_Util'], data_dict['Q12_Cripto'], data_dict['Q13_RSA_Longo'], data_dict['Q14_Canais'], data_dict['Q15_PQC'], data_dict['Q16_QKD'],
            data_dict['Q17_Media'], data_dict['Q18_Resposta']
        ]
    })

    # --- 4. CONSTRUÇÃO DA NOVA TABELA DINÂMICA DE AJUDAS / MITIGAÇÃO ---
    acoes_lista = []
    
    if data_dict['CVaR_Pior_Cenario'] > (data_dict['Orcamento_Empresa'] * 0.05):
        acoes_lista.append({
            "Ação Estratégica": "I. Contenção de Exposição Financeira",
            "Vetor Alvo": "Governação & Risco de Cauda",
            "Diretriz de Solução / Ajuda Técnica": f"A análise quantitativa revela uma exposição catastrófica potencial de {data_dict['CVaR_Pior_Cenario']:,.2f} EUR no percentil de 5% (CVaR). É mandatória a contratação de uma apólice de Ciberseguro (Cyber Insurance) calibrada para absorver especificamente este impacto de cauda pesada."
        })

    if any(k in data_dict['Q5_IoT'] for k in ["Moderada", "Alta", "Crítica"]):
        acoes_lista.append({
            "Ação Estratégica": "II. Blindagem Ciber-Física e Segmentação",
            "Vetor Alvo": "ISO 27005 / NIST Protect",
            "Diretriz de Solução / Ajuda Técnica": "Dispositivos IoT operam frequentemente com firmware não assinado. A configuração de rede atual cria pivôs de intrusão. O plano de ação exige: 1) Isolamento em VLANs estritas; 2) Políticas de arquitetura Zero-Trust; 3) Bloqueio de comunicação direta do IoT para a Internet pública."
        })
    
    if data_dict['PQR_Residual'] >= 30 or any(k in data_dict['Q12_Cripto'] for k in ["RSA", "DES"]):
        acoes_lista.append({
            "Ação Estratégica": "III. Migração Criptográfica Pós-Quântica",
            "Vetor Alvo": "Resiliência de Canal Cripto",
            "Diretriz de Solução / Ajuda Técnica": f"Dados cuja utilidade confidencial exceda os {data_dict['Q11_Vida_Util']} anos estão em risco imediato pela estratégia 'Harvest Now, Decrypt Later'. A organização deve abandonar algoritmos clássicos (RSA/ECC) e adotar urgentemente as cifras NIST ML-KEM para encapsulamento de chaves híbridas."
        })

    if any(k in data_dict['Q18_Resposta'] for k in ["Dias", "Semanas"]) or data_dict['DRI_Risco'] >= 50:
        acoes_lista.append({
            "Ação Estratégica": "IV. Deteção Precoce de Desinformação Sintética",
            "Vetor Alvo": "NIST Detect & Respond (DRI)",
            "Diretriz de Solução / Ajuda Técnica": "A inércia de resposta atual não é compatível contra campanhas impulsionadas por IA Gerativa (Deepfakes). A organização deve implementar ferramentas passivas de inteligência OSINT e definir guiões de resposta (PR Playbooks) com emissão de desmentidos oficiais em menos de 1 hora."
        })

    if any(k in data_dict['Q10_Backups'] for k in ["Inexistentes", "online"]):
        acoes_lista.append({
            "Ação Estratégica": "V. Continuidade de Negócio e Recuperação Limpa",
            "Vetor Alvo": "NIST Recover (Resiliência)",
            "Diretriz de Solução / Ajuda Técnica": "A política de backups submetida é altamente vulnerável a Ransomwares modernos. A salvaguarda da faturação operacional exige uma estratégia de backup '3-2-1' com um pilar de armazenamento Air-Gapped (offline) e imutável (WORM), isento de suborno ou encriptação remota."
        })

    if not acoes_lista:
        acoes_lista.append({
            "Ação Estratégica": "Auditoria Concluída com Sucesso",
            "Vetor Alvo": "Excelência Global",
            "Diretriz de Solução / Ajuda Técnica": "A organização demonstrou um nível de maturidade, arquitetura de rede e higiene criptográfica de excelência. Não foram detetados vetores críticos de ataque estrutural nas variáveis analisadas. Recomenda-se apenas a manutenção contínua do SOC e vigilância sobre a evolução do cronograma quântico (Y2Q)."
        })

    df_mitigacao = pd.DataFrame(acoes_lista)

    # --- 5. Tabela "Raw Data" para Dashboards ---
    df_raw = pd.DataFrame([data_dict])

    # --- DEFINIÇÃO DE CORES DINÂMICAS PARA OS CABEÇALHOS ---
    nivel = data_dict.get('Nivel_Global', 'Baixo')
    if "Baixo" in nivel:
        cor_cabecalho = '#10B981' # Verde
    elif "Moderado" in nivel:
        cor_cabecalho = '#F59E0B' # Amarelo 
    elif "Elevado" in nivel:
        cor_cabecalho = '#EA580C' # Laranja
    else:
        cor_cabecalho = '#EF4444' # Vermelho 

    # --- Processamento e Formatação do Ficheiro Excel ---
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_exec.to_excel(writer, sheet_name="Resumo Executivo", index=False)
        df_fin.to_excel(writer, sheet_name="Financeiro (FAIR)", index=False)
        df_telemetria.to_excel(writer, sheet_name="Respostas do Formulário", index=False)
        df_mitigacao.to_excel(writer, sheet_name="Plano de Mitigacao", index=False)
        df_raw.to_excel(writer, sheet_name="Raw Data (Dashboards)", index=False)
        
        workbook = writer.book
        
        # Criar estilos visuais limpos
        header_format = workbook.add_format({'bold': True, 'bg_color': cor_cabecalho, 'font_color': 'white', 'border': 1, 'valign': 'vcenter'})
        cell_format = workbook.add_format({'border': 1, 'valign': 'vcenter'})
        currency_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00 €', 'valign': 'vcenter'})
        
        # Formato especial com Text Wrap para os parágrafos de ajuda
        wrap_cell_format = workbook.add_format({'border': 1, 'valign': 'vcenter', 'text_wrap': True})

        # 1. Formatar folha "Resumo Executivo"
        ws_exec = writer.sheets["Resumo Executivo"]
        ws_exec.hide_gridlines(2)
        ws_exec.set_column('A:A', 35)
        ws_exec.set_column('B:B', 25)
        
        for col_num, value in enumerate(df_exec.columns.values):
            ws_exec.write(0, col_num, value, header_format)
        for row_num in range(len(df_exec)):
            ws_exec.write(row_num + 1, 0, df_exec.iloc[row_num, 0], cell_format)
            ws_exec.write(row_num + 1, 1, df_exec.iloc[row_num, 1], cell_format)

        # 2. Formatar folha "Financeiro (FAIR)"
        ws_fin = writer.sheets["Financeiro (FAIR)"]
        ws_fin.hide_gridlines(2)
        ws_fin.set_column('A:A', 45)
        ws_fin.set_column('B:B', 25)
        
        for col_num, value in enumerate(df_fin.columns.values):
            ws_fin.write(0, col_num, value, header_format)
        for row_num in range(len(df_fin)):
            ws_fin.write(row_num + 1, 0, df_fin.iloc[row_num, 0], cell_format)
            ws_fin.write(row_num + 1, 1, df_fin.iloc[row_num, 1], currency_format)

        # 3. Formatar folha "Telemetria"
        ws_tel = writer.sheets["Respostas do Formulário"]
        ws_tel.hide_gridlines(2)
        ws_tel.set_column('A:A', 35)
        ws_tel.set_column('B:B', 45)
        ws_tel.set_column('C:C', 80)
        
        for col_num, value in enumerate(df_telemetria.columns.values):
            ws_tel.write(0, col_num, value, header_format)
        for row_num in range(len(df_telemetria)):
            ws_tel.write(row_num + 1, 0, df_telemetria.iloc[row_num, 0], cell_format)
            ws_tel.write(row_num + 1, 1, df_telemetria.iloc[row_num, 1], cell_format)
            ws_tel.write(row_num + 1, 2, df_telemetria.iloc[row_num, 2], cell_format)

        # 4. Formatar folha "Plano de Mitigação"
        ws_mitig = writer.sheets["Plano de Mitigacao"]
        ws_mitig.hide_gridlines(2)
        ws_mitig.set_column('A:A', 35) # Ação
        ws_mitig.set_column('B:B', 25) # Vetor
        ws_mitig.set_column('C:C', 95) # Parágrafo de Ajuda Técnica
        
        for col_num, value in enumerate(df_mitigacao.columns.values):
            ws_mitig.write(0, col_num, value, header_format)
        for row_num in range(len(df_mitigacao)):
            ws_mitig.write(row_num + 1, 0, df_mitigacao.iloc[row_num, 0], cell_format)
            ws_mitig.write(row_num + 1, 1, df_mitigacao.iloc[row_num, 1], cell_format)
            ws_mitig.write(row_num + 1, 2, df_mitigacao.iloc[row_num, 2], wrap_cell_format)

    return output.getvalue()