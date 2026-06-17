import pandas as pd
import re

def clean_float_excel(val):
    """Remove moedas, espaços e lida com notações científicas e europeias de forma blindada."""
    if pd.isna(val): return None
    val_str = str(val).strip()
    if val_str.lower() in ['nan', 'none', '']: return None
    
    # Limpa tudo o que não seja número, ponto, vírgula e sinal negativo
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
        # Se tiver exatamente 3 casas decimais, assume separador de milhares
        if len(parts) == 2 and len(parts[1]) == 3:
            val_str = val_str.replace('.', '')
        else:
            pass
            
    try: return float(val_str)
    except: return None

def find_string_in_excel(xls, patterns):
    """Procura estruturalmente no Excel por uma palavra-chave e extrai APENAS o texto adjacente."""
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
                cell_val = str(df.iloc[row_idx, col_idx])
                if any(re.search(p, cell_val, re.IGNORECASE) for p in patterns):
                    # Tenta extrair à direita
                    if col_idx + 1 < len(df.columns):
                        val = str(df.iloc[row_idx, col_idx + 1]).strip()
                        if val and val.lower() not in ['nan', 'none', '']: return val
                    # Tenta extrair abaixo (ideal para cabeçalhos)
                    for offset in range(1, 4):
                        if row_idx + offset < len(df):
                            val = str(df.iloc[row_idx + offset, col_idx]).strip()
                            if val and val.lower() not in ['nan', 'none', '']: return val
    return ""

def find_metric_in_excel(xls, patterns):
    """Busca Estrutural Financeira: Caça o número na célula adjacente ou abaixo."""
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
                cell_val = str(df.iloc[row_idx, col_idx])
                if any(re.search(p, cell_val, re.IGNORECASE) for p in patterns):
                    if col_idx + 1 < len(df.columns):
                        num = clean_float_excel(df.iloc[row_idx, col_idx + 1])
                        if num is not None: return num
                    for offset in range(1, 4):
                        if row_idx + offset < len(df):
                            num = clean_float_excel(df.iloc[row_idx + offset, col_idx])
                            if num is not None: return num
    return None

def parse_excel_risk(file) -> dict:
    """Motor Semântico de Tabela para ficheiros Excel."""
    try: import openpyxl
    except ImportError: return {"erro": "O pacote 'openpyxl' está em falta."}

    try: xls = pd.ExcelFile(file)
    except Exception as e: return {"erro": f"Não foi possível ler o Excel. Detalhe: {str(e)}"}
        
    alertas = []
    
    # --- 1. EXTRAÇÃO FINANCEIRA ---
    ale_patterns = [r'\bALE\b', r'Perda Média', r'Perda Anual', r'Prejuízo', r'FAIR_ALE', r'Loss Magnitude', r'Pérdida', r'Perte Financière', r'Jahresverlust']
    ale_val = find_metric_in_excel(xls, ale_patterns)
    
    if ale_val is None:
        ale_val = 50000.0
        alertas.append("Métrica financeira de Perda (ALE) não detetada na tabela. Assumido placeholder: 50.000 €.")

    rev_patterns = [r'Faturacao', r'Faturação', r'Fat\. Global', r'Orçamento', r'Revenue', r'Receita', r'Budget', r'Ingresos', r'Chiffre', r'Umsatz']
    revenue = find_metric_in_excel(xls, rev_patterns)
    
    if revenue is None:
        revenue = 1000000.0
        alertas.append("Métrica de Faturação/Orçamento não detetada na tabela. Assumido placeholder: 1.000.000 €.")

    # --- 2. EXTRAÇÃO QUALITATIVA COM PROTEÇÃO DE COLUNA ---
    full_text = ""
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        full_text += df.to_csv(index=False, sep=' ') + "\n"

    # Maturidade NIST
    nist_patterns = [r'\bNIST\b', r'Maturidade', r'Tier', r'Maturity', r'Maturite', r'Reife', r'Madurez']
    nist_raw = find_string_in_excel(xls, nist_patterns)
    nist = None
    
    if nist_raw:
        m = re.search(r'(?:Tier\W*|Nível\W*|Niveau\W*|Level\W*|Stufe\W*)([1-4])', nist_raw, re.IGNORECASE)
        if m: nist = int(m.group(1))
        elif "1" in nist_raw: nist = 1
        elif "2" in nist_raw: nist = 2
        elif "3" in nist_raw: nist = 3
        elif "4" in nist_raw: nist = 4
        
    if nist is None:
        m = re.search(r'(?:Tier\W*|Nível\W*|Niveau\W*|Level\W*|Stufe\W*)([1-4])', full_text, re.IGNORECASE)
        if m: nist = int(m.group(1))
        else:
            nist = 1
            alertas.append("Maturidade NIST não detetada de forma clara. Assumido placeholder: Tier 1.")

    # Sensibilidade de Dados 
    dados_patterns = [r'Dados', r'Sensibilidade', r'Sensibilidad', r'Classification', r'Criticite', r'Privacy', r'Daten', r'Información']
    dados_raw = find_string_in_excel(xls, dados_patterns)
    q_dados = None
    
    if dados_raw:
        if re.search(r'(?:Crític|Critical|Kritisch|5)', dados_raw, re.IGNORECASE): q_dados = 5
        elif re.search(r'(?:Secret|4)', dados_raw, re.IGNORECASE): q_dados = 4
        elif re.search(r'(?:Confid|3)', dados_raw, re.IGNORECASE): q_dados = 3
        elif re.search(r'(?:Intern|2)', dados_raw, re.IGNORECASE): q_dados = 2
        elif re.search(r'(?:Públic|Public|1)', dados_raw, re.IGNORECASE): q_dados = 1

    if q_dados is None:
        # Fallback seguro que não confunde "IoT Crítica" com dados.
        if re.search(r'(?:Stufe\W*5|Level\W*5|Nível\W*5|Dados Críticos|Critical Data)', full_text, re.IGNORECASE): q_dados = 5
        elif re.search(r'(?:Stufe\W*4|Level\W*4|Nível\W*4|Secretos|Secret\b)', full_text, re.IGNORECASE): q_dados = 4
        elif re.search(r'(?:Stufe\W*3|Level\W*3|Nível\W*3|Confidenciais|Confidential|Confidentiel)', full_text, re.IGNORECASE): q_dados = 3
        elif re.search(r'(?:Stufe\W*2|Level\W*2|Nível\W*2|Internos|Internal)', full_text, re.IGNORECASE): q_dados = 2
        elif re.search(r'(?:Stufe\W*1|Level\W*1|Nível\W*1|Públicos|Public)', full_text, re.IGNORECASE): q_dados = 1
        else:
            q_dados = 3
            alertas.append("Sensibilidade de dados não detetada de forma clara. Assumido placeholder: Nível 3.")

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Matriz Estruturada Multi-Folha (Excel)",
        "dados_completos": {},
        "alertas": alertas
    }