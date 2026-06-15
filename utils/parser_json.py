import json
import re

def clean_float_json(val):
    """Limpa símbolos monetários e lida com formatos 10.000,00 ou 10,000.00 de forma blindada."""
    if isinstance(val, (int, float)):
        return float(val) # Se já for número, passa direto
        
    val_str = str(val).replace('€', '').replace('EUR', '').strip()
    if ',' in val_str and '.' in val_str:
        if val_str.rfind(',') > val_str.rfind('.'):
            val_str = val_str.replace('.', '').replace(',', '.') 
        else:
            val_str = val_str.replace(',', '') 
    else:
        val_str = val_str.replace(',', '.') # Converte a vírgula num ponto decimal
        
    try:
        return float(val_str)
    except:
        return None

def find_best_match(data_dict: dict, aliases: list):
    """Procura um valor num dicionário usando uma lista de sinónimos."""
    # 1. Tentativa Exata
    for alias in aliases:
        if alias in data_dict: return data_dict[alias]
    # 2. Tentativa Parcial
    for key, value in data_dict.items():
        for alias in aliases:
            if alias.lower() in key.lower(): return value
    return None

def parse_json_risk(file) -> dict:
    """Motor de Ingestão Resiliente para ficheiros JSON."""
    try:
        data = json.load(file)
    except Exception as e:
        return {"erro": f"O ficheiro não é um JSON válido. Detalhe: {str(e)}"}
        
    alertas = []
    
    # --- 1. Extração do ALE (Perda Anual) ---
    ale_raw = find_best_match(data, ["FAIR_ALE", "ale_val", "ALE", "Perda_Media", "Perda"])
    ale_val = clean_float_json(ale_raw)
    
    if ale_val is None:
        ale_val = 50000.0
        alertas.append(f"Métrica 'ALE' inválida ou não encontrada. Assumido placeholder: 50.000 €.")

    # --- 2. Extração da Faturação/Orçamento ---
    rev_raw = find_best_match(data, ["Orcamento_Empresa", "Faturacao_Empresa", "revenue", "Q1_Receita", "Faturacao", "Orcamento"])
    revenue = clean_float_json(rev_raw)
    
    if revenue is None:
        revenue = 1000000.0
        alertas.append(f"O valor de Faturação/Orçamento encontrado ('{rev_raw}') não é numérico. Assumido 1.000.000 €.")

    # --- 3. Extração da Maturidade NIST ---
    nist_raw = str(find_best_match(data, ["Q9_NIST", "nist_mat", "NIST", "Maturidade"]) or "")
    nist = 1 # Valor padrão
    if nist_raw:
        nist_match = re.search(r'(?:Tier\s*|Nível\s*)([1-4])', nist_raw, re.IGNORECASE)
        if nist_match:
            nist = int(nist_match.group(1))
        elif "1" in nist_raw: nist = 1
        elif "2" in nist_raw: nist = 2
        elif "3" in nist_raw: nist = 3
        elif "4" in nist_raw: nist = 4
        else:
            alertas.append(f"Maturidade NIST encontrada ('{nist_raw[:15]}...') não é clara. Assumido Tier 1.")
    else:
        alertas.append("Maturidade NIST não identificada. Assumido placeholder: Tier 1.")

    # --- 4. Extração da Sensibilidade de Dados ---
    dados_raw = str(find_best_match(data, ["Q3_Dados", "q_dados", "Sensibilidade", "Dados"]) or "")
    q_dados = 3 # Valor padrão
    if dados_raw:
        if re.search(r'(?:Públicos|1)', dados_raw, re.IGNORECASE): q_dados = 1
        elif re.search(r'(?:Internos|2)', dados_raw, re.IGNORECASE): q_dados = 2
        elif re.search(r'(?:Altamente Confidenciais|Confidenciais|3)', dados_raw, re.IGNORECASE): q_dados = 3
        elif re.search(r'(?:Secretos|4)', dados_raw, re.IGNORECASE): q_dados = 4
        elif re.search(r'(?:Críticos|Regulados|Pessoais|5)', dados_raw, re.IGNORECASE): q_dados = 5
        else:
            alertas.append(f"Sensibilidade de Dados ('{dados_raw[:15]}...') não clara. Assumido Nível 3.")
    else:
        alertas.append("Sensibilidade de Dados não identificada. Assumido Nível 3.")

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Telemetria Estruturada (JSON)",
        "dados_completos": data,
        "alertas": alertas
    }