import requests
import pandas as pd
import os
import joblib
import time

# --- CONFIGURAÇÕES DE CAMINHOS ---
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
MODELO_PATH = os.path.join(PASTA_ATUAL, '..', 'models', 'threat_classifier.joblib')

def fetch_live_threat_intel():
    """
    Busca as últimas vulnerabilidades na API da NIST com mecanismo de Retry e cruza com a IA.
    """
    
    # --- 1. ACORDAR A INTELIGÊNCIA ARTIFICIAL ---
    if not os.path.exists(MODELO_PATH):
        return {"erro": "Modelo de IA não encontrado. Verifica se o train_model.py correu com sucesso."}

    dados_modelo = joblib.load(MODELO_PATH)
    modelo = dados_modelo['modelo']
    colunas_esperadas = dados_modelo['colunas_treino']

    # --- 2. IR BUSCAR DADOS AO VIVO (COM TENTATIVAS AUTOMÁTICAS) ---
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=50"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    
    max_tentativas = 3
    dados = None
    
    for tentativa in range(max_tentativas):
        try:
            resposta = requests.get(url, headers=headers, timeout=20)
            if resposta.status_code == 200:
                dados = resposta.json()
                break
            elif resposta.status_code in [503, 403, 429]:
                tempo_espera = (tentativa + 1) * 3
                time.sleep(tempo_espera)
            else:
                return {"erro": f"A API da NIST devolveu o erro {resposta.status_code}."}
        except requests.exceptions.Timeout:
            time.sleep(2)
        except Exception as e:
            return {"erro": f"Erro de conexão: {str(e)}"}

    if dados is None:
        return {"erro": "Não foi possível contactar a NIST após várias tentativas. Os servidores podem estar em baixo."}

    # --- 3. FORMATAR OS DADOS CRUS ---
    cves_live = []
    for item in dados.get('vulnerabilities', []):
        cve_info = item.get('cve', {})
        cve_id = cve_info.get('id')
        if not cve_id: continue

        metrics = cve_info.get('metrics', {})
        base_score = 0
        attack_vector = 'UNKNOWN'
        attack_complexity = 'UNKNOWN'
        privileges_required = 'UNKNOWN'
        user_interaction = 'UNKNOWN'

        cvss3_list = metrics.get('cvssMetricV31', []) or metrics.get('cvssMetricV30', [])
        if cvss3_list:
            cvss_data = cvss3_list[0].get('cvssData', {})
            base_score = cvss_data.get('baseScore', 0)
            attack_vector = cvss_data.get('attackVector', 'UNKNOWN')
            attack_complexity = cvss_data.get('attackComplexity', 'UNKNOWN')
            privileges_required = cvss_data.get('privilegesRequired', 'UNKNOWN')
            user_interaction = cvss_data.get('userInteraction', 'UNKNOWN')
        elif metrics.get('cvssMetricV2'):
            cvss2_list = metrics.get('cvssMetricV2', [])
            cvss_data = cvss2_list[0].get('cvssData', {})
            base_score = cvss_data.get('baseScore', 0)
            attack_vector = cvss_data.get('accessVector', 'UNKNOWN')
            attack_complexity = cvss_data.get('accessComplexity', 'UNKNOWN')
        else:
            continue 

        descricao = "Sem descrição disponível."
        for desc in cve_info.get('descriptions', []):
            if desc.get('lang') == 'en':
                descricao = desc.get('value')
                break

        cves_live.append({
            'cve_id': cve_id,
            'descricao': descricao,
            'base_score': base_score,
            'attack_vector': attack_vector,
            'attack_complexity': attack_complexity,
            'privileges_required': privileges_required,
            'user_interaction': user_interaction
        })

    if not cves_live:
        return {"erro": "Nenhum CVE com métricas válidas encontrado hoje."}

    df_live = pd.DataFrame(cves_live)
    df_resultados = df_live[['cve_id', 'descricao', 'base_score', 'attack_vector']].copy()

    # --- 4. TRADUZIR OS DADOS PARA O MODELO ---
    features_categoricas = ['attack_vector', 'attack_complexity', 'privileges_required', 'user_interaction']
    df_features = pd.get_dummies(df_live[features_categoricas + ['base_score']])

    for col in colunas_esperadas:
        if col not in df_features.columns:
            df_features[col] = 0

    df_features = df_features[colunas_esperadas]

    # --- 5. A MAGIA: O MODELO TOMA A DECISÃO ---
    probabilidades = modelo.predict_proba(df_features)[:, 1]
    
    df_resultados['probabilidade_ia'] = probabilidades * 100 
    df_resultados = df_resultados.sort_values(by='probabilidade_ia', ascending=False)

    return {"sucesso": True, "dados": df_resultados.to_dict('records')}
def fetch_alienvault_otx(api_key, limit=50):
    """
    Busca as campanhas de malware e IoCs mais recentes subscritos pelo utilizador na AlienVault OTX.
    Requer a inserção de uma API Key válida.
    """
    import requests # Garantir que o requests está disponível
    url = f"https://otx.alienvault.com/api/v1/pulses/subscribed?limit={limit}"
    
    headers = {
        "X-OTX-API-KEY": api_key,
        "User-Agent": "CyberRiskIntelligenceHub/1.0"
    }
    
    try:
        # A AlienVault costuma ser rápida, 15s de tolerância
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            pulses_brutos = dados.get('results', [])
            
            if not pulses_brutos:
                return {"erro": "Nenhum 'Pulse' encontrado. Certifique-se que segue criadores de conteúdo na sua conta AlienVault."}
                
            lista_pulses = []
            for p in pulses_brutos:
                tags = p.get('tags', [])
                # Garantir que as tags vêm em texto (às vezes a API envia valores nulos)
                tags_limpas = [str(t) for t in tags if t] 
                
                lista_pulses.append({
                    'id': p.get('id', ''),
                    'nome': p.get('name', 'Sem Nome'),
                    'autor': p.get('author_name', 'Desconhecido'),
                    'tags_brutas': tags_limpas,
                    'tags_texto': ", ".join(tags_limpas),
                    'num_indicadores': p.get('indicator_count', 0),
                    'data_criacao': p.get('created', '')[:10]
                })
            return {"sucesso": True, "dados": lista_pulses}
            
        elif resposta.status_code == 403:
            return {"erro": "Acesso Negado: A sua API Key da AlienVault é inválida ou não tem permissões."}
        else:
            return {"erro": f"O servidor AlienVault recusou a ligação (Código {resposta.status_code})."}
            
    except Exception as e:
        return {"erro": f"Erro de conexão à internet ou à plataforma AlienVault: {str(e)}"}