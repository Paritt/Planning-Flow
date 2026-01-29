import tkinter as tk
from tkinter import ttk

class Boolean_Window:
    """Boolean operation window for ROI algebra."""
    def __init__(self, parent, designer=None, use_extended_list=False, callback=None, preload_data=None):
        self.designer = designer
        self.callback = callback
        self.boolean_data = preload_data
        self.boolean_window = tk.Toplevel(parent)
        self.boolean_window.title("ROI Algebra")
        self.boolean_window.geometry("1050x350")
        
        theFrame = tk.Frame(self.boolean_window)
        theFrame.pack(pady=5)
        
        # Frame for A and B
        frame_a_b = tk.LabelFrame(theFrame, text="ROI AB Operation", padx=10, pady=10)
        frame_a_b.grid(row=0, column=0, padx=5)

        # ROI A
        frame_a = tk.LabelFrame(frame_a_b, text="ROI A", padx=10, pady=10)
        frame_a.grid(row=0, column=0, padx=5)
        tk.Label(frame_a, text="ROI A Name").grid(row=0, column=0)
        self.roi_a = tk.StringVar()
        # Get ROI list from designer if available (extended list includes Match ROI + Condition ROI)
        if self.designer:
            roi_list = self.designer.get_extended_roi_list() if use_extended_list else self.designer.get_roi_list()
        else:
            roi_list = ['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External']
        roi_a_combo = ttk.Combobox(frame_a, textvariable=self.roi_a,
                                values=roi_list, state="readonly")
        roi_a_combo.grid(row=0, column=1)
        
        margin_label_a = tk.Label(frame_a, text="Margin")
        margin_label_a.grid(row=1, column=0)
        self.selected_value_a = tk.IntVar()
        self.selected_value_a.set(1)
        expand_a = tk.Radiobutton(frame_a, text="Expand", variable=self.selected_value_a, value=1)
        expand_a.grid(row=2, column=0)
        contract_a = tk.Radiobutton(frame_a, text="Contract", variable=self.selected_value_a, value=2)
        contract_a.grid(row=2, column=1)
        
        # Uniform margin checkbox for ROI A
        self.uniform_a_var = tk.BooleanVar()
        self.uniform_a_var.set(False)
        ttk.Checkbutton(frame_a, text="Uniform margin", variable=self.uniform_a_var, command=self.toggle_uniform_a).grid(row=3, column=0, sticky="w", padx=5)
        
        # Directional input for ROI A
        directions = ['Superior', 'Inferior', 'Right', 'Left', 'Anterior', 'Posterior']
        self.roi_a_margins = {}
        self.roi_a_entries = {}
        for i, direction in enumerate(directions):
            label = tk.Label(frame_a, text=f"{direction} (cm)")
            label.grid(row=i+4, column=0)
            margin_var = tk.StringVar()
            margin_var.set("0.00")
            self.roi_a_margins[direction] = margin_var
            entry = tk.Entry(frame_a, textvariable=margin_var)
            entry.grid(row=i+4, column=1)
            self.roi_a_entries[direction] = entry
            if direction == 'Superior':
                margin_var.trace_add('write', lambda *args: self.on_sup_a_change())
        
        # Operations (Union, Intersect, Subtract)
        
        operation_frame = tk.LabelFrame(frame_a_b, text="Select Operation:", padx=10, pady=10)
        operation_frame.grid(row=0, column=1, padx=5)
        self.selected_operation = tk.IntVar()
        self.selected_operation.set(1)
        union_button = tk.Radiobutton(operation_frame, text="Union", variable=self.selected_operation,value=1)
        union_button.grid(row=1, column=1)
        intersect_button = tk.Radiobutton(operation_frame, text="Intersect", variable=self.selected_operation,value=2)
        intersect_button.grid(row=2, column=1)
        subtract_button = tk.Radiobutton(operation_frame, text="Subtract", variable=self.selected_operation,value=3)
        subtract_button.grid(row=3, column=1)
        none_button = tk.Radiobutton(operation_frame, text="None", variable=self.selected_operation,value=4)
        none_button.grid(row=4,column=1)

        # ROI B
        frame_b = tk.LabelFrame(frame_a_b, text="ROI B", padx=10, pady=10)
        frame_b.grid(row=0, column=3, padx=5)
        tk.Label(frame_b, text="ROI B Name").grid(row=0, column=0)
        self.roi_b = tk.StringVar()
        roi_b_combo = ttk.Combobox(frame_b, textvariable=self.roi_b,
                                    values=roi_list, state="readonly")
        roi_b_combo.grid(row=0, column=1)
        
        margin_label_b = tk.Label(frame_b, text="Margin")
        margin_label_b.grid(row=1, column=0)
        self.selected_value_b = tk.IntVar()
        self.selected_value_b.set(1)
        expand_b = tk.Radiobutton(frame_b, text="Expand", variable=self.selected_value_b, value=1)
        expand_b.grid(row=2, column=0)
        contract_b = tk.Radiobutton(frame_b, text="Contract", variable=self.selected_value_b, value=2)
        contract_b.grid(row=2, column=1)
        
        # Uniform margin checkbox for ROI B
        self.uniform_b_var = tk.BooleanVar()
        self.uniform_b_var.set(False)
        ttk.Checkbutton(frame_b, text="Uniform margin", variable=self.uniform_b_var, command=self.toggle_uniform_b).grid(row=3, column=0, sticky="w", padx=5)

        # Directional input for ROI B
        self.roi_b_margins = {}
        self.roi_b_entries = {}
        self.roi_b_entries = {}
        for i, direction in enumerate(directions):
            label = tk.Label(frame_b, text=f"{direction} (cm)")
            label.grid(row=i+4, column=0)
            margin_var = tk.StringVar()
            margin_var.set("0.00")
            self.roi_b_margins[direction] = margin_var
            entry = tk.Entry(frame_b, textvariable=margin_var)
            entry.grid(row=i+4, column=1)
            self.roi_b_entries[direction] = entry
            if direction == 'Superior':
                margin_var.trace_add('write', lambda *args: self.on_sup_b_change())
            
        # Output section
        frame_output = tk.LabelFrame(theFrame, text="Output", padx=10, pady=10)
        frame_output.grid(row=0, column=2, padx=5)

        output_label = tk.Label(frame_output, text="Margin")
        output_label.grid(row=0, column=0)

        self.selected_output = tk.IntVar()
        self.selected_output.set(1)
        expand_output = tk.Radiobutton(frame_output, text="Expand", variable=self.selected_output, value=1)
        expand_output.grid(row=1, column=0)
        contract_output = tk.Radiobutton(frame_output, text="Contract", variable=self.selected_output, value=2)
        contract_output.grid(row=1, column=1)
        
        # Uniform margin checkbox for Output
        self.uniform_output_var = tk.BooleanVar()
        self.uniform_output_var.set(False)
        ttk.Checkbutton(frame_output, text="Uniform margin", variable=self.uniform_output_var, command=self.toggle_uniform_output).grid(row=2, column=0, sticky="w", padx=5)

        # Directional input for Output
        self.output_margins = {}
        self.output_entries = {}
        self.output_entries = {}
        for i, direction in enumerate(directions):
            label = tk.Label(frame_output, text=f"{direction} (cm)")
            label.grid(row=i+3, column=0)
            margin_var = tk.StringVar()
            margin_var.set("0.00")
            self.output_margins[direction] = margin_var
            entry = tk.Entry(frame_output, textvariable=margin_var)
            entry.grid(row=i+3, column=1)
            self.output_entries[direction] = entry
            if direction == 'Superior':
                margin_var.trace_add('write', lambda *args: self.on_sup_output_change())
            
        # Preload data if provided
        if preload_data:
            self.load_boolean_data(preload_data)
            
        # Save button
        save_button = tk.Button(self.boolean_window, text="Save", command=self.save_boolean_config)
        save_button.pack(pady=10)
    
    def toggle_uniform_a(self):
        """Enable/disable directional entries for ROI A based on uniform margin selection."""
        if self.uniform_a_var.get():
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.roi_a_entries[direction].config(state="disabled")
            self.sync_to_sup_a()
        else:
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.roi_a_entries[direction].config(state="normal")
    
    def on_sup_a_change(self):
        """Called when superior value changes in uniform mode for ROI A."""
        if self.uniform_a_var.get():
            self.sync_to_sup_a()
    
    def sync_to_sup_a(self):
        """Set all directional values equal to superior value for ROI A."""
        sup_val = self.roi_a_margins['Superior'].get()
        for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
            self.roi_a_margins[direction].set(sup_val)
    
    def toggle_uniform_b(self):
        """Enable/disable directional entries for ROI B based on uniform margin selection."""
        if self.uniform_b_var.get():
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.roi_b_entries[direction].config(state="disabled")
            self.sync_to_sup_b()
        else:
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.roi_b_entries[direction].config(state="normal")
    
    def on_sup_b_change(self):
        """Called when superior value changes in uniform mode for ROI B."""
        if self.uniform_b_var.get():
            self.sync_to_sup_b()
    
    def sync_to_sup_b(self):
        """Set all directional values equal to superior value for ROI B."""
        sup_val = self.roi_b_margins['Superior'].get()
        for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
            self.roi_b_margins[direction].set(sup_val)
    
    def toggle_uniform_output(self):
        """Enable/disable directional entries for Output based on uniform margin selection."""
        if self.uniform_output_var.get():
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.output_entries[direction].config(state="disabled")
            self.sync_to_sup_output()
        else:
            for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
                self.output_entries[direction].config(state="normal")
    
    def on_sup_output_change(self):
        """Called when superior value changes in uniform mode for Output."""
        if self.uniform_output_var.get():
            self.sync_to_sup_output()
    
    def sync_to_sup_output(self):
        """Set all directional values equal to superior value for Output."""
        sup_val = self.output_margins['Superior'].get()
        for direction in ['Inferior', 'Right', 'Left', 'Anterior', 'Posterior']:
            self.output_margins[direction].set(sup_val)
    
    def load_boolean_data(self, data):
        """Load existing boolean configuration into the form."""
        if not data:
            return
        
        # Load ROI A data
        if "roi_a" in data:
            roi_a_data = data["roi_a"]
            self.roi_a.set(roi_a_data.get("name", ""))
            margin_type = roi_a_data.get("margin_type", "Expand")
            self.selected_value_a.set(1 if margin_type == "Expand" else 2)
            margins = roi_a_data.get("margins", {})
            for direction, var in self.roi_a_margins.items():
                var.set(margins.get(direction, "0.00"))
        
        # Load operation
        operation = data.get("operation", "Union")
        operation_map = {"Union": 1, "Intersect": 2, "Subtract": 3, "None": 4}
        self.selected_operation.set(operation_map.get(operation, 1))
        
        # Load ROI B data
        if "roi_b" in data:
            roi_b_data = data["roi_b"]
            self.roi_b.set(roi_b_data.get("name", ""))
            margin_type = roi_b_data.get("margin_type", "Expand")
            self.selected_value_b.set(1 if margin_type == "Expand" else 2)
            margins = roi_b_data.get("margins", {})
            for direction, var in self.roi_b_margins.items():
                var.set(margins.get(direction, "0.00"))
        
        # Load output data
        if "output" in data:
            output_data = data["output"]
            margin_type = output_data.get("margin_type", "Expand")
            self.selected_output.set(1 if margin_type == "Expand" else 2)
            margins = output_data.get("margins", {})
            for direction, var in self.output_margins.items():
                var.set(margins.get(direction, "0.00"))
    
    def save_boolean_config(self):
        """Collect all boolean configuration and save it."""
        operation_map = {1: "Union", 2: "Intersect", 3: "Subtract", 4: "None"}
        margin_type_map = {1: "Expand", 2: "Contract"}
        
        self.boolean_data = {
            "roi_a": {
                "name": self.roi_a.get(),
                "margin_type": margin_type_map.get(self.selected_value_a.get(), "Expand"),
                "margins": {direction: var.get() for direction, var in self.roi_a_margins.items()}
            },
            "operation": operation_map.get(self.selected_operation.get(), "Union"),
            "roi_b": {
                "name": self.roi_b.get(),
                "margin_type": margin_type_map.get(self.selected_value_b.get(), "Expand"),
                "margins": {direction: var.get() for direction, var in self.roi_b_margins.items()}
            },
            "output": {
                "margin_type": margin_type_map.get(self.selected_output.get(), "Expand"),
                "margins": {direction: var.get() for direction, var in self.output_margins.items()}
            }
        }
        
        # Call the callback function if provided
        if self.callback:
            self.callback(self.boolean_data)
        
        self.boolean_window.destroy()
