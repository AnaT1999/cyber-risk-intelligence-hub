import re

# Isolamos a verificação do pypdf dentro do ficheiro para manter o código modular
try:
    import pypdf
    PDF_DISPONIVEL = True
except ImportError:
    PDF_DISPONIVEL = False

def clean_float_pdf(val_str):
    """Limpa símbolos monetários e formatações numéricas de texto extraído de PDF."""
    if not val_str: return None
    val_str = re.sub(r'[^\d\.,]', '', str(val_str))
    if not val_str: return None
    
    if ',' in val_str and '.' in val_str:
        if val_str.rfind(',') > val_str.rfind('.'):
            val_str = val_str.replace('.', '').replace(',', '.') # Estilo Europeu
        else:
            val_str = val_str.replace(',', '') # Estilo Americano
    else:
        val_str = val_str.replace(',', '.')
        
    try: return float(val_str)
    except: return None

def parse_pdf_risk(file) -> dict:
    """Motor Semântico para extração de métricas de texto desestruturado (PDF)."""
    if not PDF_DISPONIVEL:
        return {"erro": "O pacote 'pypdf' está em falta. Execute `pip install pypdf` no terminal."}
        
    try:
        reader = pypdf.PdfReader(file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    except Exception as e:
        return {"erro": f"Não foi possível ler o PDF. Ficheiro corrompido ou protegido? Detalhe: {str(e)}"}
        
    alertas = []
    
    '''
    # --- PASSO 0: IDENTIFICAÇÃO DO TIPO ---
    if re.search(r'CISA|CYBER SECURITY EVALUATION TOOL|RANSOMWARE READINESS', full_text, re.IGNORECASE):
        # Chama o motor para PDF complexo (CISA/NIST)
        return parse_cisa_pdf(full_text)
    else:
        # Chama o teu motor original (o que já funciona para os teus formulários)
        return parse_standard_pdf(full_text)
    '''

    # --- 1. EXTRAÇÃO FINANCEIRA ---
    # No PDF, o número aparece habitualmente na linha abaixo do título. 
    ale_match = re.search(r'(?:Perda Média Esperada|Perda Anual Esperada|ALE)[\s\S]{0,60}?([\d\.,]+)\s*(?:€|EUR)', full_text, re.IGNORECASE)
    ale_val = clean_float_pdf(ale_match.group(1)) if ale_match else None
    
    if ale_val is None:
        ale_val = 50000.0
        alertas.append("Métrica financeira de Perda (ALE) não detetada no PDF. Assumido placeholder: 50.000 €.")

    rev_match = re.search(r'(?:Faturacao|Orcamento Anual|Orçamento|Faturação|Revenue)[\s\S]{0,60}?([\d\.,]+)\s*(?:€|EUR)', full_text, re.IGNORECASE)
    revenue = clean_float_pdf(rev_match.group(1)) if rev_match else None
    
    if revenue is None:
        revenue = 1000000.0
        alertas.append("Métrica de Faturação/Orçamento não detetada no PDF. Assumido placeholder: 1.000.000 €.")

    # --- 2. EXTRAÇÃO DA MATURIDADE NIST ---
    nist = 1
    nist_match = re.search(r'(?:Tier\s*|NIST\s*Tier\s*|Maturidade\s*Tier\s*)([1-4])', full_text, re.IGNORECASE)
    if nist_match:
        nist = int(nist_match.group(1))
    else:
        alertas.append("Maturidade NIST não detetada no texto do PDF. Assumido placeholder: Tier 1.")

    # --- 3. EXTRAÇÃO DA SENSIBILIDADE DE DADOS ---
    q_dados = 3
    if re.search(r'(?:Críticos|Regulados|Pessoais|Critical|Nível 5|Level 5)', full_text, re.IGNORECASE): q_dados = 5
    elif re.search(r'(?:Secretos|Secret|Nível 4|Level 4)', full_text, re.IGNORECASE): q_dados = 4
    elif re.search(r'(?:Altamente Confidenciais|Confidenciais|Confidential|Nível 3|Level 3)', full_text, re.IGNORECASE): q_dados = 3
    elif re.search(r'(?:Internos|Internal|Nível 2|Level 2)', full_text, re.IGNORECASE): q_dados = 2
    elif re.search(r'(?:Públicos|Public|Nível 1|Level 1)', full_text, re.IGNORECASE): q_dados = 1
    else:
        alertas.append("Classificação de sensibilidade de dados não detetada no PDF. Assumido placeholder: Nível 3.")

    # --- 4. EXTRAS (IoT e Velocidade de Resposta) ---
    iot_val = "Moderada"
    if re.search(r'(?:IoT.*Crítica|IoT.*Critical|Exposição IoT[\s\S]{0,100}?Crítica)', full_text, re.IGNORECASE): iot_val = "Crítica"
    elif re.search(r'(?:IoT.*Baixa|IoT.*Low|Exposição IoT[\s\S]{0,100}?Baixa)', full_text, re.IGNORECASE): iot_val = "Baixa"
    elif re.search(r'(?:IoT.*Inexistente|IoT.*None|Exposição IoT[\s\S]{0,100}?Inexistente)', full_text, re.IGNORECASE): iot_val = "Inexistente"
    
    dwell_val = "Dias"
    # Lida com expressões frequentes no PDF como "em menos de 1 hora"
    if re.search(r'(?:Resposta.*Minutos|Reação.*Minutos|menos de 1 hora)', full_text, re.IGNORECASE): dwell_val = "Minutos"
    elif re.search(r'(?:Resposta.*Semanas|Reação.*Semanas)', full_text, re.IGNORECASE): dwell_val = "Semanas"

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Relatório Executivo Desestruturado (PDF)",
        "dados_completos": {"Q5_IoT": iot_val, "Q18_Resposta": dwell_val},
        "alertas": alertas
    }