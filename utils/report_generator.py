from fpdf import FPDF
from datetime import datetime

class CyberRiskReport(FPDF):
    def __init__(self, risk_level):
        super().__init__()
        self.risk_level = risk_level

    def header(self):
        # Cores Dinâmicas do Cabeçalho consoante a Gravidade
        if "Baixo" in self.risk_level:
            self.set_fill_color(16, 185, 129)  # Verde Esmeralda
        elif "Moderado" in self.risk_level:
            self.set_fill_color(245, 158, 11)  # Amarelo
        elif "Elevado" in self.risk_level:
            self.set_fill_color(234, 88, 12)   # Laranja
        else:
            self.set_fill_color(239, 68, 68)   # Vermelho Alerta
            
        # Banner Superior Corporativo Dinâmico
        self.rect(0, 0, 210, 38, 'F')
        
        # Posição inicial do texto no cabeçalho
        self.set_y(12)
        
        # Título do Hub / Projeto
        self.set_font("Arial", 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5, "CYBER RISK INTELLIGENCE HUB", ln=True, align='L')
        
        # Subtítulo do Relatório
        self.set_font("Arial", '', 10)
        self.set_text_color(243, 244, 246)
        self.cell(0, 8, "Relatório Oficial de Auditoria e Quantificação de Risco", ln=True, align='L')
        
        # Empurra obrigatoriamente o conteúdo da página para baixo do cabeçalho
        self.set_y(45)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(107, 114, 128)
        self.line(10, 282, 200, 282)
        self.cell(0, 10, f"Confidencial - Gerado a {datetime.now().strftime('%Y-%m-%d %H:%M')} | Página {self.page_no()}/{{nb}}", align='C')

