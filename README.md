# Cyber Risk Intelligence Hub 

## Sobre o Projeto
Plataforma modular desenvolvida no âmbito da unidade curricular de **Cybersecurity Risk Evaluation**.
Este hub integra várias vertentes da inteligência de risco cibernético, transformando dados técnicos, inteligência de ameaças e modelação em informações acionáveis para a tomada de decisão.

## Temas Abordados
O projeto explora os seguintes eixos temáticos:
* Avaliação de Risco Sistémico e Prontidão Pós-Quântica. Uma ferramenta de auditoria que avalia primeiro a maturidade de segurança base da organização e, de seguida, afere o risco específico face à transição para a criptografia pós-quântica (Crypto-Agility).
* Dashboard de Inteligência de Risco Assistido por IA.
* Risco Aumentado de Desinformação e Engenharia Social via Inteligência Artificial.

## Arquitetura do Sistema
A plataforma foi construída em Python (Streamlit) e segue uma arquitetura modular profissional:
* `/data`: Armazenamento de datasets estáticos e processados.
* `/models`: Modelos de Machine Learning treinados e isolados.
* `/pages`: Interface gráfica dividida em módulos independentes.
* `/utils`: Funções de backend, chamadas de API e cálculos de risco.

## Como Executar Localmente
1. Clone o repositório:
   `https://github.com/AnaT1999/cyber-risk-intelligence-hub.git` 
2. Instale as dependências:
   `pip install -r requirements.txt`
3. Execute a aplicação Streamlit:
   `streamlit run app.py`