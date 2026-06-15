import pandas as pd
import re

def clean_float_excel(val):
    """Remove moedas, espaços e lida com notações científicas e europeias de forma blindada."""
    if pd.isna(val): return None
    val_str = str(val).strip()
    if val_str.lower() in ['nan', 'none', '']: return None
    
    # Limpa tudo o que não seja número, ponto ou vírgula
    val_str = re.sub(r'[^\d\.,]', '', val_str)
    if not val_str: return None
    
    if ',' in val_str and '.' in val_str:
        if val_str.rfind(',') > val_str.rfind('.'):
            val_str = val_str.replace('.', '').replace(',', '.')
        else:
            val_str = val_str.replace(',', '')
    else:
        val_str = val_str.replace(',', '.')
        
    try: return float(val_str)
    except: return None

def find_metric_in_excel(xls, patterns):
    """
    Busca Estrutural: Procura num Excel como um humano. 
    Lê os cabeçalhos e as células. Se encontrar a palavra-chave, caça o número na célula adjacente!
    """
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        
        # 1. Procurar nas Colunas/Cabeçalhos
        for col_idx, col_name in enumerate(df.columns):
            col_str = str(col_name)
            if any(re.search(p, col_str, re.IGNORECASE) for p in patterns):
                # Se o cabeçalho tem o nome, o valor está nas linhas abaixo dessa coluna
                for val in df.iloc[:, col_idx]:
                    num = clean_float_excel(val)
                    if num is not None: return num
                    
        # 2. Procurar nas Células normais 
        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
                cell_val = str(df.iloc[row_idx, col_idx])
                if any(re.search(p, cell_val, re.IGNORECASE) for p in patterns):
                    # Tenta extrair da célula imediatamente à Direita
                    if col_idx + 1 < len(df.columns):
                        num = clean_float_excel(df.iloc[row_idx, col_idx + 1])
                        if num is not None: return num
                    # Tenta extrair da célula imediatamente Abaixo
                    if row_idx + 1 < len(df):
                        num = clean_float_excel(df.iloc[row_idx + 1, col_idx])
                        if num is not None: return num
    return None

def parse_excel_risk(file) -> dict:
    """Motor Semântico de Tabela para ficheiros Excel."""
    try: import openpyxl
    except ImportError:
        return {"erro": "O pacote 'openpyxl' está em falta. Execute `pip install openpyxl` no terminal."}

    try: xls = pd.ExcelFile(file)
    except Exception as e: return {"erro": f"Não foi possível ler o Excel. Detalhe: {str(e)}"}
        
    alertas = []
    
    # --- 1. EXTRAÇÃO FINANCEIRA (Busca Estrutural Nativa) ---
    ale_patterns = [r'\bALE\b', r'Perda Média', r'Perda Anual', r'Annual Loss', r'Prejuízo', r'FAIR_ALE']
    ale_val = find_metric_in_excel(xls, ale_patterns)
    
    if ale_val is None:
        ale_val = 50000.0
        alertas.append("Métrica financeira de Perda (ALE) não detetada. Assumido placeholder: 50.000 €.")

    rev_patterns = [r'Faturacao', r'Faturação', r'Orçamento', r'Revenue', r'Receita', r'Budget', r'Q1_Receita', r'Orcamento_Empresa']
    revenue = find_metric_in_excel(xls, rev_patterns)
    
    if revenue is None:
        revenue = 1000000.0
        alertas.append("Métrica de Faturação/Orçamento não detetada. Assumido placeholder: 1.000.000 €.")

    # --- 2. EXTRAÇÃO QUALITATIVA ---
    full_text = ""
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        # to_csv impede que o Pandas esconda colunas com "..."
        full_text += df.to_csv(index=False, sep=' ') + "\n"

    # Maturidade NIST
    nist = 1 # Fallback
    nist_match = re.search(r'(?:Tier\s*|NIST\s*Tier\s*|Maturidade\s*Tier\s*|Maturity\s*Tier\s*)([1-4])', full_text, re.IGNORECASE)
    if nist_match: nist = int(nist_match.group(1))
    else: alertas.append("Maturidade NIST não detetada. Assumido placeholder: Tier 1.")

    # Sensibilidade de Dados
    q_dados = 3 # Fallback
    if re.search(r'(?:Críticos|Regulados|Pessoais|Critical|Nível 5|Level 5)', full_text, re.IGNORECASE): q_dados = 5
    elif re.search(r'(?:Secretos|Secret|Nível 4|Level 4)', full_text, re.IGNORECASE): q_dados = 4
    elif re.search(r'(?:Altamente Confidenciais|Confidenciais|Confidential|Nível 3|Level 3)', full_text, re.IGNORECASE): q_dados = 3
    elif re.search(r'(?:Internos|Internal|Nível 2|Level 2)', full_text, re.IGNORECASE): q_dados = 2
    elif re.search(r'(?:Públicos|Public|Nível 1|Level 1)', full_text, re.IGNORECASE): q_dados = 1
    else: alertas.append("Sensibilidade de dados não detetada. Assumido placeholder: Nível 3.")

    # IoT e Dwell Time
    iot_val = "Moderada"
    if re.search(r'(?:IoT.*Crítica|IoT.*Critical|Exposição IoT[\s\S]{0,100}?Crítica)', full_text, re.IGNORECASE): iot_val = "Crítica"
    elif re.search(r'(?:IoT.*Baixa|IoT.*Low|Exposição IoT[\s\S]{0,100}?Baixa)', full_text, re.IGNORECASE): iot_val = "Baixa"
    elif re.search(r'(?:IoT.*Inexistente|IoT.*None|Exposição IoT[\s\S]{0,100}?Inexistente)', full_text, re.IGNORECASE): iot_val = "Inexistente"
    
    dwell_val = "Dias"
    if re.search(r'(?:Resposta.*Minutos|Reação.*Minutos)', full_text, re.IGNORECASE): dwell_val = "Minutos"
    elif re.search(r'(?:Resposta.*Semanas|Reação.*Semanas)', full_text, re.IGNORECASE): dwell_val = "Semanas"

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Matriz Estruturada Multi-Folha (Excel)",
        "dados_completos": {"Q5_IoT": iot_val, "Q18_Resposta": dwell_val},
        "alertas": alertas
    }