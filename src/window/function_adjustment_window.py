import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FunctionAdjustment_Window:
    """Open a new window for Function Adjustment step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.function_adjustment_window = tk.Toplevel(parent)
        self.function_adjustment_window.title("Function Adjustment")
        self.function_adjustment_window.geometry("1300x800")
        
        # Bold Title Label
        title_label = tk.Label(self.function_adjustment_window, text="Function Adjustment", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Old function frame
        old_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Initial Functions")
        old_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # Old function Tree with vertical scrollbar
        old_function_frame = ttk.Frame(old_function_label_frame)
        old_function_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        old_function_scroll_y = ttk.Scrollbar(old_function_frame, orient="vertical")
        
        self.old_function_tree = ttk.Treeview(old_function_frame, columns=("Function tag","Function Type", "ROI",  "Description", "Weight"), show="headings",
                                                yscrollcommand=old_function_scroll_y.set)
        
        old_function_scroll_y.config(command=self.old_function_tree.yview)
        
        self.old_function_tree.heading("Function tag", text="Function tag")
        self.old_function_tree.heading("Function Type", text="Function Type")
        self.old_function_tree.heading("ROI", text="ROI")
        self.old_function_tree.heading("Description", text="Description")
        self.old_function_tree.heading("Weight", text="Weight")
        
        self.old_function_tree.column("Function tag", width=20)
        self.old_function_tree.column("Function Type", width=20)
        self.old_function_tree.column("ROI", width=50)
        self.old_function_tree.column("Description", width=200)
        self.old_function_tree.column("Weight", width=20)
        
        self.old_function_tree.pack(side="left", fill="both", expand=True)
        old_function_scroll_y.pack(side="right", fill="y")
        
        def add_old_functions(self):
            """Add old functions to the list."""
            # Load initial functions from designer
            if self.designer.initial_functions_data:
                for func in self.designer.initial_functions_data:
                    self.old_function_tree.insert("", "end", values=(func["tag"], func["type"], func["roi"], func["description"], func["weight"]))
                
        add_old_functions(self)
        
        # Adjust Button
        self.adjust_function_btn = ttk.Button(old_function_label_frame, text="Adjust Selected Function", command=self.adjust_function)
        self.adjust_function_btn.pack(side="left", padx=5, pady=5)
        
        # Adjusted function frame
        adjusted_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Adjustment")
        adjusted_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # New function adjustment Tree with vertical scrollbar
        function_adjustment_frame = ttk.Frame(adjusted_function_label_frame)
        function_adjustment_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        function_adjustment_scroll_y = ttk.Scrollbar(function_adjustment_frame, orient="vertical")
        
        self.function_adjustment_tree = ttk.Treeview(function_adjustment_frame, columns=("If this condition TRUE", "Make this Adjustment", "Function tag", "Function Type", "ROI", "Description", "Weight"), show="headings",
                                                    yscrollcommand=function_adjustment_scroll_y.set)
        
        function_adjustment_scroll_y.config(command=self.function_adjustment_tree.yview)
        
        self.function_adjustment_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.function_adjustment_tree.heading("Make this Adjustment", text="Make this Adjustment")
        self.function_adjustment_tree.heading("Function tag", text="Function tag")
        self.function_adjustment_tree.heading("Function Type", text="Function Type")
        self.function_adjustment_tree.heading("ROI", text="ROI")
        self.function_adjustment_tree.heading("Description", text="Description")
        self.function_adjustment_tree.heading("Weight", text="Weight")
        
        self.function_adjustment_tree.column("If this condition TRUE", width=20)
        self.function_adjustment_tree.column("Make this Adjustment", width=20)
        self.function_adjustment_tree.column("Function tag", width=20)
        self.function_adjustment_tree.column("Function Type", width=20)
        self.function_adjustment_tree.column("ROI", width=50)
        self.function_adjustment_tree.column("Description", width=200)
        self.function_adjustment_tree.column("Weight", width=50)
        
        self.function_adjustment_tree.pack(side="left", fill="both", expand=True)
        function_adjustment_scroll_y.pack(side="right", fill="y")
        
        # Add Adjustment Button
        self.add_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Add New Function", command=self.open_add_function_adjustment_window)
        self.add_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Edit Adjustment Button
        self.edit_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Edit Selected Adjustment", command=self.open_edit_function_adjustment_window)
        self.edit_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Delete Adjustment Button
        self.delete_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Remove Adjustment", command=lambda: self.show_step_info("Remove Function Adjustment"))
        self.delete_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Load existing data if available
        if self.designer.function_adjustments_data:
            for item in self.designer.function_adjustments_data:
                self.function_adjustment_tree.insert("", "end", values=(item["condition"], item["adjustment"], item["tag"], item["type"], item["roi"], item["description"], item["weight"]))
        
        # Save Button
        self.save_adjustment_btn = ttk.Button(self.function_adjustment_window, text="Save", command=self.save_function_adjustments)
        self.save_adjustment_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.function_adjustment_window, text="Close", command=self.function_adjustment_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def save_function_adjustments(self):
        """Save the current list of function adjustments."""
        adjustments = []
        for child in self.function_adjustment_tree.get_children():
            values = self.function_adjustment_tree.item(child, "values")
            adjustments.append({
                "condition": values[0],
                "adjustment": values[1],
                "tag": values[2],
                "type": values[3],
                "roi": values[4],
                "description": values[5],
                "weight": values[6]
            })
        
        self.designer.function_adjustments_data = adjustments
        
        if adjustments:
            messagebox.showinfo("Save Successful", f"Function adjustments saved successfully. ({len(adjustments)} items)")
        else:
            messagebox.showwarning("Save Error", "No function adjustments to save.")
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
    
    def adjust_function(self):
        """Adjust the selected function."""
        # Get selected function from old_function_tree
        selected_item = self.old_function_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function to adjust.")
            return
        
        # Get values from selected item
        item_values = self.old_function_tree.item(selected_item[0], "values")
        selected_tag = item_values[0]
        selected_type = item_values[1]
        selected_roi = item_values[2]
        selected_description = item_values[3]
        selected_weight = item_values[4]
        
        # Open adjustment window
        adjust_window = tk.Toplevel(self.function_adjustment_window)
        adjust_window.title("Adjust Function")
        adjust_window.geometry("350x320")
        
        condition_list = self.designer.get_condition_list()
        
        ttk.Label(adjust_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar()
        self.condition_true_combo = ttk.Combobox(adjust_window, textvariable=self.condition_true_var,
                                        values=condition_list, state="readonly")
        self.condition_true_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(adjust_window, text="Function tag:").grid(row=1, column=0, padx=5, pady=5)
        self.adjustment_tag_var = tk.StringVar(value=selected_tag)
        self.adjustment_tag_entry = ttk.Entry(adjust_window, textvariable=self.adjustment_tag_var)
        self.adjustment_tag_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(adjust_window, text="ROI Name:").grid(row=2, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar(value=selected_roi)
        self.roi_name_combo = ttk.Combobox(adjust_window, textvariable=self.roi_name_var,
                                        values=self.designer.get_extended_roi_list(), state="readonly")
        self.roi_name_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(adjust_window, text="Weight:").grid(row=3, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar(value=selected_weight)
        self.weight_entry = ttk.Entry(adjust_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(adjust_window, text="Function type:").grid(row=4, column=0, padx=5, pady=5)
        self.function_type_var = tk.StringVar(value=selected_type)
        self.function_type_combo = ttk.Combobox(adjust_window, textvariable=self.function_type_var,
                                            values=['Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose', 'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'], state="readonly")
        self.function_type_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(adjust_window)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_dose_value_var = tk.StringVar()
        self.min_dose_value_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_value_var)
        self.min_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Max Dose
        frame_max_dose = ttk.Frame(adjust_window)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_dose_value_var = tk.StringVar()
        self.max_dose_value_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_value_var)
        self.max_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(adjust_window)
        ttk.Label(frame_min_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_min_dvh_var = tk.StringVar()
        self.dose_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.dose_value_min_dvh_var)
        self.dose_value_min_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_min_dvh_var = tk.StringVar()
        self.volume_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.volume_value_min_dvh_var)
        self.volume_value_min_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_min_dvh_unit = tk.StringVar()
        self.volume_value_min_dvh_unit_combo = ttk.Combobox(frame_min_dvh, textvariable=self.volume_value_min_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_min_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Max DVH
        frame_max_dvh = ttk.Frame(adjust_window)
        ttk.Label(frame_max_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_max_dvh_var = tk.StringVar()
        self.dose_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.dose_value_max_dvh_var)
        self.dose_value_max_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_max_dvh_var = tk.StringVar()
        self.volume_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.volume_value_max_dvh_var)
        self.volume_value_max_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_max_dvh_unit = tk.StringVar()
        self.volume_value_max_dvh_unit_combo = ttk.Combobox(frame_max_dvh, textvariable=self.volume_value_max_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_max_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Min EUD
        frame_min_eud = ttk.Frame(adjust_window)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_eud_value_var = tk.StringVar()
        self.min_eud_value_entry = ttk.Entry(frame_min_eud, textvariable=self.min_eud_value_var)
        self.min_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_min_eud_var = tk.StringVar()
        self.a_param_min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.a_param_min_eud_var)
        self.a_param_min_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Max EUD
        frame_max_eud = ttk.Frame(adjust_window)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_eud_value_var = tk.StringVar()
        self.max_eud_value_entry = ttk.Entry(frame_max_eud, textvariable=self.max_eud_value_var)
        self.max_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_max_eud_var = tk.StringVar()
        self.a_param_max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.a_param_max_eud_var)
        self.a_param_max_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Target EUD
        frame_target_eud = ttk.Frame(adjust_window)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.target_eud_value_var = tk.StringVar()
        self.target_eud_value_entry = ttk.Entry(frame_target_eud, textvariable=self.target_eud_value_var)
        self.target_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_target_eud_var = tk.StringVar()
        self.a_param_target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.a_param_target_eud_var)
        self.a_param_target_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(adjust_window)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.uniform_dose_value_var = tk.StringVar()
        self.uniform_dose_value_entry = ttk.Entry(frame_uniform_dose, textvariable=self.uniform_dose_value_var)
        self.uniform_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(adjust_window)
        ttk.Label(frame_dose_falloff, text="High dose level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.high_dose_value_var = tk.StringVar()
        self.high_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.high_dose_value_var)
        self.high_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose level (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.low_dose_value_var = tk.StringVar()
        self.low_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_value_var)
        self.low_dose_value_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose distance (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.low_dose_distance_var = tk.StringVar()
        self.low_dose_distance_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_distance_var)
        self.low_dose_distance_entry.grid(row=2, column=1, padx=5, pady=5)
        # Frame for Uniformity Constraint
        frame_uniformity_constraint = ttk.Frame(adjust_window)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rel_std_dev_var = tk.StringVar()
        self.rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.rel_std_dev_var)
        self.rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Parse description to pre-populate values
        self._parse_and_populate_values(selected_type, selected_description)
        
        # ------------------------------------------------------------
                                                            
        def show_selected_frame(self):
            """Show the relevant frame based on function type selection."""
            frame_min_dose.grid_forget()
            frame_max_dose.grid_forget()
            frame_min_dvh.grid_forget()
            frame_max_dvh.grid_forget()
            frame_min_eud.grid_forget()
            frame_max_eud.grid_forget()
            frame_target_eud.grid_forget()
            frame_uniform_dose.grid_forget()
            frame_dose_falloff.grid_forget()
            frame_uniformity_constraint.grid_forget()
            selection = self.function_type_var.get()
            if selection == "Min Dose":
                frame_min_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max Dose":
                frame_max_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min DVH":
                frame_min_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max DVH":
                frame_max_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min EUD":
                frame_min_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max EUD":
                frame_max_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Target EUD":
                frame_target_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniform Dose":
                frame_uniform_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Dose fall-off":
                frame_dose_falloff.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniformity Constraint":
                frame_uniformity_constraint.grid(row=5, column=0, columnspan=2, pady=5)
        self.function_type_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        # Initially show the relevant frame
        show_selected_frame(self)
        
        ttk.Button(adjust_window, text="Adjust", command=lambda: self.adjust_old_function(adjust_window)).grid(row=7, column=0, columnspan=2, pady=10)
    
    def adjust_old_function(self, popup):
        """Save the adjusted function to the adjustment list."""
        condition_true = self.condition_true_var.get().strip()
        make_adjustment = "Adjust OLD Function"
        adjustment_tag = self.adjustment_tag_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        weight = self.weight_var.get().strip()
        function_type = self.function_type_var.get().strip()
        
        # Build description based on function type and input values
        description = ""
        if function_type == "Min Dose":
            min_dose = self.min_dose_value_var.get().strip()
            description = f"Min Dose {min_dose} cGy"
        elif function_type == "Max Dose":
            max_dose = self.max_dose_value_var.get().strip()
            description = f"Max Dose {max_dose} cGy"
        elif function_type == "Min DVH":
            dose_level = self.dose_value_min_dvh_var.get().strip()
            volume_level = self.volume_value_min_dvh_var.get().strip()
            volume_unit = self.volume_value_min_dvh_unit.get().strip()
            description = f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Max DVH":
            dose_level = self.dose_value_max_dvh_var.get().strip()
            volume_level = self.volume_value_max_dvh_var.get().strip()
            volume_unit = self.volume_value_max_dvh_unit.get().strip()
            description = f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Min EUD":
            min_eud = self.min_eud_value_var.get().strip()
            a_param = self.a_param_min_eud_var.get().strip()
            description = f"Min EUD {min_eud} cGy, Parameter A {a_param}"
        elif function_type == "Max EUD":
            max_eud = self.max_eud_value_var.get().strip()
            a_param = self.a_param_max_eud_var.get().strip()
            description = f"Max EUD {max_eud} cGy, Parameter A {a_param}"
        elif function_type == "Target EUD":
            target_eud = self.target_eud_value_var.get().strip()
            a_param = self.a_param_target_eud_var.get().strip()
            description = f"Target EUD {target_eud} cGy, Parameter A {a_param}"
        elif function_type == "Uniform Dose":
            uniform_dose = self.uniform_dose_value_var.get().strip()
            description = f"Uniform Dose {uniform_dose} cGy"
        elif function_type == "Dose fall-off":
            high_dose = self.high_dose_value_var.get().strip()
            low_dose = self.low_dose_value_var.get().strip()
            low_dose_distance = self.low_dose_distance_var.get().strip()
            description = f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_dose_distance} cm"
        elif function_type == "Uniformity Constraint":
            rel_std_dev = self.rel_std_dev_var.get().strip()
            description = f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
        # Insert into function adjustment tree
        self.function_adjustment_tree.insert("", "end", values=(condition_true, make_adjustment, adjustment_tag, function_type, roi_name, description, weight))
        popup.destroy()
    
    def _parse_and_populate_values(self, function_type, description):
        """Parse the description and populate the corresponding input fields."""
        import re
        
        if function_type == "Min Dose":
            # "Min Dose 45 cGy"
            match = re.search(r'Min Dose (\S+) cGy', description)
            if match:
                self.min_dose_value_var.set(match.group(1))
        elif function_type == "Max Dose":
            # "Max Dose 10 cGy"
            match = re.search(r'Max Dose (\S+) cGy', description)
            if match:
                self.max_dose_value_var.set(match.group(1))
        elif function_type == "Min DVH":
            # "Min DVH 45 cGy to 95% volume"
            match = re.search(r'Min DVH (\S+) cGy to (\S+)(%)|(cc) volume', description)
            if match:
                self.dose_value_min_dvh_var.set(match.group(1))
                self.volume_value_min_dvh_var.set(match.group(2))
                self.volume_value_min_dvh_unit.set(match.group(3) if match.group(3) else match.group(4))
        elif function_type == "Max DVH":
            # "Max DVH 20 cGy to 10% volume"
            match = re.search(r'Max DVH (\S+) cGy to (\S+)(%)|(cc) volume', description)
            if match:
                self.dose_value_max_dvh_var.set(match.group(1))
                self.volume_value_max_dvh_var.set(match.group(2))
                self.volume_value_max_dvh_unit.set(match.group(3) if match.group(3) else match.group(4))
        elif function_type == "Min EUD":
            # "Min EUD 45 cGy, Parameter A -10"
            match = re.search(r'Min EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.min_eud_value_var.set(match.group(1))
                self.a_param_min_eud_var.set(match.group(2))
        elif function_type == "Max EUD":
            # "Max EUD 10 cGy, Parameter A 5"
            match = re.search(r'Max EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.max_eud_value_var.set(match.group(1))
                self.a_param_max_eud_var.set(match.group(2))
        elif function_type == "Target EUD":
            # "Target EUD 50 cGy, Parameter A 0"
            match = re.search(r'Target EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.target_eud_value_var.set(match.group(1))
                self.a_param_target_eud_var.set(match.group(2))
        elif function_type == "Uniform Dose":
            # "Uniform Dose 50 cGy"
            match = re.search(r'Uniform Dose (\S+) cGy', description)
            if match:
                self.uniform_dose_value_var.set(match.group(1))
        elif function_type == "Dose fall-off":
            # "Dose fall-off [H] 50 cGy [L] 20 cGy, Low dose distance 2 cm"
            match = re.search(r'Dose fall-off \[H\] (\S+) cGy \[L\] (\S+) cGy, Low dose distance (\S+) cm', description)
            if match:
                self.high_dose_value_var.set(match.group(1))
                self.low_dose_value_var.set(match.group(2))
                self.low_dose_distance_var.set(match.group(3))
        elif function_type == "Uniformity Constraint":
            # "Uniformity Constraint Rel.std.dev 10 %"
            match = re.search(r'Uniformity Constraint Rel\.std\.dev (\S+) %', description)
            if match:
                self.rel_std_dev_var.set(match.group(1))
        
    def open_add_function_adjustment_window(self):
        """Add a function adjustment to the list."""
        add_adjustment_window = tk.Toplevel(self.function_adjustment_window)
        add_adjustment_window.title("Add Function Adjustment")
        add_adjustment_window.geometry("350x320")
        
        condition_list = self.designer.get_condition_list()
        
        ttk.Label(add_adjustment_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar()
        self.condition_true_combo = ttk.Combobox(add_adjustment_window, textvariable=self.condition_true_var,
                                        values=condition_list, state="readonly")
        self.condition_true_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Function tag:").grid(row=1, column=0, padx=5, pady=5)
        self.adjustment_tag_var = tk.StringVar()
        self.adjustment_tag_entry = ttk.Entry(add_adjustment_window, textvariable=self.adjustment_tag_var)
        self.adjustment_tag_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="ROI Name:").grid(row=2, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_combo = ttk.Combobox(add_adjustment_window, textvariable=self.roi_name_var,
                                        values=self.designer.get_extended_roi_list(), state="readonly")
        self.roi_name_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Weight:").grid(row=3, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(add_adjustment_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Function type:").grid(row=4, column=0, padx=5, pady=5)
        self.function_type_var = tk.StringVar()
        self.function_type_combo = ttk.Combobox(add_adjustment_window, textvariable=self.function_type_var,
                                            values=['Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose', 'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'], state="readonly")
        self.function_type_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_dose_value_var = tk.StringVar()
        self.min_dose_value_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_value_var)
        self.min_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Max Dose
        frame_max_dose = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_dose_value_var = tk.StringVar()
        self.max_dose_value_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_value_var)
        self.max_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_min_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_min_dvh_var = tk.StringVar()
        self.dose_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.dose_value_min_dvh_var)
        self.dose_value_min_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_min_dvh_var = tk.StringVar()
        self.volume_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.volume_value_min_dvh_var)
        self.volume_value_min_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_min_dvh_unit = tk.StringVar()
        self.volume_value_min_dvh_unit_combo = ttk.Combobox(frame_min_dvh, textvariable=self.volume_value_min_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_min_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Max DVH
        frame_max_dvh = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_max_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_max_dvh_var = tk.StringVar()
        self.dose_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.dose_value_max_dvh_var)
        self.dose_value_max_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_max_dvh_var = tk.StringVar()
        self.volume_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.volume_value_max_dvh_var)
        self.volume_value_max_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_max_dvh_unit = tk.StringVar()
        self.volume_value_max_dvh_unit_combo = ttk.Combobox(frame_max_dvh, textvariable=self.volume_value_max_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_max_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Min EUD
        frame_min_eud = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_eud_value_var = tk.StringVar()
        self.min_eud_value_entry = ttk.Entry(frame_min_eud, textvariable=self.min_eud_value_var)
        self.min_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_min_eud_var = tk.StringVar()
        self.a_param_min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.a_param_min_eud_var)
        self.a_param_min_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Max EUD
        frame_max_eud = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_eud_value_var = tk.StringVar()
        self.max_eud_value_entry = ttk.Entry(frame_max_eud, textvariable=self.max_eud_value_var)
        self.max_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_max_eud_var = tk.StringVar()
        self.a_param_max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.a_param_max_eud_var)
        self.a_param_max_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Target EUD
        frame_target_eud = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.target_eud_value_var = tk.StringVar()
        self.target_eud_value_entry = ttk.Entry(frame_target_eud, textvariable=self.target_eud_value_var)
        self.target_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_target_eud_var = tk.StringVar()
        self.a_param_target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.a_param_target_eud_var)
        self.a_param_target_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.uniform_dose_value_var = tk.StringVar()
        self.uniform_dose_value_entry = ttk.Entry(frame_uniform_dose, textvariable=self.uniform_dose_value_var)
        self.uniform_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_dose_falloff, text="High dose level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.high_dose_value_var = tk.StringVar()
        self.high_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.high_dose_value_var)
        self.high_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose level (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.low_dose_value_var = tk.StringVar()
        self.low_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_value_var)
        self.low_dose_value_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose distance (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.low_dose_distance_var = tk.StringVar()
        self.low_dose_distance_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_distance_var)
        self.low_dose_distance_entry.grid(row=2, column=1, padx=5, pady=5)
        # Frame for Uniformity Constraint
        frame_uniformity_constraint = ttk.Frame(add_adjustment_window)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rel_std_dev_var = tk.StringVar()
        self.rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.rel_std_dev_var)
        self.rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # ------------------------------------------------------------
                                                            
        def show_selected_frame(self):
            """Show the relevant frame based on function type selection."""
            frame_min_dose.grid_forget()
            frame_max_dose.grid_forget()
            frame_min_dvh.grid_forget()
            frame_max_dvh.grid_forget()
            frame_min_eud.grid_forget()
            frame_max_eud.grid_forget()
            frame_target_eud.grid_forget()
            frame_uniform_dose.grid_forget()
            frame_dose_falloff.grid_forget()
            frame_uniformity_constraint.grid_forget()
            selection = self.function_type_var.get()
            if selection == "Min Dose":
                frame_min_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max Dose":
                frame_max_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min DVH":
                frame_min_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max DVH":
                frame_max_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min EUD":
                frame_min_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max EUD":
                frame_max_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Target EUD":
                frame_target_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniform Dose":
                frame_uniform_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Dose fall-off":
                frame_dose_falloff.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniformity Constraint":
                frame_uniformity_constraint.grid(row=5, column=0, columnspan=2, pady=5)
        self.function_type_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        # Initially show the relevant frame
        show_selected_frame(self)
        
        ttk.Button(add_adjustment_window, text="Add", command=lambda: self.add_function_adjustment(add_adjustment_window)).grid(row=7, column=0, columnspan=2, pady=10)
    
    def add_function_adjustment(self, popup):
        """Save the new function adjustment to the list."""
        condition_true = self.condition_true_var.get().strip()
        make_adjustment = "Add NEW function"
        adjustment_tag = self.adjustment_tag_var.get().strip()
        function_type = self.function_type_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        weight = self.weight_var.get().strip()
        
        if function_type == "Min Dose":
            min_dose = self.min_dose_value_var.get().strip()
            description = f"Min Dose {min_dose} cGy"
        elif function_type == "Max Dose":
            max_dose = self.max_dose_value_var.get().strip()
            description = f"Max Dose {max_dose} cGy"
        elif function_type == "Min DVH":
            dose_level = self.dose_value_min_dvh_var.get().strip()
            volume_level = self.volume_value_min_dvh_var.get().strip()
            volume_unit = self.volume_value_min_dvh_unit.get().strip()
            description = f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Max DVH":
            dose_level = self.dose_value_max_dvh_var.get().strip()
            volume_level = self.volume_value_max_dvh_var.get().strip()
            volume_unit = self.volume_value_max_dvh_unit.get().strip()
            description = f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Min EUD":
            min_eud = self.min_eud_value_var.get().strip()
            a_param = self.a_param_min_eud_var.get().strip()
            description = f"Min EUD {min_eud} cGy, Parameter A {a_param}"
        elif function_type == "Max EUD":
            max_eud = self.max_eud_value_var.get().strip()
            a_param = self.a_param_max_eud_var.get().strip()
            description = f"Max EUD {max_eud} cGy, Parameter A {a_param}"
        elif function_type == "Target EUD":
            target_eud = self.target_eud_value_var.get().strip()
            a_param = self.a_param_target_eud_var.get().strip()
            description = f"Target EUD {target_eud} cGy, Parameter A {a_param}"
        elif function_type == "Uniform Dose":
            uniform_dose = self.uniform_dose_value_var.get().strip()
            description = f"Uniform Dose {uniform_dose} cGy"
        elif function_type == "Dose fall-off":
            high_dose = self.high_dose_value_var.get().strip()
            low_dose = self.low_dose_value_var.get().strip()
            low_distance = self.low_dose_distance_var.get().strip()
            description = f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_distance} cm"
        elif function_type == "Uniformity Constraint":
            rel_std_dev = self.rel_std_dev_var.get().strip()
            description = f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
            
        # Here you would add the function adjustment to your data structure
        self.function_adjustment_tree.insert("", "end", values=(condition_true, make_adjustment, adjustment_tag, function_type, roi_name, description, weight))
        popup.destroy()
    
    def open_edit_function_adjustment_window(self):
        """Edit the selected function adjustment."""
        selected_item = self.function_adjustment_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function adjustment to edit.")
            return
        
        # Get values from selected item
        item_values = self.function_adjustment_tree.item(selected_item[0], "values")
        selected_condition = item_values[0]
        selected_adjustment = item_values[1]
        selected_tag = item_values[2]
        selected_type = item_values[3]
        selected_roi = item_values[4]
        selected_description = item_values[5]
        selected_weight = item_values[6]
        
        edit_adjustment_window = tk.Toplevel(self.function_adjustment_window)
        edit_adjustment_window.title("Edit Function Adjustment")
        edit_adjustment_window.geometry("350x320")
        
        condition_list = self.designer.get_condition_list()
        
        ttk.Label(edit_adjustment_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar(value=selected_condition)
        self.condition_true_combo = ttk.Combobox(edit_adjustment_window, textvariable=self.condition_true_var,
                                        values=condition_list, state="readonly")
        self.condition_true_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(edit_adjustment_window, text="Function tag:").grid(row=1, column=0, padx=5, pady=5)
        self.adjustment_tag_var = tk.StringVar(value=selected_tag)
        self.adjustment_tag_entry = ttk.Entry(edit_adjustment_window, textvariable=self.adjustment_tag_var)
        self.adjustment_tag_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(edit_adjustment_window, text="ROI Name:").grid(row=2, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar(value=selected_roi)
        self.roi_name_combo = ttk.Combobox(edit_adjustment_window, textvariable=self.roi_name_var,
                                        values=self.designer.get_extended_roi_list(), state="readonly")
        self.roi_name_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(edit_adjustment_window, text="Weight:").grid(row=3, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar(value=selected_weight)
        self.weight_entry = ttk.Entry(edit_adjustment_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(edit_adjustment_window, text="Function type:").grid(row=4, column=0, padx=5, pady=5)
        self.function_type_var = tk.StringVar(value=selected_type)
        self.function_type_combo = ttk.Combobox(edit_adjustment_window, textvariable=self.function_type_var,
                                            values=['Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose', 'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'], state="readonly")
        self.function_type_combo.grid(row=4, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_dose_value_var = tk.StringVar()
        self.min_dose_value_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_value_var)
        self.min_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Max Dose
        frame_max_dose = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_dose_value_var = tk.StringVar()
        self.max_dose_value_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_value_var)
        self.max_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_min_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_min_dvh_var = tk.StringVar()
        self.dose_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.dose_value_min_dvh_var)
        self.dose_value_min_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_min_dvh_var = tk.StringVar()
        self.volume_value_min_dvh_entry = ttk.Entry(frame_min_dvh, textvariable=self.volume_value_min_dvh_var)
        self.volume_value_min_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_min_dvh_unit = tk.StringVar()
        self.volume_value_min_dvh_unit_combo = ttk.Combobox(frame_min_dvh, textvariable=self.volume_value_min_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_min_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Max DVH
        frame_max_dvh = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_max_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.dose_value_max_dvh_var = tk.StringVar()
        self.dose_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.dose_value_max_dvh_var)
        self.dose_value_max_dvh_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_value_max_dvh_var = tk.StringVar()
        self.volume_value_max_dvh_entry = ttk.Entry(frame_max_dvh, textvariable=self.volume_value_max_dvh_var)
        self.volume_value_max_dvh_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_value_max_dvh_unit = tk.StringVar()
        self.volume_value_max_dvh_unit_combo = ttk.Combobox(frame_max_dvh, textvariable=self.volume_value_max_dvh_unit,
                                            values=['%', 'cc'], state="readonly", width=5)
        self.volume_value_max_dvh_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        # Frame for Min EUD
        frame_min_eud = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_eud_value_var = tk.StringVar()
        self.min_eud_value_entry = ttk.Entry(frame_min_eud, textvariable=self.min_eud_value_var)
        self.min_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_min_eud_var = tk.StringVar()
        self.a_param_min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.a_param_min_eud_var)
        self.a_param_min_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Max EUD
        frame_max_eud = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_eud_value_var = tk.StringVar()
        self.max_eud_value_entry = ttk.Entry(frame_max_eud, textvariable=self.max_eud_value_var)
        self.max_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_max_eud_var = tk.StringVar()
        self.a_param_max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.a_param_max_eud_var)
        self.a_param_max_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Target EUD
        frame_target_eud = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.target_eud_value_var = tk.StringVar()
        self.target_eud_value_entry = ttk.Entry(frame_target_eud, textvariable=self.target_eud_value_var)
        self.target_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_target_eud_var = tk.StringVar()
        self.a_param_target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.a_param_target_eud_var)
        self.a_param_target_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.uniform_dose_value_var = tk.StringVar()
        self.uniform_dose_value_entry = ttk.Entry(frame_uniform_dose, textvariable=self.uniform_dose_value_var)
        self.uniform_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_dose_falloff, text="High dose level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.high_dose_value_var = tk.StringVar()
        self.high_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.high_dose_value_var)
        self.high_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose level (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.low_dose_value_var = tk.StringVar()
        self.low_dose_value_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_value_var)
        self.low_dose_value_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame_dose_falloff, text="Low dose distance (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.low_dose_distance_var = tk.StringVar()
        self.low_dose_distance_entry = ttk.Entry(frame_dose_falloff, textvariable=self.low_dose_distance_var)
        self.low_dose_distance_entry.grid(row=2, column=1, padx=5, pady=5)
        # Frame for Uniformity Constraint
        frame_uniformity_constraint = ttk.Frame(edit_adjustment_window)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rel_std_dev_var = tk.StringVar()
        self.rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.rel_std_dev_var)
        self.rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Parse description to pre-populate values
        self._parse_and_populate_values(selected_type, selected_description)
        
        # ------------------------------------------------------------
                                                            
        def show_selected_frame(self):
            """Show the relevant frame based on function type selection."""
            frame_min_dose.grid_forget()
            frame_max_dose.grid_forget()
            frame_min_dvh.grid_forget()
            frame_max_dvh.grid_forget()
            frame_min_eud.grid_forget()
            frame_max_eud.grid_forget()
            frame_target_eud.grid_forget()
            frame_uniform_dose.grid_forget()
            frame_dose_falloff.grid_forget()
            frame_uniformity_constraint.grid_forget()
            selection = self.function_type_var.get()
            if selection == "Min Dose":
                frame_min_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max Dose":
                frame_max_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min DVH":
                frame_min_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max DVH":
                frame_max_dvh.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Min EUD":
                frame_min_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Max EUD":
                frame_max_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Target EUD":
                frame_target_eud.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniform Dose":
                frame_uniform_dose.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Dose fall-off":
                frame_dose_falloff.grid(row=5, column=0, columnspan=2, pady=5)
            elif selection == "Uniformity Constraint":
                frame_uniformity_constraint.grid(row=5, column=0, columnspan=2, pady=5)
        self.function_type_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        # Initially show the relevant frame
        show_selected_frame(self)
        
        def save_edited_adjustment():
            """Save the edited function adjustment."""
            condition_true = self.condition_true_var.get().strip()
            adjustment_tag = self.adjustment_tag_var.get().strip()
            function_type = self.function_type_var.get().strip()
            roi_name = self.roi_name_var.get().strip()
            weight = self.weight_var.get().strip()
            
            # Determine adjustment type based on whether it's adding new or adjusting old
            # Keep the original adjustment type
            make_adjustment = selected_adjustment
            
            # Build description based on function type and input values
            description = ""
            if function_type == "Min Dose":
                min_dose = self.min_dose_value_var.get().strip()
                description = f"Min Dose {min_dose} cGy"
            elif function_type == "Max Dose":
                max_dose = self.max_dose_value_var.get().strip()
                description = f"Max Dose {max_dose} cGy"
            elif function_type == "Min DVH":
                dose_level = self.dose_value_min_dvh_var.get().strip()
                volume_level = self.volume_value_min_dvh_var.get().strip()
                volume_unit = self.volume_value_min_dvh_unit.get().strip()
                description = f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
            elif function_type == "Max DVH":
                dose_level = self.dose_value_max_dvh_var.get().strip()
                volume_level = self.volume_value_max_dvh_var.get().strip()
                volume_unit = self.volume_value_max_dvh_unit.get().strip()
                description = f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
            elif function_type == "Min EUD":
                min_eud = self.min_eud_value_var.get().strip()
                a_param = self.a_param_min_eud_var.get().strip()
                description = f"Min EUD {min_eud} cGy, Parameter A {a_param}"
            elif function_type == "Max EUD":
                max_eud = self.max_eud_value_var.get().strip()
                a_param = self.a_param_max_eud_var.get().strip()
                description = f"Max EUD {max_eud} cGy, Parameter A {a_param}"
            elif function_type == "Target EUD":
                target_eud = self.target_eud_value_var.get().strip()
                a_param = self.a_param_target_eud_var.get().strip()
                description = f"Target EUD {target_eud} cGy, Parameter A {a_param}"
            elif function_type == "Uniform Dose":
                uniform_dose = self.uniform_dose_value_var.get().strip()
                description = f"Uniform Dose {uniform_dose} cGy"
            elif function_type == "Dose fall-off":
                high_dose = self.high_dose_value_var.get().strip()
                low_dose = self.low_dose_value_var.get().strip()
                low_dose_distance = self.low_dose_distance_var.get().strip()
                description = f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_dose_distance} cm"
            elif function_type == "Uniformity Constraint":
                rel_std_dev = self.rel_std_dev_var.get().strip()
                description = f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
            
            # Update tree item
            self.function_adjustment_tree.item(selected_item[0], values=(condition_true, make_adjustment, adjustment_tag, function_type, roi_name, description, weight))
            edit_adjustment_window.destroy()
        
        ttk.Button(edit_adjustment_window, text="Save Changes", command=save_edited_adjustment).grid(row=7, column=0, columnspan=2, pady=10)
