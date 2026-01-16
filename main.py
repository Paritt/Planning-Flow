import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class AutoPlanGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Planning Flow 🍃")
        self.geometry("570x150")

        # Treatment Parameters Section
        self.create_treatment_settings()

        # Workflow Section
        self.create_workflow_controls()

        # Loaded Workflow Data
        self.workflow_data = {}
        self.planning_window = None

    def create_treatment_settings(self):
        """Create treatment room and flow selection."""
        frame = ttk.LabelFrame(self, text="Treatment Settings")
        frame.pack(fill="x", padx=10, pady=5)

        # Treatment Room Dropdown
        ttk.Label(frame, text="Treatment Room:").grid(row=0, column=0, padx=5, pady=2)
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(frame, textvariable=self.room_var,
                                          values=['N3_VersaHD', 'N4_VersaHD', 'TrueBeam_L6', 'TrueBeam_L7', 'TrueBeam_N5'], state="readonly")
        self.room_dropdown.grid(row=0, column=1, padx=5, pady=2)

        # Planning Flow (Read-only)
        ttk.Label(frame, text="Planning Flow:").grid(row=1, column=0, padx=5, pady=2)
        self.flow_entry = ttk.Entry(frame, state="readonly")
        self.flow_entry.grid(row=1, column=1, padx=5, pady=2)

        # Load Flow Button
        self.load_flow_button = ttk.Button(frame, text="Load Flow", command=self.load_flow)
        self.load_flow_button.grid(row=1, column=2, padx=5, pady=2)

    def create_workflow_controls(self):
        """Create workflow management buttons."""
        frame = ttk.LabelFrame(self, text="Planning Flow Management")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame, text="New Flow", command=lambda: PlanFlowDesigner(self)).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Edit Flow", command=self.edit_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Start", command=self.start_planning).pack(side="right", padx=5, pady=2)

    def show_step_info(self, step):
        """Popup with step description."""
        messagebox.showinfo("Step Info", f"Details about {step} step.")

    def load_flow(self):
        """Load an existing workflow from JSON."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                self.workflow_data = json.load(f)
            messagebox.showinfo("Load Flow", f"Loaded workflow from {file_path}")

    def edit_flow(self):
        """Allow editing of the selected workflow and open the planning steps window."""
        messagebox.showwarning("Edit flow", "Please select flow first.")

    def start_planning(self):
        """Start the automated planning process."""
        messagebox.showinfo("Start Planning", "STARTING AUTOMATED PLANNING FROM SELECTED FLOW...")

    def simple_input_dialog(self, title, prompt):
        """Show a simple input dialog for user text entry."""
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x100")

        tk.Label(dialog, text=prompt).pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def on_ok():
            dialog.user_input = entry.get()
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok).pack(pady=5)
        dialog.transient()
        dialog.wait_window()
        return getattr(dialog, "user_input", None)

class PlanFlowDesigner:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for planning steps."""
    def __init__(self, parent):
        self.planning_window = tk.Toplevel(parent)
        self.planning_window.title("Planning flow")
        self.planning_window.geometry("550x450")
        
        self.name_configured(self.planning_window)
        
        self.techniques_configured(self.planning_window)
        
        self.planning_flow(self.planning_window)
        
        # Save Flow Button
        self.save_flow_btn = ttk.Button(self.planning_window, text="Save Flow", command=self.save_flow)
        self.save_flow_btn.pack(padx=200,pady=10)
        
    def save_flow(self):
        """Save the workflow to a JSON file."""
        messagebox.showinfo("Save Flow", f"Planning flow saved")
    
    def name_configured(self, popup):
        """For setting flow name and user"""
        frame = ttk.LabelFrame(popup, text="Name Configuration")
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="Flow Name").pack(side="left", padx=5, pady=2)
        self.flow_name_var = tk.StringVar()
        self.flow_name_entry = ttk.Entry(frame, textvariable=self.flow_name_var)
        self.flow_name_entry.pack(side="left", padx=5, pady=2)
        
        ttk.Label(frame, text="By").pack(side="left", padx=5, pady=2)
        self.user_name_var = tk.StringVar()
        self.user_name_entry = ttk.Entry(frame, textvariable=self.user_name_var)
        self.user_name_entry.pack(side="left", padx=5, pady=2)
    
    def techniques_configured(self, popup):
        """For setting techniques and beams"""
        frame = ttk.LabelFrame(popup, text="Technique Configuration")
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text="Techniques").pack(side="left", padx=5, pady=2)
        self.technique_var = tk.StringVar()
        self.technique_dropdown = ttk.Combobox(frame, textvariable=self.technique_var, values=['VMAT', 'IMPT'], state="readonly")
        self.technique_dropdown.pack(side="left", padx=5, pady=2)
        
        beam_settings_btn = ttk.Button(frame, text="Beam Settings", command=lambda: VMAT_beam_setting_Window(self.planning_window) if self.technique_var.get() == "VMAT" else IMPT_beam_setting_Window(self.planning_window))
        beam_settings_btn.pack(side="left", padx=5, pady=2)
        
        isocenter_settings_btn = ttk.Button(frame, text="Isocenter Settings", command=lambda: self.open_isocenter_settings_window())
        isocenter_settings_btn.pack(side="left", padx=5, pady=2)
    
    def open_isocenter_settings_window(self):
        """Open a new window for Isocenter Settings."""
        isocenter_window = tk.Toplevel(self.planning_window)
        isocenter_window.title("Isocenter Settings")
        isocenter_window.geometry("400x300")
        # Bold Title Label
        title_label = tk.Label(isocenter_window, text="Isocenter Settings", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Content can be added here
        
        # Close Button
        close_btn = ttk.Button(isocenter_window, text="Close", command=isocenter_window.destroy)
        close_btn.pack(pady=10)
    
    def planning_flow(self, popup):
        """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
        # Planning Flow Steps Frame
        frame = ttk.LabelFrame(popup, text="Planning Flow")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Steps Buttons
        self.match_roi_btn = ttk.Button(frame, text="Match ROI", command=lambda: MatchROI_Window(self.planning_window))
        self.match_roi_btn.place(x=50, y=40)
        
        self.automate_roi_btn = ttk.Button(frame, text="Create Automate ROI", command=lambda: AutomateROI_Window(self.planning_window))
        self.automate_roi_btn.place(x=200, y=40)
        
        self.initial_function_btn = ttk.Button(frame, text="Initial function", command=lambda: InitialFunction_Window(self.planning_window))
        self.initial_function_btn.place(x=380, y=40)
        
        self.optimization_btn = ttk.Button(frame, text="Optimization", command=lambda: OptimizationSetting_Window(self.planning_window))
        self.optimization_btn.place(x=380, y=100)
        
        self.final_calc_btn = ttk.Button(frame, text="Final Calculation", command=lambda: FinalCalculationSetting_Window(self.planning_window))
        self.final_calc_btn.place(x=200, y=100)
        
        self.check_condition_btn = ttk.Button(frame, text="Check Condition", command=lambda: CheckCondition_Window(self.planning_window))
        self.check_condition_btn.place(x=40, y=100)
        
        self.condition_roi_btn = ttk.Button(frame, text="Create Condition ROI", command=lambda: ConditionROI_Window(self.planning_window))
        self.condition_roi_btn.place(x=110, y=160)
        
        self.function_adjustment_btn = ttk.Button(frame, text="Conditionally Function Adjustment", command=lambda: FunctionAdjustment_Window(self.planning_window))
        self.function_adjustment_btn.place(x=270, y=160)
        
        self.end_flow_btn = ttk.Button(frame, text="End Planning Flow", command=lambda: EndPlanningFlow_Window(self.planning_window))
        self.end_flow_btn.place(x=20, y=220)

        # Arrows between steps
        self.add_arrow(frame, "→", 150, 35)
        self.add_arrow(frame, "→", 340, 35)
        self.add_arrow(frame, "↓", 430, 65)
        self.add_arrow(frame, "←", 330, 95)
        self.add_arrow(frame, "←", 150, 95)
        self.add_arrow(frame, "↓", 115, 130)
        self.add_arrow(frame, "→", 240, 155)
        self.add_arrow(frame, "↑", 430, 130)
        self.add_arrow(frame, "↓", 60, 130)
        self.add_arrow(frame, "↓", 60, 160)
        self.add_arrow(frame, "↓", 60, 190)

    def add_arrow(self, parent, symbol, x, y):
        """Helper function to add arrows between steps."""
        label = tk.Label(parent, text=symbol, font=("Arial", 14))
        label.place(x=x, y=y)   

    def show_step_info(self, message):
        """Display information about the selected step."""
        messagebox.showinfo("Step Information", message)

class IMPT_beam_setting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for IMRT beam settings."""
    def __init__(self, parent):
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
        self.add_beam_btn = ttk.Button(self.beam_window, text="Add Beam", command=lambda: self.show_step_info("Add Beam"))
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
        
class VMAT_beam_setting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for VMAT beam settings."""
    def __init__(self, parent):
        self.beam_window = tk.Toplevel(parent)
        self.beam_window.title("VMAT Beam Settings")
        self.beam_window.geometry("800x500")
        # Bold Title Label
        title_label = tk.Label(self.beam_window, text="VMAT Beam Settings", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Beams tree with scrollbar
        beam_tree_frame = ttk.Frame(self.beam_window)
        beam_tree_frame.pack(pady=5, fill="both", expand=True)
        
        beam_tree_scroll_y = ttk.Scrollbar(beam_tree_frame, orient="vertical")
        beam_tree_scroll_x = ttk.Scrollbar(beam_tree_frame, orient="horizontal")
        
        self.beam_tree = ttk.Treeview(beam_tree_frame, columns=("Beam name", "Energy [MV]","Gantry Start [deg]", "Gantry Stop [deg]", "Rotation", "Couch [deg]"), 
                                       show="headings", yscrollcommand=beam_tree_scroll_y.set, xscrollcommand=beam_tree_scroll_x.set)
        
        beam_tree_scroll_y.config(command=self.beam_tree.yview)
        beam_tree_scroll_x.config(command=self.beam_tree.xview)
        
        self.beam_tree.heading("Beam name", text="Beam name")
        self.beam_tree.heading("Energy [MV]", text="Energy [MV]")
        self.beam_tree.heading("Gantry Start [deg]", text="Gantry Start [deg]")
        self.beam_tree.heading("Gantry Stop [deg]", text="Gantry Stop [deg]")
        self.beam_tree.heading("Rotation", text="Rotation")
        self.beam_tree.heading("Couch [deg]", text="Couch [deg]")
        
        self.beam_tree.column("Beam name", width=100)
        self.beam_tree.column("Energy [MV]", width=50)
        self.beam_tree.column("Gantry Start [deg]", width=50)
        self.beam_tree.column("Gantry Stop [deg]", width=50)
        self.beam_tree.column("Rotation", width=50)
        self.beam_tree.column("Couch [deg]", width=50)
        
        self.beam_tree.grid(row=0, column=0, sticky="nsew")
        beam_tree_scroll_y.grid(row=0, column=1, sticky="ns")
        beam_tree_scroll_x.grid(row=1, column=0, sticky="ew")
        beam_tree_frame.grid_rowconfigure(0, weight=1)
        beam_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add Beam Button
        self.add_beam_btn = ttk.Button(self.beam_window, text="Add Beam", command=lambda: self.show_step_info("Add Beam"))
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

class MatchROI_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Match ROI step."""
    def __init__(self, parent):
        match_roi_window = tk.Toplevel(parent)
        match_roi_window.title("Match ROI")
        match_roi_window.geometry("600x400")

        # Bold Title Label
        title_label = tk.Label(match_roi_window, text="Match ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # ROI tree with vertical scrollbar
        roi_tree_frame = ttk.Frame(match_roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("ROI name", "Possible ROI name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set, height=8)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("ROI name", text="ROI name")
        self.roi_tree.heading("Possible ROI name", text="Possible ROI name")
        
        self.roi_tree.column("ROI name", width=200)
        self.roi_tree.column("Possible ROI name", width=200)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")

        # Add ROI Button
        self.add_roi_btn = ttk.Button(match_roi_window, text="Add ROI", command=lambda: self.open_add_roi_popup(match_roi_window))
        self.add_roi_btn.pack(side="left", pady=5)
        # Remove ROI Button
        self.remove_roi_btn = ttk.Button(match_roi_window, text="Remove Selected ROI", command=self.remove_match_roi)
        self.remove_roi_btn.pack(side="left", pady=5)
        # Edit ROI Button
        self.edit_roi_btn = ttk.Button(match_roi_window, text="Edit Selected ROI", command=lambda: self.show_step_info("Edit ROI"))
        self.edit_roi_btn.pack(side="left", pady=5)
        # Save ROI List Button
        self.save_roi_list = ttk.Button(match_roi_window, text="Save", command=lambda: self.save_match_roi_list())
        self.save_roi_list.pack(side="left", pady=5)
        # Close Button
        self.close_btn = ttk.Button(match_roi_window, text="Close", command=match_roi_window.destroy)
        self.close_btn.pack(pady=5)
        
    def open_add_roi_popup(self, parent):
        """Open a popup window to add ROI."""
        add_roi_popup = tk.Toplevel(parent)
        add_roi_popup.title("Add ROI")
        add_roi_popup.geometry("250x100")

        ttk.Label(add_roi_popup, text="ROI Name:").grid(row=0, column=0, pady=5, padx=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_entry = ttk.Entry(add_roi_popup, textvariable=self.roi_name_var)
        self.roi_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(add_roi_popup, text="Possible ROI Name:").grid(row=1, column=0, pady=5, padx=5)
        self.possible_roi_name_var = tk.StringVar()
        self.possible_roi_name_entry = ttk.Entry(add_roi_popup, textvariable=self.possible_roi_name_var)
        self.possible_roi_name_entry.grid(row=1, column=1, pady=5)

        ttk.Button(add_roi_popup, text="Add", command=lambda: self.add_match_roi(add_roi_popup)).grid(row=2, column=0, columnspan=2, pady=5)
        
    def add_match_roi(self, popup):
        """Add ROI to the tree."""
        print("Adding ROI")
        roi_name = self.roi_name_var.get().strip()
        print("ROI Name:", roi_name)
        if roi_name:
            possible_roi_name = self.possible_roi_name_var.get().strip()
            self.roi_tree.insert("", "end", values=(roi_name, possible_roi_name))
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "ROI Name cannot be empty.")
            popup.destroy()

    def remove_match_roi(self):
        """Remove selected ROI item from the treeview."""
        selected_item = self.roi_tree.selection()
        for item in selected_item:
            self.roi_tree.delete(item)
            
    def save_match_roi_list(self):
        """Save the current list of matched ROI items."""
        roi_items = [self.roi_tree.item(child, "values") for child in self.roi_tree.get_children()]
        if roi_items:
            messagebox.showinfo("Save Successful", "Matched ROI saved successfully.")
        else:
            messagebox.showwarning("Save Error", "No ROI items to save.")
    def show_step_info(self, step):
        """Popup with step description."""
        messagebox.showinfo("Step Info", f"Details about {step} step.")        

class AutomateROI_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Automate ROI step."""
    def __init__(self, parent):
        self.roi_window = tk.Toplevel(parent)
        self.roi_window.title("Automate ROI")
        self.roi_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(self.roi_window, text="Automate ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for ROI List (Supports Ordering and Functions) with vertical scrollbar
        roi_tree_frame = ttk.Frame(self.roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("Order", "ROI Name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("Order", text="Order")
        self.roi_tree.heading("ROI Name", text="ROI Name")
        
        self.roi_tree.column("Order", width=80)
        self.roi_tree.column("ROI Name", width=300)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")

        # Button Frame for New, Remove, Edit Function, and Save
        button_frame = ttk.Frame(self.roi_window)
        button_frame.pack(pady=5)

        self.new_roi_btn = ttk.Button(button_frame, text="New", command=self.open_new_roi_popup)
        self.new_roi_btn.pack(side="left", padx=5)
        self.remove_roi_btn = ttk.Button(button_frame, text="Remove", command=self.remove_roi)
        self.remove_roi_btn.pack(side="left", padx=5)
        
        self.move_up_btn = ttk.Button(button_frame, text="Move Up", command=lambda: self.move_roi_order(-1))
        self.move_up_btn.pack(side="left", padx=5)

        self.move_down_btn = ttk.Button(button_frame, text="Move Down", command=lambda: self.move_roi_order(1))
        self.move_down_btn.pack(side="left", padx=5)

        self.edit_function_btn = ttk.Button(button_frame, text="Edit Function", command=self.edit_roi_function)
        self.edit_function_btn.pack(side="left", padx=5)

        self.save_roi_btn = ttk.Button(button_frame, text="Save", command=self.save_roi_list)
        self.save_roi_btn.pack(side="left", padx=5)
        # Close Button
        self.close_btn = ttk.Button(self.roi_window, text="Close", command=self.roi_window.destroy)
        self.close_btn.pack(pady=10)
        
    def open_automate_roi_window(self, parent):
        """Open a new window for Automate ROI step."""
        roi_window = tk.Toplevel(parent)
        roi_window.title("Automate ROI")
        roi_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(roi_window, text="Automate ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for ROI List (Supports Ordering and Functions) with vertical scrollbar
        roi_tree_frame = ttk.Frame(roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("Order", "ROI Name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("Order", text="Order")
        self.roi_tree.heading("ROI Name", text="ROI Name")
        
        self.roi_tree.column("Order", width=80)
        self.roi_tree.column("ROI Name", width=300)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")

        # Button Frame for New, Remove, Edit Function, and Save
        button_frame = ttk.Frame(roi_window)
        button_frame.pack(pady=5)

        self.new_roi_btn = ttk.Button(button_frame, text="New", command=self.open_new_roi_popup)
        self.new_roi_btn.pack(side="left", padx=5)
        self.remove_roi_btn = ttk.Button(button_frame, text="Remove", command=self.remove_roi)
        self.remove_roi_btn.pack(side="left", padx=5)
        
        self.move_up_btn = ttk.Button(button_frame, text="Move Up", command=lambda: self.move_roi_order(-1))
        self.move_up_btn.pack(side="left", padx=5)

        self.move_down_btn = ttk.Button(button_frame, text="Move Down", command=lambda: self.move_roi_order(1))
        self.move_down_btn.pack(side="left", padx=5)

        self.edit_function_btn = ttk.Button(button_frame, text="Edit Function", command=self.edit_roi_function)
        self.edit_function_btn.pack(side="left", padx=5)

        self.save_roi_btn = ttk.Button(button_frame, text="Save", command=self.save_roi_list)
        self.save_roi_btn.pack(side="left", padx=5)
        # Close Button
        self.close_btn = ttk.Button(self.roi_window, text="Close", command=self.roi_window.destroy)
        self.close_btn.pack(pady=10)

    def open_new_roi_popup(self):
        """Open a popup window to add a new ROI item."""
        new_roi_popup = tk.Toplevel(self.roi_window)
        new_roi_popup.title("Add ROI")
        new_roi_popup.geometry("150x150")

        ttk.Label(new_roi_popup, text="ROI Name:").pack(pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_entry = ttk.Entry(new_roi_popup, textvariable=self.roi_name_var)
        self.roi_name_entry.pack(pady=5)

        ttk.Button(new_roi_popup, text="Add Function", command=self.open_boolean_window).pack(pady=5)

        ttk.Button(new_roi_popup, text="Add", command=lambda: self.add_roi(new_roi_popup)).pack(pady=5)
    
    def add_roi(self, popup):
        """Add a new ROI item with function to the list."""
        roi_name = self.roi_name_var.get().strip()
        if roi_name:
            order = len(self.roi_tree.get_children()) + 1
            self.roi_tree.insert("", "end", values=(order, roi_name))
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "Both ROI Name and Function are required.")

    def remove_roi(self):
        """Remove selected ROI item from the treeview."""
        selected_item = self.roi_tree.selection()
        for item in selected_item:
            self.roi_tree.delete(item)

    def edit_roi_function(self):
        """Edit the function of the selected ROI item."""
        selected_item = self.roi_tree.selection()
        if selected_item:
            item_values = self.roi_tree.item(selected_item, "values")
            self.open_boolean_window()
        else:
            messagebox.showwarning("Selection Error", "Please select a ROI item to edit.")
            
    def move_roi_order(self, direction):
        """Move the selected ROI item up or down and update order numbers."""
        selected_item = self.roi_tree.selection()
        if selected_item:
            index = self.roi_tree.index(selected_item)
            new_index = index + direction
            items = self.roi_tree.get_children()
            if 0 <= new_index < len(items):
                self.roi_tree.move(selected_item, "", new_index)
                self.update_roi_order()
                
    def update_roi_order(self):
        """Update order numbers in the ROI tree."""
        items = self.roi_tree.get_children()
        for i, item in enumerate(items, start=1):
            values = self.roi_tree.item(item, "values")
            self.roi_tree.item(item, values=(i, values[1]))

    def save_roi_list(self):
        """Save the current list of ROI items."""
        roi_items = [self.roi_tree.item(child, "values") for child in self.roi_tree.get_children()]
        if roi_items:
            messagebox.showinfo("Save Successful", "ROI list saved successfully.")
        else:
            messagebox.showwarning("Save Error", "No ROI items to save.")
            
    def open_boolean_window(self):
        """Open a new window for Boolean function editing."""
        Boolean_Window(self.roi_window)

class Boolean_Window:
    """Boolean operation window for ROI algebra."""
    def __init__(self, parent):
        self.boolean_window = tk.Toplevel(parent)
        self.boolean_window.title("ROI Algebra")
        self.boolean_window.geometry("900x330")
        
        theFrame = tk.Frame(self.boolean_window)
        theFrame.pack(pady=5)
        
        # Frame for A and B
        frame_a_b = tk.LabelFrame(theFrame, text="ROI AB Operation", padx=10, pady=10)
        frame_a_b.grid(row=0, column=0, padx=5)

        # ROI A
        frame_a = tk.LabelFrame(frame_a_b, text="ROI A", padx=10, pady=10)
        frame_a.grid(row=0, column=0, padx=5)
        tk.Label(frame_a, text="ROI A Name").grid(row=0, column=0)
        self.roi_a = tk.StringVar()
        roi_a_combo = ttk.Combobox(frame_a, textvariable=self.roi_a,
                                values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        roi_a_combo.grid(row=0, column=1)
        
        margin_label_a = tk.Label(frame_a, text="Margin")
        margin_label_a.grid(row=1, column=0)
        selected_value_a = tk.IntVar()
        selected_value_a.set(1)
        expand_a = tk.Radiobutton(frame_a, text="Expand", variable=selected_value_a, value=1)
        expand_a.grid(row=2, column=0)
        contract_a = tk.Radiobutton(frame_a, text="Contract", variable=selected_value_a, value=2)
        contract_a.grid(row=2, column=1)
        
        # Directional input for ROI A
        directions = ['Superior', 'Inferior', 'Right', 'Left', 'Anterior', 'Posterior']
        for i, direction in enumerate(directions):
            label = tk.Label(frame_a, text=f"{direction} (cm)")
            label.grid(row=i+3, column=0)
            default_value = tk.StringVar()
            default_value.set("0.00")
            entry = tk.Entry(frame_a, textvariable=default_value)
            entry.grid(row=i+3, column=1)
        
        # Operations (Union, Intersect, Subtract)
        
        operation_frame = tk.LabelFrame(frame_a_b, text="Select Operation:", padx=10, pady=10)
        operation_frame.grid(row=0, column=1, padx=5)
        selected_operation = tk.IntVar()
        selected_operation.set(1)
        union_button = tk.Radiobutton(operation_frame, text="Union", variable=selected_operation,value=1)
        union_button.grid(row=1, column=1)
        intersect_button = tk.Radiobutton(operation_frame, text="Intersect", variable=selected_operation,value=2)
        intersect_button.grid(row=2, column=1)
        subtract_button = tk.Radiobutton(operation_frame, text="Subtract", variable=selected_operation,value=3)
        subtract_button.grid(row=3, column=1)
        none_button = tk.Radiobutton(operation_frame, text="None", variable=selected_operation,value=4)
        none_button.grid(row=4,column=1)

        # ROI B
        frame_b = tk.LabelFrame(frame_a_b, text="ROI B", padx=10, pady=10)
        frame_b.grid(row=0, column=3, padx=5)
        tk.Label(frame_b, text="ROI B Name").grid(row=0, column=0)
        self.roi_b = tk.StringVar()
        roi_b_combo = ttk.Combobox(frame_b, textvariable=self.roi_b,
                                    values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        roi_b_combo.grid(row=0, column=1)
        
        margin_label_b = tk.Label(frame_b, text="Margin")
        margin_label_b.grid(row=1, column=0)
        selected_value_b = tk.IntVar()
        selected_value_b.set(1)
        expand_b = tk.Radiobutton(frame_b, text="Expand", variable=selected_value_b, value=1)
        expand_b.grid(row=2, column=0)
        contract_b = tk.Radiobutton(frame_b, text="Contract", variable=selected_value_b, value=2)
        contract_b.grid(row=2, column=1)

        # Directional input for ROI B
        for i, direction in enumerate(directions):
            label = tk.Label(frame_b, text=f"{direction} (cm)")
            label.grid(row=i+3, column=0)
            default_value = tk.StringVar()
            default_value.set("0.00")
            entry = tk.Entry(frame_b, textvariable=default_value)
            entry.grid(row=i+3, column=1)
            
        # Output section
        frame_output = tk.LabelFrame(theFrame, text="Output", padx=10, pady=10)
        frame_output.grid(row=0, column=2, padx=5)

        output_label = tk.Label(frame_output, text="Margin")
        output_label.grid(row=0, column=0)

        expand_output = tk.Radiobutton(frame_output, text="Expand", value=1)
        expand_output.grid(row=1, column=0)
        contract_output = tk.Radiobutton(frame_output, text="Contract", value=2)
        contract_output.grid(row=1, column=1)

        # Directional input for Output
        for i, direction in enumerate(directions):
            label = tk.Label(frame_output, text=f"{direction} (cm)")
            label.grid(row=i+2, column=0)
            default_value = tk.StringVar()
            default_value.set("0.00")
            entry = tk.Entry(frame_output, textvariable=default_value)
            entry.grid(row=i+2, column=1)
            
        # Save button
        save_button = tk.Button(self.boolean_window, text="Save", command=self.boolean_window.destroy)
        save_button.pack(pady=10)

class InitialFunction_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Initial Function step."""
    def __init__(self, parent):
        self.initial_function_window = tk.Toplevel(parent)
        self.initial_function_window.title("Initial Optimization function")
        self.initial_function_window.geometry("1200x400")

        # Bold Title Label
        title_label = tk.Label(self.initial_function_window, text="Initial Optimization function", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Content can be added here - with vertical scrollbar
        initial_function_frame = ttk.Frame(self.initial_function_window)
        initial_function_frame.pack(pady=5, fill="both", expand=True)
        
        initial_function_scroll_y = ttk.Scrollbar(initial_function_frame, orient="vertical")
        
        self.initial_function_tree = ttk.Treeview(initial_function_frame, columns=("Function tag", "Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings",
                                                  yscrollcommand=initial_function_scroll_y.set)
        
        initial_function_scroll_y.config(command=self.initial_function_tree.yview)
        
        self.initial_function_tree.heading("Function tag", text="Function tag")
        self.initial_function_tree.heading("Function Type", text="Function Type")
        self.initial_function_tree.heading("ROI", text="ROI")
        self.initial_function_tree.heading("Weight", text="Weight")
        self.initial_function_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.initial_function_tree.heading("Volume level (%)", text="Volume level (%)")
        
        self.initial_function_tree.column("Function tag", width=100)
        self.initial_function_tree.column("Function Type", width=120)
        self.initial_function_tree.column("ROI", width=100)
        self.initial_function_tree.column("Weight", width=80)
        self.initial_function_tree.column("Dose level (Gy)", width=120)
        self.initial_function_tree.column("Volume level (%)", width=120)
        
        self.initial_function_tree.pack(side="left", fill="both", expand=True)
        initial_function_scroll_y.pack(side="right", fill="y")
        
        # Add Objective Button
        self.add_objective_btn = ttk.Button(self.initial_function_window, text="Add function", command=self.open_add_function_window)
        self.add_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Objective Button
        self.delete_objective_btn = ttk.Button(self.initial_function_window, text="Delete Selected function", command=self.delete_function)
        self.delete_objective_btn.pack(side="left", padx=5, pady=5)

        # Save Button
        self.save_initial_function_btn = ttk.Button(self.initial_function_window, text="Save", command=lambda: self.show_step_info("Initial Functions Saved"))
        self.save_initial_function_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.initial_function_window, text="Close", command=self.initial_function_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def open_add_function_window(self):
        """Add an optimization function to the list."""
        add_function_window = tk.Toplevel(self.initial_function_window)
        add_function_window.title("Add Optimization function")
        add_function_window.geometry("300x250")
        
        # function tag
        ttk.Label(add_function_window, text="Function tag").grid(row=0, column=0, pady=5)
        self.function_tag_var = tk.StringVar()
        self.function_tag_entry = ttk.Entry(add_function_window, textvariable=self.function_tag_var)
        self.function_tag_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="ROI Name:").grid(row=1, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_combo = ttk.Combobox(add_function_window, textvariable=self.roi_name_var,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Function type:").grid(row=2, column=0, padx=5, pady=5)
        self.function_var = tk.StringVar()
        self.function_combo = ttk.Combobox(add_function_window, textvariable=self.function_var,
                                            values=['Min Dose', 'Min DVH', 'Min EUD', 'Max Dose', 'Max DVH', 'Max EUD', 'Uniform Dose', 'Dose fall-off'], state="readonly")
        self.function_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Weight:").grid(row=3, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(add_function_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Dose Level (Gy):").grid(row=4, column=0, padx=5, pady=5)
        self.dose_value_var = tk.StringVar()
        self.dose_value_entry = ttk.Entry(add_function_window, textvariable=self.dose_value_var)
        self.dose_value_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(add_function_window, text="Volume Level (%):").grid(row=5, column=0, padx=5, pady=5)
        self.volume_value_var = tk.StringVar()
        self.volume_value_entry = ttk.Entry(add_function_window, textvariable=self.volume_value_var)
        self.volume_value_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Button(add_function_window, text="Add", command=lambda: self.add_function(add_function_window)).grid(row=6, column=0, columnspan=2, pady=10)
        
    def add_function(self, popup):
        """Save the new function to the list."""
        function_tag = self.function_tag_var.get().strip()
        function = self.function_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        dose_level = self.dose_value_var.get().strip()
        volume_level = self.volume_value_var.get().strip()
        weight = self.weight_var.get().strip()
        # Here you would add the objective to your data structure
        self.initial_function_tree.insert("", "end", values=(function_tag, function, roi_name, weight, dose_level, volume_level))
        popup.destroy()
    
    def delete_function(self):
        """Delete the selected function from the list."""
        selected_item = self.initial_function_tree.selection()
        for item in selected_item:
            self.initial_function_tree.delete(item)
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)        
        
class OptimizationSetting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Optimization Settings step."""
    def __init__(self, parent):
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
        
        # Save Button
        ttk.Button(optimization_window, text="Save", command=lambda: self.show_step_info("Optimization Settings Saved")).grid(row=2, column=0, pady=10)

        # Close Button
        ttk.Button(optimization_window, text="Close", command=optimization_window.destroy).grid(row=2, column=1, columnspan=2, pady=10)
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)

class FinalCalculationSetting_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Final Calculation step."""
    def __init__(self, parent):
        final_calc_window = tk.Toplevel(parent)
        final_calc_window.title("Final Calculation")
        final_calc_window.geometry("250x70")

        ttk.Label(final_calc_window, text="Algorithm").grid(row=0, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        ttk.Combobox(final_calc_window, values=['Pencil beam', 'CC', 'MonteCarlo'], state="readonly", textvariable=self.algorithm_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Save Button
        ttk.Button(final_calc_window, text="Save", command=lambda: self.show_step_info("Final Calculation Settings Saved")).grid(row=1, column=0,padx=5, pady=10)
        
        # Close Button
        ttk.Button(final_calc_window, text="Close", command=final_calc_window.destroy).grid(row=1, column=1, padx=5, pady=10)
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)

class CheckCondition_Window:
    """Open a new window for Check Condition step."""
    def __init__(self, parent):
        self.check_condition_window = tk.Toplevel(parent)
        self.check_condition_window.title("Check Condition")
        self.check_condition_window.geometry("1000x400")
        
        # Bold Title Label
        title_label = tk.Label(self.check_condition_window, text="Check Condition", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Condition tree with vertical scrollbar
        condition_tree_frame = ttk.Frame(self.check_condition_window)
        condition_tree_frame.pack(pady=5, fill="both", expand=True)
        
        condition_tree_scroll_y = ttk.Scrollbar(condition_tree_frame, orient="vertical")
        
        self.condition_tree = ttk.Treeview(condition_tree_frame, columns=("Condition Name", "ROI",  "Condition Type", "Criteria"), show="headings",
                                            yscrollcommand=condition_tree_scroll_y.set)
        
        condition_tree_scroll_y.config(command=self.condition_tree.yview)
        
        self.condition_tree.heading("Condition Name", text="Condition Name")
        self.condition_tree.heading("ROI", text="ROI")
        self.condition_tree.heading("Condition Type", text="Condition Type")
        self.condition_tree.heading("Criteria", text="Criteria")
        
        self.condition_tree.column("Condition Name", width=150)
        self.condition_tree.column("ROI", width=100)
        self.condition_tree.column("Condition Type", width=130)
        self.condition_tree.column("Criteria", width=200)
        
        self.condition_tree.pack(side="left", fill="both", expand=True)
        condition_tree_scroll_y.pack(side="right", fill="y")
        
        # Add Condition Button
        self.add_condition_btn = ttk.Button(self.check_condition_window, text="New", command=self.open_add_condition_window)
        self.add_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition Button
        self.delete_condition_btn = ttk.Button(self.check_condition_window, text="Remove", command=self.remove_condition)
        self.delete_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit Condition Button
        self.edit_condition_btn = ttk.Button(self.check_condition_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Save Button
        self.save_condition_btn = ttk.Button(self.check_condition_window, text="Save", command=lambda: self.show_step_info("Conditions Saved"))
        self.save_condition_btn.pack(side="left", padx=5, pady=5)

        # Close Button
        self.close_btn = ttk.Button(self.check_condition_window, text="Close", command=self.check_condition_window.destroy)
        self.close_btn.pack(pady=10)
    
    def open_add_condition_window(self):
        """Add a condition to the list."""
        add_condition_window = tk.Toplevel(self.check_condition_window)
        add_condition_window.title("Add Condition")
        add_condition_window.geometry("350x220")
        
        ttk.Label(add_condition_window, text="Condition Name:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_name_var = tk.StringVar()
        self.condition_name_entry = ttk.Entry(add_condition_window, textvariable=self.condition_name_var)
        self.condition_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_window, text="Condition Type:").grid(row=1, column=0, padx=5, pady=5)
        self.condition_type_var = tk.StringVar()
        self.condition_type_combo = ttk.Combobox(add_condition_window, textvariable=self.condition_type_var,
                                            values=['Optimization Round', 'Max Dose','Max DaV', 'Max VaD', 'Max Dmean', 'Min Dose','Min DaV', 'Min VaD', 'Min Dmean'], state="readonly")
        self.condition_type_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # --------------------
        # Frame for each type
        # --------------------
        
        # Frame for optimization round
        frame_opt_round = ttk.Frame(add_condition_window)
        ttk.Label(frame_opt_round, text="Optimization Round ≥").grid(row=0, column=0, padx=5, pady=5)
        self.opt_round_var = tk.StringVar()
        self.opt_round_entry = ttk.Entry(frame_opt_round, textvariable=self.opt_round_var)
        self.opt_round_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame for Max Dose
        frame_max_dose = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dose, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dose = tk.StringVar()
        self.roi_name_combo_max_dose = ttk.Combobox(frame_max_dose, textvariable=self.roi_name_var_max_dose,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_max_dose.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_max_dose, text="Max Dose (Gy):").grid(row=1, column=0, padx=5, pady=5)
        self.max_dose_var = tk.StringVar()
        self.max_dose_entry = ttk.Entry(frame_max_dose, textvariable=self.max_dose_var)
        self.max_dose_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dose, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dose = tk.StringVar()
        self.roi_name_combo_min_dose = ttk.Combobox(frame_min_dose, textvariable=self.roi_name_var_min_dose,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_min_dose.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dose, text="Min Dose (Gy):").grid(row=1, column=0, padx=5, pady=5)
        self.min_dose_var = tk.StringVar()
        self.min_dose_entry = ttk.Entry(frame_min_dose, textvariable=self.min_dose_var)
        self.min_dose_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame for Max DaV
        frame_max_dav = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dav, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dav = tk.StringVar()
        self.roi_name_combo_max_dav = ttk.Combobox(frame_max_dav, textvariable=self.roi_name_var_max_dav,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_max_dav.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dav, text="Dose (cGy) at most:").grid(row=1, column=0, padx=5, pady=5)
        self.dose_max_dav_var = tk.StringVar()
        self.dose_max_dav_entry = ttk.Entry(frame_max_dav, textvariable=self.dose_max_dav_var)
        self.dose_max_dav_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dav, text="at Volume:").grid(row=2, column=0, padx=5, pady=5)
        self.volume_max_dav_var = tk.StringVar()
        self.volume_max_dav_entry = ttk.Entry(frame_max_dav, textvariable=self.volume_max_dav_var)
        self.volume_max_dav_entry.grid(row=2, column=1, padx=5, pady=5)
        self.volume_max_dav_unit = tk.StringVar()
        self.volume_max_dav_unit_combo = ttk.Combobox(frame_max_dav, textvariable=self.volume_max_dav_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_max_dav_unit_combo.grid(row=2, column=2, padx=5, pady=5)
        
        # Frame for Min DaV
        frame_min_dav = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dav, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dav = tk.StringVar()
        self.roi_name_combo_min_dav = ttk.Combobox(frame_min_dav, textvariable=self.roi_name_var_min_dav,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_min_dav.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_dav, text="Dose (cGy) at least:").grid(row=1, column=0, padx=5, pady=5)
        self.dose_min_dav_var = tk.StringVar()
        self.dose_min_dav_entry = ttk.Entry(frame_min_dav, textvariable=self.dose_min_dav_var)
        self.dose_min_dav_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_dav, text="at Volume:").grid(row=2, column=0, padx=5, pady=5)
        self.volume_min_dav_var = tk.StringVar()
        self.volume_min_dav_entry = ttk.Entry(frame_min_dav, textvariable=self.volume_min_dav_var)
        self.volume_min_dav_entry.grid(row=2, column=1, padx=5, pady=5)
        self.volume_min_dav_unit = tk.StringVar()
        self.volume_min_dav_unit_combo = ttk.Combobox(frame_min_dav, textvariable=self.volume_min_dav_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_min_dav_unit_combo.grid(row=2, column=2, padx=5, pady=5)
        
        # Frame Max VaD
        frame_max_vad = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_vad, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_vad = tk.StringVar()
        self.roi_name_combo_max_vad = ttk.Combobox(frame_max_vad, textvariable=self.roi_name_var_max_vad,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_max_vad.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_vad, text="Volume at most:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_max_vad_var = tk.StringVar()
        self.volume_max_vad_entry = ttk.Entry(frame_max_vad, textvariable=self.volume_max_vad_var)
        self.volume_max_vad_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_max_vad_unit = tk.StringVar()
        self.volume_max_vad_unit_combo = ttk.Combobox(frame_max_vad, textvariable=self.volume_max_vad_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_max_vad_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(frame_max_vad, text="at Dose (cGy):").grid(row=2, column=0, padx=5, pady=5)
        self.dose_max_vad_var = tk.StringVar()
        self.dose_max_vad_entry = ttk.Entry(frame_max_vad, textvariable=self.dose_max_vad_var)
        self.dose_max_vad_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Frame Min VaD
        frame_min_vad = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_vad, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_vad = tk.StringVar()
        self.roi_name_combo_min_vad = ttk.Combobox(frame_min_vad, textvariable=self.roi_name_var_min_vad,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_min_vad.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_min_vad, text="Volume at most:").grid(row=1, column=0, padx=5, pady=5)
        self.volume_min_vad_var = tk.StringVar()
        self.volume_min_vad_entry = ttk.Entry(frame_min_vad, textvariable=self.volume_min_vad_var)
        self.volume_min_vad_entry.grid(row=1, column=1, padx=5, pady=5)
        self.volume_min_vad_unit = tk.StringVar()
        self.volume_min_vad_unit_combo = ttk.Combobox(frame_min_vad, textvariable=self.volume_min_vad_unit, values=['%', 'cc'], state="readonly", width=5)
        self.volume_min_vad_unit_combo.grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(frame_min_vad, text="at Dose (cGy):").grid(row=2, column=0, padx=5, pady=5)
        self.dose_min_vad_var = tk.StringVar()
        self.dose_min_vad_entry = ttk.Entry(frame_min_vad, textvariable=self.dose_min_vad_var)
        self.dose_min_vad_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Fram Max Dmean
        frame_max_dmean = ttk.Frame(add_condition_window)
        ttk.Label(frame_max_dmean, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_max_dmean = tk.StringVar()
        self.roi_name_combo_max_dmean = ttk.Combobox(frame_max_dmean, textvariable=self.roi_name_var_max_dmean,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_max_dmean.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_max_dmean, text="Max Dmean (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.max_dmean_var = tk.StringVar()
        self.max_dmean_entry = ttk.Entry(frame_max_dmean, textvariable=self.max_dmean_var)
        self.max_dmean_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame Min Dmean
        frame_min_dmean = ttk.Frame(add_condition_window)
        ttk.Label(frame_min_dmean, text="ROI Name:").grid(row=0, column=0, padx=5, pady=5)
        self.roi_name_var_min_dmean = tk.StringVar()
        self.roi_name_combo_min_dmean = ttk.Combobox(frame_min_dmean, textvariable=self.roi_name_var_min_dmean,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo_min_dmean.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_min_dmean, text="Min Dmean (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.min_dmean_var = tk.StringVar()
        self.min_dmean_entry = ttk.Entry(frame_min_dmean, textvariable=self.min_dmean_var)
        self.min_dmean_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def show_selected_frame(self):
            """Show the relevant frame based on condition type selection."""
            frame_opt_round.grid_forget()
            frame_max_dose.grid_forget()
            frame_min_dose.grid_forget()
            frame_max_dav.grid_forget()
            frame_min_dav.grid_forget()
            frame_max_vad.grid_forget()
            frame_min_vad.grid_forget()
            frame_max_dmean.grid_forget()
            frame_min_dmean.grid_forget()
            selection = self.condition_type_var.get()
            if selection == 'Optimization Round':
                frame_opt_round.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max Dose':
                frame_max_dose.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min Dose':
                frame_min_dose.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max DaV':
                frame_max_dav.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min DaV':
                frame_min_dav.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max VaD':
                frame_max_vad.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min VaD':
                frame_min_vad.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Max Dmean':
                frame_max_dmean.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            elif selection == 'Min Dmean':
                frame_min_dmean.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
                
        self.condition_type_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_frame(self))
        show_selected_frame(self)  # Show the initial frame based on the default selection
        
        ttk.Button(add_condition_window, text="Add", command=lambda: self.add_condition(add_condition_window)).grid(row=5, column=0, columnspan=2, pady=10)

    def add_condition(self, popup):
        """Save the new condition to the list."""
        condition_name = self.condition_name_var.get().strip()
        condition_type = self.condition_type_var.get().strip()
        if condition_type == 'Optimization Round':
            roi_name = 'N/A'
            opt_round = self.opt_round_var.get().strip()
            criteria = f"Round ≥ {opt_round}"
        elif condition_type == 'Max Dose':
            roi_name = self.roi_name_var_max_dose.get().strip()
            max_dose = self.max_dose_var.get().strip()
            criteria = f"Dmax (Gy) ≥ {max_dose}"
        elif condition_type == 'Min Dose':
            roi_name = self.roi_name_var_min_dose.get().strip()
            min_dose = self.min_dose_var.get().strip()
            criteria = f"Dmin (Gy) ≤ {min_dose}"
        elif condition_type == 'Max DaV':
            roi_name = self.roi_name_var_max_dav.get().strip()
            dose_max_dav = self.dose_max_dav_var.get().strip()
            volume_max_dav = self.volume_max_dav_var.get().strip()
            volume_max_dav_unit = self.volume_max_dav_unit.get().strip()
            criteria = f"D{volume_max_dav}{volume_max_dav_unit} ≥ {dose_max_dav} cGy"
        elif condition_type == 'Min DaV':
            roi_name = self.roi_name_var_min_dav.get().strip()
            dose_min_dav = self.dose_min_dav_var.get().strip()
            volume_min_dav = self.volume_min_dav_var.get().strip()
            volume_min_dav_unit = self.volume_min_dav_unit.get().strip()
            criteria = f"D{volume_min_dav}{volume_min_dav_unit} ≤ {dose_min_dav} cGy"
        elif condition_type == 'Max VaD':
            roi_name = self.roi_name_var_max_vad.get().strip()
            volume_max_vad = self.volume_max_vad_var.get().strip()
            volume_max_vad_unit = self.volume_max_vad_unit.get().strip()
            dose_max_vad = self.dose_max_vad_var.get().strip()
            criteria = f"V{dose_max_vad} cGy ≥ {volume_max_vad}{volume_max_vad_unit}"
        elif condition_type == 'Min VaD':
            roi_name = self.roi_name_var_min_vad.get().strip()
            volume_min_vad = self.volume_min_vad_var.get().strip()
            volume_min_vad_unit = self.volume_min_vad_unit.get().strip()
            dose_min_vad = self.dose_min_vad_var.get().strip()
            criteria = f"V{dose_min_vad} cGy ≤ {volume_min_vad}{volume_min_vad_unit}"
        elif condition_type == 'Max Dmean':
            roi_name = self.roi_name_var_max_dmean.get().strip()
            max_dmean = self.max_dmean_var.get().strip()
            criteria = f"Dmean (cGy) ≥ {max_dmean}"
        elif condition_type == 'Min Dmean':
            roi_name = self.roi_name_var_min_dmean.get().strip()
            min_dmean = self.min_dmean_var.get().strip()
            criteria = f"Dmean (cGy) ≤ {min_dmean}"
        # Here you would add the condition to your data structure
        self.condition_tree.insert("", "end", values=(condition_name, roi_name, condition_type, criteria))
        popup.destroy()
    
    def remove_condition(self):
        """Remove the selected condition from the list."""
        selected_item = self.condition_tree.selection()
        for item in selected_item:
            self.condition_tree.delete(item)
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
            
class ConditionROI_Window:
    """Open a new window for Condition ROI step."""
    def __init__(self, parent):
        self.condition_roi_window = tk.Toplevel(parent)
        self.condition_roi_window.title("Condition ROI")
        self.condition_roi_window.geometry("800x400")
        
        # Bold Title Label
        title_label = tk.Label(self.condition_roi_window, text="Condition ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Treeview for Condition ROI List with vertical scrollbar
        condition_roi_frame = ttk.Frame(self.condition_roi_window)
        condition_roi_frame.pack(pady=5, fill="both", expand=True)
        
        condition_roi_scroll_y = ttk.Scrollbar(condition_roi_frame, orient="vertical")
        
        self.condition_roi_tree = ttk.Treeview(condition_roi_frame, columns=("Order","If this condition TRUE", "Create this ROI", "By this method"), show="headings",
                                                yscrollcommand=condition_roi_scroll_y.set)
        
        condition_roi_scroll_y.config(command=self.condition_roi_tree.yview)
        
        self.condition_roi_tree.heading("Order", text="Order")
        self.condition_roi_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.condition_roi_tree.heading("Create this ROI", text="Create this ROI")
        self.condition_roi_tree.heading("By this method", text="By this method")
        
        self.condition_roi_tree.column("Order", width=60)
        self.condition_roi_tree.column("If this condition TRUE", width=180)
        self.condition_roi_tree.column("Create this ROI", width=150)
        self.condition_roi_tree.column("By this method", width=180)
        
        self.condition_roi_tree.pack(side="left", fill="both", expand=True)
        condition_roi_scroll_y.pack(side="right", fill="y")
        
        # Add Condition ROI Button
        self.add_condition_roi_btn = ttk.Button(self.condition_roi_window, text="New", command=self.open_add_condition_roi_window)
        self.add_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition ROI Button
        self.delete_condition_roi_btn = ttk.Button(self.condition_roi_window, text="Remove", command=self.remove_condition_roi)
        self.delete_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Move Up Button
        self.move_up_condition_btn = ttk.Button(self.condition_roi_window, text="Move Up", command=lambda: self.move_condition_roi_order(-1))
        self.move_up_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Move Down Button
        self.move_down_condition_btn = ttk.Button(self.condition_roi_window, text="Move Down", command=lambda: self.move_condition_roi_order(1))
        self.move_down_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit
        self.edit_condition_btn = ttk.Button(self.condition_roi_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        
        # Save Button
        self.save_condition_roi_btn = ttk.Button(self.condition_roi_window, text="Save", command=lambda: self.show_step_info("Condition ROIs Saved"))
        self.save_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        ttk.Button(self.condition_roi_window, text="Close", command=self.condition_roi_window.destroy).pack(pady=10)
    
    def open_add_condition_roi_window(self):
        """Add a condition ROI to the list."""
        add_condition_roi_window = tk.Toplevel(self.condition_roi_window)
        add_condition_roi_window.title("Add Condition ROI")
        add_condition_roi_window.geometry("300x200")
        
        ttk.Label(add_condition_roi_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar()
        self.condition_true_entry = ttk.Entry(add_condition_roi_window, textvariable=self.condition_true_var)
        self.condition_true_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_roi_window, text="Create this ROI:").grid(row=1, column=0, padx=5, pady=5)
        self.create_roi_var = tk.StringVar()
        self.create_roi_entry = ttk.Entry(add_condition_roi_window, textvariable=self.create_roi_var)
        self.create_roi_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_roi_window, text="By this method:").grid(row=2, column=0, padx=5, pady=5)
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(add_condition_roi_window, textvariable=self.method_var,
                                        values=['Boolean operation', 'Convert Dose to ROI'], state="readonly")
        self.method_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Boolean frame
        frame_boolean = ttk.Frame(add_condition_roi_window)
        ttk.Button(frame_boolean, text="Boolean operation", command=lambda: Boolean_Window(add_condition_roi_window)).grid(row=0, column=0, padx=5, pady=5)
        
        # Convert Dose to ROI frame
        frame_dose_to_roi = ttk.Frame(add_condition_roi_window)
        ttk.Label(frame_dose_to_roi, text="Convert Dose (Gy) to ROI").grid(row=0, column=0, padx=5, pady=5)
        self.dose_to_roi_var = tk.StringVar()
        self.dose_to_roi_entry = ttk.Entry(frame_dose_to_roi, textvariable=self.dose_to_roi_var)
        self.dose_to_roi_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def show_selected_method(self):
            """Show the relevant input based on method selection."""
            frame_boolean.grid_forget()
            frame_dose_to_roi.grid_forget()
            selection = self.method_var.get()
            if selection == 'Boolean operation':
                frame_boolean.grid(row=3, column=1, padx=5, pady=5)
            elif selection == 'Convert Dose to ROI':
                frame_dose_to_roi.grid(row=3, column=0, columnspan=2,padx=5, pady=5)
                
        self.method_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_method(self))
        show_selected_method(self)  # Show the initial frame based on the default selection
        
        ttk.Button(add_condition_roi_window, text="Add", command=lambda: self.add_condition_roi(add_condition_roi_window)).grid(row=5, column=0, columnspan=2, pady=10)
    
    def add_condition_roi(self, popup):
        """Save the new condition ROI to the list."""
        condition_true = self.condition_true_var.get().strip()
        create_roi = self.create_roi_var.get().strip()
        method = self.method_var.get().strip()
        order = len(self.condition_roi_tree.get_children()) + 1
        # Here you would add the condition ROI to your data structure
        self.condition_roi_tree.insert("", "end", values=(order, condition_true, create_roi, method))
        popup.destroy()
        
    def remove_condition_roi(self):
        """Remove the selected condition ROI from the list."""
        selected_item = self.condition_roi_tree.selection()
        for item in selected_item:
            self.condition_roi_tree.delete(item)
    
    def move_condition_roi_order(self, direction):
        """Move the selected ROI item up or down and update order numbers."""
        selected_item = self.condition_roi_tree.selection()
        if selected_item:
            index = self.condition_roi_tree.index(selected_item)
            new_index = index + direction
            items = self.condition_roi_tree.get_children()
            if 0 <= new_index < len(items):
                self.condition_roi_tree.move(selected_item, "", new_index)
                self.update_condition_roi_order()
                
    def update_condition_roi_order(self):
        """Update order numbers in the ROI tree."""
        items = self.condition_roi_tree.get_children()
        for i, item in enumerate(items, start=1):
            values = self.condition_roi_tree.item(item, "values")
            self.condition_roi_tree.item(item, values=(i, values[1]))
            
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)

class FunctionAdjustment_Window:
    """Open a new window for Function Adjustment step."""
    def __init__(self, parent):
        self.function_adjustment_window = tk.Toplevel(parent)
        self.function_adjustment_window.title("Function Adjustment")
        self.function_adjustment_window.geometry("1700x800")
        
        # Bold Title Label
        title_label = tk.Label(self.function_adjustment_window, text="Function Adjustment", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Old function frame
        old_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Initial Functions")
        old_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # Old function Tree with vertical scrollbar
        old_function_frame = ttk.Frame(old_function_label_frame)
        old_function_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        old_function_scroll_y = ttk.Scrollbar(old_function_frame, orient="vertical")
        
        self.old_function_tree = ttk.Treeview(old_function_frame, columns=("Function tag","Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings",
                                                yscrollcommand=old_function_scroll_y.set)
        
        old_function_scroll_y.config(command=self.old_function_tree.yview)
        
        self.old_function_tree.heading("Function tag", text="Function tag")
        self.old_function_tree.heading("Function Type", text="Function Type")
        self.old_function_tree.heading("ROI", text="ROI")
        self.old_function_tree.heading("Weight", text="Weight")
        self.old_function_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.old_function_tree.heading("Volume level (%)", text="Volume level (%)")
        
        self.old_function_tree.column("Function tag", width=100)
        self.old_function_tree.column("Function Type", width=120)
        self.old_function_tree.column("ROI", width=100)
        self.old_function_tree.column("Weight", width=80)
        self.old_function_tree.column("Dose level (Gy)", width=120)
        self.old_function_tree.column("Volume level (%)", width=120)
        
        self.old_function_tree.pack(side="left", fill="both", expand=True)
        old_function_scroll_y.pack(side="right", fill="y")
        
        def add_old_functions(self):
            """Add old functions to the list."""
            # Sample data for old functions
            sample_functions = [
                ("Func1", "Min Dose", "PTV", "100", "50", ""),
                ("Func2", "Max Dose", "Bladder", "10", "30", "0"),
                ("Func3", "Min DVH", "Rectum", "20", "25", "10"),
            ]
            for func in sample_functions:
                self.old_function_tree.insert("", "end", values=func)
                
        add_old_functions(self)
        
        # Adjust Button
        self.adjust_function_btn = ttk.Button(old_function_label_frame, text="Adjust Selected Function", command=lambda: self.show_step_info("Adjust Function"))
        self.adjust_function_btn.pack(side="left", padx=5, pady=5)
        
        # Adjusted function frame
        adjusted_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Adjustment")
        adjusted_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # New function adjustment Tree with vertical scrollbar
        function_adjustment_frame = ttk.Frame(adjusted_function_label_frame)
        function_adjustment_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        function_adjustment_scroll_y = ttk.Scrollbar(function_adjustment_frame, orient="vertical")
        
        self.function_adjustment_tree = ttk.Treeview(function_adjustment_frame, columns=("If this condition TRUE", "Make this Adjustment", "Function tag","Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings",
                                                    yscrollcommand=function_adjustment_scroll_y.set)
        
        function_adjustment_scroll_y.config(command=self.function_adjustment_tree.yview)
        
        self.function_adjustment_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.function_adjustment_tree.heading("Make this Adjustment", text="Make this Adjustment")
        self.function_adjustment_tree.heading("Function tag", text="Function tag")
        self.function_adjustment_tree.heading("ROI", text="ROI")
        self.function_adjustment_tree.heading("Function Type", text="Function Type")
        self.function_adjustment_tree.heading("Weight", text="Weight")
        self.function_adjustment_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.function_adjustment_tree.heading("Volume level (%)", text="Volume level (%)")
        
        self.function_adjustment_tree.column("If this condition TRUE", width=150)
        self.function_adjustment_tree.column("Make this Adjustment", width=150)
        self.function_adjustment_tree.column("Function tag", width=100)
        self.function_adjustment_tree.column("ROI", width=100)
        self.function_adjustment_tree.column("Function Type", width=120)
        self.function_adjustment_tree.column("Weight", width=80)
        self.function_adjustment_tree.column("Dose level (Gy)", width=120)
        self.function_adjustment_tree.column("Volume level (%)", width=120)
        
        self.function_adjustment_tree.pack(side="left", fill="both", expand=True)
        function_adjustment_scroll_y.pack(side="right", fill="y")
        
        # Add Adjustment Button
        self.add_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Add New Function", command=self.open_add_function_adjustment_window)
        self.add_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Delete Adjustment Button
        self.delete_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Remove Adjustment", command=lambda: self.show_step_info("Remove Function Adjustment"))
        self.delete_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_adjustment_btn = ttk.Button(self.function_adjustment_window, text="Save", command=lambda: self.show_step_info("Function Adjustments Saved"))
        self.save_adjustment_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.function_adjustment_window, text="Close", command=self.function_adjustment_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
    
    def open_add_function_adjustment_window(self):
        """Add a function adjustment to the list."""
        add_adjustment_window = tk.Toplevel(self.function_adjustment_window)
        add_adjustment_window.title("Add Function Adjustment")
        add_adjustment_window.geometry("300x260")
        
        ttk.Label(add_adjustment_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar()
        self.condition_true_entry = ttk.Entry(add_adjustment_window, textvariable=self.condition_true_var)
        self.condition_true_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Function tag:").grid(row=1, column=0, padx=5, pady=5)
        self.adjustment_tag_var = tk.StringVar()
        self.adjustment_tag_entry = ttk.Entry(add_adjustment_window, textvariable=self.adjustment_tag_var)
        self.adjustment_tag_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Function Type:").grid(row=2, column=0, padx=5, pady=5)
        self.function_type_var = tk.StringVar()
        self.function_type_combo = ttk.Combobox(add_adjustment_window, textvariable=self.function_type_var,
                                            values=['Min Dose', 'Min DVH', 'Min EUD', 'Max Dose', 'Max DVH', 'Max EUD', 'Uniform Dose', 'Dose fall-off'], state="readonly")
        self.function_type_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="ROI Name:").grid(row=3, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_combo = ttk.Combobox(add_adjustment_window, textvariable=self.roi_name_var,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Weight:").grid(row=4, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(add_adjustment_window, textvariable=self.weight_var)
        self.weight_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Dose Level (Gy):").grid(row=5, column=0, padx=5, pady=5)
        self.dose_value_var = tk.StringVar()
        self.dose_value_entry = ttk.Entry(add_adjustment_window, textvariable=self.dose_value_var)
        self.dose_value_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(add_adjustment_window, text="Volume Level (%):").grid(row=6, column=0, padx=5, pady=5)
        self.volume_value_var = tk.StringVar()
        self.volume_value_entry = ttk.Entry(add_adjustment_window, textvariable=self.volume_value_var)
        self.volume_value_entry.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Button(add_adjustment_window, text="Add", command=lambda: self.add_function_adjustment(add_adjustment_window)).grid(row=7, column=0, columnspan=2, pady=10)
    
    def add_function_adjustment(self, popup):
        """Save the new function adjustment to the list."""
        condition_true = self.condition_true_var.get().strip()
        adjustment_type = "Add New Function"
        adjustment_tag = self.adjustment_tag_var.get().strip()
        function_type = self.function_type_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        weight = self.weight_var.get().strip()
        dose_level = self.dose_value_var.get().strip()
        volume_level = self.volume_value_var.get().strip()
        # Here you would add the function adjustment to your data structure
        self.function_adjustment_tree.insert("", "end", values=(condition_true, adjustment_type, adjustment_tag, roi_name, function_type, weight, dose_level, volume_level))
        popup.destroy()

class EndPlanningFlow_Window:
    """Open a new window for End Planning Flow step."""
    def __init__(self, parent):
        end_planning_window = tk.Toplevel(parent)
        end_planning_window.title("End Planning Flow")
        end_planning_window.geometry("300x100")
        
        ttk.Label(end_planning_window, text="End flow after optimize").grid(row=0, column=0, padx=5, pady=5)
        self.max_optimize_var = tk.IntVar()
        max_optimize_entry = ttk.Entry(end_planning_window, textvariable=self.max_optimize_var, width=5)
        max_optimize_entry.grid(row=0, column=1, padx=0, pady=5)
        ttk.Label(end_planning_window, text="rounds").grid(row=0, column=2, padx=0, pady=5)
        # Save Button
        ttk.Button(end_planning_window, text="Save", command=lambda: self.show_step_info("End Planning Flow Settings Saved")).grid(row=1, column=0, padx=5, pady=10)
        
        # Close Button
        ttk.Button(end_planning_window, text="Close", command=end_planning_window.destroy).grid(row=1, column=1, padx=5, pady=10)  
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
        
if __name__ == "__main__":
    app = AutoPlanGUI()
    app.mainloop()
