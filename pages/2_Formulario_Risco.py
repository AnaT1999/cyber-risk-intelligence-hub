import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.markdown("## Motor Estocástico de Avaliação de Risco")
st.write("Insira os parâmetros organizacionais para calcular o risco em tempo real.")

# Seletor do Motor de Risco
motor_escolhido = st.selectbox(
    "Selecione o Modelo de Risco a Avaliar:",
    ["Risco Pós-Quântico (PQR)", "Índice de Desinformação Sintética (DRI)"]
)

st.markdown("---")

if motor_escolhido == "Risco Pós-Quântico (PQR)":
    
    st.markdown("### Avaliação de Risco Pós-Quântico (Teorema de Mosca)")
    st.info("Baseado na equação $D + M > Q$, onde avaliamos a vulnerabilidade da organização a ataques do tipo *'Harvest Now, Decrypt Later'*.")

    with st.form("form_pqr"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Variáveis Organizacionais**")
            # Variável D (Data Shelf-life)
            d_val = st.slider(
                "Tempo de vida útil da confidencialidade dos dados (D - Anos):", 
                min_value=0, max_value=20, value=5,
                help="Durante quantos anos os dados que a sua empresa guarda precisam de ser mantidos em segredo?"
            )
            
            # Variável M (Migration Time)
            m_val = st.slider(
                "Tempo estimado de migração criptográfica (M - Anos):", 
                min_value=1, max_value=15, value=3,
                help="Quantos anos demoraria a substituir todos os algoritmos atuais da sua empresa por criptografia pós-quântica?"
            )
            
        with col2:
            st.markdown("**Variáveis de Ameaça (Threat Landscape)**")
            # Variável Q (Quantum Y2Q)
            q_val = st.slider(
                "Estimativa para a quebra do RSA/ECC (Q - Anos):", 
                min_value=1, max_value=20, value=8,
                help="A estimativa da indústria para quando um Computador Quântico Criptograficamente Relevante (CRQC) existirá (Y2Q)."
            )
            
        st.markdown("---")
        # Botão de submissão
        submitted = st.form_submit_button(" Executar Motor Matemático PQR", use_container_width=True)

    # --- PROCESSAMENTO E RELATÓRIO ---
    if submitted:
        st.markdown("### Relatório Executivo de Decisão")
        
        # 1. O Motor Matemático
        soma_vulneravel = d_val + m_val
        margem_risco = soma_vulneravel - q_val
        
        # 2. KPIs de Resultados
        colA, colB, colC = st.columns(3)
        colA.metric("Necessidade de Proteção (D + M)", f"{soma_vulneravel} Anos")
        colB.metric("Horizonte Quântico (Q)", f"{q_val} Anos")
        
        # Lógica Condicional de Estado de Risco
        if margem_risco > 0:
            estado = "CRÍTICO"
            cor = ":red_circle:"
            delta_cor = "inverse"
            mensagem = f"A sua organização ficará vulnerável {margem_risco} ano(s) antes de conseguir migrar a infraestrutura."
        elif margem_risco == 0:
            estado = "ELEVADO"
            cor = ":orange_circle:"
            delta_cor = "off"
            mensagem = "A sua organização tem margem zero. A migração deve começar imediatamente."
        else:
            estado = "CONTROLADO"
            cor = ":green_circle:"
            delta_cor = "normal"
            mensagem = f"A organização possui uma margem de segurança de {abs(margem_risco)} ano(s)."
            
        colC.metric("Score de Risco Quântico", estado, delta=f"{margem_risco} Anos de Margem", delta_color=delta_cor)
        
        # 3. Alertas Visuais
        if margem_risco > 0:
            st.error(f"**{cor} RISCO ATIVO DETETADO:** {mensagem} Está atualmente exposto a ataques de roubo de tráfego encriptado para decifragem futura.")
        elif margem_risco == 0:
            st.warning(f"**{cor} ALERTA DE PRAZO:** {mensagem}")
        else:
            st.success(f"**{cor} POSTURA SEGURA:** {mensagem}")
            
        # 4. Motor de Recomendações (Inteligência Artificial de Decisão)
        st.markdown("#### Recomendações Estratégicas Automatizadas")
        if m_val > 5:
            st.write(" **Redução de M:** O seu tempo de migração é muito elevado (> 5 anos). Recomenda-se iniciar o inventário criptográfico de imediato e adotar uma arquitetura de *Cripto-Agilidade*.")
        if d_val > 10:
            st.write(" **Proteção de D:** Guarda dados com vida útil extrema (> 10 anos). Aplique encriptação simétrica pesada (AES-256) imediatamente, pois é mais resistente a ataques quânticos do que o RSA.")
        if margem_risco <= 0:
            st.write(" **Manutenção:** Mantenha a vigilância sobre a variável Q. Se os avanços quânticos acelerarem, a sua margem desaparecerá.")

        st.markdown("---")
        
        st.markdown("#### Exportar Dados e Relatório")
        
        # Criar o dicionário de dados
        dados_exportacao = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Avaliacao": "Risco Pos-Quantico (PQR)",
            "Vida_Util_Dados_D": d_val,
            "Tempo_Migracao_M": m_val,
            "Horizonte_Quantico_Q": q_val,
            "Margem_de_Risco_Anos": margem_risco,
            "Estado_Global": estado
        }
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Gerar JSON
            json_string = json.dumps(dados_exportacao, indent=4)
            st.download_button(
                label="Descarregar Relatório (JSON)",
                file_name="relatorio_pqr.json",
                mime="application/json",
                data=json_string,
                use_container_width=True
            )
            
        with col_export2:
            # Gerar CSV
            df_export = pd.DataFrame([dados_exportacao])
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descarregar Tabela (CSV)",
                file_name="relatorio_pqr.csv",
                mime="text/csv",
                data=csv_data,
                use_container_width=True
            )

elif motor_escolhido == "Índice de Desinformação Sintética (DRI)":
    st.info("O motor DRI está em desenvolvimento e será ativado no próximo patch.")