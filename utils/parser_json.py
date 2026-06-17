import json
import re

def clean_float_json(val):
    """Limpa símbolos monetários e lida com qualquer formato mundial de forma blindada."""
    if val is None or str(val).strip() == "": return None
    if isinstance(val, (int, float)): return float(val)
    
    val_str = str(val)
    # Remove tudo exceto dígitos, vírgula, ponto e sinal negativo
    val_str = re.sub(r'[^\d\.,\-]', '', val_str)
    if not val_str: return None
    
    commas = val_str.count(',')
    dots = val_str.count('.')
    
    # Dedução inteligente de formato
    if commas > 1 and dots <= 1:
        val_str = val_str.replace(',', '') # Ex: 2,000,000
    elif dots > 1 and commas <= 1:
        val_str = val_str.replace('.', '').replace(',', '.') # Ex: 2.000.000,00
    elif commas == 1 and dots == 1:
        if val_str.rfind(',') > val_str.rfind('.'):
            val_str = val_str.replace('.', '').replace(',', '.') # Ex: 1.000,50
        else:
            val_str = val_str.replace(',', '') # Ex: 1,000.50
    elif commas == 1 and dots == 0:
        parts = val_str.split(',')
        if len(parts) == 2 and len(parts[1]) == 3:
            val_str = val_str.replace(',', '') # Assume separador de milhares (5,000)
        else:
            val_str = val_str.replace(',', '.') # Assume decimal (5000,50)
            
    try:
        return float(val_str)
    except:
        return None

def get_all_kv_pairs(obj):
    """Achatamento recursivo absoluto. Mapeia TUDO para garantir que nada se perde."""
    pairs = []
    if isinstance(obj, dict):
        # Truque Mágico para Arrays Chave-Valor (ex: Banco Espanhol)
        if len(obj) == 2:
            vals = list(obj.values())
            if not isinstance(vals[0], (dict, list)) and not isinstance(vals[1], (dict, list)):
                pairs.append((str(vals[0]), str(vals[1])))
                pairs.append((str(vals[1]), str(vals[0])))
        
        for k, v in obj.items():
            if not isinstance(v, (dict, list)):
                pairs.append((str(k), str(v)))
            else:
                pairs.extend(get_all_kv_pairs(v))
    elif isinstance(obj, list):
        for item in obj:
            pairs.extend(get_all_kv_pairs(item))
    return pairs

def find_best_match(pairs: list, aliases: list):
    """Procura um valor na lista de pares, garantindo correspondência segura."""
    # 1. Tentativa Exata
    for alias in aliases:
        for k, v in pairs:
            if alias.lower() == k.lower(): return v
    
    # 2. Tentativa Parcial Segura
    for alias in aliases:
        for k, v in pairs:
            if alias.lower() in k.lower(): return v
    return None