def generate_luxury_pdf(data_dict: dict) -> bytes:
    pdf = CyberRiskReport(risk_level=data_dict['Nivel_Global'])
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- CAPÍTULO 1: RESUMO EXECUTIVO ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "1. Resumo Executivo e Postura Global", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    # Caixa de Destaque da Pontuação Global
    pdf.set_fill_color(243, 244, 246)
    pdf.set_draw_color(209, 213, 219)
    pdf.rect(10, pdf.get_y(), 190, 18, 'DF')
    
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(55, 65, 81)
    pdf.set_x(15)
    pdf.cell(100, 18, f"SCORE GLOBAL DE POSTURA DE RISCO: {data_dict['Score_Global']:.1f} / 100", align='L')
    pdf.cell(80, 18, f"NÍVEL: {data_dict['Nivel_Global']}", align='R', ln=True)
    pdf.ln(5)
    
    # Métricas Qualitativas
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(229, 231, 235)
    pdf.cell(110, 7, " Vetor de Risco Avaliado", border=1, fill=True)
    pdf.cell(40, 7, " Impacto (%)", border=1, fill=True, align='C')
    pdf.cell(40, 7, " Estado Qualitativo", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(110, 7, " Risco de Infraestrutura e IoT (ISO 27005)", border=1)
    pdf.cell(40, 7, f" {data_dict['IoT_ISO_Risco']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_IoT']}", border=1, align='C', ln=True)
    
    pdf.cell(110, 7, " Postura Criptográfica e Ameaça Pós-Quântica Residual", border=1)
    pdf.cell(40, 7, f" {data_dict['PQR_Residual']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_PQR']}", border=1, align='C', ln=True)
    
    pdf.cell(110, 7, " Índice de Desinformação Sintética e Imagem (DRI)", border=1)
    pdf.cell(40, 7, f" {data_dict['DRI_Risco']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_DRI']}", border=1, align='C', ln=True)
    pdf.ln(10)
    
    # --- CAPÍTULO 2: VALORAÇÃO FINANCEIRA (FAIR) ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "2. Quantificação Financeira de Danos (Modelo FAIR)", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    # Caixas Financeiras
    pdf.set_font("Arial", '', 10)
    
    # Caixa 1: ALE
    pdf.set_fill_color(239, 246, 255)
    pdf.rect(10, pdf.get_y(), 60, 20, 'F')
    pdf.set_xy(12, pdf.get_y()+2)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(56, 4, "PERDA MÉDIA ESPERADA (ALE)", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(12)
    pdf.cell(56, 8, f"{data_dict['FAIR_ALE']:,.2f} EUR", ln=True)
    
    # Caixa 2: VaR 95%
    pdf.set_xy(75, pdf.get_y()-14)
    pdf.set_fill_color(254, 242, 242)
    pdf.rect(75, pdf.get_y(), 60, 20, 'F')
    pdf.set_xy(77, pdf.get_y()+2)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_text_color(153, 27, 27)
    pdf.cell(56, 4, "VALUE AT RISK (VaR 95%)", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(77)
    pdf.cell(56, 8, f"{data_dict['VaR_95']:,.2f} EUR", ln=True)
    
    # Caixa 3: CVaR
    pdf.set_xy(140, pdf.get_y()-14)
    pdf.set_fill_color(255, 247, 237)
    pdf.rect(140, pdf.get_y(), 60, 20, 'F')
    pdf.set_xy(142, pdf.get_y()+2)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_text_color(154, 52, 18)
    pdf.cell(56, 4, "CONDITIONAL CVaR (PIOR CENÁRIO)", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(142)
    pdf.cell(56, 8, f"{data_dict['CVaR_Pior_Cenario']:,.2f} EUR", ln=True)
    
    pdf.set_xy(10, pdf.get_y()+8)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Nota Estatística: O cálculo do Value at Risk e Conditional VaR baseia-se numa distribuição Lognormal de cauda pesada com 1.000 iterações estocásticas. O CVaR representa a média financeira dos piores 5% de cenários de impacto simulados.")
    pdf.ln(8)

    # --- CAPÍTULO 3: MAPEAMENTO DE RESPOSTAS COMPLETAS ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "3. Registo Integral de Telemetria", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    # Função auxiliar com MULTI_CELL para as respostas nunca serem cortadas
    def draw_data_row(label, value):
        pdf.set_font("Arial", 'B', 9)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 5, f"{label}:", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, f"{value}")
        pdf.ln(3) # Espaço entre perguntas

    # Bloco 1
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(31, 41, 55)
    pdf.set_fill_color(229, 231, 235)
    pdf.cell(0, 6, " Bloco 1: Contexto de Negócio e Ativos", border=1, fill=True, ln=True)
    pdf.ln(3)
    draw_data_row("1. Faturação / Orçamento Anual da Organização", f"{data_dict['Q1_Receita']:,.2f} EUR")
    draw_data_row("2. Importância deste ativo/sistema para a operação", data_dict['Q2_Ativo'])
    draw_data_row("3. Tipo de dados guardados ou processados", data_dict['Q3_Dados'])
    draw_data_row("4. Nível de exposição à rede deste sistema", data_dict['Q4_Exposicao_Rede'])
    pdf.ln(2)

    # Bloco 2
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 6, " Bloco 2: Infraestrutura, Ameaças e Maturidade", border=1, fill=True, ln=True)
    pdf.ln(3)
    draw_data_row("5. Nível de Exposição de Dispositivos IoT na Rede", data_dict['Q5_IoT'])
    draw_data_row("6. Frequência estimada de tentativas de ataque (Phishing, Scans)", data_dict['Q6_TEF'])
    draw_data_row("7. Perfil de atacante mais provável para o setor", data_dict['Q7_Adversario'])
    draw_data_row("8. Estado de atualizações e falhas conhecidas (CVEs)", data_dict['Q8_CVE'])
    draw_data_row("9. Nível de maturidade geral dos controlos de segurança (NIST Tiers)", data_dict['Q9_NIST'])
    draw_data_row("10. Estado das cópias de segurança (Backups) e recuperação", data_dict['Q10_Backups'])
    pdf.ln(2)

    # Bloco 3
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 6, " Bloco 3: Postura Criptográfica e Risco Pós-Quântico", border=1, fill=True, ln=True)
    pdf.ln(3)
    draw_data_row("11. Anos que os dados precisam de se manter confidenciais", f"{data_dict['Q11_Vida_Util']} Anos")
    draw_data_row("12. Algoritmo de Encriptação Primário Atual", data_dict['Q12_Cripto'])
    draw_data_row("13. Uso de criptografia clássica (RSA/ECC) para dados longos", data_dict['Q13_RSA_Longo'])
    draw_data_row("14. Circulação de dados por canais suscetíveis a gravação (Harvesting)", data_dict['Q14_Canais'])
    draw_data_row("15. Plano de migração ativa para criptografia Pós-Quântica (PQC)", data_dict['Q15_PQC'])
    draw_data_row("16. Utilização ou plano de implementação de QKD", data_dict['Q16_QKD'])
    pdf.ln(2)

    # Bloco 4
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 6, " Bloco 4: Desinformação Sintética e Reputação (DRI)", border=1, fill=True, ln=True)
    pdf.ln(3)
    draw_data_row("17. Dependência Reputacional e Exposição Mediática", f"{data_dict['Q17_Media']}%")
    draw_data_row("18. Tempo formal de reação e desmentido a desinformação", data_dict['Q18_Resposta'])
    pdf.ln(6)

    # --- CAPÍTULO 4: PLANO FORMAL DE MELHORIAS (INTELIGENTE E DINÂMICO) ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "4. Plano Estrategico de Mitigacao e Aconselhamento", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Com base na auditoria multivetorial realizada atraves das metodologias FAIR, ISO/IEC 27005 e na arquitetura de governacao NIST CSF 2.0, o algoritmo determinou as seguintes acoes prioritarias, filtradas estritamente para as lacunas detetadas na sua infraestrutura:")
    pdf.ln(6)
    
    recomendacoes_geradas = False

    # Ação I: Governança FAIR (Dispara se o CVaR for maior que 5% da Faturação)
    if data_dict['CVaR_Pior_Cenario'] > (data_dict['Orcamento_Empresa'] * 0.05):
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "I. Contencao de Exposicao Financeira (Governanca e Risco de Cauda)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, f"A analise quantitativa revela uma exposicao catastrofica potencial de {data_dict['CVaR_Pior_Cenario']:,.2f} EUR no percentil de 5% (CVaR). É mandatoria a contratacao de uma apolice de Ciberseguro (Cyber Insurance) calibrada para absorver especificamente este impacto de cauda pesada.")
        pdf.ln(4)

    # Ação II: IoT e Redes (Dispara apenas se a rede não for Baixa/Segmentada)
    if "Moderada" in data_dict['Q5_IoT'] or "Alta" in data_dict['Q5_IoT'] or "Crítica" in data_dict['Q5_IoT']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "II. Blindagem Ciber-Fisica e Segmentacao (ISO 27005 / NIST Protect)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "Dispositivos IoT operam frequentemente com firmware nao assinado. A configuracao de rede atual cria pivôs de intrusao. O plano de acao exige: 1) Isolamento em VLANs estritas; 2) Politicas de arquitetura Zero-Trust; 3) Bloqueio de comunicacao direta do IoT para a Internet publica.")
        pdf.ln(4)
    
    # Ação III: Quântico (Dispara se usarem Cripto Legada ou Risco Quântico Residual Elevado)
    if data_dict['PQR_Residual'] >= 30 or "RSA" in data_dict['Q12_Cripto'] or "DES" in data_dict['Q12_Cripto']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "III. Migracao Criptografica Pos-Quantica e Resiliencia de Canal", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, f"Dados cuja utilidade confidencial exceda os {data_dict['Q11_Vida_Util']} anos estao em risco imediato pela estrategia 'Harvest Now, Decrypt Later'. A organizacao deve abandonar algoritmos classicos (RSA/ECC) e adotar urgentemente as cifras NIST ML-KEM para encapsulamento de chaves hibridas.")
        pdf.ln(4)

    # Ação IV: DRI e Reputação (Dispara se a resposta demorar mais de 24h ou Risco > 50%)
    if "Dias" in data_dict['Q18_Resposta'] or "Semanas" in data_dict['Q18_Resposta'] or data_dict['DRI_Risco'] >= 50:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "IV. Detecao Precoce de Desinformacao Sintetica (NIST Detect & Respond)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "A inercia de resposta atual nao e compativel contra campanhas impulsionadas por IA Gerativa (Deepfakes). A organizacao deve implementar ferramentas passivas de inteligencia OSINT e definir guioes de resposta (PR Playbooks) com emissao de desmentidos oficiais em menos de 1 hora.")
        pdf.ln(4)

    # Ação V: Resiliência de Dados (Dispara se os backups forem Inexistentes ou puramente Online)
    if "Inexistentes" in data_dict['Q10_Backups'] or "online" in data_dict['Q10_Backups']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "V. Continuidade de Negocio e Recuperacao Limpa (NIST Recover)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "A politica de backups submetida e altamente vulneravel a Ransomwares modernos. A salvaguarda da faturacao operacional exige uma estrategia de backup '3-2-1' com um pilar de armazenamento Air-Gapped (offline) e imutavel (WORM), isento de suborno ou encriptacao remota.")

    # MENSAGEM DE EXCELÊNCIA (Se a empresa não falhou em nada)
    if not recomendacoes_geradas:
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(22, 163, 74) # Verde sucesso
        pdf.multi_cell(0, 6, "Auditoria Concluida: A organizacao demonstrou um nivel de maturidade, arquitetura de rede e higiene criptografica de excelencia. Nao foram detetados vetores criticos de ataque estrutural nas variaveis analisadas. Recomenda-se apenas a manutencao continua do SOC e vigilancia sobre a evolucao do cronograma quantico (Y2Q).")

    return bytes(pdf.output())