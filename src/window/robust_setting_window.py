import tkinter as tk
from tkinter import ttk, messagebox

class RoustSetting_Window:
    def __init__(self, parent, plan_flow_designer):
        self.parent = parent
        self.plan_flow = plan_flow_designer
        
        # Create popup window
        self.window = tk.Toplevel(parent)
        self.window.title("Robustness Settings")
        self.window.geometry("300x550")
        self.window.attributes('-topmost', True)
        self.window.grab_set()
        
        # Method frame
        method_frame = ttk.LabelFrame(self.window, text="Robust Methods", padding="10")
        method_frame.pack(fill="x", pady=10, padx=10)
        
        # Positioning Uncertainty
        pos_frame = ttk.LabelFrame(self.window, text="Positioning Uncertainty", padding="10")
        pos_frame.pack(fill="x", pady=10, padx=10)
        
        # Density Uncertainty
        dens_frame = ttk.LabelFrame(self.window, text="Density Uncertainty", padding="10")
        dens_frame.pack(fill="x", pady=10, padx=10)
        
        # Method selection
        self.method_var = tk.StringVar()
        self.method_var.set("Composite worst cases (minimax)")
        tk.Radiobutton(method_frame, text="Composite worst cases (minimax)", variable=self.method_var, value="Composite worst cases (minimax)").pack(anchor="w", padx=5, pady=5)
        tk.Radiobutton(method_frame, text="Voxelwise worst cases", variable=self.method_var, value="Voxelwise worst cases").pack(anchor="w", padx=5, pady=5)
        
        # Positioning Uncertainty inputs
        
        # Checkbox for use isotropic uncertainty
        self.iso_var = tk.BooleanVar()
        self.iso_var.set(True)
        ttk.Checkbutton(pos_frame, text="Use isotropic uncertainty", variable=self.iso_var, command=self.toggle_uncertainty_mode).grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        
        ttk.Label(pos_frame, text="Superior (cm):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sup_var = tk.DoubleVar()
        self.sup_entry = ttk.Entry(pos_frame, textvariable=self.sup_var, width=20)
        self.sup_entry.grid(row=1, column=1, padx=5, pady=5)
        self.sup_var.set(0.0)
        self.sup_var.trace_add('write', self.on_sup_change)
        
        
        ttk.Label(pos_frame, text="Inferior (cm):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.inf_var = tk.DoubleVar()
        self.inf_entry = ttk.Entry(pos_frame, textvariable=self.inf_var, width=20)
        self.inf_entry.grid(row=2, column=1, padx=5, pady=5)
        self.inf_var.set(0.0)
        
        ttk.Label(pos_frame, text="Left (cm):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.left_var = tk.DoubleVar()
        self.left_entry = ttk.Entry(pos_frame, textvariable=self.left_var, width=20)
        self.left_entry.grid(row=3, column=1, padx=5, pady=5)
        self.left_var.set(0.0)
        
        ttk.Label(pos_frame, text="Right (cm):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.right_var = tk.DoubleVar()
        self.right_entry = ttk.Entry(pos_frame, textvariable=self.right_var, width=20)
        self.right_entry.grid(row=4, column=1, padx=5, pady=5)
        self.right_var.set(0.0)
        
        ttk.Label(pos_frame, text="Anterior (cm):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.ant_var = tk.DoubleVar()
        self.ant_entry = ttk.Entry(pos_frame, textvariable=self.ant_var, width=20)
        self.ant_entry.grid(row=5, column=1, padx=5, pady=5)
        self.ant_var.set(0.0)
        
        ttk.Label(pos_frame, text="Posterior (cm):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.post_var = tk.DoubleVar()
        self.post_entry = ttk.Entry(pos_frame, textvariable=self.post_var, width=20)
        self.post_entry.grid(row=6, column=1, padx=5, pady=5)
        self.post_var.set(0.0)
        
        # Initialize the state based on isotropic selection
        self.toggle_uncertainty_mode()
        
        # Density Uncertainty inputs
        ttk.Label(dens_frame, text="Density uncertainty (%):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.dens_var = tk.DoubleVar()
        self.dens_entry = ttk.Entry(dens_frame, textvariable=self.dens_var, width=10)
        self.dens_entry.grid(row=0, column=1, padx=5, pady=5)
        self.dens_var.set(0.0)
        
        # Buttons frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", pady=10, padx=10)
        
        # Load existing data if available
        self.load_existing_data()
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save", command=self.save).pack(side="left", padx=5)
    
    def load_existing_data(self):
        """Load existing robust settings data if available."""
        if self.plan_flow.robust_settings_data:
            robust_data = self.plan_flow.robust_settings_data
            self.method_var.set(robust_data.get("method", "Composite worst cases (minimax)"))
            pos_uncertainty = robust_data.get("positioning_uncertainty", {})
            self.iso_var.set(pos_uncertainty.get("isotropic", True))
            self.sup_var.set(pos_uncertainty.get("superior", 0.0))
            self.inf_var.set(pos_uncertainty.get("inferior", 0.0))
            self.left_var.set(pos_uncertainty.get("left", 0.0))
            self.right_var.set(pos_uncertainty.get("right", 0.0))
            self.ant_var.set(pos_uncertainty.get("anterior", 0.0))
            self.post_var.set(pos_uncertainty.get("posterior", 0.0))
            self.dens_var.set(robust_data.get("density_uncertainty", 0.0))
            self.toggle_uncertainty_mode()
    
    def toggle_uncertainty_mode(self):
        """Enable/disable directional entries based on isotropic/anisotropic selection."""
        if self.iso_var.get():
            # Isotropic mode: disable and sync all fields to superior
            self.inf_entry.config(state="disabled")
            self.left_entry.config(state="disabled")
            self.right_entry.config(state="disabled")
            self.ant_entry.config(state="disabled")
            self.post_entry.config(state="disabled")
            self.sync_to_superior()
        else:
            # Anisotropic mode: enable all fields
            self.inf_entry.config(state="normal")
            self.left_entry.config(state="normal")
            self.right_entry.config(state="normal")
            self.ant_entry.config(state="normal")
            self.post_entry.config(state="normal")
    
    def on_sup_change(self, *args):
        """Called when superior value changes in isotropic mode."""
        if self.iso_var.get():
            self.sync_to_superior()
    
    def sync_to_superior(self):
        """Set all directional values equal to superior value."""
        sup_val = self.sup_var.get()
        self.inf_var.set(sup_val)
        self.left_var.set(sup_val)
        self.right_var.set(sup_val)
        self.ant_var.set(sup_val)
        self.post_var.set(sup_val)
    
    def cancel(self):
        """Close the window without saving."""
        self.window.destroy()
    
    def save(self):
        """Save the robust settings to the planning flow."""
        # Collect all robust settings data
        robust_data = {
            "method": self.method_var.get(),
            "positioning_uncertainty": {
                "isotropic": self.iso_var.get(),
                "superior": self.sup_var.get(),
                "inferior": self.inf_var.get(),
                "left": self.left_var.get(),
                "right": self.right_var.get(),
                "anterior": self.ant_var.get(),
                "posterior": self.post_var.get()
            },
            "density_uncertainty": self.dens_var.get()
        }
        
        # Pass data back to parent PlanFlowDesigner via callback
        if hasattr(self.plan_flow, 'set_robust_settings'):
            self.plan_flow.set_robust_settings(robust_data)
        
        messagebox.showinfo("Save", "Robust settings saved successfully.")
        self.window.destroy()