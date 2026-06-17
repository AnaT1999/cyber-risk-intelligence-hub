import re

# Isolamos a verificação do pypdf dentro do ficheiro para manter o código modular
try:
    import pypdf
    PDF_DISPONIVEL = True
except ImportError:
    PDF_DISPONIVEL = False

def clean_float_pdf(val_str):
    """Limpa símbolos monetários e lida com formatos numéricos mundiais de forma blindada."""
    if not val_str: return None
    val_str = str(val_str).strip()
    
    val_str = re.sub(r'[^\d\.,\-]', '', val_str)
    if not val_str: return None
    
    commas = val_str.count(',')
    dots = val_str.count('.')
    
    if commas > 1 and dots <= 1:
        val_str = val_str.replace(',', '')
    elif dots > 1 and commas <= 1:
        val_str = val_str.replace('.', '').replace(',', '.')
    elif commas == 1 and dots == 1:
        if val_str.rfind(',') > val_str.rfind('.'):
            val_str = val_str.replace('.', '').replace(',', '.')
        else:
            val_str = val_str.replace(',', '')
    elif commas == 1 and dots == 0:
        parts = val_str.split(',')
        if len(parts) == 2 and len(parts[1]) == 3:
            val_str = val_str.replace(',', '')
        else:
            val_str = val_str.replace(',', '.')
    elif dots == 1 and commas == 0:
        parts = val_str.split('.')
        if len(parts) == 2 and len(parts[1]) == 3:
            val_str = val_str.replace('.', '')
            
    try: return float(val_str)
    except: return None

def find_financial_value(text, keywords):
    """Radar Financeiro com Filtro Anti-Spoofing."""
    for kw in keywords:
        pattern = rf'({kw})([\s\S]{{0,80}}?)([1-9][\d\.,]{{4,}})'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            miolo = match.group(2).lower()
            if "assumido" in miolo or "não detetad" in miolo or "placeholder" in miolo:
                continue 
            val = clean_float_pdf(match.group(3))
            if val is not None and val > 3000:
                return val
    return None

def find_data_sensitivity(text):
    """Janela de Contexto de Alta Precisão para Dados."""
    keywords = r'(?i)(dados|data|information|sensibilidade|classification|criticite|privacy|daten|ficheiros|files|información)'
    matches = list(re.finditer(keywords, text))
    
    for m in matches:
        start = max(0, m.start() - 5)
        end = min(len(text), m.end() + 65)
        context = text[start:end]
        
        lvl_match = re.search(r'(?:Nível|Level|Stufe)\W*([1-5])', context, re.IGNORECASE)
        if lvl_match: return int(lvl_match.group(1))
        
        if re.search(r'(?:Crític|Critical|Kritisch|Regulados|Pessoais)', context, re.IGNORECASE): return 5
        if re.search(r'(?:Secret|Top Secret)', context, re.IGNORECASE): return 4
        if re.search(r'(?:Altamente Confidencial|Confidencial|Confidential|Confidentiel)', context, re.IGNORECASE): return 3
        if re.search(r'(?:Intern|Internal)', context, re.IGNORECASE): return 2
        if re.search(r'(?:Públic|Public)', context, re.IGNORECASE): return 1
        
    return None

def parse_cset_pdf(full_text) -> dict:
    """Módulo Especializado para Relatórios do Governo Americano (CISA/CSET)."""
    alertas = []

    # CSET nunca contém dados financeiros empresariais
    ale_val = 50000.0
    alertas.append("Relatório CSET detetado (Sem dados financeiros). Placeholder para Perda (ALE): 50.000 €.")
    revenue = 1000000.0
    alertas.append("Relatório CSET detetado (Sem dados financeiros). Placeholder para Faturação: 1.000.000 €.")

    # 1. Extração de Maturidade através das percentagens do RRA
    nist = 1
    adv_match = re.search(r'Advanced[\s\n]*(\d+)', full_text, re.IGNORECASE)
    int_match = re.search(r'Intermediate[\s\n]*(\d+)', full_text, re.IGNORECASE)
    bas_match = re.search(r'Basic[\s\n]*(\d+)', full_text, re.IGNORECASE)
    
    if adv_match and int(adv_match.group(1)) > 50: nist = 4
    elif int_match and int(int_match.group(1)) > 50: nist = 3
    elif bas_match and int(bas_match.group(1)) > 50: nist = 2
    else: nist = 1

    # 2. Extração de Dados Sensíveis através do Security Assurance Level (SAL)
    q_dados = 3
    sal_match = re.search(r'CALCULATED LEVEL[\s\n]*(Low|Moderate|High|Very High)', full_text, re.IGNORECASE)
    if sal_match:
        level_str = sal_match.group(1).lower()
        if level_str == 'very high': q_dados = 5
        elif level_str == 'high': q_dados = 4
        elif level_str == 'moderate': q_dados = 3
        else: q_dados = 2
    else:
        alertas.append("Security Assurance Level (SAL) não gerado no relatório. Assumido Nível de Dados 3.")

    # 3. Extração de IoT e Resposta via Códigos de Falha (Deficiency Report)
    iot_val = "Moderada"
    # Se AM:I.Q03 (Detetar hardware/IoT rogue) tiver um "No" colado, está crítico!
    if re.search(r'AM:(?:I|A)\.Q0[34][\s\S]{0,100}?No\b', full_text, re.IGNORECASE):
        iot_val = "Crítica"
        
    dwell_val = "Horas"
    if re.search(r'IR:(?:B|I)\.Q0[34][\s\S]{0,100}?No\b', full_text, re.IGNORECASE):
        dwell_val = "Semanas"

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Auditoria Governamental CISA/CSET (PDF)",
        "dados_completos": {"Q5_IoT": iot_val, "Q18_Resposta": dwell_val},
        "alertas": alertas
    }

