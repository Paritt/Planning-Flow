import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .function_frame import FunctionConfigFrame

class FunctionAdjustment_Window:
    """Open a new window for Function Adjustment step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.function_adjustment_window = tk.Toplevel(parent)
        self.function_adjustment_window.title("Function Adjustment")
        self.function_adjustment_window.geometry("1500x800")
        
        # Bold Title Label
        title_label = tk.Label(self.function_adjustment_window, text="Function Adjustment", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Old function frame
        old_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Initial Functions")
        old_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # Old function Tree with vertical scrollbar
        old_function_frame = ttk.Frame(old_function_label_frame)
        old_function_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        old_function_scroll_y = ttk.Scrollbar(old_function_frame, orient="vertical")
        
        self.old_function_tree = ttk.Treeview(old_function_frame, columns=("Function tag","Function Type", "ROI",  "Description", "Weight", "Objective/Constraint", "Robust", "Restrict to Beam", "Beam"), show="headings",
                                                yscrollcommand=old_function_scroll_y.set)
        
        old_function_scroll_y.config(command=self.old_function_tree.yview)
        
        self.old_function_tree.heading("Function tag", text="Function tag")
        self.old_function_tree.heading("Function Type", text="Function Type")
        self.old_function_tree.heading("ROI", text="ROI")
        self.old_function_tree.heading("Description", text="Description")
        self.old_function_tree.heading("Weight", text="Weight")
        self.old_function_tree.heading("Objective/Constraint", text="Constraint")
        self.old_function_tree.heading("Robust", text="Robust")
        self.old_function_tree.heading("Restrict to Beam", text="Restrict to Beam")
        self.old_function_tree.heading("Beam", text="Beam")
        
        self.old_function_tree.column("Function tag", width=20)
        self.old_function_tree.column("Function Type", width=20)
        self.old_function_tree.column("ROI", width=50)
        self.old_function_tree.column("Description", width=200)
        self.old_function_tree.column("Weight", width=20)
        self.old_function_tree.column("Objective/Constraint", width=20)
        self.old_function_tree.column("Robust", width=20)
        self.old_function_tree.column("Restrict to Beam", width=30)
        self.old_function_tree.column("Beam", width=80)
        
        self.old_function_tree.pack(side="left", fill="both", expand=True)
        old_function_scroll_y.pack(side="right", fill="y")
        
        def add_old_functions(self):
            """Add old functions to the list."""
            # Load initial functions from designer
            if self.designer.initial_functions_data:
                for item in self.designer.initial_functions_data:
                    self.old_function_tree.insert(
                        "",
                        "end",
                        values=(
                            item["tag"],
                            item["type"],
                            item["roi"],
                            item["description"],
                            "" if item.get("objective_constraint") == "Constraint" else item["weight"],
                            "" if item.get("objective_constraint", "Objective") == "Objective" else "⭐",
                            "" if item.get("is_robust", False) is False else "⚙️",
                            "" if item.get("restrict_to_beam", False) is False else "✔️",
                            item.get("selected_beam", "")
                        )
                    )
                
        add_old_functions(self)
        
        # Adjust Button
        self.adjust_function_btn = ttk.Button(old_function_label_frame, text="Adjust Selected Function", command=self.adjust_function)
        self.adjust_function_btn.pack(side="left", padx=5, pady=5)
        
        # Adjusted function frame
        adjusted_function_label_frame = tk.LabelFrame(self.function_adjustment_window, text="Adjustment")
        adjusted_function_label_frame.pack(fill="both", expand=True, pady=10, padx=10)
        
        # New function adjustment Tree with vertical scrollbar
        function_adjustment_frame = ttk.Frame(adjusted_function_label_frame)
        function_adjustment_frame.pack(pady=5, fill="both", expand=True, padx=10)
        
        function_adjustment_scroll_y = ttk.Scrollbar(function_adjustment_frame, orient="vertical")
        
        self.function_adjustment_tree = ttk.Treeview(function_adjustment_frame, columns=("If this condition TRUE", "Make this Adjustment", "Function tag", "Function Type", "ROI", "Description", "Weight", "Objective/Constraint", "Robust", "Restrict to Beam", "Beam"), show="headings",
                                                    yscrollcommand=function_adjustment_scroll_y.set)
        
        function_adjustment_scroll_y.config(command=self.function_adjustment_tree.yview)
        
        self.function_adjustment_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.function_adjustment_tree.heading("Make this Adjustment", text="Make this Adjustment")
        self.function_adjustment_tree.heading("Function tag", text="Function tag")
        self.function_adjustment_tree.heading("Function Type", text="Function Type")
        self.function_adjustment_tree.heading("ROI", text="ROI")
        self.function_adjustment_tree.heading("Description", text="Description")
        self.function_adjustment_tree.heading("Weight", text="Weight")
        self.function_adjustment_tree.heading("Objective/Constraint", text="Constraint")
        self.function_adjustment_tree.heading("Robust", text="Robust")
        self.function_adjustment_tree.heading("Restrict to Beam", text="Restrict to Beam")
        self.function_adjustment_tree.heading("Beam", text="Beam")
        
        self.function_adjustment_tree.column("If this condition TRUE", width=80)
        self.function_adjustment_tree.column("Make this Adjustment", width=80)
        self.function_adjustment_tree.column("Function tag", width=20)
        self.function_adjustment_tree.column("Function Type", width=20)
        self.function_adjustment_tree.column("ROI", width=40)
        self.function_adjustment_tree.column("Description", width=200)
        self.function_adjustment_tree.column("Weight", width=50)
        self.function_adjustment_tree.column("Objective/Constraint", width=20)
        self.function_adjustment_tree.column("Robust", width=20)
        self.function_adjustment_tree.column("Restrict to Beam", width=30)
        self.function_adjustment_tree.column("Beam", width=80)
        
        self.function_adjustment_tree.pack(side="left", fill="both", expand=True)
        function_adjustment_scroll_y.pack(side="right", fill="y")
        
        # Add Adjustment Button
        self.add_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Add New Function", command=self.open_add_function_adjustment_window)
        self.add_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Edit Adjustment Button
        self.edit_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Edit Selected Adjustment", command=self.open_edit_function_adjustment_window)
        self.edit_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Delete Adjustment Button
        self.delete_adjustment_btn = ttk.Button(adjusted_function_label_frame, text="Remove Adjustment", command=lambda: self.show_step_info("Remove Function Adjustment"))
        self.delete_adjustment_btn.pack(side="left", padx=5, pady=5)
        # Load existing data if available
        if self.designer.function_adjustments_data:
            for item in self.designer.function_adjustments_data:
                self.function_adjustment_tree.insert(
                    "",
                    "end",
                    values=(
                        item["condition"],
                        item["adjustment"],
                        item["tag"],
                        item["type"],
                        item["roi"],
                        item["description"],
                        "" if item.get("objective_constraint") == "Constraint" else item["weight"],
                        "" if item.get("objective_constraint", "Objective") == "Objective" else "⭐",
                        "" if item.get("is_robust", False) is False else "⚙️",
                        "" if item.get("restrict_to_beam", False) is False else "✔️",
                        item.get("selected_beam", "")
                    )
                )
        
        # Save Button
        self.save_adjustment_btn = ttk.Button(self.function_adjustment_window, text="Save", command=self.save_function_adjustments)
        self.save_adjustment_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.function_adjustment_window, text="Close", command=self.function_adjustment_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def save_function_adjustments(self):
        """Save the current list of function adjustments."""
        adjustments = []
        for child in self.function_adjustment_tree.get_children():
            values = self.function_adjustment_tree.item(child)["values"]
            adjustments.append({
                "condition": values[0],
                "adjustment": values[1],
                "tag": values[2],
                "type": values[3],
                "roi": values[4],
                "description": values[5],
                "weight": values[6],
                "objective_constraint": "Constraint" if values[7] == "⭐" else "Objective",
                "is_robust": values[8] == "⚙️",
                "restrict_to_beam": values[9] == "✔️",
                "selected_beam": values[10]
            })
        
        self.designer.function_adjustments_data = adjustments
        
        if adjustments:
            messagebox.showinfo("Save Successful", f"Function adjustments saved successfully. ({len(adjustments)} items)")
        else:
            messagebox.showwarning("Save Error", "No function adjustments to save.")
        
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
    
    def adjust_function(self):
        """Adjust the selected function."""
        # Get selected function from old_function_tree
        selected_item = self.old_function_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function to adjust.")
            return
        
        # Get values from selected item
        item_values = self.old_function_tree.item(selected_item[0])["values"]
        selected_data = {
            "tag": item_values[0],
            "type": item_values[1],
            "roi": item_values[2],
            "description": item_values[3],
            "weight": item_values[4],
            "objective_constraint": "Constraint" if item_values[5] == "⭐" else "Objective",
            "is_robust": item_values[6] == "⚙️",
            "restrict_to_beam": item_values[7] == "✔️",
            "selected_beam": item_values[8]
        }
        
        # Open adjustment window
        adjust_window = tk.Toplevel(self.function_adjustment_window)
        adjust_window.title("Adjust Function")
        adjust_window.geometry("650x350")
        
        # Condition selector frame
        condition_frame = ttk.Frame(adjust_window)
        condition_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(condition_frame, text="If this condition TRUE:").pack(side="left", padx=5)
        self.condition_true_var = tk.StringVar()
        condition_combo = ttk.Combobox(
            condition_frame, textvariable=self.condition_true_var,
            values=self.designer.get_condition_list(), state="readonly"
        )
        condition_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # Create function config frame in edit mode with disabled fields
        config_frame = FunctionConfigFrame(
            adjust_window, self.designer, mode="edit",
            selected_data=selected_data,
            disable_fields=["tag"]
        )
        config_frame.pack(padx=10, pady=10)
        
        def save_adjustment():
            """Save the adjusted function."""
            condition_true = self.condition_true_var.get().strip()
            if not condition_true:
                messagebox.showwarning("No Condition", "Please select a condition.")
                return
            
            values = config_frame.get_values()
            # Insert into function adjustment tree with condition and adjustment type
            self.function_adjustment_tree.insert(
                "",
                "end",
                values=(
                    condition_true, "Adjust OLD Function", values["tag"], values["type"],
                    values["roi"], values["description"],
                    "" if values.get("objective_constraint") == "Constraint" else values["weight"],
                    "" if values.get("objective_constraint", "Objective") == "Objective" else "⭐",
                    "" if values.get("is_robust", False) is False else "⚙️",
                    "" if values.get("restrict_to_beam", False) is False else "✔️",
                    values.get("selected_beam", "")
                )
            )
            adjust_window.destroy()
        
        ttk.Button(adjust_window, text="Adjust", command=save_adjustment).pack(pady=10)
    
    def open_add_function_adjustment_window(self):
        """Add a function adjustment to the list."""
        add_adjustment_window = tk.Toplevel(self.function_adjustment_window)
        add_adjustment_window.title("Add Function Adjustment")
        add_adjustment_window.geometry("650x350")
        
        # Condition selector frame
        condition_frame = ttk.Frame(add_adjustment_window)
        condition_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(condition_frame, text="If this condition TRUE:").pack(side="left", padx=5)
        self.condition_true_var = tk.StringVar()
        condition_combo = ttk.Combobox(
            condition_frame, textvariable=self.condition_true_var,
            values=self.designer.get_condition_list(), state="readonly"
        )
        condition_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # Create function config frame in add mode
        config_frame = FunctionConfigFrame(add_adjustment_window, self.designer, mode="add")
        config_frame.pack(padx=10, pady=10)
        
        def save_new_adjustment():
            """Save the new function adjustment."""
            condition_true = self.condition_true_var.get().strip()
            if not condition_true:
                messagebox.showwarning("No Condition", "Please select a condition.")
                return
            
            values = config_frame.get_values()
            # Validate required fields
            if not values["tag"] or not values["type"] or not values["roi"] or not values["weight"]:
                messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
                return
            
            # Insert into function adjustment tree with condition and adjustment type
            self.function_adjustment_tree.insert(
                "",
                "end",
                values=(
                    condition_true, "Add NEW function", values["tag"], values["type"],
                    values["roi"], values["description"],
                    "" if values.get("objective_constraint") == "Constraint" else values["weight"],
                    "" if values.get("objective_constraint", "Objective") == "Objective" else "⭐",
                    "" if values.get("is_robust", False) is False else "⚙️",
                    "" if values.get("restrict_to_beam", False) is False else "✔️",
                    values.get("selected_beam", "")
                )
            )
            add_adjustment_window.destroy()
        
        ttk.Button(add_adjustment_window, text="Add", command=save_new_adjustment).pack(pady=10)
    
    def open_edit_function_adjustment_window(self):
        """Edit the selected function adjustment."""
        selected_item = self.function_adjustment_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function adjustment to edit.")
            return
        
        # Get values from selected item
        item_values = self.function_adjustment_tree.item(selected_item[0])["values"]
        selected_condition = item_values[0]
        selected_adjustment = item_values[1]
        selected_data = {
            "tag": item_values[2],
            "type": item_values[3],
            "roi": item_values[4],
            "description": item_values[5],
            "weight": item_values[6],
            "objective_constraint": "Constraint" if item_values[7] == "⭐" else "Objective",
            "is_robust": item_values[8] == "⚙️",
            "restrict_to_beam": item_values[9] == "✔️",
            "selected_beam": item_values[10]
        }
        
        edit_adjustment_window = tk.Toplevel(self.function_adjustment_window)
        edit_adjustment_window.title("Edit Function Adjustment")
        edit_adjustment_window.geometry("650x350")
        
        # Condition selector frame
        condition_frame = ttk.Frame(edit_adjustment_window)
        condition_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(condition_frame, text="If this condition TRUE:").pack(side="left", padx=5)
        condition_true_var = tk.StringVar(value=selected_condition)
        condition_combo = ttk.Combobox(
            condition_frame, textvariable=condition_true_var,
            values=self.designer.get_condition_list(), state="readonly"
        )
        condition_combo.pack(side="left", padx=5, fill="x", expand=True)
        
        # Create function config frame in edit mode with conditional disabled fields
        disable_fields = ["type", "roi"] if selected_adjustment == "Adjust OLD Function" else None
        config_frame = FunctionConfigFrame(
            edit_adjustment_window, self.designer, mode="edit",
            selected_data=selected_data,
            disable_fields=disable_fields
        )
        config_frame.pack(padx=10, pady=10)
        
        def save_edited_adjustment():
            """Save the edited function adjustment."""
            condition_true = condition_true_var.get().strip()
            if not condition_true:
                messagebox.showwarning("No Condition", "Please select a condition.")
                return
            
            values = config_frame.get_values()
            # Update tree item with condition and original adjustment type
            self.function_adjustment_tree.item(
                selected_item[0],
                values=(
                    condition_true, selected_adjustment, values["tag"], values["type"],
                    values["roi"], values["description"],
                    "" if values.get("objective_constraint") == "Constraint" else values["weight"],
                    "" if values.get("objective_constraint", "Objective") == "Objective" else "⭐",
                    "" if values.get("is_robust", False) is False else "⚙️",
                    "" if values.get("restrict_to_beam", False) is False else "✔️",
                    values.get("selected_beam", "")
                )
            )
            edit_adjustment_window.destroy()
        
        ttk.Button(edit_adjustment_window, text="Save Changes", command=save_edited_adjustment).pack(pady=10)
