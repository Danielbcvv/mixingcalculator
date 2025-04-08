import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import sys
import threading
import time
import queue
from typing import Dict, List, Set, Tuple

# Importing the original file (assuming it's in the same directory)
# You may need to adjust the path if necessary
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from schedule1 import optimize, items, effect_multipliers, item_prices
except ImportError:
    print("Error importing the main module. Ensure the 'schedule1.py' file is in the same directory.")
    sys.exit(1)

# Modification in raw materials configuration
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
        
        # Variables
        self.raw_material_var = tk.StringVar()
        self.combo_size_var = tk.IntVar(value=4)
        self.banned_items_vars = {}
        self.raw_material_img = None
        self.item_images = {}
        
        # Initialize dictionaries to store results
        self.result_combination = []
        self.result_multiplier = 0.0
        self.result_effects = {}
        self.result_cost = 0.0
        self.result_profit = 0.0
        
        # Queue for communication between threads
        self.progress_queue = queue.Queue()
        self.is_calculating = False
        
        self.create_widgets()
        
        # Start monitoring the progress queue
        self.monitor_progress_queue()
    
    def create_widgets(self):
        # Main frame divided into two columns
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column (input parameters)
        input_frame = ttk.LabelFrame(main_frame, text="Parameters")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right column (results)
        self.result_frame = ttk.LabelFrame(main_frame, text="Results")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Raw Material Section
        raw_mat_frame = ttk.LabelFrame(input_frame, text="Raw Material")
        raw_mat_frame.pack(fill=tk.X, padx=5, pady=5)
        
        raw_mat_dropdown = ttk.Combobox(raw_mat_frame, textvariable=self.raw_material_var, 
                                         values=list(RAW_MATERIALS.keys()), state="readonly")
        raw_mat_dropdown.pack(fill=tk.X, padx=5, pady=5)
        raw_mat_dropdown.bind("<<ComboboxSelected>>", self.update_raw_material)
        raw_mat_dropdown.current(0)  # Selects the first item by default
        
        self.raw_mat_img_label = ttk.Label(raw_mat_frame)
        self.raw_mat_img_label.pack(padx=5, pady=5)
        
        self.raw_mat_info_label = ttk.Label(raw_mat_frame, text="")
        self.raw_mat_info_label.pack(padx=5, pady=5)
        
        # Item Quantity Section
        items_count_frame = ttk.LabelFrame(input_frame, text="Item Quantity")
        items_count_frame.pack(fill=tk.X, padx=5, pady=5)
        
        items_scale = ttk.Scale(items_count_frame, from_=1, to=8, orient=tk.HORIZONTAL,
                               variable=self.combo_size_var, command=self.update_combo_size)
        items_scale.pack(fill=tk.X, padx=5, pady=5)
        
        self.items_count_label = ttk.Label(items_count_frame, text="Quantity: 4")
        self.items_count_label.pack(padx=5, pady=5)
        
        # Banned Items Section
        banned_items_frame = ttk.LabelFrame(input_frame, text="Banned Items")
        banned_items_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas with scrollbar for banned items checkboxes
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
        
        # Add checkboxes for each item
        for i, item_name in enumerate(sorted(items.keys())):
            var = tk.BooleanVar()
            self.banned_items_vars[item_name] = var
            
            item_frame = ttk.Frame(scrollable_frame)
            item_frame.pack(fill=tk.X, padx=2, pady=2)
            
            check = ttk.Checkbutton(item_frame, text=item_name, variable=var)
            check.pack(side=tk.LEFT)
            
            # Space for item image (optional)
            img_label = ttk.Label(item_frame)
            img_label.pack(side=tk.RIGHT)
            self.item_images[item_name] = {"label": img_label, "img": None}
        
        # Calculate Button with highlighted style
        calc_button_frame = ttk.Frame(input_frame)
        calc_button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Calculate Button with better highlight
        self.calc_button = tk.Button(calc_button_frame, text="CALCULATE", 
                               command=self.run_calculation,
                               bg="#4CAF50", fg="white",
                               font=("Arial", 12, "bold"),
                               relief=tk.RAISED,
                               padx=20, pady=10)
        self.calc_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Cancel Button (initially disabled)
        self.cancel_button = tk.Button(calc_button_frame, text="CANCEL", 
                                     command=self.cancel_calculation,
                                     bg="#f44336", fg="white",
                                     font=("Arial", 12, "bold"),
                                     relief=tk.RAISED,
                                     padx=20, pady=10,
                                     state=tk.DISABLED)
        self.cancel_button.pack(fill=tk.X, padx=5, pady=5)
        
        # Initialize raw material display
        self.update_raw_material()
        
        # Prepare the results frame
        self.prepare_result_frame()
    
    def prepare_result_frame(self):
        """Prepares the results frame with empty widgets"""
        # Label to show calculation status
        self.calc_status_label = ttk.Label(self.result_frame, text="Waiting for calculation...")
        self.calc_status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Progress bar
        self.progress_frame = ttk.Frame(self.result_frame)
        self.progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, 
                                           length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_text = ttk.Label(self.progress_frame, text="0%")
        self.progress_text.pack(padx=5, pady=2)
        
        # Detailed progress status
        self.progress_details = ttk.Label(self.progress_frame, text="")
        self.progress_details.pack(padx=5, pady=2)
        
        # Frame for numerical results
        nums_frame = ttk.Frame(self.result_frame)
        nums_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Labels for numerical results
        self.mult_label = ttk.Label(nums_frame, text="Multiplier: -")
        self.mult_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.cost_label = ttk.Label(nums_frame, text="Total Cost: -")
        self.cost_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.profit_label = ttk.Label(nums_frame, text="Estimated Profit: -")
        self.profit_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Frame for item list
        items_list_frame = ttk.LabelFrame(self.result_frame, text="Best Combination")
        items_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox to display items in the combination
        self.items_listbox = tk.Listbox(items_list_frame)
        self.items_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame for effects
        effects_frame = ttk.LabelFrame(self.result_frame, text="Active Effects")
        effects_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox to display effects
        self.effects_listbox = tk.Listbox(effects_frame)
        self.effects_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_raw_material(self, event=None):
        """Updates the information of the selected raw material"""
        selected = self.raw_material_var.get()
        if selected in RAW_MATERIALS:
            material_info = RAW_MATERIALS[selected]
            effect_name = material_info["effect"]
            base_value = material_info["value"]
            
            # Check if the effect is "None" or exists in multipliers
            if effect_name == "None":
                effect_value = 0
                info_text = f"Effect: None\nBase Value: ${base_value:.2f}"
            else:
                effect_value = effect_multipliers[effect_name]
                info_text = f"Effect: {effect_name} (+{effect_value:.2f})\nBase Value: ${base_value:.2f}"
            
            self.raw_mat_info_label.config(text=info_text)
            
            # Update the image if available
            if material_info["img_path"] and os.path.exists(material_info["img_path"]):
                self.load_image(self.raw_mat_img_label, material_info["img_path"], size=(100, 100))
            else:
                self.raw_mat_img_label.config(image="")
    
    def update_combo_size(self, event=None):
        """Updates the item quantity label"""
        count = self.combo_size_var.get()
        self.items_count_label.config(text=f"Quantity: {count}")
    
    def load_image(self, label, path, size=(50, 50)):
        """Loads an image and displays it in the specified label"""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo  # Keeps a reference
            return photo
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def run_calculation(self):
        """Runs the calculation in a separate thread to avoid freezing the UI"""
        if self.is_calculating:
            return  # Avoids multiple clicks
        
        # Mark as calculating and update the UI
        self.is_calculating = True
        self.calc_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Clear previous results
        self.calc_status_label.config(text="Starting calculation...")
        self.progress_bar['value'] = 0
        self.progress_text.config(text="0%")
        self.progress_details.config(text="Preparing...")
        self.items_listbox.delete(0, tk.END)
        self.effects_listbox.delete(0, tk.END)
        self.mult_label.config(text="Multiplier: -")
        self.cost_label.config(text="Total Cost: -")
        self.profit_label.config(text="Estimated Profit: -")
        
        # Get parameters
        selected_material = self.raw_material_var.get()
        material_info = RAW_MATERIALS[selected_material]
        
        # Check if the effect is "None"
        if material_info["effect"] == "None":
            initial_effects = {}  # No initial effects
        else:
            initial_effects = {material_info["effect"]: effect_multipliers[material_info["effect"]]}
        
        base_value = material_info["value"]
        combo_size = self.combo_size_var.get()
        
        # Get banned items
        banned_items = [item for item, var in self.banned_items_vars.items() if var.get()]
        
        # Update initial status
        self.calc_status_label.config(text=f"Calculating with {selected_material}...")
        self.progress_details.config(text=f"Searching for the best combination of {combo_size} items...")
        self.update()  # Force UI update before starting the calculation
        
        # Start the calculation in a separate thread
        self.calculation_thread = threading.Thread(
            target=self.perform_calculation, 
            args=(initial_effects, banned_items, combo_size, base_value)
        )
        self.calculation_thread.daemon = True  # Terminates the thread when the main program ends
        self.calculation_thread.start()
    
    def cancel_calculation(self):
        """Cancels the ongoing calculation"""
        if self.is_calculating:
            # Add a cancellation signal to the progress queue
            self.progress_queue.put(("cancel", None))
            self.calc_status_label.config(text="Canceling calculation...")
            self.progress_details.config(text="Please wait, finishing operations...")
    
    def monitor_progress_queue(self):
        """Monitors the progress queue and updates the UI"""
        try:
            # Check if there are new items in the queue
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
                    # Update results
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
        
        # Schedule the next check
        self.after(100, self.monitor_progress_queue)
    
    def perform_calculation(self, initial_effects, banned_items, combo_size, base_value):
        """Performs the calculation and updates the UI with the results"""
        try:
            # Inform the start of the calculation
            self.progress_queue.put(("status", "Initializing optimizer..."))
            self.progress_queue.put(("progress", (5, "Preparing calculation environment")))
            
            print("Starting calculation with the following parameters:")
            print(f"Initial effects: {initial_effects}")
            print(f"Banned items: {banned_items}")
            print(f"Combination size: {combo_size}")
            print(f"Base value: {base_value}")
            
            # Execute the modified optimization function with progress feedback
            result = optimize_with_progress(
                initial_effects=initial_effects,
                banned_items=banned_items,
                time_limit_seconds=60,  # Adjust as needed
                combo_size=combo_size,
                max_perms_to_test=5000,  # Adjust as needed
                base_value=base_value,
                progress_callback=self.update_progress,
                # Do not display console output
                verbose=False
            )
            
            # Check if the calculation was canceled
            if not self.is_calculating:
                return
            
            # Extract results
            self.result_combination, self.result_multiplier, self.result_effects, self.result_cost, self.result_profit = result
            
            # Inform that the calculation is complete
            self.progress_queue.put(("progress", (95, "Finalizing and processing results")))
            time.sleep(0.5)  # Small pause for visualization
            self.progress_queue.put(("complete", None))
            
        except Exception as e:
            print(f"Error during calculation: {e}")
            self.progress_queue.put(("error", str(e)))
    
    def update_progress(self, percentage, message=None):
        """Callback to update calculation progress"""
        # Check if the calculation was canceled
        if not self.is_calculating:
            return False  # Return False to indicate it should stop
        
        # Send progress to the queue
        self.progress_queue.put(("progress", (percentage, message)))
        return True  # Continue the calculation
    
    def update_results(self):
        """Updates the UI with the calculation results"""
        # Update numerical labels
        self.mult_label.config(text=f"Multiplier: {self.result_multiplier:.2f}")
        self.cost_label.config(text=f"Total Cost: ${self.result_cost:.2f}")
        self.profit_label.config(text=f"Estimated Profit: ${self.result_profit:.2f}")
        
        # Update items listbox
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.result_combination, 1):
            self.items_listbox.insert(tk.END, f"{i}. {item} (${item_prices[item]})")
        
        # Update effects listbox
        self.effects_listbox.delete(0, tk.END)
        for effect, value in sorted(self.result_effects.items(), key=lambda x: x[1], reverse=True):
            self.effects_listbox.insert(tk.END, f"{effect}: +{value:.2f}")
        
        # Update final status
        self.progress_details.config(text=f"Analyzed {len(self.result_combination)} item combinations.")

    def set_image_for_raw_material(self, raw_material_name, image_path):
        """Sets the image for a specific raw material"""
        if raw_material_name in RAW_MATERIALS:
            RAW_MATERIALS[raw_material_name]["img_path"] = image_path
            # If this raw material is selected, update the image
            if self.raw_material_var.get() == raw_material_name:
                self.update_raw_material()
    
    def set_image_for_item(self, item_name, image_path):
        """Sets the image for a specific item"""
        if item_name in self.item_images:
            if os.path.exists(image_path):
                photo = self.load_image(self.item_images[item_name]["label"], image_path, size=(30, 30))
                self.item_images[item_name]["img"] = photo

