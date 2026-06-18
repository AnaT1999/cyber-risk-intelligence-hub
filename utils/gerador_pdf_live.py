import io
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --- FUNÇÃO PARA DESENHAR CABEÇALHO E RODAPÉ  ---
def adicionar_cabecalho_rodape(canvas, doc):
    canvas.saveState()
    
    # Faixa no Topo 
    canvas.setFillColor(colors.HexColor('#475569')) 
    canvas.rect(0, letter[1] - 0.5 * inch, letter[0], 0.5 * inch, fill=1, stroke=0)
    
    # Texto do Cabeçalho
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(40, letter[1] - 0.35 * inch, "CYBER RISK INTELLIGENCE HUB")
    
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(letter[0] - 40, letter[1] - 0.35 * inch, "Confidencial - Uso Interno")
    
    # Rodapé
    canvas.setFillColor(colors.gray)
    canvas.setFont("Helvetica", 9)
    canvas.drawString(40, 0.4 * inch, f"Gerado pelo Motor IA XGBoost | © {datetime.datetime.now().year}")
    canvas.drawRightString(letter[0] - 40, 0.4 * inch, f"Página {doc.page}")
    
    canvas.restoreState()


def gerar_relatorio_live(df, hora_api_str):
    """
    Gera um relatório executivo com design leve, narrativas densas explicativas e um Top 15.
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=60)
    elementos = []
    
    # --- Folha de Estilos ---
    styles = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle('TituloPrincipal', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#1e293b'), spaceAfter=6)
    estilo_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=12, textColor=colors.HexColor('#64748b'), spaceAfter=20)
    
    # Azul suave para as secções
    estilo_seccao = ParagraphStyle('Seccao', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#2563eb'), spaceBefore=20, spaceAfter=10)
    
    estilo_normal = ParagraphStyle('Corpo', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, spaceAfter=10, alignment=4)
    
    # Estilos de Tabela
    estilo_cabecalho_tabela = ParagraphStyle('TabHead', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=1)
    estilo_celula = ParagraphStyle('TabCell', fontName='Helvetica', fontSize=9, alignment=1)

    # --- Título e Timestamps ---
    agora = datetime.datetime.now()
    hora_pdf_str = agora.strftime("%d/%m/%Y às %H:%M:%S")
    
    elementos.append(Paragraph("Executive Threat Briefing", estilo_titulo))
    elementos.append(Paragraph("Relatório Automático de Triagem de Vulnerabilidades", estilo_subtitulo))
    
    dados_meta = [
        [Paragraph("<b>Data/Hora do Scan NIST API:</b>", estilo_celula), Paragraph(hora_api_str, estilo_celula)],
        [Paragraph("<b>Data/Hora Geração do PDF:</b>", estilo_celula), Paragraph(hora_pdf_str, estilo_celula)]
    ]
    tabela_meta = Table(dados_meta, colWidths=[200, 200], hAlign='LEFT')
    tabela_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    elementos.append(tabela_meta)
    elementos.append(Spacer(1, 15))

    # --- Sumário Executivo ---
    total_analisados = len(df)
    cvss_criticos = len(df[df['base_score'] >= 7.0])
    ia_criticos = len(df[df['probabilidade_ia'] >= 70.0])
    poupanca = cvss_criticos - ia_criticos
    reducao_percentual = (poupanca / cvss_criticos * 100) if cvss_criticos > 0 else 0

    elementos.append(Paragraph("1. Sumário Executivo Operacional", estilo_seccao))
    
    texto_narrativa = f"""
    Durante a mais recente análise live, o motor de inteligência analisou <b>{total_analisados}</b> novas vulnerabilidades. 
    Se a organização dependesse exclusivamente da métrica tradicional (CVSS), a equipa de IT seria obrigada a processar <b>{cvss_criticos}</b> incidentes como sendo de severidade alta ou crítica.<br/><br/>
    No entanto, a avaliação preditiva determinou que <b>apenas {ia_criticos} ameaças</b> apresentam uma probabilidade real de exploração armada superior a 70%. Esta triagem inteligente traduz-se numa redução de <b>{reducao_percentual:.1f}% no ruído operacional</b>, permitindo o direcionamento imediato dos recursos técnicos.
    """
    elementos.append(Paragraph(texto_narrativa, estilo_normal))

    # --- Justificação IA  ---
    elementos.append(Paragraph("2. Análise Comparativa: CVSS Tradicional vs. Previsão IA", estilo_seccao))
    
    texto_scatter = """
    Embora o sistema CVSS (Common Vulnerability Scoring System) seja o padrão regulamentar da indústria, este baseia-se numa pontuação isolada e estática que frequentemente gera "Fadiga de Alertas". O nosso motor <b>XGBoost</b> atua como um filtro analítico que reavalia este risco baseando-se no contexto real da viabilidade de um ataque.<br/><br/>
    <b>A Reclassificação de Risco:</b> Vulnerabilidades com um CVSS elevado (ex: 8.0 ou 9.0) mas que exigem acesso físico local ou privilégios de administrador complexos são categoricamente rebaixadas pela IA. Em contrapartida, falhas de segurança expostas diretamente à Internet (Vetor: NETWORK) e que não requerem interação da vítima, são sinalizadas com probabilidades críticas de exploração (>70%), independentemente de possuírem um CVSS base médio (ex: 5.0 ou 6.0). A triagem abaixo reflete exclusivamente esta "Zona de Perigo" realística.
    """
    elementos.append(Paragraph(texto_scatter, estilo_normal))

    # --- Distribuição do Risco ---
    elementos.append(Paragraph("3. Matriz de Distribuição do Risco", estilo_seccao))
    
    texto_distribuicao = """
    A presente Matriz de Distribuição converte as probabilidades brutas geradas pela Inteligência Artificial num guião de <b>Priorização Operacional</b>. Em vez de despejar dezenas de alertas não filtrados sobre a equipa de Segurança da Informação, o modelo categoriza as ameaças em três limiares acionáveis:<br/><br/>
    • O nível <b>Crítico</b> exige protocolos de mitigação (patching ou isolamento) no imediato, uma vez que estas falhas estão altamente propensas a ser ativamente exploradas por atores maliciosos.<br/>
    • O nível <b>Elevado</b> representa um risco latente, requerendo monitorização acrescida nos firewalls e IDS (Intrusion Detection Systems) até que surja uma janela de manutenção regular.<br/>
    • O nível <b>Baixo/Moderado</b> engloba o "ruído" estatístico; vulnerabilidades que, apesar de existirem tecnicamente, não reúnem as condições ambientais para uma exploração bem-sucedida, podendo ser deferidas com segurança.
    """
    elementos.append(Paragraph(texto_distribuicao, estilo_normal))
    elementos.append(Spacer(1, 10))
    
    elevados = len(df[(df['probabilidade_ia'] < 70.0) & (df['probabilidade_ia'] >= 40.0)])
    baixos = len(df[df['probabilidade_ia'] < 40.0])
    
    dados_distribuicao = [
        [Paragraph("Categoria de Risco", estilo_cabecalho_tabela), Paragraph("Condição IA", estilo_cabecalho_tabela), Paragraph("Quantidade Alertas", estilo_cabecalho_tabela)]
    ]
    dados_distribuicao.append([Paragraph("<font color='#dc2626'><b>Crítico (Ação Imediata)</b></font>", estilo_celula), Paragraph("≥ 70.0%", estilo_celula), Paragraph(f"<b>{ia_criticos}</b>", estilo_celula)])
    dados_distribuicao.append([Paragraph("<font color='#d97706'><b>Elevado (Monitorizar)</b></font>", estilo_celula), Paragraph("40.0% - 69.9%", estilo_celula), Paragraph(f"<b>{elevados}</b>", estilo_celula)])
    dados_distribuicao.append([Paragraph("<font color='#2563eb'><b>Baixo/Moderado</b></font>", estilo_celula), Paragraph("< 40.0%", estilo_celula), Paragraph(f"<b>{baixos}</b>", estilo_celula)])
    
    tabela_distribuicao = Table(dados_distribuicao, colWidths=[180, 160, 160])
    tabela_distribuicao.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#64748b')), 
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elementos.append(tabela_distribuicao)
    
    # ---  Espaçamento mínimo ---
    elementos.append(Spacer(1, 25))

    # --- Tabela Top 15 Detalhada ---
    elementos.append(Paragraph("4. Triage Prioritária (Top 15 Ameaças Iminentes)", estilo_seccao))
    elementos.append(Paragraph("Listagem das 15 vulnerabilidades mais críticas, ordenadas pela probabilidade de exploração prevista. Recomenda-se o patching focado dos sistemas afetados por estas falhas.", estilo_normal))
    
    top15_df = df.head(15).copy()
    
    dados_top15 = [[
        Paragraph("Código CVE", estilo_cabecalho_tabela), 
        Paragraph("Vetor Ataque", estilo_cabecalho_tabela), 
        Paragraph("CVSS", estilo_cabecalho_tabela), 
        Paragraph("Risco IA", estilo_cabecalho_tabela),
        Paragraph("Nível", estilo_cabecalho_tabela) 
    ]]
    
    for index, row in top15_df.iterrows():
        # Calcular a cor e label da nova coluna
        prob = row['probabilidade_ia']
        if prob >= 70.0:
            nivel_str = "<font color='#dc2626'><b>Crítico</b></font>"
        elif prob >= 40.0:
            nivel_str = "<font color='#d97706'><b>Elevado</b></font>"
        else:
            nivel_str = "<font color='#2563eb'><b>Baixo</b></font>"

        dados_top15.append([
            Paragraph(row['cve_id'], estilo_celula), 
            Paragraph(row['attack_vector'], estilo_celula), 
            Paragraph(str(row['base_score']), estilo_celula), 
            Paragraph(f"<b>{prob:.1f}%</b>", estilo_celula),
            Paragraph(nivel_str, estilo_celula)
        ])

    tabela_top = Table(dados_top15, colWidths=[110, 110, 70, 100, 110])
    tabela_top.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')), # Azul Royal claro no cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')), 
    ]))
    elementos.append(tabela_top)

    # --- Gerar o PDF ---
    doc.build(elementos, onFirstPage=adicionar_cabecalho_rodape, onLaterPages=adicionar_cabecalho_rodape)
    buffer.seek(0)
    return buffer