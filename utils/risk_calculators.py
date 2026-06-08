import math
import numpy as np
import pandas as pd
from typing import Tuple, Dict

## --- Risco Criptográfico Pós-Quântico (PQR) --- ##

def calculate_pqr(criticality:int, algo_vulnerability:float, mitigation_level:float) -> float:
    r"""
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
    r"""
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
    r"""
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
                weight_ji = adjacency_matrix[j, i]
                if weight_ji > 0: #aplicar decaimento temporal e fator amortecedor
                    cascading_effect += current_risk[j] * (weight_ji * decay_factor) * (1.0 - current_risk[i])

            next_risk[i] = current_risk[i] +  cascading_effect
            next_risk[i] = min(next_risk[i], 1.0) # garante que o risco não ultrapasse 100%

        current_risk = next_risk

    return current_risk


## --- Value at Risk e Conditional VaR --- ##

def calculate_var_cvar(losses: np.ndarray, confidence_level:float = 0.95) -> Tuple[float, float]:
    r"""
    Calcula o Value at Risk (VaR) e o Conditional VaR (CVaR).
    Converte impacto de ameaças em métricas financeiras/operacionais de cauda pesada.
    """

    if len(losses) == 0:
        return 0.0, 0.0
    
    #VaR
    var = np.percentile(losses, confidence_level * 100)

    #CVaR
    tail_losses = losses[losses > var]
    cvar = np.mean(tail_losses) if len(tail_losses) > 0 else var

    return float(var), float(cvar)


## --- Simulação de Monte Carlo Baseada em SDEs -- ##

def simulate_monte_carlo_risk(initial_risk: float, drift: float, volatility: float, steps: int = 30, simulations: int = 1000) -> np.ndarray:
    r"""
    Simulação de trajetórias de risco baseada no Movimento Browniano Geométrico (SDE).
    Devolve uma matriz com milhares de caminhos possíveis para visualização no dashboard.
    """

    dt = 1.0 /steps
    paths = np.zeros((steps +1, simulations))
    paths[0] = initial_risk

    for t in range(1, steps + 1):
        random_shock = np.random.standard_normal(simulations) # ruido estocástico

        #Lema de Ito aplicado na variação
        growth_factor = np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * random_shock)
        paths[t] = paths[t-1] * growth_factor

        paths[t] = np.clip(paths[t], 0.0, 100.0) # limite do risco máximo a 100%
    
    return paths


## --- Meta-Risco (Score Global) --- ##

def calculate_meta_risk(cvar: float, systemic_score: float, model_uncertainty:float, weights: Dict[str, float] = None) -> float:
    r"""
    Calcula o Meta-Risco (MR) como uma função agregada de múltiplas métricas.
    Agrega as métricas complexas num Score de Decisão Executivo Único (Meta-Risco).
    Permite personalização de pesos para cada componente.
    Fórmula: $MR = w_1 \cdot CVaR + w_2 \cdot Systemic\_Score + w_3 \cdot Uncertainty$
    """

    if weights is None:
        weights = {
            'cvar': 0.40,
            'systemic': 0.40,
            'uncertainty': 0.20
        }

    meta_score = (cvar * weights['cvar']) + (systemic_score * weights['systemic']) + (model_uncertainty * weights['uncertainty'])
    
    return float (np.clip(meta_score, 0.0, 100.0)) # garante que o Meta-Risco esteja entre 0 e 100