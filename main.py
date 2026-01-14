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

        ttk.Button(frame, text="New Flow", command=self.new_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Edit Flow", command=self.edit_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Start", command=self.start_planning).pack(side="right", padx=5, pady=2)

    def open_planning_steps_window(self):
        """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
        """Open a new window for planning steps."""
        if self.planning_window is not None:
            self.planning_window.destroy()

        self.planning_window = tk.Toplevel(self)
        self.planning_window.title("Planning flow")
        self.planning_window.geometry("550x300")
        
        frame = ttk.LabelFrame(self.planning_window, text="Planning Flow")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Flow Name Label + Entry
        ttk.Label(frame, text="Flow Name:").place(x=20, y=0)
        self.flow_name_var = tk.StringVar()
        self.flow_name_entry = ttk.Entry(frame, textvariable=self.flow_name_var)
        self.flow_name_entry.place(x=100, y=0, width=150)

        # User Name Label + Entry
        ttk.Label(frame, text="By:").place(x=260, y=0)
        self.user_name_var = tk.StringVar()
        self.user_name_entry = ttk.Entry(frame, textvariable=self.user_name_var)
        self.user_name_entry.place(x=290, y=0, width=150)

        # Steps Buttons
        self.match_roi_btn = ttk.Button(frame, text="Match ROI", command=self.open_match_roi_window)
        self.match_roi_btn.place(x=50, y=40)
        
        self.automate_roi_btn = ttk.Button(frame, text="Create Automate ROI", command=self.open_automate_roi_window)
        self.automate_roi_btn.place(x=200, y=40)
        
        self.initial_function_btn = ttk.Button(frame, text="Initial function", command=self.open_initial_function_window)
        self.initial_function_btn.place(x=380, y=40)
        
        self.optimization_btn = ttk.Button(frame, text="Optimization", command=self.open_optimization_settings_window)
        self.optimization_btn.place(x=380, y=100)
        
        self.final_calc_btn = ttk.Button(frame, text="Final Calculation", command=self.open_final_calculation_window)
        self.final_calc_btn.place(x=200, y=100)
        
        self.check_condition_btn = ttk.Button(frame, text="Check Condition", command=self.open_check_condition_window)
        self.check_condition_btn.place(x=40, y=100)
        
        self.condition_roi_btn = ttk.Button(frame, text="Create Condition ROI", command=self.open_condition_roi_window)
        self.condition_roi_btn.place(x=110, y=160)
        
        self.function_adjustment_btn = ttk.Button(frame, text="Conditionally Function Adjustment", command=self.open_function_adjustment_window)
        self.function_adjustment_btn.place(x=270, y=160)
        
        self.end_flow_btn = ttk.Button(frame, text="End Planning Flow", command=self.open_end_planning_flow_window)
        self.end_flow_btn.place(x=20, y=220)

        # Save Flow Button
        self.save_flow_btn = ttk.Button(frame, text="Save Flow", command=self.save_flow)
        self.save_flow_btn.place(x=400, y=220)

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

    def show_step_info(self, step):
        """Popup with step description."""
        messagebox.showinfo("Step Info", f"Details about {step} step.")

    def new_flow(self):
        """Reset the workflow to create a new one."""
        self.workflow_data = {"flow_name": "", "steps": []}
        self.open_planning_steps_window()

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
        messagebox.showinfo("Start Planning", "The automated planning process has begun.")

    def save_flow(self):
        """Save the workflow to a JSON file."""
        # Update the workflow data with flow_name and user_name
        self.workflow_data["flow_name"] = self.flow_name_var.get()
        self.workflow_data["user_name"] = self.user_name_var.get()

        if not self.workflow_data["flow_name"]:
            messagebox.showwarning("Save Flow", "Please enter a flow name.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.workflow_data, f, indent=4)
            messagebox.showinfo("Save Flow", f"Workflow saved to {file_path}")

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
    
    def open_match_roi_window(self):
        """Open a new window for Match ROI step."""
        match_roi_window = tk.Toplevel(self)
        match_roi_window.title("Match ROI")
        match_roi_window.geometry("430x360")

        # Bold Title Label
        title_label = tk.Label(match_roi_window, text="Match ROI", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # ROI tree
        self.roi_tree = ttk.Treeview(match_roi_window, columns=("ROI name", "Possible ROI name"), show="headings")
        self.roi_tree.heading("ROI name", text="ROI name")
        self.roi_tree.heading("Possible ROI name", text="Possible ROI name")
        self.roi_tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        # Add ROI Button
        self.add_roi_btn = ttk.Button(match_roi_window, text="Add ROI", command=self.open_add_roi_popup)
        self.add_roi_btn.grid(row=2, column=0, pady=5)
        # Remove ROI Button
        self.remove_roi_btn = ttk.Button(match_roi_window, text="Remove Selected ROI", command=self.remove_match_roi)
        self.remove_roi_btn.grid(row=2, column=1, pady=5)
        # Edit ROI Button
        self.edit_roi_btn = ttk.Button(match_roi_window, text="Edit Selected ROI", command=lambda: self.show_step_info("Edit ROI"))
        self.edit_roi_btn.grid(row=2, column=2, pady=5)
        # Save ROI List Button
        self.save_roi_list = ttk.Button(match_roi_window, text="Save", command=lambda: self.save_match_roi_list())
        self.save_roi_list.grid(row=3, column=0, pady=5)
        # Close Button
        self.close_btn = ttk.Button(match_roi_window, text="Close", command=match_roi_window.destroy)
        self.close_btn.grid(row=3, column=1, pady=5)

    def open_add_roi_popup(self):
        """Open a popup window to add ROI."""
        add_roi_popup = tk.Toplevel(self)
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
            
    def open_automate_roi_window(self):
        """Open a new window for Automate ROI step."""
        roi_window = tk.Toplevel(self)
        roi_window.title("Automate ROI")
        roi_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(roi_window, text="Automate ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for ROI List (Supports Ordering and Functions)
        self.roi_tree = ttk.Treeview(roi_window, columns=("Order", "ROI Name"), show="headings")
        self.roi_tree.heading("Order", text="Order")
        self.roi_tree.heading("ROI Name", text="ROI Name")
        self.roi_tree.pack(pady=5, fill="both", expand=True)

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
        self.close_btn = ttk.Button(roi_window, text="Close", command=roi_window.destroy)
        self.close_btn.pack(pady=10)

    def open_new_roi_popup(self):
        """Open a popup window to add a new ROI item."""
        new_roi_popup = tk.Toplevel(self)
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
        self.boolean_window = tk.Toplevel(self)
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
        save_button = tk.Button(self.boolean_window, text="Save", command=lambda: self.boolean_window.destroy())
        save_button.pack(pady=10)
        
    def open_initial_function_window(self):
        """Open a new window for Initial Objective step."""
        initial_function_window = tk.Toplevel(self)
        initial_function_window.title("Initial Optimization function")
        initial_function_window.geometry("1200x400")

        # Bold Title Label
        title_label = tk.Label(initial_function_window, text="Initial Optimization function", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Content can be added here
        self.initial_function_tree = ttk.Treeview(initial_function_window, columns=("Function tag", "Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings")
        self.initial_function_tree.heading("Function tag", text="Function tag")
        self.initial_function_tree.heading("Function Type", text="Function Type")
        self.initial_function_tree.heading("ROI", text="ROI")
        self.initial_function_tree.heading("Weight", text="Weight")
        self.initial_function_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.initial_function_tree.heading("Volume level (%)", text="Volume level (%)")
        self.initial_function_tree.pack(pady=5, fill="both", expand=True)
        
        # Add Objective Button
        self.add_objective_btn = ttk.Button(initial_function_window, text="Add function", command=self.open_add_function_window)
        self.add_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Objective Button
        self.delete_objective_btn = ttk.Button(initial_function_window, text="Delete Selected function", command=lambda: self.show_step_info("Delete function"))
        self.delete_objective_btn.pack(side="left", padx=5, pady=5)

        # Save Button
        self.save_initial_function_btn = ttk.Button(initial_function_window, text="Save", command=lambda: self.show_step_info("Initial Functions Saved"))
        self.save_initial_function_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(initial_function_window, text="Close", command=initial_function_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
        
    def open_add_function_window(self):
        """Add an optimization function to the list."""
        add_function_window = tk.Toplevel(self)
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
        
    def open_optimization_settings_window(self):
        """Open a new window for Optimization step."""
        optimization_window = tk.Toplevel(self)
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
        
    def open_final_calculation_window(self):
        """Open a new window for Final Calculation step."""
        final_calc_window = tk.Toplevel(self)
        final_calc_window.title("Final Calculation")
        final_calc_window.geometry("250x70")

        ttk.Label(final_calc_window, text="Algorithm").grid(row=0, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        ttk.Combobox(final_calc_window, values=['Pencil beam', 'CC', 'MonteCarlo'], state="readonly", textvariable=self.algorithm_var).grid(row=0, column=1, padx=5, pady=5)
        
        # Save Button
        ttk.Button(final_calc_window, text="Save", command=lambda: self.show_step_info("Final Calculation Settings Saved")).grid(row=1, column=0,padx=5, pady=10)
        
        # Close Button
        ttk.Button(final_calc_window, text="Close", command=final_calc_window.destroy).grid(row=1, column=1, padx=5, pady=10)
    
    def open_check_condition_window(self):
        """Open a new window for Check Condition step."""
        check_condition_window = tk.Toplevel(self)
        check_condition_window.title("Check Condition")
        check_condition_window.geometry("800x400")
        
        # Bold Title Label
        title_label = tk.Label(check_condition_window, text="Check Condition", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        self.condition_tree = ttk.Treeview(check_condition_window, columns=("Condition Name", "ROI",  "Condition Type", "Parameter Value", "Criteria"), show="headings")
        self.condition_tree.heading("Condition Name", text="Condition Name")
        self.condition_tree.heading("ROI", text="ROI")
        self.condition_tree.heading("Condition Type", text="Condition Type")
        self.condition_tree.heading("Parameter Value", text="Parameter Value")
        self.condition_tree.heading("Criteria", text="Criteria")
        self.condition_tree.pack(pady=5, fill="both", expand=True)
        
        # Add Condition Button
        self.add_condition_btn = ttk.Button(check_condition_window, text="New", command=self.open_add_condition_window)
        self.add_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition Button
        self.delete_condition_btn = ttk.Button(check_condition_window, text="Remove", command=lambda: self.show_step_info("Remove Condition"))
        self.delete_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit Condition Button
        self.edit_condition_btn = ttk.Button(check_condition_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Save Button
        self.save_condition_btn = ttk.Button(check_condition_window, text="Save", command=lambda: self.show_step_info("Conditions Saved"))
        self.save_condition_btn.pack(side="left", padx=5, pady=5)

        # Close Button
        self.close_btn = ttk.Button(check_condition_window, text="Close", command=check_condition_window.destroy)
        self.close_btn.pack(pady=10)
        
    def open_add_condition_window(self):
        """Add a condition to the list."""
        add_condition_window = tk.Toplevel(self)
        add_condition_window.title("Add Condition")
        add_condition_window.geometry("300x200")
        
        ttk.Label(add_condition_window, text="Condition Name:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_name_var = tk.StringVar()
        self.condition_name_entry = ttk.Entry(add_condition_window, textvariable=self.condition_name_var)
        self.condition_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_window, text="Condition Type:").grid(row=2, column=0, padx=5, pady=5)
        self.condition_type_var = tk.StringVar()
        self.condition_type_combo = ttk.Combobox(add_condition_window, textvariable=self.condition_type_var,
                                            values=['Optimization Round','Max DaV', 'Max VaD', 'Max Dmean', 'Min DaV', 'Min VaD', 'Min Dmean'], state="readonly")
        self.condition_type_combo.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_window, text="ROI Name:").grid(row=1, column=0, padx=5, pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_combo = ttk.Combobox(add_condition_window, textvariable=self.roi_name_var,
                                        values=['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External'], state="readonly")
        self.roi_name_combo.grid(row=1, column=1, padx=5, pady=5)
        
        
        ttk.Label(add_condition_window, text="Parameter value:").grid(row=3, column=0, padx=5, pady=5)
        self.parameter_value_var = tk.StringVar()
        self.parameter_value_entry = ttk.Entry(add_condition_window, textvariable=self.parameter_value_var)
        self.parameter_value_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_window, text="Criteria:").grid(row=4, column=0, padx=5, pady=5)
        self.criteria_var = tk.StringVar()
        self.criteria_entry = ttk.Entry(add_condition_window, textvariable=self.criteria_var)
        self.criteria_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Button(add_condition_window, text="Add", command=lambda: self.add_condition(add_condition_window)).grid(row=5, column=0, columnspan=2, pady=10)

    def add_condition(self, popup):
        """Save the new condition to the list."""
        condition_name = self.condition_name_var.get().strip()
        roi_name = self.roi_name_var.get().strip()
        condition_type = self.condition_type_var.get().strip()
        parameter_value = self.parameter_value_var.get().strip()
        criteria = self.criteria_var.get().strip()
        # Here you would add the condition to your data structure
        self.condition_tree.insert("", "end", values=(condition_name, roi_name, condition_type, parameter_value, criteria))
        popup.destroy()
    
    def open_condition_roi_window(self):
        """Open a new window for Condition ROI step."""
        condition_roi_window = tk.Toplevel(self)
        condition_roi_window.title("Condition ROI")
        condition_roi_window.geometry("800x400")
        
        # Bold Title Label
        title_label = tk.Label(condition_roi_window, text="Condition ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Treeview for Condition ROI List
        self.condition_roi_tree = ttk.Treeview(condition_roi_window, columns=("Order","If this condition TRUE", "Create this ROI", "By this method"), show="headings")
        self.condition_roi_tree.heading("Order", text="Order")
        self.condition_roi_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.condition_roi_tree.heading("Create this ROI", text="Create this ROI")
        self.condition_roi_tree.heading("By this method", text="By this method")
        self.condition_roi_tree.pack(pady=5, fill="both", expand=True)
        
        # Add Condition ROI Button
        self.add_condition_roi_btn = ttk.Button(condition_roi_window, text="New", command=self.open_add_condition_roi_window)
        self.add_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition ROI Button
        self.delete_condition_roi_btn = ttk.Button(condition_roi_window, text="Remove", command=lambda: self.show_step_info("Remove Condition ROI"))
        self.delete_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Move Up Button
        self.move_up_condition_btn = ttk.Button(condition_roi_window, text="Move Up", command=lambda: self.show_step_info("Move Condition Up"))
        self.move_up_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Move Down Button
        self.move_down_condition_btn = ttk.Button(condition_roi_window, text="Move Down", command=lambda: self.show_step_info("Move Condition Down"))
        self.move_down_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit
        self.edit_condition_btn = ttk.Button(condition_roi_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        
        # Save Button
        self.save_condition_roi_btn = ttk.Button(condition_roi_window, text="Save", command=lambda: self.show_step_info("Condition ROIs Saved"))
        self.save_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        ttk.Button(condition_roi_window, text="Close", command=condition_roi_window.destroy).pack(pady=10)
    
    def open_add_condition_roi_window(self):
        """Add a condition ROI to the list."""
        add_condition_roi_window = tk.Toplevel(self)
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
        
        ttk.Button(add_condition_roi_window, text="Boolean operation", command=self.open_boolean_window).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_roi_window, text="Convert Dose (Gy) to ROI").grid(row=4, column=0, padx=5, pady=5)
        self.dose_to_roi_var = tk.StringVar()
        self.dose_to_roi_entry = ttk.Entry(add_condition_roi_window, textvariable=self.dose_to_roi_var)
        self.dose_to_roi_entry.grid(row=4, column=1, padx=5, pady=5)
        
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
        
    def open_function_adjustment_window(self):
        """Open a new window for Function Adjustment step."""
        function_adjustment_window = tk.Toplevel(self)
        function_adjustment_window.title("Function Adjustment")
        function_adjustment_window.geometry("1500x800")
        
        # Bold Title Label
        title_label = tk.Label(function_adjustment_window, text="Function Adjustment", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Old function frame
        old_function_label_frame = tk.LabelFrame(function_adjustment_window, text="Initial Functions")
        old_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # Old function Tree
        self.old_function_tree = ttk.Treeview(old_function_label_frame, columns=("Function tag","Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings")
        self.old_function_tree.heading("Function tag", text="Function tag")
        self.old_function_tree.heading("Function Type", text="Function Type")
        self.old_function_tree.heading("ROI", text="ROI")
        self.old_function_tree.heading("Weight", text="Weight")
        self.old_function_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.old_function_tree.heading("Volume level (%)", text="Volume level (%)")
        self.old_function_tree.pack(pady=5, fill="both", expand=True, padx=10)
        
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
        adjusted_function_label_frame = tk.LabelFrame(function_adjustment_window, text="Adjustment")
        adjusted_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # New function adjustment Tree
        self.function_adjustment_tree = ttk.Treeview(adjusted_function_label_frame, columns=("If this condition TRUE", "Make this Adjustment", "Function tag","Function Type", "ROI",  "Weight", "Dose level (Gy)","Volume level (%)"), show="headings")
        self.function_adjustment_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.function_adjustment_tree.heading("Make this Adjustment", text="Make this Adjustment")
        self.function_adjustment_tree.heading("Function tag", text="Function tag")
        self.function_adjustment_tree.heading("ROI", text="ROI")
        self.function_adjustment_tree.heading("Function Type", text="Function Type")
        self.function_adjustment_tree.heading("Weight", text="Weight")
        self.function_adjustment_tree.heading("Dose level (Gy)", text="Dose level (Gy)")
        self.function_adjustment_tree.heading("Volume level (%)", text="Volume level (%)")
        self.function_adjustment_tree.pack(pady=5, fill="both", expand=True, padx=10)
        
        # Add Adjustment Button
        self.add_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Add New Function", command=self.open_add_function_adjustment_window)
        self.add_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Delete Adjustment Button
        self.delete_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Remove Adjustment", command=lambda: self.show_step_info("Remove Function Adjustment"))
        self.delete_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Save Button
        self.save_adjustment_btn = ttk.Button(function_adjustment_window, text="Save", command=lambda: self.show_step_info("Function Adjustments Saved"))
        self.save_adjustment_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(function_adjustment_window, text="Close", command=function_adjustment_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def open_add_function_adjustment_window(self):
        """Add a function adjustment to the list."""
        add_adjustment_window = tk.Toplevel(self)
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
    
    def open_end_planning_flow_window(self):
        """Open a new window for End Planning Flow step."""
        end_planning_window = tk.Toplevel(self)
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
        
if __name__ == "__main__":
    app = AutoPlanGUI()
    app.mainloop()