def parse_pdf_risk(file) -> dict:
    """Motor Principal de Gestão e Desvio (Interceptor)."""
    if not PDF_DISPONIVEL:
        return {"erro": "O pacote 'pypdf' está em falta. Execute `pip install pypdf` no terminal."}
        
    try:
        reader = pypdf.PdfReader(file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    except Exception as e:
        return {"erro": f"Não foi possível ler o PDF. Detalhe: {str(e)}"}
        
    # --- O INTERCETOR ---
    # Se o documento tiver a assinatura governamental, enviamos para o módulo CSET
    if re.search(r'CYBER SECURITY EVALUATION TOOL|CISA RANSOMWARE READINESS|SITE DETAIL REPORT', full_text, re.IGNORECASE):
        return parse_cset_pdf(full_text)

    # --- MOTOR GENÉRICO (Se não for CSET) ---
    alertas = []

    ale_keywords = [r'\bALE\b', r'Perda Média', r'Perda Anual', r'Annual[\s_]*Loss', r'Prejuízo', r'Perte Financière', r'Pérdida']
    ale_val = find_financial_value(full_text, ale_keywords)
    if ale_val is None:
        ale_val = 50000.0
        alertas.append("Métrica financeira de Perda (ALE) não detetada no PDF. Assumido placeholder: 50.000 €.")

    rev_keywords = [r'Faturação', r'Faturacao', r'Orçamento', r'Revenue', r'Turnover', r'Budget', r'Chiffre', r'Ingresos']
    revenue = find_financial_value(full_text, rev_keywords)
    if revenue is None:
        revenue = 1000000.0
        alertas.append("Métrica de Faturação/Orçamento não detetada no PDF. Assumido placeholder: 1.000.000 €.")

    nist = 1
    nist_found = False
    for m in re.finditer(r'(?:Tier\W*|Nível\W*|Niveau\W*|Level\W*|Stufe\W*|Maturidade\W*|NIST\W*)([1-4])', full_text, re.IGNORECASE):
        context_before = full_text[max(0, m.start()-40):m.start()].lower()
        if "assumido" not in context_before and "não detetad" not in context_before:
            nist = int(m.group(1))
            nist_found = True
            break
    if not nist_found:
        alertas.append("Maturidade NIST não detetada claramente no texto do PDF. Assumido placeholder: Tier 1.")

    q_dados = find_data_sensitivity(full_text)
    if q_dados is None:
        q_dados = 3
        alertas.append("Classificação de sensibilidade de dados não detetada no PDF. Assumido placeholder: Nível 3.")

    iot_val = "Moderada"
    if re.search(r'(?:IoT.*Crítica|IoT.*Critical|Exposição IoT[\s\S]{0,100}?Crítica)', full_text, re.IGNORECASE): iot_val = "Crítica"
    elif re.search(r'(?:IoT.*Baixa|IoT.*Low|Exposição IoT[\s\S]{0,100}?Baixa)', full_text, re.IGNORECASE): iot_val = "Baixa"
    elif re.search(r'(?:IoT.*Inexistente|IoT.*None|Exposição IoT[\s\S]{0,100}?Inexistente|inexistente)', full_text, re.IGNORECASE): iot_val = "Inexistente"
    
    dwell_val = "Dias"
    if re.search(r'(?:Resposta.*Minutos|Reação.*Minutos|menos de 1 hora|Minutes)', full_text, re.IGNORECASE): dwell_val = "Minutos"
    elif re.search(r'(?:Resposta.*Semanas|Reação.*Semanas|Weeks)', full_text, re.IGNORECASE): dwell_val = "Semanas"
    elif re.search(r'(?:Resposta.*Dias|Reação.*Dias)', full_text, re.IGNORECASE): dwell_val = "Dias"

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Relatório Executivo Desestruturado (PDF)",
        "dados_completos": {"Q5_IoT": iot_val, "Q18_Resposta": dwell_val},
        "alertas": alertas
    }