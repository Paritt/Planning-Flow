import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from src.PlanFlowDesigner import PlanFlowDesigner

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
                                        values=['Agility', 'P1'], state="readonly")
        # self.room_dropdown = ttk.Combobox(frame, textvariable=self.room_var,
        #                                 values=['N3_VersaHD', 'N4_VersaHD', 'TrueBeam_L6', 'TrueBeam_L7', 'TrueBeam_N5'], state="readonly")
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

        ttk.Button(frame, text="New Flow", command=self.new_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Edit Flow", command=self.edit_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Start", command=self.start_planning).pack(side="right", padx=5, pady=2)

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
        messagebox.showinfo("Start Planning", "STARTING AUTOMATED PLANNING FROM SELECTED FLOW...")

if __name__ == "__main__":
    app = AutoPlanGUI()
    app.mainloop()
