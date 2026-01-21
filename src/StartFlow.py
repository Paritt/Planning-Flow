from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current
import raystation.v2025.typing as rstype
import tkinter as tk
from tkinter import ttk, messagebox
from .flow.start_match_roi import MatchROI
from .flow.plan_creater import PlanCreater


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
            
            # 1. Load flow data from JSON file
            print("Loading flow data...")
            loaded_flow_data = self.load_flow_data(flow_data=workflow_data, plan_data=plan_data)
            
            # 2. Check Match ROI if any not match open ROIs match window then create Match ROI dictionary
            print("Matching ROIs...")
            matcher = MatchROI(loaded_flow_data['match_roi_data'], self.case)
            self.match_roi_dict = matcher.get_matched_dict()
            print("Matched ROI Dictionary:", self.match_roi_dict)
            
            # 3. Create a Plan and add beam based on the loaded flow
            print("Creating a Plan...")
            plan_creator = PlanCreater(loaded_flow_data, self.case)
            if plan_creator.execute():
                print("Success!")
            
            # 4. Create Automate ROI
            
            # 5. Add initial objective
            
            # 6. Loop Optimization Steps
            
            
    def load_flow_data(self, flow_data, plan_data):
        """Load the planning flow data to be a Dictionary format."""
        try:
            # Load basic info
            plan_name = plan_data['plan_name']
            machine = plan_data['machine']
            
            # Load all step data
            technique_data = flow_data.get("technique", {})
            vmat_beam_data = flow_data.get("vmat_beam", [])
            impt_beam_data = flow_data.get("impt_beam", [])
            isocenter_data = flow_data.get("isocenter", {})
            prescription_data = flow_data.get("prescription", {})
            
            match_roi_data = flow_data.get("match_roi", [])
            automate_roi_data = flow_data.get("automate_roi", [])
            initial_functions_data = flow_data.get("initial_functions", [])
            optimization_data = flow_data.get("optimization_settings", {})
            final_calc_data = flow_data.get("final_calculation", {})
            check_conditions_data = flow_data.get("check_conditions", [])
            condition_rois_data = flow_data.get("condition_rois", [])
            function_adjustments_data = flow_data.get("function_adjustments", [])
            end_flow_data = flow_data.get("end_flow", {})
            
            loaded_flow_data = {
                "plan_name": plan_name,
                "machine": machine,
                "technique_data": technique_data,
                "vmat_beam_data": vmat_beam_data,
                "impt_beam_data": impt_beam_data,
                "isocenter_data": isocenter_data,
                "prescription_data": prescription_data,
                "match_roi_data": match_roi_data,
                "automate_roi_data": automate_roi_data,
                "initial_functions_data": initial_functions_data,
                "optimization_data": optimization_data,
                "final_calc_data": final_calc_data,
                "check_conditions_data": check_conditions_data,
                "condition_rois_data": condition_rois_data,
                "function_adjustments_data": function_adjustments_data,
                "end_flow_data": end_flow_data
            }
            
            return loaded_flow_data
            
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