def parse_json_risk(file) -> dict:
    """Motor de Ingestão Resiliente para ficheiros JSON."""
    try:
        data = json.load(file)
    except Exception as e:
        return {"erro": f"O ficheiro não é um JSON válido. Detalhe: {str(e)}"}
        
    alertas = []
    # Cria uma lista plana com todas as chaves e valores possíveis do JSON
    pairs = get_all_kv_pairs(data)
    
    # Plano de Backup: O JSON inteiro convertido em texto
    full_json_str = json.dumps(data, ensure_ascii=False)
    
    # --- 1. Extração do ALE ---
    ale_aliases = ["FAIR_ALE", "ale_val", "ALE", "Perda_Media", "Perda", "Loss", "Exposure", "Exposicion", "Financiere", "Jahresverlust"]
    ale_raw = find_best_match(pairs, ale_aliases)
    ale_val = clean_float_json(ale_raw)
    
    if ale_val is None:
        ale_val = 50000.0
        alertas.append("Métrica 'ALE' não encontrada. Assumido placeholder: 50.000 €.")

    # --- 2. Extração da Faturação/Orçamento ---
    rev_aliases = ["Orcamento_Empresa", "Faturacao_Empresa", "revenue", "Q1_Receita", "Faturacao", "Orcamento", "Turnover", "Chiffre", "Presupuesto", "Umsatz", "Budget"]
    rev_raw = find_best_match(pairs, rev_aliases)
    revenue = clean_float_json(rev_raw)
    
    if revenue is None:
        revenue = 1000000.0
        alertas.append("Faturação/Orçamento não detetado. Assumido placeholder: 1.000.000 €.")

    # --- 3. Extração da Maturidade NIST ---
    nist = 1 
    nist_raw = str(find_best_match(pairs, ["Q9_NIST", "nist_mat", "Maturidade", "Tier", "Maturity", "NIST", "Maturite", "Reife"]) or "")
    
    # Junta o valor detetado com o JSON completo e procura padrões usando \W (qualquer não-letra, apanhando "Tier": 2)
    search_str_nist = nist_raw + " " + full_json_str
    
    if re.search(r'(?:Tier\W*4|Nível\W*4|Niveau\W*4|Level\W*4|Stufe\W*4|Adaptiv)', search_str_nist, re.IGNORECASE): nist = 4
    elif re.search(r'(?:Tier\W*3|Nível\W*3|Niveau\W*3|Level\W*3|Stufe\W*3)', search_str_nist, re.IGNORECASE): nist = 3
    elif re.search(r'(?:Tier\W*2|Nível\W*2|Niveau\W*2|Level\W*2|Stufe\W*2)', search_str_nist, re.IGNORECASE): nist = 2
    elif re.search(r'(?:Tier\W*1|Nível\W*1|Niveau\W*1|Level\W*1|Stufe\W*1)', search_str_nist, re.IGNORECASE): nist = 1
    else:
        if nist_raw.isdigit() and int(nist_raw) in [1,2,3,4]:
            nist = int(nist_raw)
        else:
            alertas.append("Maturidade NIST não identificada claramente. Assumido placeholder: Tier 1.")

    # --- 4. Extração da Sensibilidade de Dados ---
    q_dados = 3 
    dados_raw = str(find_best_match(pairs, ["Q3_Dados", "q_dados", "Sensibilidade", "Sensibilidad", "Classification", "Criticite", "Privacy", "Daten", "Dados"]) or "")
    
    search_str_dados = dados_raw + " " + full_json_str
    
    if re.search(r'(?:Críticos|Regulados|Pessoais|Critical|Kritisch|Stufe\W*5|Level\W*5|Nível\W*5)', search_str_dados, re.IGNORECASE): q_dados = 5
    elif re.search(r'(?:Secretos|Secret|Stufe\W*4|Level\W*4|Nível\W*4)', search_str_dados, re.IGNORECASE): q_dados = 4
    elif re.search(r'(?:Altamente Confidenciais|Confidenciais|Confidential|Confidentiel|Stufe\W*3|Level\W*3|Nível\W*3)', search_str_dados, re.IGNORECASE): q_dados = 3
    elif re.search(r'(?:Internos|Internal|Stufe\W*2|Level\W*2|Nível\W*2)', search_str_dados, re.IGNORECASE): q_dados = 2
    elif re.search(r'(?:Públicos|Public|Stufe\W*1|Level\W*1|Nível\W*1)', search_str_dados, re.IGNORECASE): q_dados = 1
    else:
        if dados_raw.isdigit() and int(dados_raw) in [1,2,3,4,5]:
            q_dados = int(dados_raw)
        else:
            alertas.append("Sensibilidade de Dados não identificada claramente. Assumido Nível 3.")

    return {
        "ale_val": ale_val,
        "revenue": revenue,
        "nist_mat": nist,
        "q_dados": q_dados,
        "origem": "Telemetria Estruturada (JSON)",
        "dados_completos": data,
        "alertas": alertas
    }