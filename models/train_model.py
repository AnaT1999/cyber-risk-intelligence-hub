import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve

# --- CONFIGURAÇÕES INTELIGENTES DOS CAMINHOS ---
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_NVD = os.path.join(PASTA_ATUAL, '..', 'data', 'to_process', 'datasets_nvd')
CISA_KEV_FILE = os.path.join(PASTA_ATUAL, '..', 'data', 'to_process', 'known_exploited_vulnerabilities.csv')
MODELO_OUTPUT = os.path.join(PASTA_ATUAL, 'threat_classifier.joblib')

print("=== INICIANDO O PIPELINE DE TREINO (MEDIUM GRID - BALANÇO DE RECALL) ===")

# --- 1. CARREGAR E PREPARAR O CISA KEV ---
print("\n1. A processar o catálogo CISA KEV...")
try:
    df_cisa = pd.read_csv(CISA_KEV_FILE)
    cves_exploradas = set(df_cisa['cveID'].dropna())
    print(f"-> Encontradas {len(cves_exploradas)} vulnerabilidades comprovadamente exploradas.")
except Exception as e:
    print(f"ERRO: Não foi possível ler o ficheiro CISA KEV. Detalhe: {e}")
    exit()

# --- 2. EXTRAIR DADOS DA NVD ---
print("\n2. A extrair dados dos ficheiros JSON (v2.0) da NVD...")
cve_data = []

for ficheiro in os.listdir(PASTA_NVD):
    if ficheiro.endswith('.json'):
        print(f"   -> A ler: {ficheiro}")
        caminho_json = os.path.join(PASTA_NVD, ficheiro)
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados_nvd = json.load(f)
                for item in dados_nvd.get('vulnerabilities', []):
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
                    
                    cve_data.append({
                        'cve_id': cve_id,
                        'base_score': base_score,
                        'attack_vector': attack_vector,
                        'attack_complexity': attack_complexity,
                        'privileges_required': privileges_required,
                        'user_interaction': user_interaction
                    })
        except Exception as e:
            print(f"   ERRO ao ler {ficheiro}: {e}")

df_nvd = pd.DataFrame(cve_data)
if len(df_nvd) == 0: exit()

# --- 3. O CASAMENTO DOS DADOS ---
print("\n3. A cruzar a NVD com o CISA KEV (Etiquetagem)...")
df_nvd['is_exploited'] = df_nvd['cve_id'].apply(lambda x: 1 if x in cves_exploradas else 0)

features_categoricas = ['attack_vector', 'attack_complexity', 'privileges_required', 'user_interaction']
df_features = pd.get_dummies(df_nvd[features_categoricas + ['base_score']])
df_target = df_nvd['is_exploited']

# --- 4. DIVISÃO DO TREINO ---
print("\n4. A dividir dados (80% treino, 20% teste)...")
X_train, X_test, y_train, y_test = train_test_split(df_features, df_target, test_size=0.2, random_state=42, stratify=df_target)

peso_base = (len(y_train) - y_train.sum()) / y_train.sum()

# --- 5. A MAGIA DA ITERAÇÃO (MEDIUM GRID SEARCH) ---
print("\n5. A iniciar pesquisa de hiperparâmetros (Foco no Recall)...")

xgb_base = XGBClassifier(random_state=42, eval_metric='logloss')

# Grelha Média (2 x 3 x 2 x 4 = 48 combinações x 3 Folds = 144 Fits)
param_grid = {
    'n_estimators': [150, 250],                  # Árvores
    'max_depth': [4, 5, 6],                      # Profundidade
    'learning_rate': [0.05, 0.1],                # Taxa de aprendizagem
    'scale_pos_weight': [peso_base * 0.7, peso_base * 0.85, peso_base, peso_base * 1.15] # Foco em forçar o Recall a subir
}

# Voltámos ao 'f1' para forçar o modelo a tentar apanhar os Falsos Negativos
grid_search = GridSearchCV(estimator=xgb_base, param_grid=param_grid, scoring='f1', cv=3, verbose=1, n_jobs=-1)

grid_search.fit(X_train, y_train)

print(f"\n-> Melhor combinação absoluta encontrada pelo Python:")
print(grid_search.best_params_)

modelo_otimizado = grid_search.best_estimator_

# --- 6. AVALIAÇÃO DO NOVO MODELO ---
print("\n6. A avaliar a qualidade do modelo final e substituir gráficos antigos...")
previsoes = modelo_otimizado.predict(X_test)
probabilidades = modelo_otimizado.predict_proba(X_test)[:, 1]

print("\n--- Relatório de Classificação ---")
print(classification_report(y_test, previsoes))
print(f"ROC AUC Score: {roc_auc_score(y_test, probabilidades):.4f}")

# 6.2 Matriz de Confusão
cm = confusion_matrix(y_test, previsoes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Prev: Não Explorada', 'Prev: Explorada'],
            yticklabels=['Real: Não Explorada', 'Real: Explorada'])
plt.title('Matriz de Confusão do Modelo Preditivo (V4 - Medium Grid)')
plt.ylabel('Verdade (CISA KEV)')
plt.xlabel('Previsão da IA')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_ATUAL, 'matriz_confusao.png')) 

# 6.3 Feature Importance
plt.figure(figsize=(10, 8))
feature_importances = pd.Series(modelo_otimizado.feature_importances_, index=X_train.columns)
feature_importances.nlargest(10).plot(kind='barh', color='darkorange')
plt.title('Top 10 Fatores Mais Importantes na Previsão de Ameaças')
plt.xlabel('Nível de Importância')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(PASTA_ATUAL, 'feature_importance.png')) 

# --- 7. EXPORTAR O MODELO ---
print("\n7. A sobrescrever o ficheiro .joblib...")
dados_exportacao = {
    'modelo': modelo_otimizado,
    'colunas_treino': list(X_train.columns)
}
joblib.dump(dados_exportacao, MODELO_OUTPUT)
print(f"SUCESSO! O modelo equilibrado V4 foi guardado.")
print("=== TREINO CONCLUÍDO ===")