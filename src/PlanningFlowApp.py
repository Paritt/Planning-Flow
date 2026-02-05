import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import json
import sys
from src.PlanFlowDesigner import PlanFlowDesigner
from src.StartFlow import StartFlow

try:
    from raystation import *
except ImportError:
    from connect import *



class TextRedirector:
    """Redirect stdout/stderr to a text widget."""
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.update()

    def flush(self):
        pass


class PlanningFlowApp(tk.Tk):
    def __init__(self, machine_options, beam_energy_list):
        super().__init__()

        self.machine_options = machine_options
        self.beam_energy_list = beam_energy_list
        
        self.title("Planning Flow 🍃 v1.2")
        self.geometry("570x150")

        # Treatment Parameters Section
        self.create_treatment_settings()

        # Workflow Section
        self.create_workflow_controls()
        
        # Console Output Section (create but don't show yet)
        self.create_console_output()
        self.console_frame.pack_forget()  # Hide initially

        # Loaded Workflow Data
        self.workflow_data = {}
        self.planning_window = None
        
        # Selected workflow steps (default: all enabled)
        self.selected_steps = {
            "create_plan_and_beams": True,
            "automate_roi": True,
            "add_clinical_goal": True,
            "add_objectives": True,
            "first_optimization": True,
            "loop_optimization": True,
            "Early_Stop_mode": True
        }

    def create_treatment_settings(self):
        """Create treatment room and flow selection."""
        frame = ttk.LabelFrame(self, text="Treatment Settings")
        frame.pack(fill="x", padx=10, pady=5)
        
        # Plan Name Entry
        ttk.Label(frame, text="Plan Name:").grid(row=0, column=0, padx=5, pady=2)
        self.plan_name_var = tk.StringVar()
        self.plan_name_entry = ttk.Entry(frame, textvariable=self.plan_name_var)
        self.plan_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Treatment Room Dropdown
        ttk.Label(frame, text="Treatment Room:").grid(row=0, column=2, padx=5, pady=2)
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(frame, textvariable=self.room_var,
                                        values=self.machine_options, state="readonly")
        self.room_dropdown.grid(row=0, column=3, padx=5, pady=2)

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

        ttk.Button(frame, text="New Flow", command=self.new_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Edit Flow", command=self.edit_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Start", command=self.start_planning).pack(side="right", padx=5, pady=2)
        ttk.Button(frame, text="Select Steps", command=self.select_steps).pack(side="right", padx=5, pady=2)
    
    def create_console_output(self):
        """Create console output display."""
        self.console_frame = ttk.LabelFrame(self, text="Process Log")
        self.console_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.console_text = ScrolledText(self.console_frame)
        self.console_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.console_text.config(width=65, height=15, bg="black", fg="white", font=("Consolas", 9))
        
        # Add initial message
        self.console_text.insert(tk.END, "Planning Flow Console\n")
        self.console_text.insert(tk.END, "=" * 60 + "\n")
        self.console_text.insert(tk.END, "Ready to start planning...\n\n")
        
        # Create save log button (hidden initially)
        self.save_log_button = ttk.Button(self.console_frame, text="Save Log", command=self.save_log)
        # Don't pack it yet - it will be shown after successful execution

    def show_step_info(self, step):
        """Popup with step description."""
        messagebox.showinfo("Step Info", f"Details about {step} step.")

    def load_flow(self):
        """Load an existing workflow from JSON."""
        from tkinter import filedialog
        import json
        
        file_path = filedialog.askopenfilename(
            title="Select Planning Flow JSON",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.workflow_data = json.load(f)
                
                # Display flow name in the entry field
                flow_name = self.workflow_data.get("flow_name", "Unnamed Flow")
                self.flow_entry.config(state="normal")
                self.flow_entry.delete(0, tk.END)
                self.flow_entry.insert(0, flow_name)
                self.flow_entry.config(state="readonly")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load workflow:\n{str(e)}")
                self.workflow_data = {}

    def edit_flow(self):
        """Allow editing of the loaded workflow and open the planning steps window."""
        if self.workflow_data:
            # Ensure flow name is displayed in entry field
            flow_name = self.workflow_data.get("flow_name", "Unnamed Flow")
            self.flow_entry.config(state="normal")
            self.flow_entry.delete(0, tk.END)
            self.flow_entry.insert(0, flow_name)
            self.flow_entry.config(state="readonly")
            
            # Open PlanFlowDesigner with loaded data
            PlanFlowDesigner(self, load_data=self.workflow_data, beam_energy_list=self.beam_energy_list)
        else:
            messagebox.showwarning("Edit Flow", "Please load a flow first using 'Load Flow' button.")
    
    def new_flow(self):
        """Create a completely new blank planning flow."""
        # Open PlanFlowDesigner without any data (blank flow)
        PlanFlowDesigner(self, beam_energy_list=self.beam_energy_list)
    
    def select_steps(self):
        """Open window to select which workflow steps to execute."""
        step_window = tk.Toplevel(self)
        step_window.title("Select Workflow Steps")
        step_window.geometry("350x280")
        step_window.attributes('-topmost', True)
        
        tk.Label(step_window, text="Select steps to execute:", font=("Arial", 10, "bold")).pack(pady=10)
        
        # Create checkbox variables
        check_vars = {}
        step_labels = [
            ("create_plan_and_beams", "Create Plan and Add Beams"),
            ("automate_roi", "Automate ROI"),
            ("add_clinical_goal", "Add Clinical Goal"),
            ("add_objectives", "Add Initial Objectives"),
            ("first_optimization", "Run 1st Optimization")
        ]
        
        for step_key, step_label in step_labels:
            var = tk.BooleanVar(value=self.selected_steps[step_key])
            check_vars[step_key] = var
            ttk.Checkbutton(step_window, text=step_label, variable=var).pack(anchor="w", padx=30, pady=3)
        
        loop_optimize_frame = ttk.Frame(step_window)
        check_vars["loop_optimization"] = tk.BooleanVar(value=self.selected_steps["loop_optimization"])
        ttk.Checkbutton(loop_optimize_frame, text="Run Loop Optimization", variable=check_vars["loop_optimization"]).pack(side='left', pady=3)
        check_vars["Early_Stop_mode"] = tk.BooleanVar(value=self.selected_steps["Early_Stop_mode"])
        ttk.Checkbutton(loop_optimize_frame, text="Early Stop Mode", variable=check_vars["Early_Stop_mode"]).pack(side='left', padx=5,pady=3)
        early_stop_info_but = ttk.Button(loop_optimize_frame, text="?", command=lambda: messagebox.showinfo("Early Stop Mode", "If enabled, the loop optimization will stop early if none of the defined conditions are met in a loop iteration."), width=2)
        early_stop_info_but.pack(side='left', pady=3)
        
        loop_optimize_frame.pack(anchor="w", padx=30, pady=3)
        
        def apply_selection():
            for step_key in check_vars:
                self.selected_steps[step_key] = check_vars[step_key].get()
            messagebox.showinfo("Steps Updated", "Workflow steps selection has been updated.")
            step_window.destroy()
        
        def select_all():
            for var in check_vars.values():
                var.set(True)
        
        def deselect_all():
            for var in check_vars.values():
                var.set(False)
        
        # Button frame
        btn_frame = ttk.Frame(step_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Select All", command=select_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Deselect All", command=deselect_all).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Apply", command=apply_selection).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=step_window.destroy).pack(side="left", padx=5)

    def start_planning(self):
        """Start the automated planning process."""
        plan_data = {
            'plan_name': self.plan_name_var.get(),
            'machine': self.room_var.get()
        }
        if not self.workflow_data:
            messagebox.showerror("Start Planning", "Please load a flow first using 'Load Flow' button.")
            return
        
        # Only validate plan name and machine if creating new plan
        if self.selected_steps.get("create_plan_and_beams"):
            if plan_data['plan_name'] == "":
                messagebox.showerror("Input Error", "Please enter a Plan Name.")
                return
            if plan_data['machine'] == "":
                messagebox.showerror("Input Error", "Please select a Treatment Room.")
                return
        
        
        # Expand window and show console
        self.geometry("570x500")
        self.console_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Clear console
        self.console_text.delete(1.0, tk.END)
        self.console_text.insert(tk.END, f"Starting Planning Flow: {self.workflow_data.get('flow_name', 'Unnamed')}\n")
        self.console_text.insert(tk.END, f"Plan: {plan_data['plan_name'] if plan_data['plan_name'] else 'Using existing plan'} | Machine: {plan_data['machine'] if plan_data['machine'] else 'N/A'}\n")
        self.console_text.insert(tk.END, "=" * 60 + "\n\n")
        
        # Redirect stdout and stderr to console
        sys.stdout = TextRedirector(self.console_text)
        sys.stderr = TextRedirector(self.console_text)
        self.update()
        
        try:
            StartFlow(workflow_data=self.workflow_data, plan_data=plan_data, selected_steps=self.selected_steps)
            print("\n" + "=" * 60)
            print("✅ Planning Flow Completed Successfully!")
            print("=" * 60 + "\n")
            
            # Show save log button on success
            self.save_log_button.pack(side="bottom", pady=5)
                
        except Exception as e:
            print("\n" + "=" * 60)
            print(f"❌ Error during planning flow: {str(e)}")
            print("=" * 60 + "\n")
            messagebox.showerror("Planning Flow Error", f"An error occurred:\n{str(e)}")
            
            # Ask if user wants to save error log (popup for errors)
            if messagebox.askyesno("Save Error Log", "Would you like to save the error log?"):
                self.save_log()
                
        finally:
            # Restore stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
    
    def save_log(self):
        """Save console log to a text file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Execution Log",
            initialfile=f"PlanningFlow_Log_{self.workflow_data.get('flow_name', 'Unnamed')}_{self.plan_name_var.get()}.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.console_text.get(1.0, tk.END))
                messagebox.showinfo("Log Saved", f"Log saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save log:\n{str(e)}")
            
