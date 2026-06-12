from fpdf import FPDF
from datetime import datetime

class CyberRiskReport(FPDF):
    def __init__(self, risk_level):
        super().__init__()
        self.risk_level = risk_level

    def header(self):
        # Cores Dinâmicas do Cabeçalho consoante a Gravidade
        if "Baixo" in self.risk_level:
            self.set_fill_color(16, 185, 129)  # Verde 
        elif "Moderado" in self.risk_level:
            self.set_fill_color(245, 158, 11)  # Amarelo
        elif "Elevado" in self.risk_level:
            self.set_fill_color(234, 88, 12)   # Laranja
        else:
            self.set_fill_color(239, 68, 68)   # Vermelho 
            
        self.rect(0, 0, 210, 38, 'F')
        self.set_y(12)
        
        self.set_font("Arial", 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 5, "CYBER RISK INTELLIGENCE HUB", ln=True, align='L')
        
        self.set_font("Arial", '', 10)
        self.set_text_color(243, 244, 246)
        self.cell(0, 8, "Relatorio Oficial de Auditoria e Quantificacao de Risco", ln=True, align='L')
        
        self.set_y(45)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(107, 114, 128)
        self.line(10, 282, 200, 282)
        self.cell(0, 10, f"Confidencial - Gerado a {datetime.now().strftime('%Y-%m-%d %H:%M')} | Pagina {self.page_no()}/{{nb}}", align='C')

