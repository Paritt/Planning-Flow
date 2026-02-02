import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class FinalCalculationSetting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Final Calculation step."""
    def __init__(self, parent, designer):
        self.designer = designer
        final_calc_window = tk.Toplevel(parent)
        final_calc_window.title("Final Calculation")
        final_calc_window.geometry("250x70")

        ttk.Label(final_calc_window, text="Algorithm").grid(row=0, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        if self.designer.technique_var.get() == 'IMPT':
            ttk.Combobox(final_calc_window, values=['Pencil beam', 'MonteCarlo'], state="readonly", textvariable=self.algorithm_var).grid(row=0, column=1, padx=5, pady=5)
            self.algorithm_var.set('MonteCarlo')
        else:
            ttk.Combobox(final_calc_window, values=['Collapsed Cone'], state="readonly", textvariable=self.algorithm_var).grid(row=0, column=1, padx=5, pady=5)
            self.algorithm_var.set('Collapsed Cone')
        
        
        # Load existing data if available
        if self.designer.final_calc_data:
            self.algorithm_var.set(self.designer.final_calc_data.get("algorithm", ""))
        
        # Save Button
        ttk.Button(final_calc_window, text="Save", command=self.save_final_calc_settings).grid(row=1, column=0,padx=5, pady=10)
        
        # Close Button
        ttk.Button(final_calc_window, text="Close", command=final_calc_window.destroy).grid(row=1, column=1, padx=5, pady=10)
    
    def save_final_calc_settings(self):
        """Save final calculation settings."""
        self.designer.final_calc_data = {
            "algorithm": self.algorithm_var.get()
        }
        messagebox.showinfo("Save Successful", "Final calculation settings saved successfully.")
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
