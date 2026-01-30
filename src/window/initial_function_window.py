import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .function_frame import FunctionConfigFrame

class InitialFunction_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Initial Function step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.initial_function_window = tk.Toplevel(parent)
        self.initial_function_window.title("Initial Optimization function")
        self.initial_function_window.geometry("1000x400")

        # Bold Title Label
        title_label = tk.Label(self.initial_function_window, text="Initial Optimization function", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Content can be added here - with vertical scrollbar
        initial_function_frame = ttk.Frame(self.initial_function_window)
        initial_function_frame.pack(pady=5, fill="both", expand=True)
        
        initial_function_scroll_y = ttk.Scrollbar(initial_function_frame, orient="vertical")
        
        self.initial_function_tree = ttk.Treeview(
            initial_function_frame,
            columns=(
                "Function tag",
                "Function Type",
                "ROI",
                "Description",
                "Weight",
                "Objective/Constraint",
                "Robust",
                "Restrict to Beam",
                "Beam"
            ),
            show="headings",
            yscrollcommand=initial_function_scroll_y.set
        )
        
        initial_function_scroll_y.config(command=self.initial_function_tree.yview)
        
        self.initial_function_tree.heading("Function tag", text="Function tag")
        self.initial_function_tree.heading("Function Type", text="Function Type")
        self.initial_function_tree.heading("ROI", text="ROI")
        self.initial_function_tree.heading("Description", text="Description")
        self.initial_function_tree.heading("Weight", text="Weight")
        self.initial_function_tree.heading("Objective/Constraint", text="Constraint")
        self.initial_function_tree.heading("Robust", text="Robust")
        self.initial_function_tree.heading("Restrict to Beam", text="Restrict to Beam")
        self.initial_function_tree.heading("Beam", text="Beam")
        
        self.initial_function_tree.column("Function tag", width=20)
        self.initial_function_tree.column("Function Type", width=20)
        self.initial_function_tree.column("ROI", width=50)
        self.initial_function_tree.column("Description", width=200)
        self.initial_function_tree.column("Weight", width=10)
        self.initial_function_tree.column("Objective/Constraint", width=10)
        self.initial_function_tree.column("Robust", width=10)
        self.initial_function_tree.column("Restrict to Beam", width=30)
        self.initial_function_tree.column("Beam", width=50)
        
        self.initial_function_tree.pack(side="left", fill="both", expand=True)
        initial_function_scroll_y.pack(side="right", fill="y")
        
        # Add Objective Button
        self.add_objective_btn = ttk.Button(self.initial_function_window, text="Add function", command=self.open_add_function_window)
        self.add_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Edit Objective Button
        self.edit_objective_btn = ttk.Button(self.initial_function_window, text="Edit Selected function", command=self.open_edit_function_window)
        self.edit_objective_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Objective Button
        self.delete_objective_btn = ttk.Button(self.initial_function_window, text="Delete Selected function", command=self.delete_function)
        self.delete_objective_btn.pack(side="left", padx=5, pady=5)

        # Load existing data if available
        if self.designer.initial_functions_data:
            for item in self.designer.initial_functions_data:
                self.initial_function_tree.insert(
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
        
        # Save Button
        self.save_initial_function_btn = ttk.Button(self.initial_function_window, text="Save", command=self.save_initial_functions)
        self.save_initial_function_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        self.close_btn = ttk.Button(self.initial_function_window, text="Close", command=self.initial_function_window.destroy)
        self.close_btn.pack(side="left", padx=5, pady=5)
    
    def save_initial_functions(self):
        """Save the current list of initial functions."""
        functions = []
        for child in self.initial_function_tree.get_children():
            values = self.initial_function_tree.item(child)["values"]
            functions.append({
                "tag": values[0],
                "type": values[1],
                "roi": values[2],
                "description": values[3],
                "weight": values[4],
                "objective_constraint": "Constraint" if values[5] == "⭐" else "Objective",
                "is_robust": values[6] == "⚙️",
                "restrict_to_beam": values[7] == "✔️",
                "selected_beam": values[8]
            })
        
        self.designer.initial_functions_data = functions
        
        if functions:
            messagebox.showinfo("Save Successful", f"Initial functions saved successfully. ({len(functions)} items)")
        else:
            messagebox.showwarning("Save Error", "No functions to save.")
    
    def open_add_function_window(self):
        """Add an optimization function to the list."""
        add_function_window = tk.Toplevel(self.initial_function_window)
        add_function_window.title("Add Opt. Function")
        add_function_window.geometry("650x350")
        
        # Create function config frame
        config_frame = FunctionConfigFrame(add_function_window, self.designer, mode="add")
        config_frame.pack(padx=10, pady=10)
        
        # Add button
        ttk.Button(add_function_window, text="Add", command=lambda: self.add_function(add_function_window, config_frame)).pack(pady=10)
        
    def add_function(self, popup, config_frame):
        """Save the new function to the list."""
        values = config_frame.get_values()
        
        # Validate required fields
        if not values["tag"] or not values["type"] or not values["roi"] or not values["weight"]:
            messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
            return
        
        # Insert into tree
        self.initial_function_tree.insert(
            "",
            "end",
            values=(
                values["tag"],
                values["type"],
                values["roi"],
                values["description"],
                "" if values.get("objective_constraint", "Objective") == "Constraint" else values["weight"],
                "" if values.get("objective_constraint", "Objective") == "Objective" else "⭐",
                "" if values.get("is_robust", False) is False else "⚙️",
                "" if values.get("restrict_to_beam", False) is False else "✔️",
                values.get("selected_beam", "")
            )
        )
        popup.destroy()
    
    def delete_function(self):
        """Delete the selected function from the list."""
        selected_item = self.initial_function_tree.selection()
        for item in selected_item:
            self.initial_function_tree.delete(item)
    
    def open_edit_function_window(self):
        """Edit the selected optimization function."""
        selected_item = self.initial_function_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a function to edit.")
            return
        
        # Get values from selected item
        item_values = self.initial_function_tree.item(selected_item[0])["values"]
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
        
        edit_function_window = tk.Toplevel(self.initial_function_window)
        edit_function_window.title("Edit Opt. Function")
        edit_function_window.geometry("650x350")
        
        # Create function config frame in edit mode
        config_frame = FunctionConfigFrame(
            edit_function_window, self.designer, mode="edit",
            selected_data=selected_data,
            disable_fields=[]
        )
        config_frame.pack(padx=10, pady=10)
        
        def save_edited_function():
            """Save the edited function."""
            values = config_frame.get_values()
            # Update tree item
            self.initial_function_tree.item(
                selected_item[0],
                values=(
                    values["tag"],
                    values["type"],
                    values["roi"],
                    values["description"],
                    "" if values.get("objective_constraint", "Objective") == "Constraint" else values["weight"],
                    "" if values.get("objective_constraint", "Objective") == "Objective" else "⭐",
                    "" if values.get("is_robust", False) is False else "⚙️",
                    "" if values.get("restrict_to_beam", False) is False else "✔️",
                    values.get("selected_beam", "")
                )
            )
            edit_function_window.destroy()
        
        ttk.Button(edit_function_window, text="Save Changes", command=save_edited_function).pack(pady=10)
    
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)