# Modified version of the optimize function with progress feedback
def optimize_with_progress(initial_effects=None, time_limit_seconds=30, combo_size=8, 
                         max_perms_to_test=5000, banned_items=None, cost_weight=0.3, 
                         base_value=100, verbose=True, progress_callback=None):
    """
    Version of the optimize function that provides progress feedback
    and allows cancellation
    """
    # Store the original stdout
    original_stdout = sys.stdout
    
    if not verbose:
        # Redirect to null
        sys.stdout = open(os.devnull, 'w')
    
    try:
        # Implement progress monitoring
        start_time = time.time()
        canceled = False
        
        # Report initial progress
        if progress_callback:
            if not progress_callback(10, "Initializing optimization algorithm"):
                canceled = True
                return [], 0.0, {}, 0.0, 0.0
        
        # Filter banned items
        available_items = {name: props for name, props in items.items() 
                          if banned_items is None or name not in banned_items}
        
        if progress_callback:
            if not progress_callback(15, f"Analyzing {len(available_items)} available items"):
                canceled = True
                return [], 0.0, {}, 0.0, 0.0
        
        # Generate possible combinations (simplified simulation for monitoring)
        total_items = len(available_items)
        total_combinations = min(max_perms_to_test, sum(1 for _ in range(total_items)))
        
        # Simulate progress during the main calculation phase
        if progress_callback:
            progress_updates = [
                (20, "Generating possible combinations"),
                (30, "Calculating effects for each combination"),
                (50, f"Analyzing {total_combinations} possible combinations"),
                (70, "Calculating effect multipliers"),
                (80, "Calculating combination profitability"),
                (90, "Finding the best combination")
            ]
            
            for progress, message in progress_updates:
                # Simulate work being done
                time.sleep(0.5)
                
                # Update progress
                if not progress_callback(progress, message):
                    canceled = True
                    return [], 0.0, {}, 0.0, 0.0
                
                # Check if time limit is exceeded
                if time.time() - start_time > time_limit_seconds:
                    if progress_callback:
                        progress_callback(progress, "Time limit reached, finalizing calculations")
                    break
        
        # Call the original function if not canceled
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
        # Restore original stdout
        if not verbose:
            sys.stdout.close()
            sys.stdout = original_stdout

# Replace the original function with the wrapper
import schedule1
schedule1.optimize = optimize_with_progress

if __name__ == "__main__":
    app = Schedule1Calculator()
    app.mainloop()