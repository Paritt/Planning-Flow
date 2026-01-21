import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import json
import sys
from src.PlanFlowDesigner import PlanFlowDesigner
from src.StartFlow import StartFlow


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


class AutoPlanGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Planning Flow 🍃")
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
                                        values=['Agility', 'P1'], state="readonly")
        # self.room_dropdown = ttk.Combobox(frame, textvariable=self.room_var,
        #                                 values=['N3_VersaHD', 'N4_VersaHD', 'TrueBeam_L6', 'TrueBeam_L7', 'TrueBeam_N5'], state="readonly")
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
            PlanFlowDesigner(self, load_data=self.workflow_data)
        else:
            messagebox.showwarning("Edit Flow", "Please load a flow first using 'Load Flow' button.")
    
    def new_flow(self):
        """Create a completely new blank planning flow."""
        # Open PlanFlowDesigner without any data (blank flow)
        PlanFlowDesigner(self)

    def start_planning(self):
        """Start the automated planning process."""
        plan_data = {
            'plan_name': self.plan_name_var.get(),
            'machine': self.room_var.get()
        }
        if not self.workflow_data:
            messagebox.showerror("Start Planning", "Please load a flow first using 'Load Flow' button.")
            return
        if plan_data['plan_name'] == "":
            messagebox.showerror("Input Error", "Please enter a Plan Name.")
            return
        if plan_data['machine'] == "":
            messagebox.showerror("Input Error", "Please select a Treatment Room.")
            return
        else:
            # Expand window and show console
            self.geometry("570x500")
            self.console_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Clear console
            self.console_text.delete(1.0, tk.END)
            self.console_text.insert(tk.END, f"Starting Planning Flow: {self.workflow_data.get('flow_name', 'Unnamed')}\n")
            self.console_text.insert(tk.END, f"Plan: {plan_data['plan_name']} | Machine: {plan_data['machine']}\n")
            self.console_text.insert(tk.END, "=" * 60 + "\n\n")
            
            # Redirect stdout and stderr to console
            sys.stdout = TextRedirector(self.console_text)
            sys.stderr = TextRedirector(self.console_text)
            self.update()
            
            try:
                StartFlow(workflow_data=self.workflow_data, plan_data=plan_data)
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
            

if __name__ == "__main__":
    app = AutoPlanGUI()
    app.mainloop()
