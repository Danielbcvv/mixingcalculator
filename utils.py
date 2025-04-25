"""
Módulo de utilidades para o sistema.
Contém funções auxiliares e de conveniência.
"""

import os
import sys
from typing import Optional, Any, Callable

def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho correto para arquivos, seja no desenvolvimento ou no executável.
    
    Args:
        relative_path: Caminho relativo para o arquivo
    
    Returns:
        str: Caminho absoluto para o arquivo
    """
    if hasattr(sys, '_MEIPASS'):
        # Caminho temporário quando empacotado pelo PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def safe_cast(val: Any, to_type: Callable, default: Any = None) -> Any:
    """
    Tenta converter um valor para um tipo específico, retornando um valor padrão em caso de erro.
    
    Args:
        val: Valor a ser convertido
        to_type: Função de conversão para o tipo desejado
        default: Valor padrão a ser retornado em caso de erro
    
    Returns:
        Valor convertido ou valor padrão
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def format_currency(value: float) -> str:
    """
    Formata um valor como moeda.
    
    Args:
        value: Valor a ser formatado
    
    Returns:
        str: Valor formatado como moeda
    """
    return f"${value:.2f}"

def format_percentage(value: float) -> str:
    """
    Formata um valor como porcentagem.
    
    Args:
        value: Valor a ser formatado
    
    Returns:
        str: Valor formatado como porcentagem
    """
    return f"{value * 100:.2f}%"

def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Limita um valor entre um mínimo e um máximo.
    
    Args:
        value: Valor a ser limitado
        min_value: Valor mínimo
        max_value: Valor máximo
    
    Returns:
        float: Valor limitado
    """
    return max(min_value, min(value, max_value))

def redirect_stdout(enabled: bool = True):
    """
    Redireciona a saída padrão para um arquivo nulo se enabled for True.
    
    Args:
        enabled: Se True, redireciona a saída; se False, restaura a saída padrão
    
    Returns:
        Retorna o descritor de arquivo original se a saída foi redirecionada
    """
    if enabled:
        original_stdout = sys.stdout
        null_file = open(os.devnull, 'w')
        sys.stdout = null_file
        return original_stdout, null_file
    return None, None

def restore_stdout(original_stdout, null_file=None):
    """
    Restaura a saída padrão.
    
    Args:
        original_stdout: Descritor de arquivo original
        null_file: Arquivo nulo aberto por redirect_stdout
    """
    if original_stdout:
        sys.stdout = original_stdout
    
    if null_file:
        try:
            null_file.close()
        except:
            pass