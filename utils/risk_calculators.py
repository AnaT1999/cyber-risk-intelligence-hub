import math
import numpy as np
import pandas as pd
from typing import Tuple, Dict

## --- Risco Criptográfico Pós-Quântico (PQR) --- ##

def calculate_pqr(criticality:int, algo_vulnerability:float, mitigation_level:float) -> float:
    """
    Calcula o Fator de Risco Criptográfico Pós-Quântico (PQR).
    Baseado na equação linear de auditoria algorítmica.
    Fórmula: $PQR=\alpha\cdot C+\beta\cdot V-\gamma\cdot M$
    """
    alpha = 0.40  # Peso para a criticidade
    beta = 0.45   # Peso para a vulnerabilidade do algoritmo
    gamma = 0.15  # Peso para o nível de mitigação

    pqr = (alpha * criticality) + (beta * algo_vulnerability) - (gamma * mitigation_level)
    return max (0.0, float(pqr))

## --- Índice de Risco de Desinformação (DRI) --- ##

def calculate_dri(reach:int, velocity: float, sentiment:float, ai_prob:float) -> float:
    """
    Calcula o Índice de Risco de Desinformação Baseada em IA (DRI).
    Aplica amortecimento logarítmico ao alcance e normaliza numa escala [0, 100].
    Fórmula: $DRI = \ln(\text{reach}) \cdot \text{velocity} \cdot (1.5 - \text{sentiment}) \cdot \text{ai\_prob}$
    """

    reach_safe = max(reach, 0) # evita erros do tipo log(0)
    raw_dri = math.log(reach_safe + 1) * velocity * (1.5 - sentiment) * ai_prob

    MAX_THEORICAL_DRI = 500.0 # limite operacional teorico para normalização
    normalized_dri = (raw_dri / MAX_THEORICAL_DRI) * 100.0

    return max(0.0, min(normalized_dri, 100.0))


## --- Propagação Matricial de Risco Sistémico --- ##

def propagate_systemic_risk(adjacency_matrix: np.ndarray, initial_risk: np.ndarray, iterations: int = 1, hawkes_decay_rate: float = 0.1) -> np.ndarray:
    """
    Modelo de Propagação Matricial de Risco Sistémico.
    Inclui o decaimento temporal inspirado pelo Processo de Hawkes.
    Fórmula: $R_{t+1}(i) = R_t(i) + \sum (R_t(j) \cdot W_{ji} \cdot (1-R_t(i)))$
    """

    current_risk = initial_risk.copy() # copia para garantir a pureza
    n_nodes = len(current_risk)

    for t in range(iterations):
        next_risk = current_risk.copy()
        decay_factor = math.exp (-hawkes_decay_rate * t) # decaimento temporal

        for i in range(n_nodes):
            cascading_effect = 0.0

            for j in range(n_nodes):
                weight_ji = adjancency_matrix[j, i]
                if weight_ji > 0: #aplicar decaimento temporal e fator amortecedor
                    cascading_effect += current_risk[j] * (weight_ji * decay_factor) * (1.0 - current_risk[i])

            next_risk[i] = current_risk[i] +  cascading_effect
            next_risk[i] = min(next_risk[i], 1.0) # garante que o risco não ultrapasse 100%

        current_risk = next_risk

    return current_risk

#Value at Risk ($VaR_\alpha$) e Conditional VaR ($CVaR_\alpha$):

#Simulação de Monte Carlo (Baseada em SDEs):

#Meta-Risco (Score Global):
##Fórmula: Agregação ponderada $MR = f(VaR, CVaR, C, U)$

#Processo de Hawkes (Intensidade de Decaimento): 
##Fórmula: $\lambda(t) = \mu + \sum \alpha e^{-\beta(t-t_i)}$

#Métricas de Desempenho (Precisão, Recall, F1-Score):

#Divergência de Kullback-Leibler (DKL):