def generate_pdf(data_dict: dict) -> bytes:
    nivel_global = data_dict['Nivel_Global']
    pdf = CyberRiskReport(risk_level=nivel_global)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- DEFINIÇÃO DE CORES SOFT DINÂMICAS PARA A CAIXA DE SCORE ---
    if "Baixo" in nivel_global:
        soft_bg = (209, 250, 229)  # Verde Pastel
        soft_bd = (167, 243, 208)  # Borda Verde 
    elif "Moderado" in nivel_global:
        soft_bg = (254, 243, 199)  # Amarelo Pastel
        soft_bd = (253, 230, 138)  # Borda Amarelo 
    elif "Elevado" in nivel_global:
        soft_bg = (255, 237, 213)  # Laranja Pastel
        soft_bd = (253, 186, 116)  # Borda Laranja 
    else:
        soft_bg = (254, 226, 226)  # Vermelho Pastel
        soft_bd = (254, 202, 202)  # Borda Vermelho
    
    # --- CAPÍTULO 1: RESUMO EXECUTIVO ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "1. Resumo Executivo e Postura Global", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    # --- Caixa de Score Global Dinâmica ---
    pdf.set_fill_color(*soft_bg)
    pdf.set_draw_color(*soft_bd)
    pdf.rect(10, pdf.get_y(), 190, 18, 'DF')
    
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(17, 24, 39)
    pdf.set_x(15)
    pdf.cell(100, 18, f"SCORE GLOBAL DE POSTURA DE RISCO: {data_dict['Score_Global']:.1f} / 100", align='L')
    pdf.cell(80, 18, f"NIVEL: {nivel_global}", align='R', ln=True)
    pdf.ln(5)
    
    # Métricas Qualitativas
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(243, 244, 246) #cinza
    pdf.cell(110, 7, " Vetor de Risco Avaliado", border=1, fill=True)
    pdf.cell(40, 7, " Impacto (%)", border=1, fill=True, align='C')
    pdf.cell(40, 7, " Estado Qualitativo", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(110, 7, " Risco de Infraestrutura e IoT (ISO 27005)", border=1)
    pdf.cell(40, 7, f" {data_dict['IoT_ISO_Risco']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_IoT']}", border=1, align='C', ln=True)
    
    pdf.cell(110, 7, " Postura Criptografica e Ameaca Pos-Quantica Residual", border=1)
    pdf.cell(40, 7, f" {data_dict['PQR_Residual']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_PQR']}", border=1, align='C', ln=True)
    
    pdf.cell(110, 7, " Indice de Desinformacao Sintetica e Imagem (DRI)", border=1)
    pdf.cell(40, 7, f" {data_dict['DRI_Risco']:.1f}%", border=1, align='C')
    pdf.cell(40, 7, f" {data_dict['Nivel_DRI']}", border=1, align='C', ln=True)
    pdf.ln(10)
    
    # --- CAPÍTULO 2: VALORAÇÃO FINANCEIRA (FAIR) ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "2. Quantificacao Financeira de Danos (Modelo FAIR)", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(4)
    
    pdf.set_font("Arial", '', 10)
    
    # Caixa 1: ALE
    pdf.set_fill_color(239, 246, 255)
    pdf.rect(10, pdf.get_y(), 60, 20, 'F')
    pdf.set_xy(12, pdf.get_y()+2)
    pdf.set_font("Arial", 'B', 8)
    pdf.set_text_color(30, 64, 175)
    pdf.cell(56, 4, "PERDA MEDIA ESPERADA (ALE)", ln=True)
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
    pdf.cell(56, 4, "CONDITIONAL CVaR (PIOR CENARIO)", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_x(142)
    pdf.cell(56, 8, f"{data_dict['CVaR_Pior_Cenario']:,.2f} EUR", ln=True)
    
    pdf.set_xy(10, pdf.get_y()+8)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Nota Estatistica: O calculo do Value at Risk e Conditional VaR baseia-se numa distribuicao Lognormal de cauda pesada com 1.000 iteracoes estocasticas. O CVaR representa a media financeira dos piores 5% de cenarios de impacto simulados.")
    pdf.ln(8)

    # --- CAPÍTULO 3: MAPEAMENTO DE RESPOSTAS ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 10, "3. Registo Integral de Telemetria", ln=True)
    pdf.line(10, pdf.get_y(), 65, pdf.get_y())
    pdf.ln(2)
    
    def draw_block_header(title):
        pdf.ln(4) 
        pdf.set_fill_color(239, 246, 255) # Azul 
        pdf.set_draw_color(191, 219, 254) 
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(30, 58, 138) 
        pdf.cell(0, 9, f"  {title}", border='T B', fill=True, ln=True)
        pdf.ln(5)

    def draw_data_row(label, value, is_last=False):
        pdf.set_font("Arial", 'B', 9)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 5, f"{label}", ln=True)
        
        pdf.set_font("Arial", '', 9)
        pdf.set_text_color(107, 114, 128) 
        pdf.set_x(15)
        pdf.multi_cell(0, 5, f"{value}")
        
        if not is_last:
            pdf.ln(2)
            pdf.set_draw_color(229, 231, 235) 
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(3)
        else:
            pdf.ln(3)

    # Blocos
    draw_block_header("BLOCO 1: CONTEXTO DE NEGOCIO E ATIVOS")
    draw_data_row("1. Faturacao / Orcamento Anual da Organizacao", f"{data_dict['Q1_Receita']:,.2f} EUR")
    draw_data_row("2. Importancia deste ativo/sistema para a operacao", data_dict['Q2_Ativo'])
    draw_data_row("3. Tipo de dados guardados ou processados", data_dict['Q3_Dados'])
    draw_data_row("4. Nivel de exposicao a rede deste sistema", data_dict['Q4_Exposicao_Rede'], is_last=True)

    draw_block_header("BLOCO 2: INFRAESTRUTURA, AMEACAS E MATURIDADE")
    draw_data_row("5. Nivel de Exposicao de Dispositivos IoT na Rede", data_dict['Q5_IoT'])
    draw_data_row("6. Frequencia estimada de tentativas de ataque (Phishing, Scans)", data_dict['Q6_TEF'])
    draw_data_row("7. Perfil de atacante mais provavel para o setor", data_dict['Q7_Adversario'])
    draw_data_row("8. Estado de atualizacoes e falhas conhecidas (CVEs)", data_dict['Q8_CVE'])
    draw_data_row("9. Nivel de maturidade geral dos controlos de seguranca (NIST Tiers)", data_dict['Q9_NIST'])
    draw_data_row("10. Estado das copias de seguranca (Backups) e recuperacao", data_dict['Q10_Backups'], is_last=True)

    draw_block_header("BLOCO 3: POSTURA CRIPTOGRAFICA E RISCO POS-QUANTICO")
    draw_data_row("11. Anos que os dados precisam de se manter confidenciais", f"{data_dict['Q11_Vida_Util']} Anos")
    draw_data_row("12. Algoritmo de Encriptacao Primario Atual", data_dict['Q12_Cripto'])
    draw_data_row("13. Uso de criptografia classica (RSA/ECC) para dados longos", data_dict['Q13_RSA_Longo'])
    draw_data_row("14. Circulacao de dados por canais suscetiveis a gravacao (Harvesting)", data_dict['Q14_Canais'])
    draw_data_row("15. Plano de migracao ativa para criptografia Pos-Quantica (PQC)", data_dict['Q15_PQC'])
    draw_data_row("16. Utilizacao ou plano de implementacao de QKD", data_dict['Q16_QKD'], is_last=True)

    draw_block_header("BLOCO 4: DESINFORMACAO SINTETICA E REPUTACAO (DRI)")
    draw_data_row("17. Dependencia Reputacional e Exposicao Mediatica", f"{data_dict['Q17_Media']}%")
    draw_data_row("18. Tempo formal de reacao e desmentido a desinformacao", data_dict['Q18_Resposta'], is_last=True)
    
    # --- CAPÍTULO 4: PLANO FORMAL DE MELHORIAS ---
    if pdf.get_y() > 230:
        pdf.add_page()
    else:
        pdf.ln(10)

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

    if data_dict['CVaR_Pior_Cenario'] > (data_dict['Orcamento_Empresa'] * 0.05):
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "Contencao de Exposicao Financeira (Governanca e Risco de Cauda)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, f"A analise quantitativa revela uma exposicao catastrofica potencial de {data_dict['CVaR_Pior_Cenario']:,.2f} EUR no percentil de 5% (CVaR). E mandatoria a contratacao de uma apolice de Ciberseguro (Cyber Insurance) calibrada para absorver especificamente este impacto de cauda pesada.")
        pdf.ln(4)

    if "Moderada" in data_dict['Q5_IoT'] or "Alta" in data_dict['Q5_IoT'] or "Crítica" in data_dict['Q5_IoT']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "Blindagem Ciber-Fisica e Segmentacao (ISO 27005 / NIST Protect)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "Dispositivos IoT operam frequentemente com firmware nao assinado. A configuracao de rede atual cria pivos de intrusao. O plano de acao exige: 1) Isolamento em VLANs estritas; 2) Politicas de arquitetura Zero-Trust; 3) Bloqueio de comunicacao direta do IoT para a Internet publica.")
        pdf.ln(4)
    
    if data_dict['PQR_Residual'] >= 30 or "RSA" in data_dict['Q12_Cripto'] or "DES" in data_dict['Q12_Cripto']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "Migracao Criptografica Pos-Quantica e Resiliencia de Canal", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, f"Dados cuja utilidade confidencial exceda os {data_dict['Q11_Vida_Util']} anos estao em risco imediato pela estrategia 'Harvest Now, Decrypt Later'. A organizacao deve abandonar algoritmos classicos (RSA/ECC) e adotar urgentemente as cifras NIST ML-KEM para encapsulamento de chaves hibridas.")
        pdf.ln(4)

    if "Dias" in data_dict['Q18_Resposta'] or "Semanas" in data_dict['Q18_Resposta'] or data_dict['DRI_Risco'] >= 50:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "Detecao Precoce de Desinformacao Sintetica (NIST Detect & Respond)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "A inercia de resposta atual nao e compativel contra campanhas impulsionadas por IA Gerativa (Deepfakes). A organizacao deve implementar ferramentas passivas de inteligencia OSINT e definir guioes de resposta (PR Playbooks) com emissao de desmentidos oficiais em menos de 1 hora.")
        pdf.ln(4)

    if "Inexistentes" in data_dict['Q10_Backups'] or "online" in data_dict['Q10_Backups']:
        recomendacoes_geradas = True
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(15, 118, 110)
        pdf.cell(0, 6, "Continuidade de Negocio e Recuperacao Limpa (NIST Recover)", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(55, 65, 81)
        pdf.multi_cell(0, 5, "A politica de backups submetida e altamente vulneravel a Ransomwares modernos. A salvaguarda da faturacao operacional exige uma estrategia de backup '3-2-1' com um pilar de armazenamento Air-Gapped (offline) e imutavel (WORM), isento de suborno ou encriptacao remota.")

    if not recomendacoes_geradas:
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(22, 163, 74)
        pdf.multi_cell(0, 6, "Auditoria Concluida: A organizacao demonstrou um nivel de maturidade, arquitetura de rede e higiene criptografica de excelencia. Nao foram detetados vetores criticos de ataque estrutural nas variaveis analisadas. Recomenda-se apenas a manutencao continua do SOC e vigilancia sobre a evolucao do cronograma quantico (Y2Q).")

    return bytes(pdf.output())