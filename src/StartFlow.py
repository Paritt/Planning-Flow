from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current
import raystation.v2025.typing as rstype
import tkinter as tk
from tkinter import ttk, messagebox
from Planning-Flow.src.window.planflow_designer import PlanFlowDesigner

class StartFlow(self):
    def __init__(self):
        super().__init__()
        # Check is there is an open patient
        self.patient = get_current().get_current_patient()
        if not self.patient:
            messagebox.showerror("No Patient Open", "Please open a patient before starting Planning Flow.")
            return
        # Check is there loaded Planning Flow
        if not hasattr(self, 'workflow_data') or not self.workflow_data:
            messagebox.showwarning("No Flow Loaded", "Please load a Planning Flow before starting.")
            return
        else:
            # Start Planning
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
            self.load_flow_data(flow_data=self.workflow_data, plan_data=self.get_plan_data())
            # 2. Create a Plan and add beam based on the loaded flow
            self.create_plan()
            # 3. Create Match ROI dictionary
            self.create_match_roi_dict()
            # 4. Create Automate ROI
            self.create_automate_roi()
            # 5. Add initial objective
            self.add_initial_objective()
            # 6. Loop Optimization Steps
            self.loop_optimization_steps()
            
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