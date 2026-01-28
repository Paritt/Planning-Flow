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
        
        # Storage for beam computational settings linked by beam name
        self.beam_comp_settings = {}
        
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
                                           show="headings", yscrollcommand=beam_comp_tree_scroll_y.set, xscrollcommand=beam_comp_tree_scroll_x.set, selectmode='none')
        
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
        self.remove_beam_btn = ttk.Button(self.beam_window, text="Remove Selected Beam", command=self.remove_beam)
        self.remove_beam_btn.pack(side="left", padx=5, pady=5)
        # Edit Beam Button
        self.edit_beam_btn = ttk.Button(self.beam_window, text="Edit Selected Beam", command=self.edit_beam)
        self.edit_beam_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_beam_btn = ttk.Button(self.beam_window, text="Save", command=self.save_IMPT_beam_settings)
        self.save_beam_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        close_btn = ttk.Button(self.beam_window, text="Close", command=self.beam_window.destroy)
        close_btn.pack(pady=10)
        
        # Load existing beam data if available
        if self.designer.impt_beam_data:
            self.load_beam_data(self.designer.impt_beam_data)
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
    
    def save_IMPT_beam_settings(self):
        """Save IMPT beam settings to designer."""
        # Collect beam data from tree
        beam_data = []
        for item in self.beam_tree.get_children():
            values = self.beam_tree.item(item, 'values')
            beam_name = values[0]
            
            # Create beam entry with basic settings
            beam_entry = {
                "beam_name": beam_name,
                "gantry": str(values[1]),
                "couch": str(values[2]),
                "snout": values[3],
                "range_shifter": values[4]
            }
            
            # Add computational settings if they exist
            if beam_name in self.beam_comp_settings:
                comp = self.beam_comp_settings[beam_name]
                beam_entry["comp_settings"] = {
                    "range_shifter_selection": comp['range_shifter_selection'],
                    "spot_pattern": comp['spot_pattern'],
                    "energy_layer_spacing_method": comp['energy_layer_spacing_method'],
                    "energy_layer_spacing_scale": str(comp['energy_layer_spacing_scale']),
                    "spot_spacing_method": comp['spot_spacing_method'],
                    "spot_spacing_scale": str(comp['spot_spacing_scale']),
                    "angle": str(comp['angle']),
                    "proximal_margin": str(comp['proximal_margin']),
                    "distal_margin": str(comp['distal_margin']),
                    "lateral_margin_method": comp['lateral_margin_method'],
                    "lateral_margin_scale": str(comp['lateral_margin_scale']),
                    "min_radiologic_depth": str(comp['min_radiologic_depth']),
                    "max_radiologic_depth": str(comp['max_radiologic_depth']),
                    "avoidance_rois": comp['avoidance_rois'],
                    "avoidance_proximal_margin": str(comp['avoidance_proximal_margin']),
                    "layer_repainting_method": comp['layer_repainting_method'],
                    "layer_repainting_value": str(comp['layer_repainting_value'])
                }
            
            beam_data.append(beam_entry)
        
        # Save to designer
        self.designer.impt_beam_data = beam_data
        messagebox.showinfo("Success", "IMPT beam settings saved successfully!")
    
    def load_beam_data(self, beam_data):
        """Load existing beam data into the trees."""
        for beam_entry in beam_data:
            beam_name = beam_entry.get("beam_name", "")
            gantry = float(beam_entry.get("gantry", 0))
            couch = float(beam_entry.get("couch", 0))
            snout = beam_entry.get("snout", "NONE")
            range_shifter = beam_entry.get("range_shifter", "(None)")
            
            # Add to beam tree
            self.beam_tree.insert("", "end", values=(beam_name, gantry, couch, snout, range_shifter))
            
            # Load computational settings if they exist
            if "comp_settings" in beam_entry:
                comp = beam_entry["comp_settings"]
                self.beam_comp_settings[beam_name] = {
                    'range_shifter_selection': comp.get('range_shifter_selection', 'Automatic'),
                    'spot_pattern': comp.get('spot_pattern', 'Hexagonal'),
                    'energy_layer_spacing_method': comp.get('energy_layer_spacing_method', 'Automatic with scale'),
                    'energy_layer_spacing_scale': float(comp.get('energy_layer_spacing_scale', 1.0)),
                    'spot_spacing_method': comp.get('spot_spacing_method', 'Automatic with scale'),
                    'spot_spacing_scale': float(comp.get('spot_spacing_scale', 1.0)),
                    'angle': float(comp.get('angle', 0.0)),
                    'proximal_margin': int(comp.get('proximal_margin', 1)),
                    'distal_margin': int(comp.get('distal_margin', 1)),
                    'lateral_margin_method': comp.get('lateral_margin_method', 'Automatic with scale'),
                    'lateral_margin_scale': float(comp.get('lateral_margin_scale', 1.0)),
                    'min_radiologic_depth': float(comp.get('min_radiologic_depth', 0.0)),
                    'max_radiologic_depth': float(comp.get('max_radiologic_depth', 0.0)),
                    'avoidance_rois': comp.get('avoidance_rois', []),
                    'avoidance_proximal_margin': float(comp.get('avoidance_proximal_margin', 0.0)),
                    'layer_repainting_method': comp.get('layer_repainting_method', 'No. of paintings'),
                    'layer_repainting_value': int(comp.get('layer_repainting_value', 1))
                }
                
                # Format display strings
                energy_spacing_display = f"{self.beam_comp_settings[beam_name]['energy_layer_spacing_method']}: {self.beam_comp_settings[beam_name]['energy_layer_spacing_scale']}"
                spot_spacing_display = f"{self.beam_comp_settings[beam_name]['spot_spacing_method']}: {self.beam_comp_settings[beam_name]['spot_spacing_scale']}"
                lateral_margin_display = f"{self.beam_comp_settings[beam_name]['lateral_margin_method']}: {self.beam_comp_settings[beam_name]['lateral_margin_scale']}"
                roi_display = ", ".join(self.beam_comp_settings[beam_name]['avoidance_rois']) if self.beam_comp_settings[beam_name]['avoidance_rois'] else "(None)"
                if len(roi_display) > 30:
                    roi_display = roi_display[:27] + "..."
                layer_repainting_display = f"{self.beam_comp_settings[beam_name]['layer_repainting_method']}: {self.beam_comp_settings[beam_name]['layer_repainting_value']}"
                
                # Add to beam comp tree
                self.beam_comp_tree.insert("", "end", values=(
                    beam_name,
                    self.beam_comp_settings[beam_name]['range_shifter_selection'],
                    self.beam_comp_settings[beam_name]['spot_pattern'],
                    energy_spacing_display,
                    spot_spacing_display,
                    self.beam_comp_settings[beam_name]['angle'],
                    self.beam_comp_settings[beam_name]['proximal_margin'],
                    self.beam_comp_settings[beam_name]['distal_margin'],
                    lateral_margin_display,
                    self.beam_comp_settings[beam_name]['min_radiologic_depth'],
                    self.beam_comp_settings[beam_name]['max_radiologic_depth'],
                    roi_display,
                    layer_repainting_display
                ))
    
    def edit_beam(self):
        """Edit selected beam settings."""
        # Get selected items from beam tree only
        selected_beam = self.beam_tree.selection()
        
        if not selected_beam:
            messagebox.showwarning("No Selection", "Please select a beam to edit from the beam tree.")
            return
        
        beam_values = self.beam_tree.item(selected_beam[0], 'values')
        beam_name = beam_values[0]
        
        # Store original beam name for updating
        self.original_beam_name = beam_name
        
        # Get beam data from beam_tree
        gantry_val = 0
        couch_val = 0
        snout_val = 'NONE'
        range_shifter_val = '(None)'
        
        for item in self.beam_tree.get_children():
            if self.beam_tree.item(item, 'values')[0] == beam_name:
                beam_values = self.beam_tree.item(item, 'values')
                gantry_val = float(beam_values[1])
                couch_val = float(beam_values[2])
                snout_val = beam_values[3]
                range_shifter_val = beam_values[4]
                break
        
        # Open the add beam window
        self.add_beam_window = tk.Toplevel(self.beam_window)
        self.add_beam_window.title("Edit IMPT Beam")
        self.add_beam_window.geometry("250x300")
        
        # Title label
        title_label = tk.Label(self.add_beam_window, text="Edit IMPT Beam", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Beam name (editable)
        tk.Label(self.add_beam_window, text="Beam Name:").grid(row=1, column=0, padx=5, pady=5)
        self.beam_name_var = tk.StringVar(value=beam_name)
        self.beam_name_entry = ttk.Entry(self.add_beam_window, textvariable=self.beam_name_var)
        self.beam_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.add_beam_window, text="Gantry [deg]:").grid(row=2, column=0, padx=5, pady=5)
        self.gantry_var = tk.DoubleVar(value=gantry_val)
        self.gantry_entry = ttk.Entry(self.add_beam_window, textvariable=self.gantry_var)
        self.gantry_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.add_beam_window, text="Couch [deg]:").grid(row=3, column=0, padx=5, pady=5)
        self.couch_var = tk.DoubleVar(value=couch_val)
        self.couch_entry = ttk.Entry(self.add_beam_window, textvariable=self.couch_var)
        self.couch_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self.add_beam_window, text="Snout:").grid(row=4, column=0, padx=5, pady=5)
        self.snout_var = tk.StringVar(value=snout_val)
        self.snout_combo = ttk.Combobox(self.add_beam_window, textvariable=self.snout_var, values=['SNOUT_M', 'NONE'], state="readonly")
        self.snout_combo.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self.add_beam_window, text="Range shifter:").grid(row=5, column=0, padx=5, pady=5)
        self.range_shifter_var = tk.StringVar(value=range_shifter_val)
        self.range_shifter_combo = ttk.Combobox(self.add_beam_window, textvariable=self.range_shifter_var, values=['(None)', 'RS40', 'RS40-M'], state="readonly")
        self.range_shifter_combo.grid(row=5, column=1, padx=5, pady=5)
        
        # Beam Computational Settings button
        beam_comp_setting_btn = ttk.Button(self.add_beam_window, text="Beam Computational Settings", command=self.open_IMPT_beam_comp_setting_window)
        beam_comp_setting_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Update Beam Button (instead of Add)
        update_beam_btn = ttk.Button(self.add_beam_window, text="Update Beam", command=lambda: self.update_beam(self.add_beam_window))
        update_beam_btn.grid(row=7, column=0, pady=10)
        
        # Close Button
        close_btn = ttk.Button(self.add_beam_window, text="Close", command=self.add_beam_window.destroy)
        close_btn.grid(row=7, column=1, pady=10)

    
    def remove_beam(self):
        """Remove selected beam from both trees."""
        # Get selected items from beam tree only
        selected_beam = self.beam_tree.selection()
        
        if not selected_beam:
            messagebox.showwarning("No Selection", "Please select a beam to remove from the beam tree.")
            return
        
        beam_values = self.beam_tree.item(selected_beam[0], 'values')
        beam_name = beam_values[0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove beam '{beam_name}'?"):
            # Remove from beam tree
            for item in self.beam_tree.get_children():
                if self.beam_tree.item(item, 'values')[0] == beam_name:
                    self.beam_tree.delete(item)
                    break
            
            # Remove from beam comp tree
            for item in self.beam_comp_tree.get_children():
                comp_values = self.beam_comp_tree.item(item, 'values')
                if comp_values[0] == beam_name:
                    self.beam_comp_tree.delete(item)
                    break
            
            # Remove from computational settings dictionary
            if beam_name in self.beam_comp_settings:
                del self.beam_comp_settings[beam_name]
            
            messagebox.showinfo("Removed", f"Beam '{beam_name}' has been removed.")
    
    def open_roi_selection_window(self):
        """Open a window with checkboxes for ROI selection."""
        roi_window = tk.Toplevel(self.beam_comp_window)
        roi_window.title("Select Avoidance ROIs")
        roi_window.geometry("400x450")
        
        # Title
        tk.Label(roi_window, text="Select ROIs for avoidance:", font=("Arial", 10, "bold")).pack(pady=10)
        
        # Get available ROIs from designer
        available_rois = self.designer.get_roi_list()
        
        # Frame 1: Scrollable ROI selection area (canvas is needed because tkinter doesn't have native scrollable frames)
        scrollable_area = ttk.Frame(roi_window)
        scrollable_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        canvas = tk.Canvas(scrollable_area, height=250)
        scrollbar = ttk.Scrollbar(scrollable_area, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create checkbox variables
        checkbox_vars = {}
        for roi in available_rois:
            var = tk.BooleanVar(value=roi in self.selected_avoidance_rois)
            checkbox_vars[roi] = var
            ttk.Checkbutton(scrollable_frame, text=roi, variable=var).pack(anchor="w", padx=20, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def apply_selection():
            self.selected_avoidance_rois = [roi for roi, var in checkbox_vars.items() if var.get()]
            if self.selected_avoidance_rois:
                display_text = ", ".join(self.selected_avoidance_rois)
                if len(display_text) > 40:
                    display_text = display_text[:37] + "..."
                self.roi_avoidance_structures_var.set(display_text)
            else:
                self.roi_avoidance_structures_var.set("(Select ROIs)")
            roi_window.destroy()
        
        def select_all():
            for var in checkbox_vars.values():
                var.set(True)
        
        def deselect_all():
            for var in checkbox_vars.values():
                var.set(False)
        
        # Frame 2: Fixed button frame at bottom (won't scroll)
        btn_frame = ttk.Frame(roi_window)
        btn_frame.pack(side="bottom", pady=10)
        
        ttk.Button(btn_frame, text="Select All", command=select_all).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Deselect All", command=deselect_all).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Apply", command=apply_selection).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=roi_window.destroy).pack(side='left', padx=5)
    
    def open_IMPT_add_beam_window(self):
        """Open a new window to add IMPT beam."""
        self.add_beam_window = tk.Toplevel(self.beam_window)
        self.add_beam_window.title("Add IMPT Beam")
        self.add_beam_window.geometry("250x300")
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
        # Check if beam name is defined
        if not self.beam_name_var.get():
            messagebox.showwarning("Missing Beam Name", "Please enter a beam name before configuring computational settings.")
            return
        
        self.beam_comp_window = tk.Toplevel(self.add_beam_window)
        self.beam_comp_window.title("IMPT Beam Computational Settings")
        self.beam_comp_window.geometry("400x720")
        # Bold Title Label
        title_label = tk.Label(self.beam_comp_window, text="IMPT Beam Computational Settings", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, padx=5, sticky="w")
        
        # IMPT Beam Computational Settings
        
        ## Range shifter selection
        range_shifter_selection_frame = ttk.Labelframe(self.beam_comp_window, text="Range Shifter Selection")
        range_shifter_selection_frame.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        self.range_shifter_selection_var = tk.StringVar()
        self.range_shifter_selection_combo = ttk.Combobox(range_shifter_selection_frame, textvariable=self.range_shifter_selection_var, 
                                                          values=['Manual', 'Automatic'], state="readonly")
        self.range_shifter_selection_combo.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.range_shifter_selection_combo.set('Automatic')
        
        ## Spot placement
        spot_placement_frame = ttk.Labelframe(self.beam_comp_window, text="Spot Placement")
        spot_placement_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        tk.Label(spot_placement_frame, text="Spot Pattern:").grid(row=0, column=0, padx=5, pady=5)
        self.spot_pattern_var = tk.StringVar()
        self.spot_pattern_combo = ttk.Combobox(spot_placement_frame, textvariable=self.spot_pattern_var, 
                                            values=['Square', 'Hexagonal'], state="readonly")
        self.spot_pattern_combo.grid(row=0, column=1, padx=5, pady=5)
        self.spot_pattern_combo.set('Hexagonal')
        tk.Label(spot_placement_frame, text="Energy Layer Spacing:").grid(row=1, column=0, padx=5, pady=5)
        self.energy_layer_spacing_method_var = tk.StringVar()
        self.energy_layer_spacing_method_combo = ttk.Combobox(spot_placement_frame, textvariable=self.energy_layer_spacing_method_var, 
                                                            values=['Automatic with scale', 'Constant [cm water]'], state="readonly")
        self.energy_layer_spacing_method_combo.grid(row=1, column=1, padx=5, pady=5)
        self.energy_layer_spacing_method_combo.set('Automatic with scale')
        self.energy_layer_spacing_scale_var = tk.DoubleVar()
        self.energy_layer_spacing_scale_entry = ttk.Entry(spot_placement_frame, textvariable=self.energy_layer_spacing_scale_var, width=5)
        self.energy_layer_spacing_scale_entry.grid(row=1, column=2, padx=5, pady=5)
        self.energy_layer_spacing_scale_var.set(1.0)
        tk.Label(spot_placement_frame, text="Spot Spacing:").grid(row=3, column=0, padx=5, pady=5)
        self.spot_spacing_method_var = tk.StringVar()
        self.spot_spacing_method_combo = ttk.Combobox(spot_placement_frame, textvariable=self.spot_spacing_method_var, 
                                                    values=['Automatic with scale', 'Constant [cm]'], state="readonly")
        self.spot_spacing_method_combo.grid(row=3, column=1, padx=5, pady=5)
        self.spot_spacing_method_combo.set('Automatic with scale')
        self.spot_spacing_scale_var = tk.DoubleVar()
        self.spot_spacing_scale_entry = ttk.Entry(spot_placement_frame, textvariable=self.spot_spacing_scale_var, width=5)
        self.spot_spacing_scale_entry.grid(row=3, column=2, padx=5, pady=5)
        self.spot_spacing_scale_var.set(1.0)
        tk.Label(spot_placement_frame, text="Angle [deg]:").grid(row=4, column=0, padx=5, pady=5)
        self.angle_var = tk.DoubleVar()
        self.angle_entry = ttk.Entry(spot_placement_frame, textvariable=self.angle_var)
        self.angle_entry.grid(row=4, column=1, padx=5, pady=5)
        self.angle_var.set(0.0)
        
        ## Target margins
        target_margins_frame = ttk.Labelframe(self.beam_comp_window, text="Target Margins")
        target_margins_frame.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        tk.Label(target_margins_frame, text="Proximal [Layers]:").grid(row=0, column=0, padx=5, pady=5)
        self.proximal_target_layer_margin_var = tk.IntVar()
        self.proximal_target_layer_margin_entry = ttk.Entry(target_margins_frame, textvariable=self.proximal_target_layer_margin_var)
        self.proximal_target_layer_margin_entry.grid(row=0, column=1, padx=5, pady=5)
        self.proximal_target_layer_margin_var.set(1)
        tk.Label(target_margins_frame, text="Distal [Layers]:").grid(row=1, column=0, padx=5, pady=5)
        self.distal_target_layer_margin_var = tk.IntVar()
        self.distal_target_layer_margin_entry = ttk.Entry(target_margins_frame, textvariable=self.distal_target_layer_margin_var)
        self.distal_target_layer_margin_entry.grid(row=1, column=1, padx=5, pady=5)
        self.distal_target_layer_margin_var.set(1)
        tk.Label(target_margins_frame, text="Lateral:").grid(row=2, column=0, padx=5, pady=5)
        self.lateral_margin_scale_method_var = tk.StringVar()
        self.lateral_margin_scale_method_combo = ttk.Combobox(target_margins_frame, textvariable=self.lateral_margin_scale_method_var, 
                                                            values=['Automatic with scale', 'Constant [cm]'], state="readonly")
        self.lateral_margin_scale_method_combo.grid(row=2, column=1, padx=5, pady=5)
        self.lateral_margin_scale_method_combo.set('Automatic with scale')
        self.lateral_margin_scale_var = tk.DoubleVar()
        self.lateral_margin_scale_entry = ttk.Entry(target_margins_frame, textvariable=self.lateral_margin_scale_var, width=5)
        self.lateral_margin_scale_entry.grid(row=2, column=2, padx=5, pady=5)
        self.lateral_margin_scale_var.set(1.0)
        
        ## Radiologic depth 
        radiologic_depth_frame = ttk.Labelframe(self.beam_comp_window, text="Radiologic Depth [cm]")
        radiologic_depth_frame.grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        tk.Label(radiologic_depth_frame, text="Min:").grid(row=0, column=0, padx=5, pady=5)
        self.min_radiologic_depth_margin_var = tk.DoubleVar()
        self.min_radiologic_depth_margin_entry = ttk.Entry(radiologic_depth_frame, textvariable=self.min_radiologic_depth_margin_var)
        self.min_radiologic_depth_margin_entry.grid(row=0, column=1, padx=5, pady=5)
        self.min_radiologic_depth_margin_var.set(0.0)
        tk.Label(radiologic_depth_frame, text="Max:").grid(row=1, column=0, padx=5, pady=5)
        self.max_radiologic_depth_margin_var = tk.DoubleVar()
        self.max_radiologic_depth_margin_entry = ttk.Entry(radiologic_depth_frame, textvariable=self.max_radiologic_depth_margin_var)
        self.max_radiologic_depth_margin_entry.grid(row=1, column=1, padx=5, pady=5)
        self.max_radiologic_depth_margin_var.set(0.0)
        
        ## Avoidance structures ROIs
        avoidance_structures_frame = ttk.Labelframe(self.beam_comp_window, text="Avoidance Structures ROIs")
        avoidance_structures_frame.grid(row=5, column=0, columnspan=3, pady=5, padx=5, sticky="w")
        tk.Label(avoidance_structures_frame, text="ROI Names:").grid(row=0, column=0, padx=5, pady=5)
        
        # Dropdown checkbox for ROI selection
        self.roi_avoidance_structures_var = tk.StringVar()
        self.roi_avoidance_structures_var.set("(Select ROIs)")
        self.selected_avoidance_rois = []
        
        self.roi_dropdown_btn = ttk.Button(avoidance_structures_frame, 
                                          textvariable=self.roi_avoidance_structures_var,
                                          command=self.open_roi_selection_window,
                                          width=30)
        self.roi_dropdown_btn.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(avoidance_structures_frame, text="Proximal margin [cm]:").grid(row=1, column=0, padx=5, pady=5)
        self.avoidance_proximal_margin_var = tk.DoubleVar()
        self.avoidance_proximal_margin_entry = ttk.Entry(avoidance_structures_frame, textvariable=self.avoidance_proximal_margin_var)
        self.avoidance_proximal_margin_entry.grid(row=1, column=1, padx=5, pady=5)
        self.avoidance_proximal_margin_var.set(0.0)
        
        ## Layer repainting
        layer_repainting_frame = ttk.Labelframe(self.beam_comp_window, text="Layer Repainting")
        layer_repainting_frame.grid(row=6, column=0, columnspan=3, pady=5, sticky="w")
        self.layer_repainting_method_var = tk.StringVar()
        self.layer_repainting_method_combo = ttk.Combobox(layer_repainting_frame, textvariable=self.layer_repainting_method_var, 
                                                        values=['No. of paintings', 'Max MU/layer painting', 'Max MU/repainted spot'], state="readonly")
        self.layer_repainting_method_combo.grid(row=0, column=0, padx=5, pady=5)
        self.layer_repainting_method_combo.set('No. of paintings')
        self.fixed_number_of_paintings_var = tk.IntVar()
        self.fixed_number_of_paintings_entry = ttk.Entry(layer_repainting_frame, textvariable=self.fixed_number_of_paintings_var, width=5)
        self.fixed_number_of_paintings_entry.grid(row=0, column=1, padx=5, pady=5)
        self.fixed_number_of_paintings_var.set(1)
        
        # Save Button
        save_btn = ttk.Button(self.beam_comp_window, text="Save Settings", command=self.save_comp_settings)
        save_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Close Button
        close_btn = ttk.Button(self.beam_comp_window, text="Close", command=self.beam_comp_window.destroy)
        close_btn.grid(row=8, column=0, columnspan=2, pady=10)
    
    def save_comp_settings(self):
        """Save the beam computational settings for the current beam."""
        beam_name = self.beam_name_var.get()
        
        if not beam_name:
            messagebox.showwarning("Missing Beam Name", "Please enter a beam name first.")
            return
        
        # Collect all computational settings
        self.beam_comp_settings[beam_name] = {
            'range_shifter_selection': self.range_shifter_selection_var.get(),
            'spot_pattern': self.spot_pattern_var.get(),
            'energy_layer_spacing_method': self.energy_layer_spacing_method_var.get(),
            'energy_layer_spacing_scale': self.energy_layer_spacing_scale_var.get(),
            'spot_spacing_method': self.spot_spacing_method_var.get(),
            'spot_spacing_scale': self.spot_spacing_scale_var.get(),
            'angle': self.angle_var.get(),
            'proximal_margin': self.proximal_target_layer_margin_var.get(),
            'distal_margin': self.distal_target_layer_margin_var.get(),
            'lateral_margin_method': self.lateral_margin_scale_method_var.get(),
            'lateral_margin_scale': self.lateral_margin_scale_var.get(),
            'min_radiologic_depth': self.min_radiologic_depth_margin_var.get(),
            'max_radiologic_depth': self.max_radiologic_depth_margin_var.get(),
            'avoidance_rois': self.selected_avoidance_rois.copy(),
            'avoidance_proximal_margin': self.avoidance_proximal_margin_var.get(),
            'layer_repainting_method': self.layer_repainting_method_var.get(),
            'layer_repainting_value': self.fixed_number_of_paintings_var.get()
        }
        
        messagebox.showinfo("Settings Saved", f"Beam computational settings saved for '{beam_name}'")
        self.beam_comp_window.destroy()
    
    def add_beam(self, popup):
        """Add a new beam to both beam tree and computational settings tree."""
        beam_name = self.beam_name_var.get()
        
        if not beam_name:
            messagebox.showwarning("Missing Beam Name", "Please enter a beam name.")
            return
        
        # Check if beam name already exists
        for item in self.beam_tree.get_children():
            if self.beam_tree.item(item, 'values')[0] == beam_name:
                messagebox.showwarning("Duplicate Beam Name", f"Beam name '{beam_name}' already exists. Please choose a different name.")
                return
        
        # If computational settings don't exist for this beam, create default values
        if beam_name not in self.beam_comp_settings:
            self.beam_comp_settings[beam_name] = {
                'range_shifter_selection': 'Automatic',
                'spot_pattern': 'Hexagonal',
                'energy_layer_spacing_method': 'Automatic with scale',
                'energy_layer_spacing_scale': 1.0,
                'spot_spacing_method': 'Automatic with scale',
                'spot_spacing_scale': 1.0,
                'angle': 0.0,
                'proximal_margin': 1,
                'distal_margin': 1,
                'lateral_margin_method': 'Automatic with scale',
                'lateral_margin_scale': 1.0,
                'min_radiologic_depth': 0.0,
                'max_radiologic_depth': 0.0,
                'avoidance_rois': [],
                'avoidance_proximal_margin': 0.0,
                'layer_repainting_method': 'No. of paintings',
                'layer_repainting_value': 1
            }
        
        gantry = self.gantry_var.get()
        couch = self.couch_var.get()
        snout = self.snout_var.get()
        range_shifter = self.range_shifter_var.get()
        
        # Add to beam tree
        self.beam_tree.insert("", "end", values=(beam_name, gantry, couch, snout, range_shifter))
        
        # Get computational settings
        comp = self.beam_comp_settings[beam_name]
        
        # Format display strings
        energy_spacing_display = f"{comp['energy_layer_spacing_method']}: {comp['energy_layer_spacing_scale']}"
        spot_spacing_display = f"{comp['spot_spacing_method']}: {comp['spot_spacing_scale']}"
        lateral_margin_display = f"{comp['lateral_margin_method']}: {comp['lateral_margin_scale']}"
        roi_display = ", ".join(comp['avoidance_rois']) if comp['avoidance_rois'] else "(None)"
        if len(roi_display) > 30:
            roi_display = roi_display[:27] + "..."
        layer_repainting_display = f"{comp['layer_repainting_method']}: {comp['layer_repainting_value']}"
        
        # Add to beam computational tree
        self.beam_comp_tree.insert("", "end", values=(
            beam_name,
            comp['range_shifter_selection'],
            comp['spot_pattern'],
            energy_spacing_display,
            spot_spacing_display,
            comp['angle'],
            comp['proximal_margin'],
            comp['distal_margin'],
            lateral_margin_display,
            comp['min_radiologic_depth'],
            comp['max_radiologic_depth'],
            roi_display,
            layer_repainting_display
        ))
        
        popup.destroy()
    
    def update_beam(self, popup):
        """Update an existing beam with new settings."""
        new_beam_name = self.beam_name_var.get()
        
        if not new_beam_name:
            messagebox.showwarning("Missing Beam Name", "Please enter a beam name.")
            return
        
        # Check if beam name changed and new name already exists
        if new_beam_name != self.original_beam_name:
            for item in self.beam_tree.get_children():
                if self.beam_tree.item(item, 'values')[0] == new_beam_name:
                    messagebox.showwarning("Duplicate Beam Name", f"Beam name '{new_beam_name}' already exists. Please choose a different name.")
                    return
        
        gantry = self.gantry_var.get()
        couch = self.couch_var.get()
        snout = self.snout_var.get()
        range_shifter = self.range_shifter_var.get()
        
        # Update in beam tree (use original name to find)
        for item in self.beam_tree.get_children():
            if self.beam_tree.item(item, 'values')[0] == self.original_beam_name:
                self.beam_tree.item(item, values=(new_beam_name, gantry, couch, snout, range_shifter))
                break
        
        # Update computational settings dictionary key if beam name changed
        if new_beam_name != self.original_beam_name and self.original_beam_name in self.beam_comp_settings:
            self.beam_comp_settings[new_beam_name] = self.beam_comp_settings.pop(self.original_beam_name)
        
        # Update in beam comp tree if settings exist
        if new_beam_name in self.beam_comp_settings:
            comp = self.beam_comp_settings[new_beam_name]
            
            # Format display strings
            energy_spacing_display = f"{comp['energy_layer_spacing_method']}: {comp['energy_layer_spacing_scale']}"
            spot_spacing_display = f"{comp['spot_spacing_method']}: {comp['spot_spacing_scale']}"
            lateral_margin_display = f"{comp['lateral_margin_method']}: {comp['lateral_margin_scale']}"
            roi_display = ", ".join(comp['avoidance_rois']) if comp['avoidance_rois'] else "(None)"
            if len(roi_display) > 30:
                roi_display = roi_display[:27] + "..."
            layer_repainting_display = f"{comp['layer_repainting_method']}: {comp['layer_repainting_value']}"
            
            for item in self.beam_comp_tree.get_children():
                if self.beam_comp_tree.item(item, 'values')[0] == self.original_beam_name:
                    self.beam_comp_tree.item(item, values=(
                        new_beam_name,
                        comp['range_shifter_selection'],
                        comp['spot_pattern'],
                        energy_spacing_display,
                        spot_spacing_display,
                        comp['angle'],
                        comp['proximal_margin'],
                        comp['distal_margin'],
                        lateral_margin_display,
                        comp['min_radiologic_depth'],
                        comp['max_radiologic_depth'],
                        roi_display,
                        layer_repainting_display
                    ))
                    break
        
        messagebox.showinfo("Updated", f"Beam '{new_beam_name}' has been updated successfully.")
        popup.destroy()
        