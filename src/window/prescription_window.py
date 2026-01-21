import tkinter as tk
from tkinter import ttk, messagebox


class PrescriptionSetting_Window:
    def __init__(self, parent, plan_flow_designer):
        self.parent = parent
        self.plan_flow = plan_flow_designer
        
        # Create popup window
        self.window = tk.Toplevel(parent)
        self.window.title("Prescription Settings")
        self.window.geometry("400x200")
        self.window.attributes('-topmost', True)
        self.window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Primary prescription dose (cGy)
        ttk.Label(main_frame, text="Primary prescription dose (cGy):").grid(row=0, column=0, sticky="w", padx=5, pady=10)
        self.dose_var = tk.StringVar()
        self.dose_entry = ttk.Entry(main_frame, textvariable=self.dose_var, width=20)
        self.dose_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # No. of fraction
        ttk.Label(main_frame, text="No. of fraction:").grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.fraction_var = tk.StringVar()
        self.fraction_entry = ttk.Entry(main_frame, textvariable=self.fraction_var, width=20)
        self.fraction_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Prescription primary dose to (ROI dropdown)
        ttk.Label(main_frame, text="Prescription primary dose to:").grid(row=2, column=0, sticky="w", padx=5, pady=10)
        roi_list = self.plan_flow.get_roi_list()
        self.roi_var = tk.StringVar()
        self.roi_dropdown = ttk.Combobox(main_frame, textvariable=self.roi_var, values=roi_list, state="readonly", width=18)
        self.roi_dropdown.grid(row=2, column=1, padx=5, pady=10)
        if roi_list and roi_list[0] != 'Please add ROIs first':
            self.roi_dropdown.current(0)
        
        # Load existing data if available
        self.load_existing_data()
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save", command=self.save).pack(side="left", padx=5)
    
    def load_existing_data(self):
        """Load existing prescription data if available."""
        if self.plan_flow.prescription_data:
            self.dose_var.set(self.plan_flow.prescription_data.get("primary_dose", ""))
            self.fraction_var.set(self.plan_flow.prescription_data.get("num_fractions", ""))
            self.roi_var.set(self.plan_flow.prescription_data.get("prescription_roi", ""))
    
    def validate_input(self):
        """Validate the input fields."""
        # Validate dose
        dose = self.dose_var.get().strip()
        if not dose:
            messagebox.showerror("Validation Error", "Please enter primary prescription dose.")
            return False
        try:
            dose_int = int(dose)
            if dose_int <= 0:
                messagebox.showerror("Validation Error", "Primary prescription dose must be a positive integer.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Primary prescription dose must be an integer.")
            return False
        
        # Validate fraction
        fraction = self.fraction_var.get().strip()
        if not fraction:
            messagebox.showerror("Validation Error", "Please enter number of fractions.")
            return False
        try:
            fraction_int = int(fraction)
            if fraction_int <= 0:
                messagebox.showerror("Validation Error", "Number of fractions must be a positive integer.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Number of fractions must be an integer.")
            return False
        
        # Validate ROI selection
        roi = self.roi_var.get().strip()
        if not roi or roi == 'Please add ROIs first':
            messagebox.showerror("Validation Error", "Please select an ROI for prescription.")
            return False
        
        return True
    
    def save(self):
        """Save the prescription settings."""
        if not self.validate_input():
            return
        
        # Store data in plan_flow_designer
        self.plan_flow.prescription_data = {
            "primary_dose": self.dose_var.get().strip(),
            "num_fractions": self.fraction_var.get().strip(),
            "prescription_roi": self.roi_var.get().strip()
        }
        
        messagebox.showinfo("Success", "Prescription settings saved successfully.")
        self.window.destroy()
    
    def cancel(self):
        """Cancel and close the window."""
        self.window.destroy()
