import tkinter as tk
from tkinter import ttk, messagebox
from src.window.vmat_beam_setting_window import VMAT_beam_setting_Window
from src.window.imrt_beam_setting_window import IMPT_beam_setting_Window
from src.window.match_roi_window import MatchROI_Window
from src.window.automate_roi_window import AutomateROI_Window
from src.window.initial_function_window import InitialFunction_Window
from src.window.optimization_setting_window import OptimizationSetting_Window
from src.window.final_calculation_setting_window import FinalCalculationSetting_Window
from src.window.check_condition_window import CheckCondition_Window
from src.window.condition_roi_window import ConditionROI_Window
from src.window.function_adjustment_window import FunctionAdjustment_Window
from src.window.end_planning_flow_window import EndPlanningFlow_Window

class PlanFlowDesigner:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for planning steps."""
    def __init__(self, parent, load_data=None):
        self.planning_window = tk.Toplevel(parent)
        self.planning_window.title("Planning flow")
        self.planning_window.geometry("550x450")
        
        # Initialize data storage for all steps
        self.match_roi_data = []
        self.automate_roi_data = []
        self.initial_functions_data = []
        self.optimization_data = {}
        self.final_calc_data = {}
        self.check_conditions_data = []
        self.condition_rois_data = []
        self.function_adjustments_data = []
        self.end_flow_data = {}
        self.beam_settings_data = []
        self.isocenter_data = {}
        
        self.name_configured(self.planning_window)
        
        self.techniques_configured(self.planning_window)
        
        self.planning_flow(self.planning_window)
        
        # Load existing data if provided
        if load_data:
            self.load_flow_data(load_data)
        
        # Save Flow Button
        self.save_flow_btn = ttk.Button(self.planning_window, text="Save Flow", command=self.save_flow)
        self.save_flow_btn.pack(padx=200,pady=10)
    
    def get_roi_list(self):
        """Get list of ROI names from Match ROI data."""
        roi_list = []
        for item in self.match_roi_data:
            roi_name = item.get("roi_name", "")
            if roi_name and roi_name not in roi_list:
                roi_list.append(roi_name)
        # If no ROIs defined yet, return a default list
        if not roi_list:
            roi_list = ['Add in Match ROI step']
        return roi_list
    
    def get_extended_roi_list(self):
        """Get list of ROI names from both Match ROI and Condition ROI data."""
        roi_list = []
        # Add ROIs from Match ROI
        for item in self.match_roi_data:
            roi_name = item.get("roi_name", "")
            if roi_name and roi_name not in roi_list:
                roi_list.append(roi_name)
        # Add ROIs from Condition ROI (created ROIs)
        for item in self.condition_rois_data:
            created_roi = item.get("roi", "")
            if created_roi and created_roi not in roi_list:
                roi_list.append(created_roi)
        # If no ROIs defined yet, return a default list
        if not roi_list:
            roi_list = ['Add in Match ROI or Condition ROI step']
        return roi_list
    
    def get_condition_list(self):
        """Get list of condition names from Check Condition data."""
        condition_list = []
        for item in self.check_conditions_data:
            condition_name = item.get("name", "")
            if condition_name and condition_name not in condition_list:
                condition_list.append(condition_name)
        # If no conditions defined yet, return a default list
        if not condition_list:
            condition_list = ['Add in Check Condition step']
        return condition_list
        
    def save_flow(self):
        """Save the workflow to a JSON file."""
        from datetime import datetime
        from tkinter import filedialog
        import json
        
        # Collect all flow data
        flow_data = {
            "flow_name": self.flow_name_var.get().strip(),
            "created_by": self.user_name_var.get().strip(),
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "technique": self.technique_var.get(),
            "match_roi": self.match_roi_data,
            "automate_roi": self.automate_roi_data,
            "initial_functions": self.initial_functions_data,
            "optimization_settings": self.optimization_data,
            "final_calculation": self.final_calc_data,
            "check_conditions": self.check_conditions_data,
            "condition_rois": self.condition_rois_data,
            "function_adjustments": self.function_adjustments_data,
            "end_flow": self.end_flow_data,
            "beam_settings": self.beam_settings_data,
            "isocenter": self.isocenter_data
        }
        
        # Open file dialog to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Planning Flow"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(flow_data, f, indent=4)
                messagebox.showinfo("Save Flow", f"Planning flow saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save flow:\n{str(e)}")
    
    def load_flow_data(self, data):
        """Load flow data from a dictionary."""
        try:
            # Load basic info
            self.flow_name_var.set(data.get("flow_name", ""))
            self.user_name_var.set(data.get("created_by", ""))
            self.technique_var.set(data.get("technique", ""))
            
            # Load all step data
            self.match_roi_data = data.get("match_roi", [])
            self.automate_roi_data = data.get("automate_roi", [])
            self.initial_functions_data = data.get("initial_functions", [])
            self.optimization_data = data.get("optimization_settings", {})
            self.final_calc_data = data.get("final_calculation", {})
            self.check_conditions_data = data.get("check_conditions", [])
            self.condition_rois_data = data.get("condition_rois", [])
            self.function_adjustments_data = data.get("function_adjustments", [])
            self.end_flow_data = data.get("end_flow", {})
            self.beam_settings_data = data.get("beam_settings", [])
            self.isocenter_data = data.get("isocenter", {})
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load flow data:\n{str(e)}")
    
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
        
        beam_settings_btn = ttk.Button(frame, text="Beam Settings", command=lambda: VMAT_beam_setting_Window(self.planning_window, self) if self.technique_var.get() == "VMAT" else IMPT_beam_setting_Window(self.planning_window, self))
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
        self.match_roi_btn = ttk.Button(frame, text="Match ROI", command=lambda: MatchROI_Window(self.planning_window, self))
        self.match_roi_btn.place(x=50, y=40)
        
        self.automate_roi_btn = ttk.Button(frame, text="Create Automate ROI", command=lambda: AutomateROI_Window(self.planning_window, self))
        self.automate_roi_btn.place(x=200, y=40)
        
        self.initial_function_btn = ttk.Button(frame, text="Initial function", command=lambda: InitialFunction_Window(self.planning_window, self))
        self.initial_function_btn.place(x=380, y=40)
        
        self.optimization_btn = ttk.Button(frame, text="Optimization", command=lambda: OptimizationSetting_Window(self.planning_window, self))
        self.optimization_btn.place(x=380, y=100)
        
        self.final_calc_btn = ttk.Button(frame, text="Final Calculation", command=lambda: FinalCalculationSetting_Window(self.planning_window, self))
        self.final_calc_btn.place(x=200, y=100)
        
        self.check_condition_btn = ttk.Button(frame, text="Check Condition", command=lambda: CheckCondition_Window(self.planning_window, self))
        self.check_condition_btn.place(x=40, y=100)
        
        self.condition_roi_btn = ttk.Button(frame, text="Create Condition ROI", command=lambda: ConditionROI_Window(self.planning_window, self))
        self.condition_roi_btn.place(x=110, y=160)
        
        self.function_adjustment_btn = ttk.Button(frame, text="Conditionally Function Adjustment", command=lambda: FunctionAdjustment_Window(self.planning_window, self))
        self.function_adjustment_btn.place(x=270, y=160)
        
        self.end_flow_btn = ttk.Button(frame, text="End Planning Flow", command=lambda: EndPlanningFlow_Window(self.planning_window, self))
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
