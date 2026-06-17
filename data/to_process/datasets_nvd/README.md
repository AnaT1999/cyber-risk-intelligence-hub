# NVD JSON 2.0 - Instruções de Download dos Datasets

Este projeto utiliza datasets oficiais da **NVD (National Vulnerability Database)** para treinar o modelo de IA localizado em:
`models/train_model.py`


Devido ao tamanho total dos ficheiros (≈1.5 GB), **os datasets não são incluídos neste repositório**.  
Segue as instruções abaixo para obter e preparar os ficheiros necessários.

---

## 1. Aceder ao site oficial da NVD

Visita o link:

https://nvd.nist.gov/vuln/data-feeds#divJson20Feeds

No site, desloca-te até à secção **“JSON 2.0 Feeds”**.

---

## 2. Descarregar os ficheiros necessários

Na tabela *JSON 2.0 Feeds*, descarrega os ficheiros **ZIP** correspondentes aos anos:

- CVE‑2019  
- CVE‑2020  
- CVE‑2021  
- CVE‑2022  
- CVE‑2023  
- CVE‑2024  
- CVE‑2025  
- CVE‑2026  

Cada linha da tabela contém três opções: `META`, `GZ` e `ZIP`.  
Escolhe sempre a opção **ZIP**.

---

## 3. Extrair os ficheiros ZIP

Após o download:

1. Extrai cada um dos 8 ficheiros `.zip`.
2. No final, deverás obter **exatamente 8 ficheiros JSON**, com os seguintes nomes:
- `nvdcve-2.0-2019.json`
- `nvdcve-2.0-2020.json`
- `nvdcve-2.0-2021.json`
- `nvdcve-2.0-2022.json`
- `nvdcve-2.0-2023.json`
- `nvdcve-2.0-2024.json`
- `nvdcve-2.0-2025.json`
- `nvdcve-2.0-2026.json`


> **Nota:** Os nomes podem variar ligeiramente dependendo do sistema operativo, mas devem seguir o padrão `nvdcve-2.0-YYYY.json`.

---

## 4. Onde colocar os ficheiros no repositório

Cria a seguinte estrutura:

- **/data/**
  - **/to_process/**
    - **/datasets_nvd/**
      - `nvdcve-2.0-2019.json`
      - `nvdcve-2.0-2020.json`
      - `nvdcve-2.0-2021.json`
      - `nvdcve-2.0-2022.json`
      - `nvdcve-2.0-2023.json`
      - `nvdcve-2.0-2024.json`
      - `nvdcve-2.0-2025.json`
      - `nvdcve-2.0-2026.json`



Se utilizares outro diretório, ajusta o caminho no script de treino.

---

## 5. Porque estes datasets são necessários

O modelo de IA deste repositório utiliza estes datasets para:

- análise de vulnerabilidades,
- extração de padrões,
- classificação de CVEs,
- treino de embeddings ou modelos supervisionados.

O script responsável pelo treino encontra-se em: 
`models/train_model.py`

O modelo treinado encontra-se em:
`models/theat_classifier.joblib`


---

## 6. Referências oficiais

- NVD Data Feeds - JSON 2.0  
  https://nvd.nist.gov/vuln/data-feeds#divJson20Feeds

---






