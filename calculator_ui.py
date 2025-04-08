import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import sys
import threading
import time
import queue
from typing import Dict, List, Set, Tuple

# Importação do arquivo original (assumindo que está no mesmo diretório)
# Você precisará ajustar o caminho se necessário
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from schedule1 import optimize, items, effect_multipliers, item_prices
except ImportError:
    print("Erro ao importar o módulo principal. Certifique-se de que o arquivo 'schedule1.py' está no mesmo diretório.")
    sys.exit(1)

# Modificação na configuração das matérias-primas
RAW_MATERIALS = {
    "OG Kush": {"effect": "Calming", "value": 39, "img_path": ""},
    "Sour Diesel": {"effect": "Refreshing", "value": 40, "img_path": ""},
    "Green Crack": {"effect": "Energizing", "value": 43, "img_path": ""},
    "Granddaddy Purple": {"effect": "Sedating", "value": 44, "img_path": ""},
    "Meth": {"effect": "None", "value": 70, "img_path": ""},
    "Cocaine": {"effect": "None", "value": 150, "img_path": ""}
}

class Schedule1Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schedule 1 Calculator")
        self.geometry("800x700")
        self.configure(bg="#f0f0f0")
        
        # Variáveis
        self.raw_material_var = tk.StringVar()
        self.combo_size_var = tk.IntVar(value=4)
        self.banned_items_vars = {}
        self.raw_material_img = None
        self.item_images = {}
        
        # Inicializa os dicionários para armazenar os resultados
        self.result_combination = []
        self.result_multiplier = 0.0
        self.result_effects = {}
        self.result_cost = 0.0
        self.result_profit = 0.0
        
        # Fila para comunicação entre threads
        self.progress_queue = queue.Queue()
        self.is_calculating = False
        
        self.create_widgets()
        
        # Iniciar o monitoramento da fila de progresso
        self.monitor_progress_queue()
    
    def create_widgets(self):
        # Frame principal dividido em duas colunas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Coluna esquerda (parâmetros de entrada)
        input_frame = ttk.LabelFrame(main_frame, text="Parâmetros")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Coluna direita (resultados)
        self.result_frame = ttk.LabelFrame(main_frame, text="Resultados")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Seção de Matéria Prima
        raw_mat_frame = ttk.LabelFrame(input_frame, text="Matéria Prima")
        raw_mat_frame.pack(fill=tk.X, padx=5, pady=5)
        
        raw_mat_dropdown = ttk.Combobox(raw_mat_frame, textvariable=self.raw_material_var, 
                                         values=list(RAW_MATERIALS.keys()), state="readonly")
        raw_mat_dropdown.pack(fill=tk.X, padx=5, pady=5)
        raw_mat_dropdown.bind("<<ComboboxSelected>>", self.update_raw_material)
        raw_mat_dropdown.current(0)  # Seleciona o primeiro item por padrão
        
        self.raw_mat_img_label = ttk.Label(raw_mat_frame)
        self.raw_mat_img_label.pack(padx=5, pady=5)
        
        self.raw_mat_info_label = ttk.Label(raw_mat_frame, text="")
        self.raw_mat_info_label.pack(padx=5, pady=5)
        
        # Seção de Quantidade de Itens
        items_count_frame = ttk.LabelFrame(input_frame, text="Quantidade de Itens")
        items_count_frame.pack(fill=tk.X, padx=5, pady=5)
        
        items_scale = ttk.Scale(items_count_frame, from_=1, to=8, orient=tk.HORIZONTAL,
                               variable=self.combo_size_var, command=self.update_combo_size)
        items_scale.pack(fill=tk.X, padx=5, pady=5)
        
        self.items_count_label = ttk.Label(items_count_frame, text="Quantidade: 4")
        self.items_count_label.pack(padx=5, pady=5)
        
        # Seção de Itens Banidos
        banned_items_frame = ttk.LabelFrame(input_frame, text="Itens Banidos")
        banned_items_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Cria um canvas com scrollbar para os checkboxes de itens banidos
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
        
        # Adiciona checkboxes para cada item
        for i, item_name in enumerate(sorted(items.keys())):
            var = tk.BooleanVar()
            self.banned_items_vars[item_name] = var
            
            item_frame = ttk.Frame(scrollable_frame)
            item_frame.pack(fill=tk.X, padx=2, pady=2)
            
            check = ttk.Checkbutton(item_frame, text=item_name, variable=var)
            check.pack(side=tk.LEFT)
            
            # Espaço para imagem do item (opcional)
            img_label = ttk.Label(item_frame)
            img_label.pack(side=tk.RIGHT)
            self.item_images[item_name] = {"label": img_label, "img": None}
        
        # Botão de Calcular com estilo destacado
        calc_button_frame = ttk.Frame(input_frame)
        calc_button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Botão de Calcular com melhor destaque
        self.calc_button = tk.Button(calc_button_frame, text="CALCULAR", 
                               command=self.run_calculation,
                               bg="#4CAF50", fg="white",
                               font=("Arial", 12, "bold"),
                               relief=tk.RAISED,
                               padx=20, pady=10)
        self.calc_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Botão para cancelar o cálculo (inicialmente desativado)
        self.cancel_button = tk.Button(calc_button_frame, text="CANCELAR", 
                                     command=self.cancel_calculation,
                                     bg="#f44336", fg="white",
                                     font=("Arial", 12, "bold"),
                                     relief=tk.RAISED,
                                     padx=20, pady=10,
                                     state=tk.DISABLED)
        self.cancel_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Inicializa a exibição da matéria-prima
        self.update_raw_material()
        
        # Prepara o frame de resultados
        self.prepare_result_frame()
    
    def prepare_result_frame(self):
        """Prepara o frame de resultados com widgets vazios"""
        # Rótulo para mostrar o status do cálculo
        self.calc_status_label = ttk.Label(self.result_frame, text="Aguardando cálculo...")
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
        
        # Frame para os resultados numéricos
        nums_frame = ttk.Frame(self.result_frame)
        nums_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Rótulos para os resultados numéricos
        self.mult_label = ttk.Label(nums_frame, text="Multiplicador: -")
        self.mult_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.cost_label = ttk.Label(nums_frame, text="Custo Total: -")
        self.cost_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.profit_label = ttk.Label(nums_frame, text="Lucro Estimado: -")
        self.profit_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Frame para a lista de itens
        items_list_frame = ttk.LabelFrame(self.result_frame, text="Melhor Combinação")
        items_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox para mostrar os itens na combinação
        self.items_listbox = tk.Listbox(items_list_frame)
        self.items_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para os efeitos
        effects_frame = ttk.LabelFrame(self.result_frame, text="Efeitos Ativos")
        effects_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox para mostrar os efeitos
        self.effects_listbox = tk.Listbox(effects_frame)
        self.effects_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_raw_material(self, event=None):
        """Atualiza as informações da matéria-prima selecionada"""
        selected = self.raw_material_var.get()
        if selected in RAW_MATERIALS:
            material_info = RAW_MATERIALS[selected]
            effect_name = material_info["effect"]
            base_value = material_info["value"]
            
            # Verifica se o efeito é "None" ou se existe nos multiplicadores
            if effect_name == "None":
                effect_value = 0
                info_text = f"Efeito: Nenhum\nValor Base: ${base_value:.2f}"
            else:
                effect_value = effect_multipliers[effect_name]
                info_text = f"Efeito: {effect_name} (+{effect_value:.2f})\nValor Base: ${base_value:.2f}"
            
            self.raw_mat_info_label.config(text=info_text)
            
            # Atualiza a imagem se disponível
            if material_info["img_path"] and os.path.exists(material_info["img_path"]):
                self.load_image(self.raw_mat_img_label, material_info["img_path"], size=(100, 100))
            else:
                self.raw_mat_img_label.config(image="")
    
    def update_combo_size(self, event=None):
        """Atualiza o rótulo da quantidade de itens"""
        count = self.combo_size_var.get()
        self.items_count_label.config(text=f"Quantidade: {count}")
    
    def load_image(self, label, path, size=(50, 50)):
        """Carrega uma imagem e a exibe no label especificado"""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo  # Mantém uma referência
            return photo
        except Exception as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return None
    
    def run_calculation(self):
        """Executa o cálculo em uma thread separada para não congelar a UI"""
        if self.is_calculating:
            return  # Evita múltiplos cliques
        
        # Marca como calculando e atualiza a UI
        self.is_calculating = True
        self.calc_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Limpa os resultados anteriores
        self.calc_status_label.config(text="Iniciando cálculo...")
        self.progress_bar['value'] = 0
        self.progress_text.config(text="0%")
        self.progress_details.config(text="Preparando...")
        self.items_listbox.delete(0, tk.END)
        self.effects_listbox.delete(0, tk.END)
        self.mult_label.config(text="Multiplicador: -")
        self.cost_label.config(text="Custo Total: -")
        self.profit_label.config(text="Lucro Estimado: -")
        
        # Obtém os parâmetros
        selected_material = self.raw_material_var.get()
        material_info = RAW_MATERIALS[selected_material]
        
        # Verifica se o efeito é "None"
        if material_info["effect"] == "None":
            initial_effects = {}  # Sem efeitos iniciais
        else:
            initial_effects = {material_info["effect"]: effect_multipliers[material_info["effect"]]}
        
        base_value = material_info["value"]
        combo_size = self.combo_size_var.get()
        
        # Obtém os itens banidos
        banned_items = [item for item, var in self.banned_items_vars.items() if var.get()]
        
        # Atualiza o status inicial
        self.calc_status_label.config(text=f"Calculando com {selected_material}...")
        self.progress_details.config(text=f"Buscando melhor combinação de {combo_size} itens...")
        self.update()  # Força atualização da interface antes de iniciar o cálculo
        
        # Inicia o cálculo em uma thread separada
        self.calculation_thread = threading.Thread(
            target=self.perform_calculation, 
            args=(initial_effects, banned_items, combo_size, base_value)
        )
        self.calculation_thread.daemon = True  # Encerra a thread quando o programa principal encerrar
        self.calculation_thread.start()
    
    def cancel_calculation(self):
        """Cancela o cálculo em andamento"""
        if self.is_calculating:
            # Adiciona um sinal de cancelamento à fila de progresso
            self.progress_queue.put(("cancel", None))
            self.calc_status_label.config(text="Cancelando cálculo...")
            self.progress_details.config(text="Aguarde, finalizando operações...")
    
    def monitor_progress_queue(self):
        """Monitora a fila de progresso e atualiza a UI"""
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
                    self.calc_status_label.config(text="Cálculo concluído!")
                    # Atualiza os resultados
                    self.update_results()
                
                elif msg_type == "error":
                    self.is_calculating = False
                    self.calc_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    self.calc_status_label.config(text=f"Erro: {data}")
                    self.progress_details.config(text="O cálculo foi interrompido devido a um erro.")
                
                elif msg_type == "cancel":
                    self.is_calculating = False
                    self.calc_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    self.calc_status_label.config(text="Cálculo cancelado pelo usuário.")
                    self.progress_details.config(text="")
        
        except Exception as e:
            print(f"Erro ao monitorar fila de progresso: {e}")
        
        # Agenda a próxima verificação
        self.after(100, self.monitor_progress_queue)
    
    def perform_calculation(self, initial_effects, banned_items, combo_size, base_value):
        """Realiza o cálculo e atualiza a UI com os resultados"""
        try:
            # Informa o início do cálculo
            self.progress_queue.put(("status", "Inicializando otimizador..."))
            self.progress_queue.put(("progress", (5, "Preparando ambiente de cálculo")))
            
            print("Iniciando cálculo com os seguintes parâmetros:")
            print(f"Efeitos iniciais: {initial_effects}")
            print(f"Itens banidos: {banned_items}")
            print(f"Tamanho da combinação: {combo_size}")
            print(f"Valor base: {base_value}")
            
            # Executa a função de otimização modificada com feedback de progresso
            result = optimize_with_progress(
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
            
            # Extrai os resultados
            self.result_combination, self.result_multiplier, self.result_effects, self.result_cost, self.result_profit = result
            
            # Informa que o cálculo foi concluído
            self.progress_queue.put(("progress", (95, "Finalizando e processando resultados")))
            time.sleep(0.5)  # Pequena pausa para visualização
            self.progress_queue.put(("complete", None))
            
        except Exception as e:
            print(f"Erro durante o cálculo: {e}")
            self.progress_queue.put(("error", str(e)))
    
    def update_progress(self, percentage, message=None):
        """Callback para atualizar o progresso do cálculo"""
        # Verifica se o cálculo foi cancelado
        if not self.is_calculating:
            return False  # Retorna False para indicar que deve parar
        
        # Envia o progresso para a fila
        self.progress_queue.put(("progress", (percentage, message)))
        return True  # Continua o cálculo
    
    def update_results(self):
        """Atualiza a UI com os resultados do cálculo"""
        # Atualiza os rótulos numéricos
        self.mult_label.config(text=f"Multiplicador: {self.result_multiplier:.2f}")
        self.cost_label.config(text=f"Custo Total: ${self.result_cost:.2f}")
        self.profit_label.config(text=f"Lucro Estimado: ${self.result_profit:.2f}")
        
        # Atualiza a listbox de itens
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.result_combination, 1):
            self.items_listbox.insert(tk.END, f"{i}. {item} (${item_prices[item]})")
        
        # Atualiza a listbox de efeitos
        self.effects_listbox.delete(0, tk.END)
        for effect, value in sorted(self.result_effects.items(), key=lambda x: x[1], reverse=True):
            self.effects_listbox.insert(tk.END, f"{effect}: +{value:.2f}")
        
        # Atualiza o status final
        self.progress_details.config(text=f"Analisadas {len(self.result_combination)} combinações de itens.")

    def set_image_for_raw_material(self, raw_material_name, image_path):
        """Define a imagem para uma matéria-prima específica"""
        if raw_material_name in RAW_MATERIALS:
            RAW_MATERIALS[raw_material_name]["img_path"] = image_path
            # Se esta matéria-prima estiver selecionada, atualiza a imagem
            if self.raw_material_var.get() == raw_material_name:
                self.update_raw_material()
    
    def set_image_for_item(self, item_name, image_path):
        """Define a imagem para um item específico"""
        if item_name in self.item_images:
            if os.path.exists(image_path):
                photo = self.load_image(self.item_images[item_name]["label"], image_path, size=(30, 30))
                self.item_images[item_name]["img"] = photo

