import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VMAT_beam_setting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for VMAT beam settings."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.beam_window = tk.Toplevel(parent)
        self.beam_window.title("VMAT Beam Settings")
        self.beam_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(self.beam_window, text="VMAT Beam Settings", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Beams tree with scrollbar
        beam_tree_frame = ttk.Frame(self.beam_window)
        beam_tree_frame.pack(pady=5, fill="both", expand=True)
        
        beam_tree_scroll_y = ttk.Scrollbar(beam_tree_frame, orient="vertical")
        beam_tree_scroll_x = ttk.Scrollbar(beam_tree_frame, orient="horizontal")
        
        self.beam_tree = ttk.Treeview(beam_tree_frame, columns=("Beam name", "Energy [MV]","Gantry Start [deg]", "Gantry Stop [deg]", "Rotation", "Coll. [deg]","Couch [deg]"), 
                                        show="headings", yscrollcommand=beam_tree_scroll_y.set, xscrollcommand=beam_tree_scroll_x.set)
        
        beam_tree_scroll_y.config(command=self.beam_tree.yview)
        beam_tree_scroll_x.config(command=self.beam_tree.xview)
        
        self.beam_tree.heading("Beam name", text="Beam name")
        self.beam_tree.heading("Energy [MV]", text="Energy [MV]")
        self.beam_tree.heading("Gantry Start [deg]", text="Gantry Start [deg]")
        self.beam_tree.heading("Gantry Stop [deg]", text="Gantry Stop [deg]")
        self.beam_tree.heading("Rotation", text="Rotation")
        self.beam_tree.heading("Coll. [deg]", text="Coll. [deg]")
        self.beam_tree.heading("Couch [deg]", text="Couch [deg]")
        
        self.beam_tree.column("Beam name", width=100)
        self.beam_tree.column("Energy [MV]", width=50)
        self.beam_tree.column("Gantry Start [deg]", width=50)
        self.beam_tree.column("Gantry Stop [deg]", width=50)
        self.beam_tree.column("Rotation", width=50)
        self.beam_tree.column("Coll. [deg]", width=50)
        self.beam_tree.column("Couch [deg]", width=50)
        
        self.beam_tree.grid(row=0, column=0, sticky="nsew")
        beam_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        beam_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        beam_tree_frame.grid_rowconfigure(0, weight=1)
        beam_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add Beam Button
        self.add_beam_btn = ttk.Button(self.beam_window, text="Add Beam", command=self.open_VMAT_add_beam_window)
        self.add_beam_btn.pack(side="left", padx=5, pady=5)
        # Remove Beam Button
        self.remove_beam_btn = ttk.Button(self.beam_window, text="Remove Selected Beam", command=self.remove_beam)
        self.remove_beam_btn.pack(side="left", padx=5, pady=5)
        # Edit Beam Button
        self.edit_beam_btn = ttk.Button(self.beam_window, text="Edit Selected Beam", command=self.edit_beam)
        self.edit_beam_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_beam_btn = ttk.Button(self.beam_window, text="Save", command=self.save_beam_settings)
        self.save_beam_btn.pack(side="left", padx=5, pady=5)
        # Close Button
        close_btn = ttk.Button(self.beam_window, text="Close", command=self.beam_window.destroy)
        close_btn.pack(pady=10)
        
        # Load existing beam data if available
        if self.designer.vmat_beam_data:
            for beam in self.designer.vmat_beam_data:
                self.beam_tree.insert("", "end", values=(beam["beam_name"], beam["energy"], beam["gantry_start"], beam["gantry_stop"], beam["rotation"], beam["collimator"], beam["couch"]))
    
    def open_VMAT_add_beam_window(self):
        """Open a new window to add a VMAT beam."""
        self.add_beam_window = tk.Toplevel(self.beam_window)
        self.add_beam_window.title("Add VMAT Beam")
        self.add_beam_window.geometry("300x330")
        # Bold Title Label
        title_label = tk.Label(self.add_beam_window, text="Add VMAT Beam", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.add_beam_window, text="Beam Name:").grid(row=1, column=0, padx=5, pady=5)
        self.beam_name_var = tk.StringVar()
        self.beam_name_entry = ttk.Entry(self.add_beam_window, textvariable=self.beam_name_var)
        self.beam_name_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Energy [MV]:").grid(row=2, column=0, padx=5, pady=5)
        self.energy_var = tk.StringVar()
        self.energy_combo = ttk.Combobox(self.add_beam_window, textvariable=self.energy_var, values=['6X', '10X', '15X'], state="readonly")
        self.energy_combo.grid(row=2, column=1, padx=5, pady=5)
        self.energy_combo.set('10X')
        tk.Label(self.add_beam_window, text="Gantry Start [deg]:").grid(row=3, column=0, padx=5, pady=5)
        self.gantry_start_var = tk.DoubleVar()
        self.gantry_start_entry = ttk.Entry(self.add_beam_window, textvariable=self.gantry_start_var)
        self.gantry_start_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Gantry Stop [deg]:").grid(row=4, column=0, padx=5, pady=5)
        self.gantry_stop_var = tk.DoubleVar()
        self.gantry_stop_entry = ttk.Entry(self.add_beam_window, textvariable=self.gantry_stop_var)
        self.gantry_stop_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Rotation:").grid(row=5, column=0, padx=5, pady=5)
        self.rotation_var = tk.StringVar()
        self.rotation_combo = ttk.Combobox(self.add_beam_window, textvariable=self.rotation_var, values=['CW', 'CCW'], state="readonly")
        self.rotation_combo.grid(row=5, column=1, padx=5, pady=5)
        self.rotation_combo.set('CW')
        tk.Label(self.add_beam_window, text="Collimator [deg]:").grid(row=6, column=0, padx=5, pady=5)
        self.collimator_var = tk.DoubleVar()
        self.collimator_entry = ttk.Entry(self.add_beam_window, textvariable=self.collimator_var)
        self.collimator_entry.grid(row=6, column=1, padx=5, pady=5)
        tk.Label(self.add_beam_window, text="Couch [deg]:").grid(row=7, column=0, padx=5, pady=5)
        self.couch_var = tk.DoubleVar()
        self.couch_entry = ttk.Entry(self.add_beam_window, textvariable=self.couch_var)
        self.couch_entry.grid(row=7, column=1, padx=5, pady=5)
        
        # Add Beam Button
        add_beam_btn = ttk.Button(self.add_beam_window, text="Add Beam", command=lambda: self.add_beam(self.add_beam_window))
        add_beam_btn.grid(row=8, column=0, pady=10)
        
        # Close Button
        close_btn = ttk.Button(self.add_beam_window, text="Close", command=self.add_beam_window.destroy)
        close_btn.grid(row=8, column=1, pady=10)
    
    def add_beam(self, popup):
        """Add a new beam to the beam tree."""
        beam_name = self.beam_name_var.get()
        energy = self.energy_var.get()
        gantry_start = self.gantry_start_var.get()
        gantry_stop = self.gantry_stop_var.get()
        rotation = self.rotation_var.get()
        couch = self.couch_var.get()
        collimator = self.collimator_var.get()
        if not beam_name:
            messagebox.showwarning("Input Error", "Please enter a Beam Name.")
            return
        
        self.beam_tree.insert("", "end", values=(beam_name, energy, gantry_start, gantry_stop, rotation, collimator, couch))
        popup.destroy()
    
    def remove_beam(self):
        """Remove the selected beam from the beam tree."""
        selected_item = self.beam_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a beam to remove.")
            return
        self.beam_tree.delete(selected_item)
    
    def edit_beam(self):
        """Edit the selected beam in the beam tree."""
        selected_item = self.beam_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a beam to edit.")
            return
        
        beam_values = self.beam_tree.item(selected_item, "values")
        
        self.edit_beam_window = tk.Toplevel(self.beam_window)
        self.edit_beam_window.title("Edit VMAT Beam")
        self.edit_beam_window.geometry("300x330")
        # Bold Title Label
        title_label = tk.Label(self.edit_beam_window, text="Edit VMAT Beam", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(self.edit_beam_window, text="Beam Name:").grid(row=1, column=0, padx=5, pady=5)
        self.edit_beam_name_var = tk.StringVar(value=beam_values[0])
        self.edit_beam_name_entry = ttk.Entry(self.edit_beam_window, textvariable=self.edit_beam_name_var)
        self.edit_beam_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.edit_beam_window, text="Energy [MV]:").grid(row=2, column=0, padx=5, pady=5)
        self.edit_energy_var = tk.StringVar(value=beam_values[1])
        self.edit_energy_combo = ttk.Combobox(self.edit_beam_window, textvariable=self.edit_energy_var, values=['6', '10', '15', '6 FFF', '10 FFF'], state="readonly")
        self.edit_energy_combo.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.edit_beam_window, text="Gantry Start [deg]:").grid(row=3, column=0, padx=5, pady=5)
        self.edit_gantry_start_var = tk.DoubleVar(value=beam_values[2])
        self.edit_gantry_start_entry = ttk.Entry(self.edit_beam_window, textvariable=self.edit_gantry_start_var)
        self.edit_gantry_start_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.edit_beam_window, text="Gantry Stop [deg]:").grid(row=4, column=0, padx=5, pady=5)
        self.edit_gantry_stop_var = tk.DoubleVar(value=beam_values[3])
        self.edit_gantry_stop_entry = ttk.Entry(self.edit_beam_window, textvariable=self.edit_gantry_stop_var)
        self.edit_gantry_stop_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Label(self.edit_beam_window, text="Rotation:").grid(row=5, column=0, padx=5, pady=5)
        self.edit_rotation_var = tk.StringVar(value=beam_values[4])
        self.edit_rotation_combo = ttk.Combobox(self.edit_beam_window, textvariable=self.edit_rotation_var, values=['CW', 'CCW'], state="readonly")
        self.edit_rotation_combo.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(self.edit_beam_window, text="Collimator [deg]:").grid(row=6, column=0, padx=5, pady=5)
        self.edit_collimator_var = tk.DoubleVar(value=beam_values[5])
        self.edit_collimator_entry = ttk.Entry(self.edit_beam_window, textvariable=self.edit_collimator_var)
        self.edit_collimator_entry.grid(row=6, column=1, padx=5, pady=5)
        
        tk.Label(self.edit_beam_window, text="Couch [deg]:").grid(row=7, column=0, padx=5, pady=5)
        self.edit_couch_var = tk.DoubleVar(value=beam_values[6])
        self.edit_couch_entry = ttk.Entry(self.edit_beam_window, textvariable=self.edit_couch_var)
        self.edit_couch_entry.grid(row=7, column=1, padx=5, pady=5)
        # Save Changes Button
        save_changes_btn = ttk.Button(self.edit_beam_window, text="Save Changes", command=lambda: self.save_beam_changes(selected_item))
        save_changes_btn.grid(row=8, column=0, pady=10)
        # Close Button
        close_btn = ttk.Button(self.edit_beam_window, text="Close", command=self.edit_beam_window.destroy)
        close_btn.grid(row=8, column=1, pady=10)
        
    def save_beam_changes(self, item):
        """Save the changes made to the selected beam."""
        beam_name = self.edit_beam_name_var.get()
        energy = self.edit_energy_var.get()
        gantry_start = self.edit_gantry_start_var.get()
        gantry_stop = self.edit_gantry_stop_var.get()
        rotation = self.edit_rotation_var.get()
        collimator = self.edit_collimator_var.get()
        couch = self.edit_couch_var.get()
        
        if not beam_name:
            messagebox.showwarning("Input Error", "Please enter a Beam Name.")
            return
        
        self.beam_tree.item(item, values=(beam_name, energy, gantry_start, gantry_stop, rotation, collimator, couch))
        self.edit_beam_window.destroy()
        
    def save_beam_settings(self):
        """Save the current beam settings."""
        beam_items = []
        for child in self.beam_tree.get_children():
            values = self.beam_tree.item(child, "values")
            beam_items.append({
                "beam_name": values[0],
                "energy": values[1],
                "gantry_start": values[2],
                "gantry_stop": values[3],
                "rotation": values[4],
                "collimator": values[5],
                "couch": values[6]
            })
        self.designer.vmat_beam_data = beam_items
        messagebox.showinfo("Save Successful", "VMAT Beam settings have been saved.")
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
