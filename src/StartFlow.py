from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current
import raystation.v2025.typing as rstype
import tkinter as tk
from tkinter import ttk, messagebox
from .catwork import CatWork
from .start_match_roi import MatchROI


class StartFlow:
    def __init__(self, workflow_data, plan_data):
        super().__init__()
        # Check is there is an open case
        try:
            self.case = get_current("Case")
        except:
            self.case = None
        
        if not self.case:
            messagebox.showerror("No Case Open", "Please open a case before starting Planning Flow.")
            return
        else:
            # Start Planning
            # Show cat_work.gif to indicate processing
            catwork = CatWork(message="Starting Planning Flow...", gif_name='cat_work.gif')
            catwork.start()
            
            # 0. Initialize data storage for all steps
            self.vmat_beam_data = []
            self.impt_beam_data = []
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
            
            # 1. Load flow data from JSON file
            self.load_flow_data(flow_data=workflow_data, plan_data=plan_data)
            # 2. Check Match ROI if any not match open ROIs match window then create Match ROI dictionary
            matcher = MatchROI(self.match_roi_data, self.case)
            self.match_roi_dict = matcher.get_matched_dict()
            print("Matched ROI Dictionary:", self.match_roi_dict)
            # 3. Create a Plan and add beam based on the loaded flow
            self.create_plan()
            # 4. Create Automate ROI
            self.create_automate_roi()
            # 5. Add initial objective
            self.add_initial_objective()
            # 6. Loop Optimization Steps
            self.loop_optimization_steps()
            
            catwork.stop()
            
    def load_flow_data(self, flow_data, plan_data):
        """Load the planning flow data to be a Dictionary format."""
        try:
            # Load basic info
            self.plan_name = plan_data['plan_name']
            self.machine = plan_data['machine']
            
            # Load all step data
            self.technique_data = flow_data.get("technique", {})
            self.vmat_beam_data = flow_data.get("vmat_beam", [])
            self.impt_beam_data = flow_data.get("impt_beam", [])
            self.isocenter_data = flow_data.get("isocenter", {})
            
            self.match_roi_data = flow_data.get("match_roi", [])
            self.automate_roi_data = flow_data.get("automate_roi", [])
            self.initial_functions_data = flow_data.get("initial_functions", [])
            self.optimization_data = flow_data.get("optimization_settings", {})
            self.final_calc_data = flow_data.get("final_calculation", {})
            self.check_conditions_data = flow_data.get("check_conditions", [])
            self.condition_rois_data = flow_data.get("condition_rois", [])
            self.function_adjustments_data = flow_data.get("function_adjustments", [])
            self.end_flow_data = flow_data.get("end_flow", {})
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load flow data:\n{str(e)}")
                
    def get_plan_data(self):
        """Retrieve current plan data as a dictionary."""
        plan_name = None
        machine = None
        
        plan_data = {
            "plan_name": plan_name,
            "machine": machine
        }
        
        return plan_data
    
    def create_plan(self):
        """Create a new plan in the current patient."""
        try:
            # Create a new plan
            self.plan = self.patient.add_new_plan(self.plan_name, self.machine)
        except Exception as e:
            messagebox.showerror("Plan Creation Error", f"Failed to create plan:\n{str(e)}")
            
    def create_match_roi_dict(self):
        """Create Match ROI dictionary based on loaded data."""
        try:
            self.match_roi_dict = {}
            for match in self.match_roi_data:
                roi_name = match.get("roi_name")
                match_params = match.get("match_params", {})
                self.match_roi_dict[roi_name] = match_params
        except Exception as e:
            messagebox.showerror("Match ROI Error", f"Failed to create Match ROI dictionary:\n{str(e)}")
            
    def create_automate_roi(self):
        """Create Automate ROI based on loaded data."""
        try:
            for automate in self.automate_roi_data:
                roi_name = automate.get("roi_name")
                automate_params = automate.get("automate_params", {})
                # Implement the logic to create or modify ROI based on automate_params
                # This is a placeholder for actual implementation
        except Exception as e:
            messagebox.showerror("Automate ROI Error", f"Failed to create Automate ROI:\n{str(e)}")
    
    def add_initial_objective(self):
        """Add initial objectives to the plan based on loaded data."""
        try:
            for objective in self.initial_functions_data:
                roi_name = objective.get("roi_name")
                function_params = objective.get("function_params", {})
                # Implement the logic to add objectives to the plan based on function_params
                # This is a placeholder for actual implementation
        except Exception as e:
            messagebox.showerror("Initial Objective Error", f"Failed to add initial objectives:\n{str(e)}")
    
    def loop_optimization_steps(self):
        """Loop through optimization steps based on loaded data."""
        try:
            for step in self.optimization_data.get("steps", []):
                step_name = step.get("step_name")
                step_params = step.get("step_params", {})
                # Implement the logic to perform optimization steps based on step_params
                # This is a placeholder for actual implementation
        except Exception as e:
            messagebox.showerror("Optimization Error", f"Failed during optimization steps:\n{str(e)}")