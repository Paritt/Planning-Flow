import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class EndPlanningFlow_Window:
    """Open a new window for End Planning Flow step."""
    def __init__(self, parent, designer):
        self.designer = designer
        end_planning_window = tk.Toplevel(parent)
        end_planning_window.title("End Planning Flow")
        end_planning_window.geometry("400x80")
        
        ttk.Label(end_planning_window, text="End flow after 1st optimize and additional").grid(row=0, column=0, padx=5, pady=5)
        self.max_optimize_var = tk.IntVar()
        max_optimize_entry = ttk.Entry(end_planning_window, textvariable=self.max_optimize_var, width=5)
        max_optimize_entry.grid(row=0, column=1, padx=0, pady=5)
        ttk.Label(end_planning_window, text="optimization rounds").grid(row=0, column=2, padx=0, pady=5)
        
        # Load existing data if available
        if self.designer.end_flow_data:
            self.max_optimize_var.set(self.designer.end_flow_data.get("max_optimize_rounds", 0))
        
        # Save Button
        ttk.Button(end_planning_window, text="Save", command=self.save_end_flow_settings).grid(row=1, column=0, columnspan=3, padx=5, pady=10)
        
    
    def save_end_flow_settings(self):
        """Save end planning flow settings."""
        self.designer.end_flow_data = {
            "max_optimize_rounds": self.max_optimize_var.get()
        }
        messagebox.showinfo("Save Successful", "End planning flow settings saved successfully.")
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
        