# Versão modificada da função optimize com feedback de progresso
def optimize_with_progress(initial_effects=None, time_limit_seconds=30, combo_size=8, 
                         max_perms_to_test=5000, banned_items=None, cost_weight=0.3, 
                         base_value=100, verbose=True, progress_callback=None):
    """
    Versão da função optimize que fornece feedback sobre o progresso
    e permite cancelamento
    """
    # Armazena o stdout original
    original_stdout = sys.stdout
    
    if not verbose:
        # Redireciona para o vazio
        sys.stdout = open(os.devnull, 'w')
    
    try:
        # Implementa monitoramento de progresso
        start_time = time.time()
        canceled = False
        
        # Reporta progresso inicial
        if progress_callback:
            if not progress_callback(10, "Inicializando algoritmo de otimização"):
                canceled = True
                return [], 0.0, {}, 0.0, 0.0
        
        # Filtra itens banidos
        available_items = {name: props for name, props in items.items() 
                          if banned_items is None or name not in banned_items}
        
        if progress_callback:
            if not progress_callback(15, f"Analisando {len(available_items)} itens disponíveis"):
                canceled = True
                return [], 0.0, {}, 0.0, 0.0
        
        # Gera combinações possíveis (simulação simplificada para o monitoramento)
        total_items = len(available_items)
        total_combinations = min(max_perms_to_test, sum(1 for _ in range(total_items)))
        
        # Simula o progresso durante a fase principal de cálculo
        if progress_callback:
            progress_updates = [
                (20, "Gerando combinações possíveis"),
                (30, "Calculando efeitos para cada combinação"),
                (50, f"Analisando {total_combinations} combinações possíveis"),
                (70, "Calculando multiplicadores de efeito"),
                (80, "Calculando lucratividade das combinações"),
                (90, "Encontrando a melhor combinação")
            ]
            
            for progress, message in progress_updates:
                # Simula trabalho sendo feito
                time.sleep(0.5)
                
                # Atualiza o progresso
                if not progress_callback(progress, message):
                    canceled = True
                    return [], 0.0, {}, 0.0, 0.0
                
                # Verifica se ultrapassou o tempo limite
                if time.time() - start_time > time_limit_seconds:
                    if progress_callback:
                        progress_callback(progress, "Tempo limite atingido, finalizando cálculos")
                    break
        
        # Chama a função original se não cancelado
        if not canceled:
            result = optimize(
                initial_effects=initial_effects,
                time_limit_seconds=max(1, time_limit_seconds - (time.time() - start_time)),
                combo_size=combo_size,
                max_perms_to_test=max_perms_to_test,
                banned_items=banned_items,
                cost_weight=cost_weight,
                base_value=base_value
            )
            return result
        else:
            return [], 0.0, {}, 0.0, 0.0
        
    finally:
        # Restaura o stdout original
        if not verbose:
            sys.stdout.close()
            sys.stdout = original_stdout

# Substituir a função original pela wrapper
import schedule1
schedule1.optimize = optimize_with_progress

if __name__ == "__main__":
    app = Schedule1Calculator()
    app.mainloop()