import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FinalCalculationSetting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Final Calculation step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.final_calc_window = tk.Toplevel(parent)
        self.final_calc_window.title("Final Calculation")
        self.final_calc_window.geometry("220x120")

        self.algorithm_var = tk.StringVar()
        self.uncer_or_spot_var = tk.StringVar()
        self.uncer_spot_value_var = tk.StringVar()
        
        # Algorithm Combobox
        if self.designer.technique_var.get() == 'IMPT':
            self.algorithm_combo = ttk.Combobox(self.final_calc_window, values=['Pencil beam', 'MonteCarlo'], state="readonly", textvariable=self.algorithm_var, width=20)
            self.algorithm_combo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            self.algorithm_combo.bind("<<ComboboxSelected>>", self.update_algorithm_options)
            self.algorithm_var.set('MonteCarlo')
        else:
            self.algorithm_combo = ttk.Combobox(self.final_calc_window, values=['Collapsed Cone'], state="readonly", textvariable=self.algorithm_var, width=20)
            self.algorithm_combo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            self.algorithm_var.set('Collapsed Cone')
        
        # MonteCarlo-specific widgets (created but hidden initially)
        self.uncer_or_spot_combo = ttk.Combobox(self.final_calc_window, values=['Uncert[%]', 'Ions/spot'], state="readonly", textvariable=self.uncer_or_spot_var, width=10)
        self.uncer_or_spot_combo.bind("<<ComboboxSelected>>", self.update_uncer_spot_default)
        self.uncer_or_spot_var.set('Uncert[%]')
        
        self.uncer_spot_entry = ttk.Entry(self.final_calc_window, textvariable=self.uncer_spot_value_var, width=8)
        self.uncer_spot_value_var.set("1.0")
        
        # Load existing data if available
        if self.designer.final_calc_data:
            self.algorithm_var.set(self.designer.final_calc_data.get("algorithm", self.algorithm_var.get()))
            if self.designer.final_calc_data.get("algorithm", "") == "MonteCarlo":
                self.uncer_or_spot_var.set(self.designer.final_calc_data.get("uncer_or_spot", "Uncert[%]"))
                self.uncer_spot_value_var.set(self.designer.final_calc_data.get("uncer_spot_value", "1.0" if self.uncer_or_spot_var.get() == "Uncert[%]" else "10000"))
        
        # Display algorithm-specific options
        self.update_algorithm_options()
        
        # Save Button
        ttk.Button(self.final_calc_window, text="Save", command=self.save_final_calc_settings).grid(row=2, column=0, padx=5, pady=10)
        
        # Close Button
        ttk.Button(self.final_calc_window, text="Close", command=self.final_calc_window.destroy).grid(row=2, column=1, padx=5, pady=10)
    
    def update_algorithm_options(self, event=None):
        """Show or hide MonteCarlo-specific options based on algorithm selection."""
        if self.algorithm_var.get() == "MonteCarlo":
            # Show the MonteCarlo-specific widgets
            self.uncer_or_spot_combo.grid(row=1, column=0, padx=15, pady=5)
            self.uncer_spot_entry.grid(row=1, column=1, padx=1, pady=5)
        else:
            # Hide the MonteCarlo-specific widgets
            self.uncer_or_spot_combo.grid_remove()
            self.uncer_spot_entry.grid_remove()
    
    def update_uncer_spot_default(self, event=None):
        """Update the default value based on uncer_or_spot selection."""
        if self.uncer_or_spot_var.get() == 'Uncert[%]':
            self.uncer_spot_value_var.set("1.0")
        elif self.uncer_or_spot_var.get() == 'Ions/spot':
            self.uncer_spot_value_var.set("10000")
    
    def save_final_calc_settings(self):
        """Save final calculation settings."""
        self.designer.final_calc_data = {
            "algorithm": self.algorithm_var.get(),
            "uncer_or_spot": self.uncer_or_spot_var.get() if self.algorithm_var.get() == "MonteCarlo" else "",
            "uncer_spot_value": self.uncer_spot_value_var.get() if self.algorithm_var.get() == "MonteCarlo" else ""
        }
        messagebox.showinfo("Save Successful", "Final calculation settings saved successfully.")
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
