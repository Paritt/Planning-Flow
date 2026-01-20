import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class InitialFunction_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Initial Function step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.initial_function_window = tk.Toplevel(parent)
        self.initial_function_window.title("Initial Optimization function")
        self.initial_function_window.geometry("800x400")

        # Bold Title Label
        title_label = tk.Label(self.initial_function_window, text="Initial Optimization function", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Content can be added here - with vertical scrollbar
        initial_function_frame = ttk.Frame(self.initial_function_window)
        initial_function_frame.pack(pady=5, fill="both", expand=True)
        
        initial_function_scroll_y = ttk.Scrollbar(initial_function_frame, orient="vertical")
        
        self.initial_function_tree = ttk.Treeview(initial_function_frame, columns=("Function tag", "Function Type", "ROI", "Description", "Weight"), show="headings",
                                                yscrollcommand=initial_function_scroll_y.set)
        
        initial_function_scroll_y.config(command=self.initial_function_tree.yview)
        
        self.initial_function_tree.heading("Function tag", text="Function tag")
        self.initial_function_tree.heading("Function Type", text="Function Type")
        self.initial_function_tree.heading("ROI", text="ROI")
        self.initial_function_tree.heading("Description", text="Description")
        self.initial_function_tree.heading("Weight", text="Weight")
        
        self.initial_function_tree.column("Function tag", width=20)
        self.initial_function_tree.column("Function Type", width=20)
        self.initial_function_tree.column("ROI", width=50)
        self.initial_function_tree.column("Description", width=200)
        self.initial_function_tree.column("Weight", width=20)
        
        self.initial_function_tree.pack(side="left", fill="both", expand=True)
        initial_function_scroll_y.pack(side="right", fill="y")
        
        # Add Objective Button
        self.add_objective_btn = ttk.Button(self.initial_function_window, text="Add function", command=self.open_add_function_window)
        self.add_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Edit Objective Button
        self.edit_objective_btn = ttk.Button(self.initial_function_window, text="Edit Selected function", command=self.open_edit_function_window)
        self.edit_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Objective Button
        self.delete_objective_btn = ttk.Button(self.initial_function_window, text="Delete Selected function", command=self.delete_function)
        self.delete_objective_btn.pack(side="left", padx=5, pady=5)

        # Load existing data if available
        if self.designer.initial_functions_data:
            for item in self.designer.initial_functions_data:
                self.initial_function_tree.insert("", "end", values=(item["tag"], item["type"], item["roi"], item["description"], item["weight"]))
        
        # Save Button
        self.save_initial_function_btn = ttk.Button(self.initial_function_window, text="Save", command=self.save_initial_functions)
        self.save_initial_function_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.initial_function_window, text="Close", command=self.initial_function_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def save_initial_functions(self):
        """Save the current list of initial functions."""
        functions = []
        for child in self.initial_function_tree.get_children():
            values = self.initial_function_tree.item(child, "values")
            functions.append({
                "tag": values[0],
                "type": values[1],
                "roi": values[2],
                "description": values[3],
                "weight": values[4]
            })
        
        self.designer.initial_functions_data = functions
        
        if functions:
            messagebox.showinfo("Save Successful", f"Initial functions saved successfully. ({len(functions)} items)")
        else:
            messagebox.showwarning("Save Error", "No functions to save.")
    
    def open_add_function_window(self):
        """Add an optimization function to the list."""
        add_function_window = tk.Toplevel(self.initial_function_window)
        add_function_window.title("Add Opt. Function")
        add_function_window.geometry("300x280")
        
        # function tag
        ttk.Label(add_function_window, text="Function tag").grid(row=0, column=0, pady=5)
        self.function_tag_var = tk.StringVar()
        self.function_tag_entry = ttk.Entry(add_function_window, textvariable=self.function_tag_var)
        self.function_tag_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="ROI Name:").grid(row=1, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_combo = ttk.Combobox(add_function_window, textvariable=self.roi_name_var,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Weight:").grid(row=2, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(add_function_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Function type:").grid(row=3, column=0, padx=5, pady=5)
        self.function_var = tk.StringVar()
        self.function_combo = ttk.Combobox(add_function_window, textvariable=self.function_var,
                                            values=['Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose', 'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'], state="readonly")
        self.function_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(add_function_window)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_dose_value_var = tk.StringVar()
        self.min_dose_value_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_value_var)
        self.min_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Max Dose
        frame_max_dose = ttk.Frame(add_function_window)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_dose_value_var = tk.StringVar()
        self.max_dose_value_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_value_var)
        self.max_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(add_function_window)
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
        frame_max_dvh = ttk.Frame(add_function_window)
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
        frame_min_eud = ttk.Frame(add_function_window)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_eud_value_var = tk.StringVar()
        self.min_eud_value_entry = ttk.Entry(frame_min_eud, textvariable=self.min_eud_value_var)
        self.min_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_min_eud_var = tk.StringVar()
        self.a_param_min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.a_param_min_eud_var)
        self.a_param_min_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Max EUD
        frame_max_eud = ttk.Frame(add_function_window)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_eud_value_var = tk.StringVar()
        self.max_eud_value_entry = ttk.Entry(frame_max_eud, textvariable=self.max_eud_value_var)
        self.max_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_max_eud_var = tk.StringVar()
        self.a_param_max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.a_param_max_eud_var)
        self.a_param_max_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Target EUD
        frame_target_eud = ttk.Frame(add_function_window)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.target_eud_value_var = tk.StringVar()
        self.target_eud_value_entry = ttk.Entry(frame_target_eud, textvariable=self.target_eud_value_var)
        self.target_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_target_eud_var = tk.StringVar()
        self.a_param_target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.a_param_target_eud_var)
        self.a_param_target_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(add_function_window)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.uniform_dose_value_var = tk.StringVar()
        self.uniform_dose_value_entry = ttk.Entry(frame_uniform_dose, textvariable=self.uniform_dose_value_var)
        self.uniform_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(add_function_window)
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
        frame_uniformity_constraint = ttk.Frame(add_function_window)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rel_std_dev_var = tk.StringVar()
        self.rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.rel_std_dev_var)
        self.rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # ------------------------------------------------------------
                                                            
        def show_selected_frame(self):
            """Show the relevant frame based on condition type selection."""
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
            selection = self.function_var.get()
            if selection == "Min Dose":
                frame_min_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max Dose":
                frame_max_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Min DVH":
                frame_min_dvh.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max DVH":
                frame_max_dvh.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Min EUD":
                frame_min_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max EUD":
                frame_max_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Target EUD":
                frame_target_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Uniform Dose":
                frame_uniform_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Dose fall-off":
                frame_dose_falloff.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Uniformity Constraint":
                frame_uniformity_constraint.grid(row=4, column=0, columnspan=2, pady=5)
        self.function_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        # Initially show the relevant frame
        show_selected_frame(self)
        
        ttk.Button(add_function_window, text="Add", command=lambda: self.add_function(add_function_window)).grid(row=6, column=0, columnspan=2, pady=10)
        
    def add_function(self, popup):
        """Save the new function to the list."""
        function_tag = self.function_tag_var.get().strip()
        function = self.function_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        weight = self.weight_var.get().strip()
        if function == "Min Dose":
            min_dose = self.min_dose_value_var.get().strip()
            description = f"Min Dose {min_dose} cGy"
        elif function == "Max Dose":
            max_dose = self.max_dose_value_var.get().strip()
            description = f"Max Dose {max_dose} cGy"
        elif function == "Min DVH":
            dose_level = self.dose_value_min_dvh_var.get().strip()
            volume_level = self.volume_value_min_dvh_var.get().strip()
            volume_unit = self.volume_value_min_dvh_unit.get().strip()
            description = f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function == "Max DVH":
            dose_level = self.dose_value_max_dvh_var.get().strip()
            volume_level = self.volume_value_max_dvh_var.get().strip()
            volume_unit = self.volume_value_max_dvh_unit.get().strip()
            description = f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function == "Min EUD":
            min_eud = self.min_eud_value_var.get().strip()
            a_param = self.a_param_min_eud_var.get().strip()
            description = f"Min EUD {min_eud} cGy, Parameter A {a_param}"
        elif function == "Max EUD":
            max_eud = self.max_eud_value_var.get().strip()
            a_param = self.a_param_max_eud_var.get().strip()
            description = f"Max EUD {max_eud} cGy, Parameter A {a_param}"
        elif function == "Target EUD":
            target_eud = self.target_eud_value_var.get().strip()
            a_param = self.a_param_target_eud_var.get().strip()
            description = f"Target EUD {target_eud} cGy, Parameter A {a_param}"
        elif function == "Uniform Dose":
            uniform_dose = self.uniform_dose_value_var.get().strip()
            description = f"Uniform Dose {uniform_dose} cGy"
        elif function == "Dose fall-off":
            high_dose = self.high_dose_value_var.get().strip()
            low_dose = self.low_dose_value_var.get().strip()
            low_distance = self.low_dose_distance_var.get().strip()
            description = f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_distance} cm"
        elif function == "Uniformity Constraint":
            rel_std_dev = self.rel_std_dev_var.get().strip()
            description = f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
            
        # Here you would add the objective to your data structure
        self.initial_function_tree.insert("", "end", values=(function_tag, function, roi_name, description, weight))
        popup.destroy()
    
    def delete_function(self):
        """Delete the selected function from the list."""
        selected_item = self.initial_function_tree.selection()
        for item in selected_item:
            self.initial_function_tree.delete(item)
    
    def open_edit_function_window(self):
        """Edit the selected optimization function."""
        selected_item = self.initial_function_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function to edit.")
            return
        
        # Get values from selected item
        item_values = self.initial_function_tree.item(selected_item[0], "values")
        selected_tag = item_values[0]
        selected_type = item_values[1]
        selected_roi = item_values[2]
        selected_description = item_values[3]
        selected_weight = item_values[4]
        
        edit_function_window = tk.Toplevel(self.initial_function_window)
        edit_function_window.title("Edit Opt. Function")
        edit_function_window.geometry("300x280")
        
        # function tag
        ttk.Label(edit_function_window, text="Function tag").grid(row=0, column=0, pady=5)
        self.function_tag_var = tk.StringVar(value=selected_tag)
        self.function_tag_entry = ttk.Entry(edit_function_window, textvariable=self.function_tag_var)
        self.function_tag_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(edit_function_window, text="ROI Name:").grid(row=1, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar(value=selected_roi)
        self.roi_name_combo = ttk.Combobox(edit_function_window, textvariable=self.roi_name_var,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(edit_function_window, text="Weight:").grid(row=2, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar(value=selected_weight)
        self.weight_entry = ttk.Entry(edit_function_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(edit_function_window, text="Function type:").grid(row=3, column=0, padx=5, pady=5)
        self.function_var = tk.StringVar(value=selected_type)
        self.function_combo = ttk.Combobox(edit_function_window, textvariable=self.function_var,
                                            values=['Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose', 'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'], state="readonly")
        self.function_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(edit_function_window)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_dose_value_var = tk.StringVar()
        self.min_dose_value_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_value_var)
        self.min_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Max Dose
        frame_max_dose = ttk.Frame(edit_function_window)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_dose_value_var = tk.StringVar()
        self.max_dose_value_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_value_var)
        self.max_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(edit_function_window)
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
        frame_max_dvh = ttk.Frame(edit_function_window)
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
        frame_min_eud = ttk.Frame(edit_function_window)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.min_eud_value_var = tk.StringVar()
        self.min_eud_value_entry = ttk.Entry(frame_min_eud, textvariable=self.min_eud_value_var)
        self.min_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_min_eud_var = tk.StringVar()
        self.a_param_min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.a_param_min_eud_var)
        self.a_param_min_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Max EUD
        frame_max_eud = ttk.Frame(edit_function_window)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.max_eud_value_var = tk.StringVar()
        self.max_eud_value_entry = ttk.Entry(frame_max_eud, textvariable=self.max_eud_value_var)
        self.max_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_max_eud_var = tk.StringVar()
        self.a_param_max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.a_param_max_eud_var)
        self.a_param_max_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Target EUD
        frame_target_eud = ttk.Frame(edit_function_window)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.target_eud_value_var = tk.StringVar()
        self.target_eud_value_entry = ttk.Entry(frame_target_eud, textvariable=self.target_eud_value_var)
        self.target_eud_value_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.a_param_target_eud_var = tk.StringVar()
        self.a_param_target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.a_param_target_eud_var)
        self.a_param_target_eud_entry.grid(row=1, column=1, padx=5, pady=5)
        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(edit_function_window)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.uniform_dose_value_var = tk.StringVar()
        self.uniform_dose_value_entry = ttk.Entry(frame_uniform_dose, textvariable=self.uniform_dose_value_var)
        self.uniform_dose_value_entry.grid(row=0, column=1, padx=5, pady=5)
        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(edit_function_window)
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
        frame_uniformity_constraint = ttk.Frame(edit_function_window)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rel_std_dev_var = tk.StringVar()
        self.rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.rel_std_dev_var)
        self.rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Parse description to pre-populate values
        self._parse_and_populate_values(selected_type, selected_description)
        
        # ------------------------------------------------------------
                                                            
        def show_selected_frame(self):
            """Show the relevant frame based on condition type selection."""
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
            selection = self.function_var.get()
            if selection == "Min Dose":
                frame_min_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max Dose":
                frame_max_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Min DVH":
                frame_min_dvh.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max DVH":
                frame_max_dvh.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Min EUD":
                frame_min_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Max EUD":
                frame_max_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Target EUD":
                frame_target_eud.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Uniform Dose":
                frame_uniform_dose.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Dose fall-off":
                frame_dose_falloff.grid(row=4, column=0, columnspan=2, pady=5)
            elif selection == "Uniformity Constraint":
                frame_uniformity_constraint.grid(row=4, column=0, columnspan=2, pady=5)
        self.function_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        # Initially show the relevant frame
        show_selected_frame(self)
        
        def save_edited_function():
            """Save the edited function."""
            function_tag = self.function_tag_var.get().strip()
            function = self.function_var.get().strip()
            roi_name = self.roi_name_var.get().strip()
            weight = self.weight_var.get().strip()
            
            if function == "Min Dose":
                min_dose = self.min_dose_value_var.get().strip()
                description = f"Min Dose {min_dose} cGy"
            elif function == "Max Dose":
                max_dose = self.max_dose_value_var.get().strip()
                description = f"Max Dose {max_dose} cGy"
            elif function == "Min DVH":
                dose_level = self.dose_value_min_dvh_var.get().strip()
                volume_level = self.volume_value_min_dvh_var.get().strip()
                volume_unit = self.volume_value_min_dvh_unit.get().strip()
                description = f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
            elif function == "Max DVH":
                dose_level = self.dose_value_max_dvh_var.get().strip()
                volume_level = self.volume_value_max_dvh_var.get().strip()
                volume_unit = self.volume_value_max_dvh_unit.get().strip()
                description = f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
            elif function == "Min EUD":
                min_eud = self.min_eud_value_var.get().strip()
                a_param = self.a_param_min_eud_var.get().strip()
                description = f"Min EUD {min_eud} cGy, Parameter A {a_param}"
            elif function == "Max EUD":
                max_eud = self.max_eud_value_var.get().strip()
                a_param = self.a_param_max_eud_var.get().strip()
                description = f"Max EUD {max_eud} cGy, Parameter A {a_param}"
            elif function == "Target EUD":
                target_eud = self.target_eud_value_var.get().strip()
                a_param = self.a_param_target_eud_var.get().strip()
                description = f"Target EUD {target_eud} cGy, Parameter A {a_param}"
            elif function == "Uniform Dose":
                uniform_dose = self.uniform_dose_value_var.get().strip()
                description = f"Uniform Dose {uniform_dose} cGy"
            elif function == "Dose fall-off":
                high_dose = self.high_dose_value_var.get().strip()
                low_dose = self.low_dose_value_var.get().strip()
                low_distance = self.low_dose_distance_var.get().strip()
                description = f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_distance} cm"
            elif function == "Uniformity Constraint":
                rel_std_dev = self.rel_std_dev_var.get().strip()
                description = f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
            
            # Update tree item
            self.initial_function_tree.item(selected_item[0], values=(function_tag, function, roi_name, description, weight))
            edit_function_window.destroy()
        
        ttk.Button(edit_function_window, text="Save Changes", command=save_edited_function).grid(row=6, column=0, columnspan=2, pady=10)
    
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
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)        
      