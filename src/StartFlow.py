import tkinter as tk
from tkinter import ttk, messagebox
from src.flow.start_match_roi import MatchROI
from src.flow.plan_creater import PlanCreater
from src.flow.automate_roi_creater import Automate_ROI_Creater
from src.flow.objecitve_adder import ObjectiveAdder
from src.flow.condition_checker import ConditionChecker
from src.flow.conditional_ROI_creater import ConditionalROICreator
from src.flow.objective_adjuster import ObjectiveAdjuster
from src.flow.ClinicalGoalAdder import ClinicalGoalAdder
import time
from datetime import datetime
import warnings

try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *


class StartFlow:
    def __init__(self, workflow_data, plan_data, selected_steps=None):
        super().__init__()
        # Initialize timing dictionary
        self.step_times = {}
        self.overall_start_time = time.time()
        self.ui = get_current("ui")
        self.case = get_current("Case")
        self.Patient = get_current("Patient")
        
        # Store selected steps (default: all enabled)
        if selected_steps is None:
            self.selected_steps = {
                "create_plan_and_beams": True,
                "automate_roi": True,
                "add_objectives": True,
                "first_optimization": True,
                "loop_optimization": True
            }
        else:
            self.selected_steps = selected_steps
        
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
            elapsed = self._format_time(self.step_times["Load Flow Data"])
            print(f"✅ Completed in {elapsed}\n")
            print('#' * 50 + '\n')
            
            # 2. Check Match ROI if any not match open ROIs match window then create Match ROI dictionary
            print("Matching ROIs...")
            step_start = time.time()
            matcher = MatchROI(loaded_flow_data['match_roi_data'], self.case)
            self.match_roi_dict = matcher.get_matched_dict()
            self.step_times["Match ROIs"] = time.time() - step_start
            print("Matched ROI Dictionary:", self.match_roi_dict)
            elapsed = self._format_time(self.step_times["Match ROIs"])
            print(f"✅ Completed in {elapsed}\n")
            print('#' * 50 + '\n')
            
            # 3. Create a Plan and add beam based on the loaded flow
            if self.selected_steps.get("create_plan_and_beams"):
                print("Plan creation...")
                step_start = time.time()
                self.ui.Navigation.MenuItem['Plan design'].Click()
                self.ui.Navigation.MenuItem['Plan design'].Popup.MenuItem['Plan setup'].Click()
                plan_creator = PlanCreater(loaded_flow_data, self.case, self.selected_examination, self.match_roi_dict)
                plan_creator.create_plan_step()
                self.Patient.Save()
                self.ui.Workspace.TabControl['Plan'].TabItem['Beams'].Select()
                plan_creator.add_beams_step()
                self.Patient.Save()
                self.step_times["Create Plan and Beams"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Create Plan and Beams"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Plan creation - Using existing plan")
                selected_plan_name = None
                
                # First, try to get currently open plan
                try:
                    current_plan = get_current("Plan")
                    selected_plan_name = current_plan.Name
                    print(f"Using currently open plan: {selected_plan_name}")
                except:
                    # No plan currently open, let user select from available plans
                    available_plans = [plan.Name for plan in self.case.TreatmentPlans]
                    
                    if not available_plans:
                        messagebox.showerror("No Plan Available", "No plans found in this case. Please enable 'Create Plan and Add Beams' option.")
                        return
                    elif len(available_plans) == 1:
                        # Only one plan, use it
                        selected_plan_name = available_plans[0]
                        print(f"Using plan: {selected_plan_name}")
                    else:
                        # Multiple plans, let user choose
                        selected_plan_var = tk.StringVar()
                        
                        def on_plan_select():
                            nonlocal selected_plan_name
                            selected_plan_name = selected_plan_var.get()
                            plan_window.destroy()
                        
                        plan_window = tk.Toplevel()
                        plan_window.title("Select Plan")
                        tk.Label(plan_window, text="Multiple plans found. Please select one:").pack(pady=10)
                        
                        plan_combo = ttk.Combobox(plan_window, textvariable=selected_plan_var, values=available_plans, state="readonly")
                        plan_combo.pack(pady=5)
                        plan_combo.current(0)
                        
                        select_button = tk.Button(plan_window, text="Select", command=on_plan_select)
                        select_button.pack(pady=10)
                        
                        plan_window.grab_set()
                        plan_window.wait_window()
                        
                        if selected_plan_name:
                            print(f"Using plan: {selected_plan_name}")
                
                # Update plan_data to reflect selected plan name
                plan_data['plan_name'] = selected_plan_name
                self.plan = self.case.TreatmentPlans[selected_plan_name]
                print()
                
            # 4. Create Automate ROI
            if self.selected_steps.get("automate_roi"):
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
                self.Patient.Save()
                self.step_times["Create Automate ROIs"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Create Automate ROIs"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Automate ROI creation\n")
                
            # 5 Add Clinical Goals from Template
            if self.selected_steps.get("add_clinical_goal") and loaded_flow_data['clinical_goal_data']:
                print("Adding Clinical Goals from Template...")
                step_start = time.time()
                self.ui.Navigation.MenuItem['Plan optimization'].Click()
                self.ui.Navigation.MenuItem['Plan optimization'].Popup.MenuItem['Plan optimization'].Click()
                self.ui.Workspace.TabControl['DVH'].TabItem['Clinical goals'].Select()
                clinical_goal_adder = ClinicalGoalAdder(
                    clinical_goal_data=loaded_flow_data['clinical_goal_data'],
                    matched_roi_dict=self.match_roi_dict,
                    case=self.case,
                    plan_name=plan_data['plan_name']
                )
                clinical_goal_adder.add_clinical_goals()
                self.Patient.Save()
                self.step_times["Add Clinical Goals"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Add Clinical Goals"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Adding Clinical Goals\n")
            
            # 6. Add initial objective
            if self.selected_steps.get("add_objectives"):
                print("Adding Initial Objectives...")
                step_start = time.time()
                self.ui.Navigation.MenuItem['Plan optimization'].Click()
                self.ui.Navigation.MenuItem['Plan optimization'].Popup.MenuItem['Plan optimization'].Click()
                self.ui.Workspace.TabControl['Objectives/constraints'].TabItem['Objectives/constraints'].Select()
                opjective_adder = ObjectiveAdder(
                    initial_functions_data=loaded_flow_data['initial_functions_data'],
                    case=self.case,
                    plan_name=plan_data['plan_name'],
                    matched_roi_dict=self.match_roi_dict,
                    robust_settings=loaded_flow_data['robust_settings']
                )
                opjective_adder.add_initial_objectives()
                self.Patient.Save()
                self.step_times["Add Initial Objectives"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Add Initial Objectives"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Add initial objectives\n")
            
            # 7. Set Optimization Settings and Calculation algorithm
            # TODO: Calculation setting for Proton plan
            if self.selected_steps.get("add_objectives") or self.selected_steps.get("first_optimization"):
                print("Setting Opt. and Cal. Settings...")
                step_start = time.time()
                # Optimization Settings
                self.plan = self.case.TreatmentPlans[plan_data['plan_name']]
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
                self.step_times["Opt. and Cal. Settings"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Opt. and Cal. Settings"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Optimization settings\n")
                
            # 8. First Optimization
            if self.selected_steps.get("first_optimization"):
                print("Starting First Optimization...")
                step_start = time.time()
                self.po.RunOptimization()
                self.Patient.Save()
                self.step_times["First Optimization"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["First Optimization"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] First optimization\n")
                
            # 9. Loop Optimization
            if self.selected_steps.get("loop_optimization"):
                print("Starting Loop Optimization...")
                step_start = time.time()
                # 9.1 Check Conditions
                conditions_checker = ConditionChecker(
                    check_conditions_data=loaded_flow_data['check_conditions_data'],
                    case=self.case,
                    plan_name=plan_data['plan_name'],
                    matched_roi_dict=self.match_roi_dict
                )
                
                # 9.2 Create conditional ROIs
                conditional_roi_creator = ConditionalROICreator(
                    condition_rois_data=loaded_flow_data['condition_rois_data'],
                    matched_roi_dict=self.match_roi_dict,
                    case=self.case,
                    examination=self.selected_examination,
                    plan=self.plan
                )
                
                # 9.3 Adjust objectives
                objective_adjuster = ObjectiveAdjuster(
                    function_adjustments_data=loaded_flow_data['function_adjustments_data'],
                    matched_roi_dict=self.match_roi_dict,
                    case=self.case,
                    plan=self.plan,
                    robust_settings=loaded_flow_data['robust_settings']
                )
                
                # 9.4 Run optimization loop
                for i in range(loaded_flow_data['end_flow_data']['max_optimize_rounds']):
                    self.plan = self.case.TreatmentPlans[plan_data['plan_name']]
                    self.po = self.plan.PlanOptimizations[0]
                    print("  ---------------------")
                    print(f"  Optimization Loop {i+1}/{loaded_flow_data['end_flow_data']['max_optimize_rounds']}...")
                    print("  ---------------------")
                    print("  Checking conditions...")
                    conditions_checker.set_optimization_round(i+1)
                    met_condition = conditions_checker.check_all_conditions()
                    print(f"  Met Condition: {met_condition}")
                    if not met_condition:
                        print("  No conditions met. Exiting optimization loop.\n")
                        break
                    else:
                        loop_start = time.time()
                        conditional_roi_creator.create_all_conditional_rois(met_condition)
                        objective_adjuster.adjust_objectives(met_condition)
                        print("  Running optimization...")
                        self.po.RunOptimization()
                        self.Patient.Save()
                        loop_time = time.time() - loop_start
                        formatted_loop_time = self._format_time(loop_time)
                        print(f"  ✅ Loop {i+1} completed in {formatted_loop_time}\n")
                    
                self.step_times["Loop Optimization"] = time.time() - step_start
                elapsed = self._format_time(self.step_times["Loop Optimization"])
                print(f"✅ Completed in {elapsed}\n")
                print('#' * 50 + '\n')
            else:
                print("[SKIPPED] Loop optimization\n")
            
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
            clinical_goal_data = flow_data.get("clinical_goal", {})
            robust_settings = flow_data.get("robust_settings", {})
            
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
                "end_flow_data": end_flow_data,
                "clinical_goal_data": clinical_goal_data,
                "robust_settings": robust_settings
            }
            
            return loaded_flow_data
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load flow data:\n{str(e)}")
    
    def _format_time(self, seconds):
        """Format time in seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def print_timing_summary(self):
        """Print execution time summary."""
        total_time = time.time() - self.overall_start_time
        
        print("\n" + "=" * 60)
        print("EXECUTION TIME SUMMARY")
        print("=" * 60)
        
        for step_name, step_time in self.step_times.items():
            percentage = (step_time / total_time) * 100
            formatted_time = self._format_time(step_time)
            print(f"{step_name:<30} {formatted_time:>10} ({percentage:>5.1f}%)")
        
        print("-" * 60)
        total_formatted = self._format_time(total_time)
        print(f"{'TOTAL EXECUTION TIME':<30} {total_formatted:>10} (100.0%)")
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