import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CheckCondition_Window:
    """Open a new window for Check Condition step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.check_condition_window = tk.Toplevel(parent)
        self.check_condition_window.title("Check Condition")
        self.check_condition_window.geometry("1000x400")
        
        # Bold Title Label
        title_label = tk.Label(self.check_condition_window, text="Check Condition", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Condition tree with vertical scrollbar
        condition_tree_frame = ttk.Frame(self.check_condition_window)
        condition_tree_frame.pack(pady=5, fill="both", expand=True)
        
        condition_tree_scroll_y = ttk.Scrollbar(condition_tree_frame, orient="vertical")
        
        self.condition_tree = ttk.Treeview(condition_tree_frame, columns=("Condition Name", "ROI",  "Condition Type", "Criteria"), show="headings",
                                            yscrollcommand=condition_tree_scroll_y.set)
        
        condition_tree_scroll_y.config(command=self.condition_tree.yview)
        
        self.condition_tree.heading("Condition Name", text="Condition Name")
        self.condition_tree.heading("ROI", text="ROI")
        self.condition_tree.heading("Condition Type", text="Condition Type")
        self.condition_tree.heading("Criteria", text="Criteria")
        
        self.condition_tree.column("Condition Name", width=150)
        self.condition_tree.column("ROI", width=100)
        self.condition_tree.column("Condition Type", width=130)
        self.condition_tree.column("Criteria", width=200)
        
        self.condition_tree.pack(side="left", fill="both", expand=True)
        condition_tree_scroll_y.pack(side="right", fill="y")
        
        # Add Condition Button
        self.add_condition_btn = ttk.Button(self.check_condition_window, text="New", command=self.open_add_condition_window)
        self.add_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition Button
        self.delete_condition_btn = ttk.Button(self.check_condition_window, text="Remove", command=self.remove_condition)
        self.delete_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit Condition Button
        self.edit_condition_btn = ttk.Button(self.check_condition_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Load existing data if available
        if self.designer.check_conditions_data:
            for item in self.designer.check_conditions_data:
                self.condition_tree.insert("", "end", values=(item["name"], item["roi"], item["type"], item["criteria"]))
        
        # Save Button
        self.save_condition_btn = ttk.Button(self.check_condition_window, text="Save", command=self.save_conditions)
        self.save_condition_btn.pack(side="left", padx=5, pady=5)

        # Close Button
        self.close_btn = ttk.Button(self.check_condition_window, text="Close", command=self.check_condition_window.destroy)
        self.close_btn.pack(pady=10)
    
    def save_conditions(self):
        """Save the current list of conditions."""
        conditions = []
        for child in self.condition_tree.get_children():
            values = self.condition_tree.item(child, "values")
            conditions.append({
                "name": values[0],
                "roi": values[1],
                "type": values[2],
                "criteria": values[3]
            })
        
        self.designer.check_conditions_data = conditions
        
        if conditions:
            messagebox.showinfo("Save Successful", f"Conditions saved successfully. ({len(conditions)} items)")
        else:
            messagebox.showwarning("Save Error", "No conditions to save.")
    
    def open_add_condition_window(self):
        """Add a condition to the list."""
        add_condition_window = tk.Toplevel(self.check_condition_window)
        add_condition_window.title("Add Condition")
        add_condition_window.geometry("350x220")
        
        ttk.Label(add_condition_window, text="Condition Name:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_name_var = tk.StringVar()
        self.condition_name_entry = ttk.Entry(add_condition_window, textvariable=self.condition_name_var)
        self.condition_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_window, text="Condition Type:").grid(row=1, column=0, padx=5, pady=5)
        self.condition_type_var = tk.StringVar()
        self.condition_type_combo = ttk.Combobox(add_condition_window, textvariable=self.condition_type_var,
                                            values=['Optimization Round', 'Max Dose','Max DaV', 'Max VaD', 'Max Dmean', 'Min Dose','Min DaV', 'Min VaD', 'Min Dmean'], state="readonly")
        self.condition_type_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for optimization round
        frame_opt_round = ttk.Frame(add_condition_window)
        ttk.Label(frame_opt_round, text="Optimization Round ≥").grid(row=0, column=0, padx=5, pady=5)
        self.opt_round_var = tk.StringVar()
        self.opt_round_entry = ttk.Entry(frame_opt_round, textvariable=self.opt_round_var)
        self.opt_round_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame for Max Dose
        frame_max_dose = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dose, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dose = tk.StringVar()
        self.roi_name_combo_max_dose = ttk.Combobox(frame_max_dose, textvariable=self.roi_name_var_max_dose,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_max_dose.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_dose, text="Max Dose (Gy):").grid(row=1, column=0, padx=5, pady=5)
        self.max_dose_var = tk.StringVar()
        self.max_dose_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_var)
        self.max_dose_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dose, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dose = tk.StringVar()
        self.roi_name_combo_min_dose = ttk.Combobox(frame_min_dose, textvariable=self.roi_name_var_min_dose,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_min_dose.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dose, text="Min Dose (Gy):").grid(row=1, column=0, padx=5, pady=5)
        self.min_dose_var = tk.StringVar()
        self.min_dose_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_var)
        self.min_dose_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame for Max DaV
        frame_max_dav = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dav, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dav = tk.StringVar()
        self.roi_name_combo_max_dav = ttk.Combobox(frame_max_dav, textvariable=self.roi_name_var_max_dav,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_max_dav.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dav, text="Dose (cGy) at most:").grid(row=1, column=0, padx=5, pady=5)
        self.dose_max_dav_var = tk.StringVar()
        self.dose_max_dav_entry = ttk.Entry(frame_max_dav, textvariable=self.dose_max_dav_var)
        self.dose_max_dav_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dav, text="at Volume:").grid(row=2, column=0, padx=5, pady=5)
        self.volume_max_dav_var = tk.StringVar()
        self.volume_max_dav_entry = ttk.Entry(frame_max_dav, textvariable=self.volume_max_dav_var)
        self.volume_max_dav_entry.grid(row=2, column=1, padx=5, pady=5)
        self.volume_max_dav_unit = tk.StringVar()
        self.volume_max_dav_unit_combo = ttk.Combobox(frame_max_dav, textvariable=self.volume_max_dav_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_max_dav_unit_combo.grid(row=2, column=2, padx=5, pady=5)
        
        # Frame for Min DaV
        frame_min_dav = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dav, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dav = tk.StringVar()
        self.roi_name_combo_min_dav = ttk.Combobox(frame_min_dav, textvariable=self.roi_name_var_min_dav,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_min_dav.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_dav, text="Dose (cGy) at least:").grid(row=1, column=0, padx=5, pady=5)
        self.dose_min_dav_var = tk.StringVar()
        self.dose_min_dav_entry = ttk.Entry(frame_min_dav, textvariable=self.dose_min_dav_var)
        self.dose_min_dav_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_dav, text="at Volume:").grid(row=2, column=0, padx=5, pady=5)
        self.volume_min_dav_var = tk.StringVar()
        self.volume_min_dav_entry = ttk.Entry(frame_min_dav, textvariable=self.volume_min_dav_var)
        self.volume_min_dav_entry.grid(row=2, column=1, padx=5, pady=5)
        self.volume_min_dav_unit = tk.StringVar()
        self.volume_min_dav_unit_combo = ttk.Combobox(frame_min_dav, textvariable=self.volume_min_dav_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_min_dav_unit_combo.grid(row=2, column=2, padx=5, pady=5)
        
        # Frame Max VaD
        frame_max_vad = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_vad, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_vad = tk.StringVar()
        self.roi_name_combo_max_vad = ttk.Combobox(frame_max_vad, textvariable=self.roi_name_var_max_vad,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_max_vad.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_vad, text="Volume at most:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_max_vad_var = tk.StringVar()
        self.volume_max_vad_entry = ttk.Entry(frame_max_vad, textvariable=self.volume_max_vad_var)
        self.volume_max_vad_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_max_vad_unit = tk.StringVar()
        self.volume_max_vad_unit_combo = ttk.Combobox(frame_max_vad, textvariable=self.volume_max_vad_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_max_vad_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(frame_max_vad, text="at Dose (cGy):").grid(row=2, column=0, padx=5, pady=5)
        self.dose_max_vad_var = tk.StringVar()
        self.dose_max_vad_entry = ttk.Entry(frame_max_vad, textvariable=self.dose_max_vad_var)
        self.dose_max_vad_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Frame Min VaD
        frame_min_vad = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_vad, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_vad = tk.StringVar()
        self.roi_name_combo_min_vad = ttk.Combobox(frame_min_vad, textvariable=self.roi_name_var_min_vad,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_min_vad.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_vad, text="Volume at most:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_min_vad_var = tk.StringVar()
        self.volume_min_vad_entry = ttk.Entry(frame_min_vad, textvariable=self.volume_min_vad_var)
        self.volume_min_vad_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_min_vad_unit = tk.StringVar()
        self.volume_min_vad_unit_combo = ttk.Combobox(frame_min_vad, textvariable=self.volume_min_vad_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_min_vad_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(frame_min_vad, text="at Dose (cGy):").grid(row=2, column=0, padx=5, pady=5)
        self.dose_min_vad_var = tk.StringVar()
        self.dose_min_vad_entry = ttk.Entry(frame_min_vad, textvariable=self.dose_min_vad_var)
        self.dose_min_vad_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Fram Max Dmean
        frame_max_dmean = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dmean, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dmean = tk.StringVar()
        self.roi_name_combo_max_dmean = ttk.Combobox(frame_max_dmean, textvariable=self.roi_name_var_max_dmean,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_max_dmean.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dmean, text="Max Dmean (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.max_dmean_var = tk.StringVar()
        self.max_dmean_entry = ttk.Entry(frame_max_dmean, textvariable=self.max_dmean_var)
        self.max_dmean_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame Min Dmean
        frame_min_dmean = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dmean, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dmean = tk.StringVar()
        self.roi_name_combo_min_dmean = ttk.Combobox(frame_min_dmean, textvariable=self.roi_name_var_min_dmean,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_name_combo_min_dmean.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dmean, text="Min Dmean (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.min_dmean_var = tk.StringVar()
        self.min_dmean_entry = ttk.Entry(frame_min_dmean, textvariable=self.min_dmean_var)
        self.min_dmean_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def show_selected_frame(self):
            """Show the relevant frame based on condition type selection."""
            frame_opt_round.grid_forget()
            frame_max_dose.grid_forget()
            frame_min_dose.grid_forget()
            frame_max_dav.grid_forget()
            frame_min_dav.grid_forget()
            frame_max_vad.grid_forget()
            frame_min_vad.grid_forget()
            frame_max_dmean.grid_forget()
            frame_min_dmean.grid_forget()
            selection = self.condition_type_var.get()
            if selection == 'Optimization Round':
                frame_opt_round.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max Dose':
                frame_max_dose.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min Dose':
                frame_min_dose.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max DaV':
                frame_max_dav.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min DaV':
                frame_min_dav.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max VaD':
                frame_max_vad.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min VaD':
                frame_min_vad.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max Dmean':
                frame_max_dmean.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min Dmean':
                frame_min_dmean.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
                
        self.condition_type_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        show_selected_frame(self)  # Show the initial frame based on the default selection
        
        ttk.Button(add_condition_window, text="Add", command=lambda: self.add_condition(add_condition_window)).grid(row=5, column=0, columnspan=2, pady=10)

    def add_condition(self, popup):
        """Save the new condition to the list."""
        condition_name = self.condition_name_var.get().strip()
        condition_type = self.condition_type_var.get().strip()
        if condition_type == 'Optimization Round':
            roi_name = 'N/A'
            opt_round = self.opt_round_var.get().strip()
            criteria = f"Round ≥ {opt_round}"
        elif condition_type == 'Max Dose':
            roi_name = self.roi_name_var_max_dose.get().strip()
            max_dose = self.max_dose_var.get().strip()
            criteria = f"Dmax (Gy) ≥ {max_dose}"
        elif condition_type == 'Min Dose':
            roi_name = self.roi_name_var_min_dose.get().strip()
            min_dose = self.min_dose_var.get().strip()
            criteria = f"Dmin (Gy) ≤ {min_dose}"
        elif condition_type == 'Max DaV':
            roi_name = self.roi_name_var_max_dav.get().strip()
            dose_max_dav = self.dose_max_dav_var.get().strip()
            volume_max_dav = self.volume_max_dav_var.get().strip()
            volume_max_dav_unit = self.volume_max_dav_unit.get().strip()
            criteria = f"D{volume_max_dav}{volume_max_dav_unit} ≥ {dose_max_dav} cGy"
        elif condition_type == 'Min DaV':
            roi_name = self.roi_name_var_min_dav.get().strip()
            dose_min_dav = self.dose_min_dav_var.get().strip()
            volume_min_dav = self.volume_min_dav_var.get().strip()
            volume_min_dav_unit = self.volume_min_dav_unit.get().strip()
            criteria = f"D{volume_min_dav}{volume_min_dav_unit} ≤ {dose_min_dav} cGy"
        elif condition_type == 'Max VaD':
            roi_name = self.roi_name_var_max_vad.get().strip()
            volume_max_vad = self.volume_max_vad_var.get().strip()
            volume_max_vad_unit = self.volume_max_vad_unit.get().strip()
            dose_max_vad = self.dose_max_vad_var.get().strip()
            criteria = f"V{dose_max_vad} cGy ≥ {volume_max_vad}{volume_max_vad_unit}"
        elif condition_type == 'Min VaD':
            roi_name = self.roi_name_var_min_vad.get().strip()
            volume_min_vad = self.volume_min_vad_var.get().strip()
            volume_min_vad_unit = self.volume_min_vad_unit.get().strip()
            dose_min_vad = self.dose_min_vad_var.get().strip()
            criteria = f"V{dose_min_vad} cGy ≤ {volume_min_vad}{volume_min_vad_unit}"
        elif condition_type == 'Max Dmean':
            roi_name = self.roi_name_var_max_dmean.get().strip()
            max_dmean = self.max_dmean_var.get().strip()
            criteria = f"Dmean (cGy) ≥ {max_dmean}"
        elif condition_type == 'Min Dmean':
            roi_name = self.roi_name_var_min_dmean.get().strip()
            min_dmean = self.min_dmean_var.get().strip()
            criteria = f"Dmean (cGy) ≤ {min_dmean}"
        # Here you would add the condition to your data structure
        self.condition_tree.insert("", "end", values=(condition_name, roi_name, condition_type, criteria))
        popup.destroy()
    
    def remove_condition(self):
        """Remove the selected condition from the list."""
        selected_item = self.condition_tree.selection()
        for item in selected_item:
            self.condition_tree.delete(item)
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
        