from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current
import raystation.v2025.typing as rstype
import tkinter as tk
from tkinter import ttk, messagebox
from .flow.start_match_roi import MatchROI
from .flow.plan_creater import PlanCreater
from src.flow.automate_roi_creater import Automate_ROI_Creater
from src.flow.objecitve_adder import ObjectiveAdder
import time
from datetime import datetime
import warnings

# Suppress RayStation's deprecation warnings about CLR module loading
warnings.filterwarnings('ignore', category=DeprecationWarning, module='raystation.v2025.__api__')


class StartFlow:
    def __init__(self, workflow_data, plan_data):
        super().__init__()
        # Initialize timing dictionary
        self.step_times = {}
        self.overall_start_time = time.time()
        self.ui = get_current("ui")
        self.case = get_current("Case")
        
        # Check is the Plan Name not Unique
        plan_name = plan_data.get('plan_name', '')
        existing_plans = [plan.Name for plan in self.case.TreatmentPlans]
        if plan_name in existing_plans:
            messagebox.showerror("Plan Name Exists", f"A plan named '{plan_name}' already exists. Please rename.")
            return
        else:
            pass  # Plan name is unique, proceed
        
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
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("")
            
            # 0. Ask user to choose examination if multiple exist
            if len(self.case.Examinations) > 1:
                exam_names = [exam.Name for exam in self.case.Examinations]
                selected_exam = tk.StringVar()
                
                def on_select():
                    chosen_exam = selected_exam.get()
                    for exam in self.case.Examinations:
                        if exam.Name == chosen_exam:
                            self.selected_examination = exam
                            break
                    exam_window.destroy()
                
                exam_window = tk.Toplevel()
                exam_window.title("Select Examination")
                tk.Label(exam_window, text="Multiple examinations found. Please select one:").pack(pady=10)
                
                exam_combo = ttk.Combobox(exam_window, textvariable=selected_exam, values=exam_names, state="readonly")
                exam_combo.pack(pady=5)
                exam_combo.current(0)
                
                select_button = tk.Button(exam_window, text="Select", command=on_select)
                select_button.pack(pady=10)
                
                exam_window.grab_set()
                exam_window.wait_window()
            else:
                self.selected_examination = self.case.Examinations[0]
            
            # 1. Load flow data from JSON file
            print("Loading flow data...")
            step_start = time.time()
            loaded_flow_data = self.load_flow_data(flow_data=workflow_data, plan_data=plan_data)
            self.step_times["Load Flow Data"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['Load Flow Data']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # 2. Check Match ROI if any not match open ROIs match window then create Match ROI dictionary
            print("Matching ROIs...")
            step_start = time.time()
            matcher = MatchROI(loaded_flow_data['match_roi_data'], self.case)
            self.match_roi_dict = matcher.get_matched_dict()
            self.step_times["Match ROIs"] = time.time() - step_start
            print("Matched ROI Dictionary:", self.match_roi_dict)
            print(f"✅ Completed in {self.step_times['Match ROIs']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # 3. Create a Plan and add beam based on the loaded flow
            print("Plan creation...")
            step_start = time.time()
            self.ui.Navigation.MenuItem['Plan design'].Click()
            self.ui.Navigation.MenuItem['Plan design'].Popup.MenuItem['Plan setup'].Click()
            plan_creator = PlanCreater(loaded_flow_data, self.case, self.selected_examination)
            plan_creator.execute()
            self.step_times["Create Plan and Beams"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['Create Plan and Beams']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # 4. Create Automate ROI
            print("Creating Automate ROIs...")
            self.ui.Navigation.MenuItem['Patient modeling'].Click()
            self.ui.Navigation.MenuItem['Patient modeling'].Popup.MenuItem['Structure definition'].Click()
            self.ui.ToolPanel.TabItem['ROIs'].Select()
            step_start = time.time()
            roi_creater = Automate_ROI_Creater(
                automate_roi_data=loaded_flow_data['automate_roi_data'],
                matched_roi_dict=self.match_roi_dict,
                case=self.case,
                examination=self.selected_examination
            )
            roi_creater.create_all_rois()
            self.step_times["Create Automate ROIs"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['Create Automate ROIs']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # 5. Add initial objective
            print("Adding Initial Objectives...")
            step_start = time.time()
            self.ui.Navigation.MenuItem['Plan optimization'].Click()
            self.ui.Navigation.MenuItem['Plan optimization'].Popup.MenuItem['Plan optimization'].Click()
            self.ui.Workspace.TabControl['Objectives/constraints'].TabItem['Objectives/constraints'].Select()
            opjective_adder = ObjectiveAdder(
                initial_functions_data=loaded_flow_data['initial_functions_data'],
                case=self.case,
                plan_name=plan_data['plan_name'],
                matched_roi_dict=self.match_roi_dict
            )
            opjective_adder.add_initial_objectives()
            self.step_times["Add Initial Objectives"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['Add Initial Objectives']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # 6. Set Optimization Settings and Calculation algorithm
            print("Setting Optimization and Calculation Settings...")
            step_start = time.time()
            # Optimization Settings
            self.plan = self.case.TreatmentPlans[plan_name]
            self.po = self.plan.PlanOptimizations[0]
            self.po.OptimizationParameters.Algorithm.MaxNumberOfIterations = loaded_flow_data['optimization_data']['max_iterations']
            self.po.OptimizationParameters.Algorithm.OptimalityTolerance = loaded_flow_data['optimization_data']['tolerance']
            # Set Calculation algorithm
            if loaded_flow_data['technique_data'] == 'VMAT':
                print("[VMAT] Using default calculation algorithm -> Collapsed Cone...")
            elif loaded_flow_data['technique_data'] == 'IMPT':
                print("[IMPT] Setting calculation algorithm to Proton Pencil Beam...")
            else:
                print("Unknown technique type for calculation algorithm setting.")
            self.step_times["Optimization and Calculation Settings"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['Optimization and Calculation Settings']:.2f}s\n")
            print('#' * 50 + '\n')
                
            # 7. First Optimization
            print("Starting First Optimization...")
            step_start = time.time()
            self.po.RunOptimization()
            self.step_times["First Optimization"] = time.time() - step_start
            print(f"✅ Completed in {self.step_times['First Optimization']:.2f}s\n")
            print('#' * 50 + '\n')
            
            # Print timing summary
            self.print_timing_summary()
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
    
    def print_timing_summary(self):
        """Print execution time summary."""
        total_time = time.time() - self.overall_start_time
        
        print("\n" + "=" * 60)
        print("EXECUTION TIME SUMMARY")
        print("=" * 60)
        
        for step_name, step_time in self.step_times.items():
            percentage = (step_time / total_time) * 100
            print(f"{step_name:<30} {step_time:>8.2f}s ({percentage:>5.1f}%)")
        
        print("-" * 60)
        print(f"{'TOTAL EXECUTION TIME':<30} {total_time:>8.2f}s (100.0%)")
        print("=" * 60)
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")
                
    def get_plan_data(self):
        """Retrieve current plan data as a dictionary."""
        plan_name = None
        machine = None
        
        plan_data = {
            "plan_name": plan_name,
            "machine": machine
        }
        
        return plan_data