# IoT Cyber Behavior Dataset — Dataset Estático (Kaggle)

Este repositório utiliza um dataset estático proveniente do Kaggle para alimentar os dashboards presentes em:
`pages/1_Dashboard_Estatico.py`


O dataset **não é incluído no repositório** devido ao seu tamanho e por não ser necessário para treino de modelos de IA.  
A sua função é exclusivamente **fornecer dados aos dashboards estáticos** relacionados com comportamento de dispositivos IoT.

---

## 1. Fonte oficial do dataset

O dataset pode ser descarregado a partir de:
https://www.kaggle.com/datasets/programmer3/iot-cyber-behavior-dataset

Na página, encontrarás o título:
**“IoT Cyber Behavior Dataset”**

No canto superior direito, clica no botão **Download** e escolhe a opção:

- **Download dataset as .zip**

Um ficheiro chamado **`archive.zip`** será descarregado.

---

## 2. Onde colocar o ficheiro no repositório

Move o ficheiro `archive.zip` para:
`data/raw/iot/`


A estrutura deverá ficar assim:
`/data/`
`  |_/raw/`
`     |_/iot/`
`        |_archive.zip`


---

## 3. Extrair o conteúdo

Dentro da pasta `data/raw/iot/`, extrai o ficheiro `archive.zip`.

Após a extração, deverá aparecer **um único ficheiro CSV**:
`iot_behavior.csv`
Este é o ficheiro utilizado pelos dashboards.

---

## 4. Finalidade do dataset

Este dataset **não é dinâmico** e **não é utilizado para treinar IA**.  
A sua função é exclusivamente:

- alimentar dashboards estáticos,
- permitir visualização de métricas de comportamento IoT,
- suportar análises exploratórias,
- fornecer dados sobre atividade legítima, comprometida e maliciosa em dispositivos IoT.

Os dashboards que utilizam estes dados encontram-se em:
`pages/1_Dashboard_Estatico.py`


---

## 5. Sobre o conteúdo do dataset

O dataset contém registos de comportamento de dispositivos IoT, incluindo:

- padrões de tráfego,
- interações de rede,
- tentativas de autenticação,
- métricas de CPU e sinais operacionais,
- deteção de comportamentos genuínos, comprometidos e maliciosos.

Inclui ainda um campo de classificação (`class_label`) com:

- **0 — Genuine**  
- **1 — Compromised**  
- **2 — Counterfeit** (dependendo da versão do dataset)

---

## 6. Referência oficial

Kaggle — IoT Cyber Behavior Dataset  
https://www.kaggle.com/datasets/programmer3/iot-cyber-behavior-dataset

---