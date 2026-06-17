# UNSW-NB15 - Dataset Estático (Kaggle)

Este repositório utiliza parte do dataset **UNSW-NB15**, disponível no Kaggle, para alimentar os dashboards presentes em:
`pages/1_Dashboard_Estatico.py`


O dataset **não é incluído no repositório** devido ao seu tamanho (o ficheiro necessário ocupa ~161 MB) e por não ser utilizado para treino de modelos de IA.  
A sua função é exclusivamente **fornecer dados aos dashboards estáticos** relacionados com tráfego de rede e deteção de intrusões.

---

## 1. Fonte oficial do dataset

O dataset pode ser descarregado a partir de:
https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15

Na página, encontrarás o título:

**“UNSW_NB15”**

No canto superior direito, clica no botão **Download** e escolhe a opção:

- **Download dataset as .zip**

Um ficheiro chamado **`archive.zip`** será descarregado.

---

## 2. Onde colocar o ficheiro no repositório

Move o ficheiro `archive.zip` para:
`data/raw/network/`


A estrutura deverá ficar assim:


Cria a seguinte estrutura:

- **/data/**
  - **/raw/**
    - **/network/**
      - `archive.zip`


---

## 3. Extrair o conteúdo

Dentro da pasta `data/raw/network/`, extrai o ficheiro `archive.zip`.

A extração irá gerar **vários ficheiros CSV**, incluindo:

- `UNSW-NB15_1.csv`
- `UNSW-NB15_2.csv`
- `UNSW-NB15_3.csv`
- `UNSW-NB15_4.csv`
- `UNSW-NB15_GT.csv`
- `UNSW-NB15_LIST_EVENTS.csv`
- `UNSW_NB15_training-set.csv`
- `UNSW_NB15_testing-set.csv`
- entre outros ficheiros auxiliares

---

## 4. Ficheiro utilizado neste projeto

Diferente dos outros datasets, **apenas um ficheiro é necessário**:
`UNSW-NB15_1.csv`

Todos os restantes ficheiros podem ser removidos após a extração.

A estrutura final deverá ser:

- **/data/**
  - **/raw/**
    - **/network/**
      - `UNSW-NB15_1.csv`

---

## 5. Finalidade do dataset

Este dataset **não é dinâmico** e **não é utilizado para treinar IA**.  
A sua função é exclusivamente:

- alimentar dashboards estáticos,
- permitir visualização de métricas de tráfego de rede,
- suportar análises exploratórias,
- fornecer dados sobre ataques e comportamentos maliciosos capturados em ambiente real/sintético.

Os dashboards que utilizam estes dados encontram-se em:
`pages/1_Dashboard_Estatico.py`

---

## 6. Sobre o conteúdo do dataset

O dataset UNSW-NB15 contém tráfego de rede capturado com o gerador **IXIA PerfectStorm**, incluindo:

- tráfego normal moderno,
- tráfego malicioso sintético,
- 9 tipos de ataques (Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms),
- 49 features extraídas com ferramentas como Argus e Bro-IDS,
- milhões de registos distribuídos por vários ficheiros.

Neste projeto, apenas o ficheiro **UNSW-NB15_1.csv** é utilizado para visualização.

---

## 7. Referência oficial

Kaggle - UNSW-NB15 Dataset  
https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15

---