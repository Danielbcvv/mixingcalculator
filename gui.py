"""
Interface gráfica do usuário para o Schedule 1 Calculator.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import sys
import threading
import time
import queue
from typing import Dict, List, Tuple, Optional, Callable

# Importações dos módulos locais
from effects import effect_multipliers
from items import items, item_prices, get_all_items
from raw_materials import RAW_MATERIALS
from utils import resource_path
from optimizer import optimize

class Schedule1Calculator(tk.Tk):
    """Interface gráfica para o Schedule 1 Calculator."""
    
    def __init__(self):
        """Inicializa a interface gráfica."""
        super().__init__()
        self.title("Schedule 1 Calculator")
        self.geometry("850x800")
        self.configure(bg="#f0f0f0")
        
        # Variáveis
        self.raw_material_var = tk.StringVar()
        self.combo_size_var = tk.IntVar(value=4)
        self.banned_items_vars = {}
        self.raw_material_img = None
        
        # Inicializa dicionários para armazenar resultados
        self.result_combination = []
        self.result_multiplier = 0.0
        self.result_effects = {}
        self.result_cost = 0.0
        self.result_profit = 0.0
        self.result_sell_price = 0.0
        
        # Fila para comunicação entre threads
        self.progress_queue = queue.Queue()
        self.is_calculating = False
        
        self.create_widgets()
        
        # Inicia monitoramento da fila de progresso
        self.monitor_progress_queue()
    
    def create_widgets(self):
        """Cria os widgets da interface gráfica."""
        # Frame principal dividido em duas colunas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Coluna esquerda (parâmetros de entrada)
        input_frame = ttk.LabelFrame(main_frame, text="Parameters")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Coluna direita (resultados)
        self.result_frame = ttk.LabelFrame(main_frame, text="Results")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Seção de Matéria-Prima
        self._create_raw_material_section(input_frame)
        
        # Seção de Quantidade de Itens
        self._create_items_count_section(input_frame)
        
        # Seção de Itens Banidos
        self._create_banned_items_section(input_frame)
        
        # Botões de Calcular e Cancelar
        self._create_action_buttons(input_frame)
        
        # Inicializa a exibição da matéria-prima
        self.update_raw_material()
        
        # Prepara o frame de resultados
        self.prepare_result_frame()
    
    def _create_raw_material_section(self, parent_frame):
        """Cria a seção de matéria-prima."""
        raw_mat_frame = ttk.LabelFrame(parent_frame, text="Raw Material")
        raw_mat_frame.pack(fill=tk.X, padx=5, pady=5)
        
        raw_mat_dropdown = ttk.Combobox(raw_mat_frame, textvariable=self.raw_material_var, 
                                       values=list(RAW_MATERIALS.keys()), state="readonly")
        raw_mat_dropdown.pack(fill=tk.X, padx=5, pady=5)
        raw_mat_dropdown.bind("<<ComboboxSelected>>", self.update_raw_material)
        raw_mat_dropdown.current(0)  # Seleciona o primeiro item por padrão
        
        # Frame para conter imagem da matéria-prima com fundo próprio
        self.raw_mat_img_frame = ttk.Frame(raw_mat_frame, style="RawMat.TFrame")
        self.raw_mat_img_frame.pack(padx=5, pady=5)
        
        # Criar estilo com fundo cinza escuro para contraste
        style = ttk.Style()
        style.configure("RawMat.TFrame", background="#333333")
        
        self.raw_mat_img_label = ttk.Label(self.raw_mat_img_frame, background="#555555")
        self.raw_mat_img_label.pack(padx=5, pady=5)
        
        self.raw_mat_info_label = ttk.Label(raw_mat_frame, text="")
        self.raw_mat_info_label.pack(padx=5, pady=5)
    
    def _create_items_count_section(self, parent_frame):
        """Cria a seção de quantidade de itens."""
        items_count_frame = ttk.LabelFrame(parent_frame, text="Item Quantity")
        items_count_frame.pack(fill=tk.X, padx=5, pady=5)
        
        items_scale = ttk.Scale(items_count_frame, from_=1, to=8, orient=tk.HORIZONTAL,
                               variable=self.combo_size_var, command=self.update_combo_size)
        items_scale.pack(fill=tk.X, padx=5, pady=5)
        
        self.items_count_label = ttk.Label(items_count_frame, text="Quantity: 4")
        self.items_count_label.pack(padx=5, pady=5)
    
    def _create_banned_items_section(self, parent_frame):
        """Cria a seção de itens banidos."""
        banned_items_frame = ttk.LabelFrame(parent_frame, text="Banned Items")
        banned_items_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Cria um canvas com barra de rolagem para checkboxes de itens banidos
        canvas = tk.Canvas(banned_items_frame)
        scrollbar = ttk.Scrollbar(banned_items_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Adiciona checkboxes para cada item sem rótulos de imagem
        for i, item_name in enumerate(sorted(items.keys())):
            var = tk.BooleanVar()
            self.banned_items_vars[item_name] = var
            
            # Criar um frame para cada item para garantir alinhamento uniforme
            item_frame = ttk.Frame(scrollable_frame)
            item_frame.pack(fill=tk.X, padx=2, pady=2)
            
            # Usar checkbutton padrão do Tkinter com parâmetros para remover bordas
            # e definir anchor=tk.W para alinhar à esquerda
            check = tk.Checkbutton(item_frame, text=item_name, variable=var, 
                                  highlightthickness=0, bd=0, anchor=tk.W)
            check.pack(fill=tk.X, padx=5, pady=0)
    
    def _create_action_buttons(self, parent_frame):
        """Cria os botões de ação (Calcular e Cancelar)."""
        calc_button_frame = ttk.Frame(parent_frame)
        calc_button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Botão Calcular com melhor destaque
        self.calc_button = tk.Button(calc_button_frame, text="CALCULATE", 
                                   command=self.run_calculation,
                                   bg="#4CAF50", fg="white",
                                   font=("Arial", 12, "bold"),
                                   relief=tk.RAISED,
                                   padx=20, pady=10)
        self.calc_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Botão Cancelar (inicialmente desabilitado)
        self.cancel_button = tk.Button(calc_button_frame, text="CANCEL", 
                                     command=self.cancel_calculation,
                                     bg="#f44336", fg="white",
                                     font=("Arial", 12, "bold"),
                                     relief=tk.RAISED,
                                     padx=20, pady=10,
                                     state=tk.DISABLED)
        self.cancel_button.pack(fill=tk.X, padx=5, pady=5)
    
    def prepare_result_frame(self):
        """Prepara o frame de resultados com widgets vazios."""
        # Rótulo para mostrar o status do cálculo
        self.calc_status_label = ttk.Label(self.result_frame, text="Waiting for calculation...")
        self.calc_status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Barra de progresso
        self.progress_frame = ttk.Frame(self.result_frame)
        self.progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, 
                                           length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_text = ttk.Label(self.progress_frame, text="0%")
        self.progress_text.pack(padx=5, pady=2)
        
        # Status detalhado do progresso
        self.progress_details = ttk.Label(self.progress_frame, text="")
        self.progress_details.pack(padx=5, pady=2)
        
        # Frame para resultados numéricos
        nums_frame = ttk.Frame(self.result_frame)
        nums_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Rótulos para resultados numéricos
        self.mult_label = ttk.Label(nums_frame, text="Multiplier: -")
        self.mult_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.cost_label = ttk.Label(nums_frame, text="Total Cost: -")
        self.cost_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.profit_label = ttk.Label(nums_frame, text="Estimated Profit: -")
        self.profit_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Adicionar rótulo para Sell Price
        self.sell_price_label = ttk.Label(nums_frame, text="Sell Price: -")
        self.sell_price_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Frame para lista de itens
        items_list_frame = ttk.LabelFrame(self.result_frame, text="Best Combination")
        items_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox para exibir itens na combinação
        self.items_listbox = tk.Listbox(items_list_frame)
        self.items_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para efeitos
        effects_frame = ttk.LabelFrame(self.result_frame, text="Active Effects")
        effects_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox para exibir efeitos
        self.effects_listbox = tk.Listbox(effects_frame)
        self.effects_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_raw_material(self, event=None):
        """Atualiza as informações da matéria-prima selecionada."""
        selected = self.raw_material_var.get()
        if selected in RAW_MATERIALS:
            material_info = RAW_MATERIALS[selected]
            effect_name = material_info["effect"]
            base_value = material_info["value"]
            
            # Verifica se o efeito é "None" ou existe nos multiplicadores
            if effect_name == "None":
                effect_value = 0
                info_text = f"Effect: None\nBase Value: ${base_value:.2f}"
            else:
                effect_value = effect_multipliers[effect_name]
                info_text = f"Effect: {effect_name} (+{effect_value:.2f})\nBase Value: ${base_value:.2f}"
            
            self.raw_mat_info_label.config(text=info_text)
            
            # Atualiza a imagem se disponível
            img_path = material_info["img_path"]
            if img_path and os.path.exists(img_path):
                self.load_image(self.raw_mat_img_label, img_path, size=(100, 100))
            else:
                self.raw_mat_img_label.config(image="")
    
    def update_combo_size(self, event=None):
        """Atualiza o rótulo de quantidade de itens."""
        count = self.combo_size_var.get()
        self.items_count_label.config(text=f"Quantity: {count}")
    
    def load_image(self, label, path, size=(50, 50)):
        """Carrega uma imagem e a exibe em um label."""
        try:
            img_path = resource_path(path)
            print(f"Tentando carregar imagem de: {img_path}")  # Linha de depuração
            img = Image.open(img_path)
            img = img.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo  # Mantém uma referência
            return photo
        except Exception as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return None
        
    def run_calculation(self):
        """Executa o cálculo em uma thread separada para evitar congelar a UI."""
        if self.is_calculating:
            return  # Evita múltiplos cliques
        
        # Marca como calculando e atualiza a UI
        self.is_calculating = True
        self.calc_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Limpa resultados anteriores
        self.calc_status_label.config(text="Starting calculation...")
        self.progress_bar['value'] = 0
        self.progress_text.config(text="0%")
        self.progress_details.config(text="Preparing...")
        self.items_listbox.delete(0, tk.END)
        self.effects_listbox.delete(0, tk.END)
        self.mult_label.config(text="Multiplier: -")
        self.cost_label.config(text="Total Cost: -")
        self.profit_label.config(text="Estimated Profit: -")
        self.sell_price_label.config(text="Sell Price: -")
        
        # Obtém parâmetros
        selected_material = self.raw_material_var.get()
        material_info = RAW_MATERIALS[selected_material]
        
        # Verifica se o efeito é "None"
        if material_info["effect"] == "None":
            initial_effects = {}  # Sem efeitos iniciais
        else:
            initial_effects = {material_info["effect"]: effect_multipliers[material_info["effect"]]}
        
        base_value = material_info["value"]
        combo_size = self.combo_size_var.get()
        
        # Obtém itens banidos
        banned_items = [item for item, var in self.banned_items_vars.items() if var.get()]
        
        # Atualiza status inicial
        self.calc_status_label.config(text=f"Calculating with {selected_material}...")
        self.progress_details.config(text=f"Searching for the best combination of {combo_size} items...")
        self.update()  # Força atualização da UI antes de iniciar o cálculo
        
        # Inicia o cálculo em uma thread separada
        self.calculation_thread = threading.Thread(
            target=self.perform_calculation, 
            args=(initial_effects, banned_items, combo_size, base_value)
        )
        self.calculation_thread.daemon = True  # Termina a thread quando o programa principal termina
        self.calculation_thread.start()
    
    def cancel_calculation(self):
        """Cancela o cálculo em andamento."""
        if self.is_calculating:
            # Adiciona um sinal de cancelamento à fila de progresso
            self.progress_queue.put(("cancel", None))
            self.calc_status_label.config(text="Canceling calculation...")
            self.progress_details.config(text="Please wait, finishing operations...")
    
    def monitor_progress_queue(self):
        """Monitora a fila de progresso e atualiza a UI."""
        try:
            # Verifica se há novos itens na fila
            while not self.progress_queue.empty():
                msg_type, data = self.progress_queue.get_nowait()
                
                if msg_type == "progress":
                    progress, details = data
                    self.progress_bar['value'] = progress
                    self.progress_text.config(text=f"{progress}%")
                    if details:
                        self.progress_details.config(text=details)
                
                elif msg_type == "status":
                    self.calc_status_label.config(text=data)
                
                elif msg_type == "complete":
                    self.is_calculating = False
                    self.calc_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    self.progress_bar['value'] = 100
                    self.progress_text.config(text="100%")
                    self.calc_status_label.config(text="Calculation completed!")
                    # Atualiza resultados
                    self.update_results()
                
                elif msg_type == "error":
                    self.is_calculating = False
                    self.calc_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    self.calc_status_label.config(text=f"Error: {data}")
                    self.progress_details.config(text="The calculation was interrupted due to an error.")
                
                elif msg_type == "cancel":
                    self.is_calculating = False
                    self.calc_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    self.calc_status_label.config(text="Calculation canceled by the user.")
                    self.progress_details.config(text="")
        
        except Exception as e:
            print(f"Error monitoring progress queue: {e}")
        
        # Agenda a próxima verificação
        self.after(100, self.monitor_progress_queue)
    
    def perform_calculation(self, initial_effects, banned_items, combo_size, base_value):
        """Executa o cálculo e atualiza a UI com os resultados."""
        try:
            # Informa o início do cálculo
            self.progress_queue.put(("status", "Initializing optimizer..."))
            self.progress_queue.put(("progress", (5, "Preparing calculation environment")))
            
            print("Starting calculation with the following parameters:")
            print(f"Initial effects: {initial_effects}")
            print(f"Banned items: {banned_items}")
            print(f"Combination size: {combo_size}")
            print(f"Base value: {base_value}")
            
            # Executa a função de otimização modificada com feedback de progresso
            result = optimize(
                initial_effects=initial_effects,
                banned_items=banned_items,
                time_limit_seconds=60,  # Ajuste conforme necessário
                combo_size=combo_size,
                max_perms_to_test=5000,  # Ajuste conforme necessário
                base_value=base_value,
                progress_callback=self.update_progress,
                # Não exibe saída no console
                verbose=False
            )
            
            # Verifica se o cálculo foi cancelado
            if not self.is_calculating:
                return
            
            # Extrai resultados
            self.result_combination, self.result_multiplier, self.result_effects, self.result_cost, self.result_profit = result
            
            # Calcula o Sell Price (base_value * multiplier)
            self.result_sell_price = base_value * self.result_multiplier
            
            # Informa que o cálculo está completo
            self.progress_queue.put(("progress", (95, "Finalizing and processing results")))
            time.sleep(0.5)  # Pequena pausa para visualização
            self.progress_queue.put(("complete", None))
            
        except Exception as e:
            print(f"Error during calculation: {e}")
            self.progress_queue.put(("error", str(e)))
    
    def update_progress(self, percentage, message=None):
        """Callback para atualizar o progresso do cálculo."""
        # Verifica se o cálculo foi cancelado
        if not self.is_calculating:
            return False  # Retorna False para indicar que deve parar
        
        # Envia progresso para a fila
        self.progress_queue.put(("progress", (percentage, message)))
        return True  # Continua o cálculo
    
    def update_results(self):
        """Atualiza a UI com os resultados do cálculo."""
        # Atualiza rótulos numéricos
        self.mult_label.config(text=f"Multiplier: {self.result_multiplier:.2f}")
        self.cost_label.config(text=f"Total Cost: ${self.result_cost:.2f}")
        self.profit_label.config(text=f"Estimated Profit: ${round(self.result_profit)}")
        self.sell_price_label.config(text=f"Sell Price: ${round(self.result_sell_price)}")
        
        # Atualiza listbox de itens
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.result_combination, 1):
            self.items_listbox.insert(tk.END, f"{i}. {item} (${item_prices[item]})")
        
        # Atualiza listbox de efeitos
        self.effects_listbox.delete(0, tk.END)
        for effect, value in sorted(self.result_effects.items(), key=lambda x: x[1], reverse=True):
            self.effects_listbox.insert(tk.END, f"{effect}: +{value:.2f}")
        
        # Atualiza status final
        self.progress_details.config(text=f"Analyzed {len(self.result_combination)} item combinations.")

    def set_image_for_raw_material(self, raw_material_name, image_path):
        """Define a imagem para uma matéria-prima específica."""
        if raw_material_name in RAW_MATERIALS:
            RAW_MATERIALS[raw_material_name]["img_path"] = image_path
            # Se esta matéria-prima estiver selecionada, atualiza a imagem
            if self.raw_material_var.get() == raw_material_name:
                self.update_raw_material()