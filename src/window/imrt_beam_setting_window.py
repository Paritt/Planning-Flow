import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class IMPT_beam_setting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for IMRT beam settings."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.beam_window = tk.Toplevel(parent)
        self.beam_window.title("IMPT Beam Settings")
        self.beam_window.geometry("1500x700")
        # Bold Title Label
        title_label = tk.Label(self.beam_window, text="IMPT Beam Settings", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Beams tree with scrollbar
        beam_tree_frame = ttk.Frame(self.beam_window)
        beam_tree_frame.pack(pady=5, fill="both", expand=True)
        
        beam_tree_scroll_y = ttk.Scrollbar(beam_tree_frame, orient="vertical")
        beam_tree_scroll_x = ttk.Scrollbar(beam_tree_frame, orient="horizontal")
        
        self.beam_tree = ttk.Treeview(beam_tree_frame, columns=("Beam name", "Gantry [deg]", "Couch [deg]", "Snout", "Range shifter"), 
                                       show="headings", yscrollcommand=beam_tree_scroll_y.set, xscrollcommand=beam_tree_scroll_x.set)
        
        beam_tree_scroll_y.config(command=self.beam_tree.yview)
        beam_tree_scroll_x.config(command=self.beam_tree.xview)
        
        self.beam_tree.heading("Beam name", text="Beam name")
        self.beam_tree.heading("Gantry [deg]", text="Gantry [deg]")
        self.beam_tree.heading("Couch [deg]", text="Couch [deg]")
        self.beam_tree.heading("Snout", text="Snout")
        self.beam_tree.heading("Range shifter", text="Range shifter")
        
        self.beam_tree.column("Beam name", width=150)
        self.beam_tree.column("Gantry [deg]", width=100)
        self.beam_tree.column("Couch [deg]", width=100)
        self.beam_tree.column("Snout", width=100)
        self.beam_tree.column("Range shifter", width=120)
        
        self.beam_tree.grid(row=0, column=0, sticky="nsew")
        beam_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        beam_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        beam_tree_frame.grid_rowconfigure(0, weight=1)
        beam_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Beam computation setting tree with scrollbar
        beam_comp_tree_frame = ttk.Frame(self.beam_window)
        beam_comp_tree_frame.pack(pady=5, fill="both", expand=True)
        
        beam_comp_tree_scroll_y = ttk.Scrollbar(beam_comp_tree_frame, orient="vertical")
        beam_comp_tree_scroll_x = ttk.Scrollbar(beam_comp_tree_frame, orient="horizontal")
        
        self.beam_comp_tree = ttk.Treeview(beam_comp_tree_frame, columns=("Beam name","Range shifter selection", "Spot pattern", "Energy layer spacing", "Spot spacing", 
                                                                "Angle", "Proximal margin [Layers]", "Distal margin [Layers]", "Lateral margin", "Min Radiol. depth [cm]", "Max Radiol. depth [cm]",
                                                                "ROI avoidance structures", "Layer repainting"), 
                                           show="headings", yscrollcommand=beam_comp_tree_scroll_y.set, xscrollcommand=beam_comp_tree_scroll_x.set)
        
        beam_comp_tree_scroll_y.config(command=self.beam_comp_tree.yview)
        beam_comp_tree_scroll_x.config(command=self.beam_comp_tree.xview)
        
        self.beam_comp_tree.heading("Beam name", text="Beam name")
        self.beam_comp_tree.heading("Range shifter selection", text="Range shifter selection")
        self.beam_comp_tree.heading("Spot pattern", text="Spot pattern")
        self.beam_comp_tree.heading("Energy layer spacing", text="Energy layer spacing")
        self.beam_comp_tree.heading("Spot spacing", text="Spot spacing")
        self.beam_comp_tree.heading("Angle", text="Angle")
        self.beam_comp_tree.heading("Proximal margin [Layers]", text="Proximal margin [Layers]")
        self.beam_comp_tree.heading("Distal margin [Layers]", text="Distal margin [Layers]")
        self.beam_comp_tree.heading("Lateral margin", text="Lateral margin")
        self.beam_comp_tree.heading("Min Radiol. depth [cm]", text="Min Radiol. depth [cm]")
        self.beam_comp_tree.heading("Max Radiol. depth [cm]", text="Max Radiol. depth [cm]")
        self.beam_comp_tree.heading("ROI avoidance structures", text="ROI avoidance structures")
        self.beam_comp_tree.heading("Layer repainting", text="Layer repainting")
        
        self.beam_comp_tree.column("Beam name", width=120)
        self.beam_comp_tree.column("Range shifter selection", width=150)
        self.beam_comp_tree.column("Spot pattern", width=100)
        self.beam_comp_tree.column("Energy layer spacing", width=140)
        self.beam_comp_tree.column("Spot spacing", width=100)
        self.beam_comp_tree.column("Angle", width=80)
        self.beam_comp_tree.column("Proximal margin [Layers]", width=160)
        self.beam_comp_tree.column("Distal margin [Layers]", width=160)
        self.beam_comp_tree.column("Lateral margin", width=120)
        self.beam_comp_tree.column("Min Radiol. depth [cm]", width=150)
        self.beam_comp_tree.column("Max Radiol. depth [cm]", width=150)
        self.beam_comp_tree.column("ROI avoidance structures", width=180)
        self.beam_comp_tree.column("Layer repainting", width=120)
        
        self.beam_comp_tree.grid(row=0, column=0, sticky="nsew")
        beam_comp_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        beam_comp_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        beam_comp_tree_frame.grid_rowconfigure(0, weight=1)
        beam_comp_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add Beam Button
        self.add_beam_btn = ttk.Button(self.beam_window, text="Add Beam", command=self.open_IMPT_add_beam_window)
        self.add_beam_btn.pack(side="left", padx=5, pady=5)
        # Remove Beam Button
        self.remove_beam_btn = ttk.Button(self.beam_window, text="Remove Selected Beam", command=lambda: self.show_step_info("Remove Beam"))
        self.remove_beam_btn.pack(side="left", padx=5, pady=5)
        # Edit Beam Button
        self.edit_beam_btn = ttk.Button(self.beam_window, text="Edit Selected Beam", command=lambda: self.show_step_info("Edit Beam"))
        self.edit_beam_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_beam_btn = ttk.Button(self.beam_window, text="Save", command=lambda: self.show_step_info("Beam Settings Saved"))
        self.save_beam_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        close_btn = ttk.Button(self.beam_window, text="Close", command=self.beam_window.destroy)
        close_btn.pack(pady=10)
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
    
    def open_IMPT_add_beam_window(self):
        """Open a new window to add IMPT beam."""
        self.add_beam_window = tk.Toplevel(self.beam_window)
        self.add_beam_window.title("Add IMPT Beam")
        self.add_beam_window.geometry("400x400")
        # Bold Title Label
        title_label = tk.Label(self.add_beam_window, text="Add IMPT Beam", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.add_beam_window, text="Beam Name:").grid(row=1, column=0, padx=5, pady=5)
        self.beam_name_var = tk.StringVar()
        self.beam_name_entry = ttk.Entry(self.add_beam_window, textvariable=self.beam_name_var)
        self.beam_name_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Gantry [deg]:").grid(row=2, column=0, padx=5, pady=5)
        self.gantry_var = tk.DoubleVar()
        self.gantry_entry = ttk.Entry(self.add_beam_window, textvariable=self.gantry_var)
        self.gantry_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Couch [deg]:").grid(row=3, column=0, padx=5, pady=5)
        self.couch_var = tk.DoubleVar()
        self.couch_entry = ttk.Entry(self.add_beam_window, textvariable=self.couch_var)
        self.couch_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Snout:").grid(row=4, column=0, padx=5, pady=5)
        self.snout_var = tk.StringVar()
        self.snout_combo = ttk.Combobox(self.add_beam_window, textvariable=self.snout_var, values=['SNOUT_M', 'NONE'], state="readonly")
        self.snout_combo.grid(row=4, column=1, padx=5, pady=5)
        self.snout_combo.set('NONE')
        tk.Label(self.add_beam_window, text="Range shifter:").grid(row=5, column=0, padx=5, pady=5)
        self.range_shifter_var = tk.StringVar()
        self.range_shifter_combo = ttk.Combobox(self.add_beam_window, textvariable=self.range_shifter_var, values=['(None)', 'RS40', 'RS40-M'], state="readonly")
        self.range_shifter_combo.grid(row=5, column=1, padx=5, pady=5)
        self.range_shifter_combo.set('(None)')
        
        # Beam Computational Settin button
        beam_comp_setting_btn = ttk.Button(self.add_beam_window, text="Beam Computational Settings", command=self.open_IMPT_beam_comp_setting_window)
        beam_comp_setting_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Add Beam Button
        add_beam_btn = ttk.Button(self.add_beam_window, text="Add Beam", command=lambda: self.add_beam(self.add_beam_window))
        add_beam_btn.grid(row=7, column=0, pady=10)
        
        # Close Button
        close_btn = ttk.Button(self.add_beam_window, text="Close", command=self.add_beam_window.destroy)
        close_btn.grid(row=7, column=1, pady=10)
    
    def open_IMPT_beam_comp_setting_window(self):
        """Open a new window for IMPT beam computational settings."""
        self.beam_comp_window = tk.Toplevel(self.add_beam_window)
        self.beam_comp_window.title("IMPT Beam Computational Settings")
        self.beam_comp_window.geometry("400x600")
        # Bold Title Label
        title_label = tk.Label(self.beam_comp_window, text="IMPT Beam Computational Settings", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Add settings fields here
        tk.Label(self.beam_comp_window, text="Range shifter selection:").grid(row=1, column=0, padx=5, pady=5)
        self.range_shifter_selection_var = tk.StringVar()
        self.range_shifter_selection_combo = ttk.Combobox(self.beam_comp_window, textvariable=self.range_shifter_selection_var, 
                                                          values=['Manual', 'Automatic'], state="readonly")
        self.range_shifter_selection_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # TODO: Add more settings fields here
        
        # Save Button
        save_btn = ttk.Button(self.beam_comp_window, text="Save Settings", command=lambda: self.show_step_info("Beam Computational Settings Saved"))
        save_btn.grid(row=9, column=0, columnspan=2, pady=10)
        
        # Close Button
        close_btn = ttk.Button(self.beam_comp_window, text="Close", command=self.beam_comp_window.destroy)
        close_btn.grid(row=10, column=0, columnspan=2, pady=10)
    
    def add_beam(self,popup):
        """Add a new beam to the beam tree."""
        beam_name = self.beam_name_var.get()
        gantry = self.gantry_var.get()
        couch = self.couch_var.get()
        snout = self.snout_var.get()
        range_shifter = self.range_shifter_var.get()
        self.beam_tree.insert("", "end", values=(beam_name, gantry, couch, snout, range_shifter))
        popup.destroy()
        