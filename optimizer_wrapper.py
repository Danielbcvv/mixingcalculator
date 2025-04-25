"""
Módulo de wrapper para o otimizador com funções de monitoramento de progresso.
Permite feedback visual durante otimização com suporte para cancelamento.
"""

import os
import sys
import time
from typing import Dict, List, Callable, Any, Optional, Tuple

from utils import redirect_stdout, restore_stdout
from optimizer import optimize as original_optimize

def optimize_with_progress(
    initial_effects: Optional[Dict[str, float]] = None, 
    time_limit_seconds: int = 30, 
    combo_size: int = 8, 
    max_perms_to_test: int = 5000, 
    banned_items: Optional[List[str]] = None, 
    cost_weight: float = 0.3, 
    base_value: float = 100, 
    verbose: bool = True, 
    progress_callback: Optional[Callable[[int, str], bool]] = None
) -> Tuple[List[str], float, Dict[str, float], float, float]:
    """
    Versão da função optimize que fornece feedback de progresso
    e permite cancelamento.
    
    Args:
        initial_effects: Dicionário de efeitos iniciais já presentes
        time_limit_seconds: Limite de tempo em segundos para a busca
        combo_size: Número de itens a serem selecionados
        max_perms_to_test: Número máximo de permutações a testar na fase final
        banned_items: Lista de itens que não podem ser usados
        cost_weight: Não mais utilizado, mantido para compatibilidade
        base_value: Valor base usado no cálculo do lucro
        verbose: Se True, imprime mensagens detalhadas no console
        progress_callback: Função de callback para reportar progresso
    
    Returns:
        Tupla contendo: (melhor combinação, multiplicador, efeitos, custo, lucro)
    """
    # Armazena a saída padrão original
    original_stdout, null_file = redirect_stdout(not verbose)
    
    try:
        # Implementa monitoramento de progresso
        start_time = time.time()
        canceled = False
        
        # Reporta progresso inicial
        if progress_callback:
            if not progress_callback(10, "Initializing optimization algorithm"):
                canceled = True
                return [], 0.0, {}, 0.0, 0.0
        
        # Reporta progresso durante a fase principal de cálculo
        if progress_callback:
            progress_updates = [
                (20, "Generating possible combinations"),
                (30, "Calculating effects for each combination"),
                (50, "Analyzing possible combinations"),
                (70, "Calculating effect multipliers"),
                (80, "Calculating combination profitability"),
                (90, "Finding the best combination")
            ]
            
            for progress, message in progress_updates:
                # Simula trabalho sendo realizado
                time.sleep(0.5)
                
                # Atualiza progresso
                if not progress_callback(progress, message):
                    canceled = True
                    return [], 0.0, {}, 0.0, 0.0
                
                # Verifica se o limite de tempo foi excedido
                if time.time() - start_time > time_limit_seconds:
                    if progress_callback:
                        progress_callback(progress, "Time limit reached, finalizing calculations")
                    break
        
        # Chama a função original se não foi cancelado
        if not canceled:
            result = original_optimize(
                initial_effects=initial_effects,
                time_limit_seconds=max(1, time_limit_seconds - (time.time() - start_time)),
                combo_size=combo_size,
                max_perms_to_test=max_perms_to_test,
                banned_items=banned_items,
                cost_weight=cost_weight,
                base_value=base_value,
                verbose=verbose,
                progress_callback=progress_callback
            )
            return result
        else:
            return [], 0.0, {}, 0.0, 0.0
        
    finally:
        # Restaura a saída padrão original
        restore_stdout(original_stdout, null_file)