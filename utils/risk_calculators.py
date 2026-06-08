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

# ==========================================
# BLOCO DE TESTE
# ==========================================
if __name__ == "__main__":
    print("A INICIAR TESTES DA CALCULADORA DE RISCO...\n")
    
    # 1. Testar PQR
    pqr_val = calculate_pqr(criticality=5, algo_vulnerability=5.0, mitigation_level=1.0)
    print(f"1. PQR (Risco Quântico) -> Esperado ~4.10 | Resultado: {pqr_val:.2f}")
    
    # 2. Testar DRI
    dri_val = calculate_dri(reach=1000000, velocity=8.5, sentiment=-0.8, ai_prob=0.95)
    print(f"2. DRI (Desinformação) -> Resultado Normalizado: {dri_val:.2f}/100.0")
    
    # 3. Testar Propagação Sistémica (Matriz 3x3)
    adj_matrix = np.array([
        [0.0, 0.8, 0.0],  # Nó 0 afeta Nó 1 fortemente
        [0.0, 0.0, 0.5],  # Nó 1 afeta Nó 2
        [0.0, 0.0, 0.0]   # Nó 2 não afeta ninguém
    ])
    init_risk = np.array([0.9, 0.2, 0.1])
    sys_risk = propagate_systemic_risk(adj_matrix, init_risk, iterations=2)
    print(f"3. Risco Sistémico -> Risco Inicial: {init_risk} | Risco Pós-Contágio: {np.round(sys_risk, 2)}")
    
    # 4. Testar VaR e CVaR (Com 1000 perdas financeiras simuladas)
    np.random.seed(42) # Para resultados consistentes no teste
    simulated_losses = np.random.normal(loc=50000, scale=15000, size=1000)
    var, cvar = calculate_var_cvar(simulated_losses)
    print(f"4. Cyber-VaR e CVaR -> VaR (95%): {var:.2f}€ | CVaR: {cvar:.2f}€")
    
    # 5. Testar Monte Carlo (Trajetórias SDE)
    mc_paths = simulate_monte_carlo_risk(initial_risk=30.0, drift=0.02, volatility=0.15, steps=10, simulations=5)
    print(f"5. Simulação Monte Carlo -> Matriz gerada com sucesso! Formato (Passos, Simulações): {mc_paths.shape}")
    
    # 6. Testar Meta-Risco Agregado
    meta = calculate_meta_risk(cvar=85.0, systemic_score=sys_risk.mean()*100, model_uncertainty=15.0)
    print(f"6. Score Executivo (Meta-Risco) -> Resultado: {meta:.2f}/100.0")
    
    print("\nTESTES CONCLUÍDOS! Se não houver erros acima, a calculadora está perfeita.")