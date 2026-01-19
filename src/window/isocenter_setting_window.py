import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class isocenter_setting_Window:
    """Window for configuring isocenter settings."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.isocenter_window = tk.Toplevel(parent)
        self.isocenter_window.title("Isocenter Settings")
        self.isocenter_window.geometry("300x180")
        # Bold title label
        title_label = ttk.Label(self.isocenter_window, text="Isocenter Settings", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Isocenter Method Selection
        ttk.Label(self.isocenter_window, text="Isocenter Method:").grid(row=1, column=0, padx=5, pady=5)
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(self.isocenter_window, textvariable=self.method_var,
                                            values=['Center of ROI', 'User Defined POI', 'Automatic'], state="readonly")
        self.method_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.method_dropdown.set('Center of ROI')  # Default selection
        
        
        # --------------
        # Frame for dynamic options
        # --------------
        
        # Frame for User Defined POI
        frame_user_poi = tk.Frame(self.isocenter_window)
        ttk.Label(frame_user_poi, text="POI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.poi_entry = ttk.Entry(frame_user_poi)
        self.poi_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame for Center of ROI
        frame_center_roi = tk.Frame(self.isocenter_window)
        ttk.Label(frame_center_roi, text="Select ROI:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_var = tk.StringVar()
        self.roi_dropdown = ttk.Combobox(frame_center_roi, textvariable=self.roi_var,
                                        values=self.designer.get_roi_list(), state="readonly")
        self.roi_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame for Automatic (could add options later)
        frame_automatic = tk.Frame(self.isocenter_window)
        auto_button = ttk.Button(frame_automatic, text="Automatic Isocenter Settings", command=lambda: messagebox.showinfo("Automatic Isocenter Settings", "Automatic Isocenter settings is not implemented yet."))
        auto_button.grid(row=0, column=0, columnspan=2, pady=5)
                
        # Dynamic GUI elements based on method selection
        def update_method_options(event):
            # Clear previous dynamic widgets
            frame_automatic.grid_forget()
            frame_center_roi.grid_forget()
            frame_user_poi.grid_forget()

            method = self.method_var.get()
            if method == "User Defined POI":
                frame_user_poi.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif method == "Center of ROI":
                frame_center_roi.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif method == "Automatic":
                # Automatic Isocenter setting button
                frame_automatic.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # Pre-fill existing settings if available
        if self.designer.isocenter_data:
            existing_method = self.designer.isocenter_data.get("method", "")
            if existing_method in ['Center of ROI', 'User Defined POI', 'Automatic']:
                self.method_var.set(existing_method)
                if existing_method == 'Center of ROI':
                    self.roi_var.set(self.designer.isocenter_data.get("roi_name", ""))
                if existing_method == 'User Defined POI':
                    self.poi_entry.delete(0, tk.END)
                    self.poi_entry.insert(0, self.designer.isocenter_data.get("poi_name", ""))
                if existing_method == 'Automatic':
                    pass  # No additional fields for Automatic currently
                            
        self.method_dropdown.bind("<<ComboboxSelected>>", lambda event: update_method_options(event))
        update_method_options(self)  # Initialize the dynamic options

        # Save Button
        save_button = ttk.Button(self.isocenter_window, text="Save Settings", command=self.save_isocenter_settings)
        save_button.grid(row=3, column=0, pady=10)
        
        # Close Button
        close_button = ttk.Button(self.isocenter_window, text="Close", command=self.isocenter_window.destroy)
        close_button.grid(row=3, column=1, pady=5)
        
    def save_isocenter_settings(self):
        """Save the isocenter settings to the designer."""
        method = self.method_var.get()
        if not method:
            messagebox.showwarning("Input Error", "Please select an isocenter method.")
            return
        # Forget previous settings
        if self.designer.isocenter_data:
            self.designer.isocenter_data = {}
        
        # Store the isocenter settings in the designer
        self.designer.isocenter_data = {
            "method": method,
            "roi_name": self.roi_var.get() if method == "Center of ROI" else "",
            "poi_name": self.poi_entry.get() if method == "User Defined POI" else ""
        }

        messagebox.showinfo("Settings Saved", "Isocenter settings have been saved.")
        self.isocenter_window.destroy()