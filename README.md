# Cyber Risk Intelligence Hub 

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Versão](https://img.shields.io/badge/Versão-1.0-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)

## Sobre o Projeto
Plataforma modular e preditiva desenvolvida no âmbito da unidade curricular de **Avaliação do Risco em Cibersegurança** (Mestrado). 

Este *Hub* foi desenhado para colmatar a maior falha do mercado atual de segurança da informação: **a barreira de comunicação entre a engenharia (SOC) e a gestão (C-Level)**. Através da implementação de uma arquitetura analítica profunda baseada em **Cálculo Estocástico, Teoria de Redes** e **Modelos Financeiros de Cauda Pesada**, a plataforma traduz vulnerabilidades técnicas (CVEs, *exploits*, falhas criptográficas) em exposição financeira e operacional rigorosa (Euros, Probabilidades e Retorno sobre o Investimento - ROSI).

---

## Pilares e Motores Analíticos

O projeto transcende as avaliações qualitativas tradicionais (mapas de calor) e explora quatro eixos temáticos avançados:

1. **Dinâmica Estocástica e Perdas Extremas:**
   * Utilização do **Modelo FAIR** conjugado com **Simulações de Monte Carlo** (Lema de Itô) para prever a trajetória financeira do risco ao longo dos anos.
   * Cálculo de **Value at Risk (VaR)** e **Conditional VaR (CVaR)** para modelar eventos *Black Swan* e desastres catastróficos.
2. **Propagação de Ameaças em Rede (Contágio Sistémico):**
   * Modelação de ataques IoT e falhas de segmentação de rede através do **Processo de Decaimento de Hawkes** e variância de portefólio (Markowitz).
3. **Modelos de Auditoria Específicos (Ameaças do Séc. XXI):**
   * **PQR (Post-Quantum Risk):** Avaliação de longevidade criptográfica e exposição à tática tática de espionagem *Harvest Now, Decrypt Later*.
   * **DRI (Disinformation Risk Index):** Quantificação do risco reputacional gerado por *Deepfakes* e campanhas sintéticas via IA (Divergência de Kullback-Leibler).
4. **Inteligência de Ameaças em Tempo Real (ML & APIs):**
   * Motor de Machine Learning (**XGBoost**) treinado para classificar vulnerabilidades prioritárias.
   * Ingestão automatizada de auditorias (PDF, Excel, JSON) e sincronização *Live* com APIs governamentais e colaborativas (NIST NVD, AlienVault OTX, CISA KEV).

---

## Arquitetura do Sistema

A plataforma foi construída em **Python (Streamlit)** e segue uma estrutura modular rígida de separação de responsabilidades (Front-End, Back-End Lógico, Modelos de Dados):

```text
📦 CYBER-RISK-INTELLIGENCE-HUB
┣ 📂 data/                   # Armazenamento de datasets físicos
┃ ┣ 📂 raw/                  # Dados estáticos para Dashboards Globais (Página 1)
┃ ┃ ┣ 📂 iot/                # Datasets de comportamento IoT
┃ ┃ ┣ 📂 network/            # Datasets de tráfego de rede (UNSW-NB15)
┃ ┃ ┗ 📂 threat_intel/       # Catálogos MITRE ATT&CK, Corpus CVE e EPSS
┃ ┗ 📂 to_process/           # Raw data da NIST e CISA KEV para treino do modelo
┣ 📂 models/                 # Modelos de Machine Learning isolados
┃ ┣ 📜 threat_classifier.joblib # O motor XGBoost pré-treinado
┃ ┣ 📜 train_model.py        # Script original de treino do modelo
┃ ┗ 🖼️ *.png                 # Gráficos de feature importance e matrizes de confusão
┣ 📂 pages/                  # Interface Gráfica (Front-End Streamlit)
┃ ┣ 📜 1_Dashboard_Estatico.py
┃ ┣ 📜 2_Formulario_Risco.py
┃ ┣ 📜 3_Simulador_Cenarios.py
┃ ┣ 📜 4_Ingestao_Dados.py
┃ ┗ 📜 5_Threat_Intel_Live.py
┣ 📂 utils/                  # Motores de Lógica, APIs e UI (Back-End)
┃ ┣ 📜 risk_calculators.py   # Todo o motor estocástico e fórmulas matemáticas
┃ ┣ 📜 api_helpers.py        # Conexões seguras à NIST e AlienVault OTX
┃ ┣ 📜 parser_*.py           # Motores de mineração e extração de dados (PDF, JSON, Excel)
┃ ┣ 📜 report_*.py           # Geradores de relatórios executivos via ReportLab e XlsxWriter
┃ ┣ 📜 ui_components.py      # Fábrica de Estética (Dark Mode, Partículas, Hero Banners)
┃ ┗ 📜 visuals.py            # Componentes gráficos transversais (Plotly)
┣ 📜 Home.py                 # Ponto de entrada da aplicação (Landing Page)
┣ 📜 requirements.txt        # Mapeamento de dependências e bibliotecas
┗ 📜 .gitignore
```

## Stack Tecnológica
* Interface & Visualização: Streamlit, Plotly Express, Plotly Graph Objects.
* Core Matemático & Processamento: Numpy, Pandas.
* Inteligência Artificial: Scikit-Learn, XGBoost, Joblib.
* Exportação & Reporting: ReportLab (PDFs dinâmicos), XlsxWriter, PyPDF.
* Rede & APIs: Requests, JSON.

## Como Executar Localmente
1. Clone o repositório:
    `https://github.com/AnaT1999/cyber-risk-intelligence-hub.git` 
    `cd cyber-risk-intelligence-hub`
2. Crie e ative um ambiente virtual:
   ```text 
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Mac/Linux:
   source venv/bin/activate
   ```
3. Instale as dependências:
   `pip install -r requirements.txt`
4. Execute a aplicação Streamlit:
   `streamlit run Home.py` ou  ` python -m streamlit run Home.py`