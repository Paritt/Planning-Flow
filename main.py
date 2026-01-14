import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class AutoPlanGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Brew Plan")
        self.geometry("570x200")

        # Treatment Parameters Section
        self.create_treatment_settings()

        # Workflow Section
        self.create_workflow_controls()

        # Loaded Workflow Data
        self.workflow_data = {}
        self.planning_window = None

    def create_treatment_settings(self):
        """Create treatment room, energy, and optimization flow selection."""
        frame = ttk.LabelFrame(self, text="Treatment Settings")
        frame.pack(fill="x", padx=10, pady=5)

        # Treatment Room Dropdown
        ttk.Label(frame, text="Treatment Room:").grid(row=0, column=0, padx=5, pady=2)
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(frame, textvariable=self.room_var,
                                          values=['N3_VersaHD', 'N4_VersaHD', 'TrueBeam_L6', 'TrueBeam_L7', 'TrueBeam_N5'], state="readonly")
        self.room_dropdown.grid(row=0, column=1, padx=5, pady=2)

        # Energy Dropdown
        ttk.Label(frame, text="Energy:").grid(row=1, column=0, padx=5, pady=2)
        self.energy_var = tk.StringVar()
        self.energy_dropdown = ttk.Combobox(frame, textvariable=self.energy_var,
                                            values=['6', '10', '6 FFF', '10 FFF'], state="readonly")
        self.energy_dropdown.grid(row=1, column=1, padx=5, pady=2)

        # Optimization Flow (Read-only)
        ttk.Label(frame, text="Optimization Flow:").grid(row=2, column=0, padx=5, pady=2)
        self.flow_entry = ttk.Entry(frame, state="readonly")
        self.flow_entry.grid(row=2, column=1, padx=5, pady=2)

        # Load Flow Button
        self.load_flow_button = ttk.Button(frame, text="Load Flow", command=self.load_flow)
        self.load_flow_button.grid(row=2, column=2, padx=5, pady=2)

    def create_workflow_controls(self):
        """Create workflow management buttons."""
        frame = ttk.LabelFrame(self, text="Workflow Management")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame, text="New Flow", command=self.new_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Edit Flow", command=self.edit_flow).pack(side="left", padx=5, pady=2)
        ttk.Button(frame, text="Start", command=self.start_planning).pack(side="right", padx=5, pady=2)

    def open_planning_steps_window(self):
        """Create a section for defining workflow steps with labels for flow/user and Save Flow button."""
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
        
        self.automate_virtual_btn = ttk.Button(frame, text="Automate Virtual", command=self.open_automate_virtual_window)
        self.automate_virtual_btn.place(x=200, y=40)
        
        self.initial_priority_btn = ttk.Button(frame, text="Initial Priority", command=lambda: self.show_step_info("Initial Priority"))
        self.initial_priority_btn.place(x=380, y=40)
        
        self.optimization_btn = ttk.Button(frame, text="Optimization", command=lambda: self.show_step_info("Optimization"))
        self.optimization_btn.place(x=380, y=100)
        
        self.final_calc_btn = ttk.Button(frame, text="Final Calculation", command=lambda: self.show_step_info("Final Calculation"))
        self.final_calc_btn.place(x=200, y=100)
        
        self.check_condition_btn = ttk.Button(frame, text="Check Condition", command=lambda: self.show_step_info("Check Condition"))
        self.check_condition_btn.place(x=20, y=100)
        
        self.automate_new_virtual_btn = ttk.Button(frame, text="Automate New Virtual", command=lambda: self.show_step_info("Automate New Virtual"))
        self.automate_new_virtual_btn.place(x=110, y=160)
        
        self.optimization_adjustment_btn = ttk.Button(frame, text="Optimization Adjustment", command=lambda: self.show_step_info("Optimization Adjustment"))
        self.optimization_adjustment_btn.place(x=330, y=160)
        
        self.end_loop_btn = ttk.Button(frame, text="End Planning Loop", command=lambda: self.show_step_info("End Planning Loop"))
        self.end_loop_btn.place(x=20, y=220)

        # Save Flow Button
        self.save_flow_btn = ttk.Button(frame, text="Save Flow", command=self.save_flow)
        self.save_flow_btn.place(x=400, y=220)

        # Arrows between steps
        self.add_arrow(frame, "→", 170, 45)
        self.add_arrow(frame, "→", 350, 45)
        self.add_arrow(frame, "↓", 430, 75)
        self.add_arrow(frame, "←", 350, 100)
        self.add_arrow(frame, "←", 170, 100)
        self.add_arrow(frame, "↓", 120, 130)
        self.add_arrow(frame, "→", 300, 160)
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
        match_roi_window.geometry("500x300")

        # Bold Title Label
        title_label = tk.Label(match_roi_window, text="Match ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Listbox to Display Added ROIs
        self.roi_listbox = tk.Listbox(match_roi_window, height=8)
        self.roi_listbox.pack(pady=5, fill="both", expand=True)

        # ROI Name Label and Entry
        ttk.Label(match_roi_window, text="ROI Name:").pack(pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_entry = ttk.Entry(match_roi_window, textvariable=self.roi_name_var)
        self.roi_name_entry.pack(pady=5)

        # Add and Remove ROI Buttons
        self.add_roi_btn = ttk.Button(match_roi_window, text="Add ROI", command=self.add_roi)
        self.add_roi_btn.pack(side="left", padx=5)
        self.remove_roi_btn = ttk.Button(match_roi_window, text="Remove Selected ROI", command=self.remove_roi)
        self.remove_roi_btn.pack(side="left", padx=5)
        self.save_roi_list = ttk.Button(match_roi_window, text="Save ROI list", command=lambda: self.show_step_info("Final Calculation"))
        self.save_roi_list.pack(side="left", padx=5)

        # Close Button
        self.close_btn = ttk.Button(match_roi_window, text="Close", command=match_roi_window.destroy)
        self.close_btn.pack(side="left", padx=5)

    def add_roi(self):
        """Add ROI to the listbox."""
        roi_name = self.roi_name_var.get().strip()
        if roi_name:
            self.roi_listbox.insert(tk.END, roi_name)
            self.roi_name_var.set("")  # Clear the entry field
        else:
            messagebox.showwarning("Input Error", "ROI Name cannot be empty.")

    def remove_roi(self):
        """Remove selected ROI from the listbox."""
        selected_indices = self.roi_listbox.curselection()
        for index in reversed(selected_indices):
            self.roi_listbox.delete(index)
            
    def open_automate_virtual_window(self):
        """Open a new window for Automate Virtual step."""
        virtual_window = tk.Toplevel(self)
        virtual_window.title("Automate Virtual")
        virtual_window.geometry("800x400")

        # Bold Title Label
        title_label = tk.Label(virtual_window, text="Automate Virtual", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for Virtual List (Supports Ordering and Functions)
        self.virtual_tree = ttk.Treeview(virtual_window, columns=("Order", "Virtual Name"), show="headings")
        self.virtual_tree.heading("Order", text="Order")
        self.virtual_tree.heading("Virtual Name", text="Virtual Name")
        self.virtual_tree.pack(pady=5, fill="both", expand=True)

        # Button Frame for New, Remove, Edit Function, and Save
        button_frame = ttk.Frame(virtual_window)
        button_frame.pack(pady=5)

        self.new_virtual_btn = ttk.Button(button_frame, text="New", command=self.open_new_virtual_popup)
        self.new_virtual_btn.pack(side="left", padx=5)

        self.remove_virtual_btn = ttk.Button(button_frame, text="Remove", command=self.remove_virtual)
        self.remove_virtual_btn.pack(side="left", padx=5)
        
        self.move_up_btn = ttk.Button(button_frame, text="Move Up", command=lambda: self.move_virtual_order(-1))
        self.move_up_btn.pack(side="left", padx=5)

        self.move_down_btn = ttk.Button(button_frame, text="Move Down", command=lambda: self.move_virtual_order(1))
        self.move_down_btn.pack(side="left", padx=5)

        self.edit_function_btn = ttk.Button(button_frame, text="Edit Function", command=self.edit_virtual_function)
        self.edit_function_btn.pack(side="left", padx=5)

        self.save_virtual_btn = ttk.Button(button_frame, text="Save", command=self.save_virtual_list)
        self.save_virtual_btn.pack(side="left", padx=5)

        # Close Button
        self.close_btn = ttk.Button(virtual_window, text="Close", command=virtual_window.destroy)
        self.close_btn.pack(pady=10)

    def open_new_virtual_popup(self):
        """Open a popup window to add a new virtual item."""
        new_virtual_popup = tk.Toplevel(self)
        new_virtual_popup.title("Add Virtual")
        new_virtual_popup.geometry("300x200")

        ttk.Label(new_virtual_popup, text="Virtual Name:").pack(pady=5)
        self.virtual_name_var = tk.StringVar()
        self.virtual_name_entry = ttk.Entry(new_virtual_popup, textvariable=self.virtual_name_var)
        self.virtual_name_entry.pack(pady=5)

        ttk.Button(new_virtual_popup, text="Add Function", command=self.open_boolean_window).pack(pady=5)

        ttk.Button(new_virtual_popup, text="Add", command=lambda: self.add_virtual(new_virtual_popup)).pack(pady=5)

    def add_virtual(self, popup):
        """Add a new virtual item with function to the list."""
        virtual_name = self.virtual_name_var.get().strip()
        if virtual_name:
            order = len(self.virtual_tree.get_children()) + 1
            self.virtual_tree.insert("", "end", values=(order, virtual_name))
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "Both Virtual Name and Function are required.")

    def remove_virtual(self):
        """Remove selected virtual item from the treeview."""
        selected_item = self.virtual_tree.selection()
        for item in selected_item:
            self.virtual_tree.delete(item)

    def edit_virtual_function(self):
        """Edit the function of the selected virtual item."""
        selected_item = self.virtual_tree.selection()
        if selected_item:
            item_values = self.virtual_tree.item(selected_item, "values")
            self.open_boolean_window()
        else:
            messagebox.showwarning("Selection Error", "Please select a virtual item to edit.")
            
    def move_virtual_order(self, direction):
        """Move the selected virtual item up or down and update order numbers."""
        selected_item = self.virtual_tree.selection()
        if selected_item:
            index = self.virtual_tree.index(selected_item)
            new_index = index + direction
            items = self.virtual_tree.get_children()
            if 0 <= new_index < len(items):
                self.virtual_tree.move(selected_item, "", new_index)
                self.update_virtual_order()
                
    def update_virtual_order(self):
        """Update order numbers in the virtual tree."""
        items = self.virtual_tree.get_children()
        for i, item in enumerate(items, start=1):
            values = self.virtual_tree.item(item, "values")
            self.virtual_tree.item(item, values=(i, values[1]))

    def save_virtual_list(self):
        """Save the current list of virtual items."""
        virtual_items = [self.virtual_tree.item(child, "values") for child in self.virtual_tree.get_children()]
        if virtual_items:
            messagebox.showinfo("Save Successful", "Virtual list saved successfully.")
        else:
            messagebox.showwarning("Save Error", "No virtual items to save.")
            
    def open_boolean_window(self):
        """Open a new window for Boolean function editing."""
        self.boolean_window = tk.Toplevel(self)
        self.boolean_window.title("ROI Algebra")
        self.boolean_window.geometry("1200x400")
        
        theFrame = tk.Frame(self.boolean_window)
        theFrame.pack(pady=5)
        
        # Frame for A and B
        frame_a_b = tk.LabelFrame(theFrame, text="AB", padx=10, pady=10)
        frame_a_b.grid(row=0, column=0, padx=5)

        # ROI A
        frame_a = tk.LabelFrame(frame_a_b, text="A", padx=10, pady=10)
        frame_a.grid(row=0, column=0, padx=5)
        margin_label_a = tk.Label(frame_a, text="Margin")
        margin_label_a.grid(row=0, column=0)
        selected_value_a = tk.IntVar()
        selected_value_a.set(1)
        expand_a = tk.Radiobutton(frame_a, text="Expand", variable=selected_value_a, value=1)
        expand_a.grid(row=1, column=0)
        contract_a = tk.Radiobutton(frame_a, text="Contract", variable=selected_value_a, value=2)
        contract_a.grid(row=1, column=1)
        
        # Directional input for ROI A
        directions = ['Superior', 'Inferior', 'Right', 'Left', 'Anterior', 'Posterior']
        for i, direction in enumerate(directions):
            label = tk.Label(frame_a, text=f"{direction} (cm)")
            label.grid(row=i+2, column=0)
            default_value = tk.StringVar()
            default_value.set("0.00")
            entry = tk.Entry(frame_a, textvariable=default_value)
            entry.grid(row=i+2, column=1)
        
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
        frame_b = tk.LabelFrame(frame_a_b, text="B", padx=10, pady=10)
        frame_b.grid(row=0, column=3, padx=5)
        margin_label_b = tk.Label(frame_b, text="Margin")
        margin_label_b.grid(row=0, column=0)
        selected_value_b = tk.IntVar()
        selected_value_b.set(1)
        expand_b = tk.Radiobutton(frame_b, text="Expand", variable=selected_value_b, value=1)
        expand_b.grid(row=1, column=0)
        contract_b = tk.Radiobutton(frame_b, text="Contract", variable=selected_value_b, value=2)
        contract_b.grid(row=1, column=1)

        # Directional input for ROI B
        for i, direction in enumerate(directions):
            label = tk.Label(frame_b, text=f"{direction} (cm)")
            label.grid(row=i+2, column=0)
            default_value = tk.StringVar()
            default_value.set("0.00")
            entry = tk.Entry(frame_b, textvariable=default_value)
            entry.grid(row=i+2, column=1)
            
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
        save_button.pack(pady=20)


if __name__ == "__main__":
    app = AutoPlanGUI()
    app.mainloop()
