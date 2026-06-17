# CVE, CISA KEV & EPSS - Dataset Estático (Kaggle)

Este repositório utiliza um dataset estático proveniente do Kaggle para alimentar os dashboards presentes em:
`pages/1_Dashboard_Estatico.py`


O dataset **não é incluído no repositório** devido ao seu tamanho (≈325 MB) e por não ser necessário para treino de modelos de IA.  
O seu único propósito é **fornecer dados aos dashboards estáticos**.

---

## 1. Fonte oficial do dataset

O dataset pode ser descarregado a partir de:

https://www.kaggle.com/datasets/francescomanzoni/vulnerability-management-datasets

Na página, encontrarás o título:

**“CVE, CISA KEV & EPSS Datasets”**

No canto superior direito, clica no botão **Download** e escolhe a opção:

- **Download dataset as .zip**

Um ficheiro chamado **`archive.zip`** será descarregado.

---

## 2. Onde colocar o ficheiro no repositório

Move o ficheiro `archive.zip` para:
`data/raw/threat_intel/`


A estrutura deverá ficar assim:

- **/data/**
  - **/raw/**
    - **/threat_intel/**
      - `archive.zip`


---

## 3. Extrair o conteúdo

Dentro da pasta `data/raw/threat_intel/`, extrai o ficheiro `archive.zip`.

Após a extração, deverão aparecer **exatamente dois ficheiros CSV**:
- `cve_cisa_epss_enriched_dataset.csv`
- `cve_corpus.csv`


Estes são os ficheiros utilizados pelos dashboards.

---

## 4. Finalidade do dataset

Este dataset **não é dinâmico** e **não é utilizado para treinar IA**.  
A sua função é exclusivamente:

- alimentar dashboards estáticos,
- permitir visualização de métricas,
- suportar análises exploratórias,
- fornecer dados consolidados sobre CVEs, CISA KEV e EPSS.

Os dashboards que utilizam estes dados encontram-se em:
`pages/1_Dashboard_Estatico.py`


---

## 5. Sobre o conteúdo do dataset

O dataset combina três fontes:

- **NVD (National Vulnerability Database)** - CVEs, CVSS, vetores de ataque, impacto, etc.
- **CISA KEV** - vulnerabilidades ativamente exploradas.
- **EPSS (Exploit Prediction Scoring System)** - probabilidade de exploração.

É fornecido em formato CSV e atualizado regularmente na fonte original, mas **neste projeto é usado como dataset estático**.

---

## 6. Referência oficial

Kaggle — Vulnerability Management Datasets  
https://www.kaggle.com/datasets/francescomanzoni/vulnerability-management-datasets

---


