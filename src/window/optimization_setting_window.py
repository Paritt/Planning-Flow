import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class OptimizationSetting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Optimization Settings step."""
    def __init__(self, parent, designer):
        self.designer = designer
        """Open a new window for Optimization step."""
        optimization_window = tk.Toplevel(parent)
        optimization_window.title("Optimization Settings")
        optimization_window.geometry("300x120")
        
        ttk.Label(optimization_window, text="Optimization tolerance:").grid(row=0, column=0, padx=5, pady=5)
        self.tolerance_var = tk.StringVar()
        self.tolerance_entry = ttk.Entry(optimization_window, textvariable=self.tolerance_var)
        self.tolerance_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(optimization_window, text="Maximum iterations:").grid(row=1, column=0, padx=5, pady=5)
        self.max_iterations_var = tk.StringVar()
        self.max_iterations_entry = ttk.Entry(optimization_window, textvariable=self.max_iterations_var)
        self.max_iterations_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Load existing data if available
        if self.designer.optimization_data:
            self.tolerance_var.set(self.designer.optimization_data.get("tolerance", ""))
            self.max_iterations_var.set(self.designer.optimization_data.get("max_iterations", ""))
        
        # Save Button
        ttk.Button(optimization_window, text="Save", command=self.save_optimization_settings).grid(row=2, column=0, pady=10)

        # Close Button
        ttk.Button(optimization_window, text="Close", command=optimization_window.destroy).grid(row=2, column=1, columnspan=2, pady=10)
    
    def save_optimization_settings(self):
        """Save optimization settings."""
        self.designer.optimization_data = {
            "tolerance": self.tolerance_var.get().strip(),
            "max_iterations": self.max_iterations_var.get().strip()
        }
        messagebox.showinfo("Save Successful", "Optimization settings saved successfully.")
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
