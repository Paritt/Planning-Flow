import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .boolean_window import Boolean_Window

class ConditionROI_Window:
    """Open a new window for Condition ROI step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.condition_roi_window = tk.Toplevel(parent)
        self.condition_roi_window.title("Condition ROI")
        self.condition_roi_window.geometry("800x400")
        
        # Bold Title Label
        title_label = tk.Label(self.condition_roi_window, text="Condition ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Treeview for Condition ROI List with vertical scrollbar
        condition_roi_frame = ttk.Frame(self.condition_roi_window)
        condition_roi_frame.pack(pady=5, fill="both", expand=True)
        
        condition_roi_scroll_y = ttk.Scrollbar(condition_roi_frame, orient="vertical")
        
        self.condition_roi_tree = ttk.Treeview(condition_roi_frame, columns=("Order","If this condition TRUE", "Create this ROI", "By this method"), show="headings",
                                                yscrollcommand=condition_roi_scroll_y.set)
        
        condition_roi_scroll_y.config(command=self.condition_roi_tree.yview)
        
        self.condition_roi_tree.heading("Order", text="Order")
        self.condition_roi_tree.heading("If this condition TRUE", text="If this condition TRUE")
        self.condition_roi_tree.heading("Create this ROI", text="Create this ROI")
        self.condition_roi_tree.heading("By this method", text="By this method")
        
        self.condition_roi_tree.column("Order", width=60)
        self.condition_roi_tree.column("If this condition TRUE", width=180)
        self.condition_roi_tree.column("Create this ROI", width=150)
        self.condition_roi_tree.column("By this method", width=180)
        
        self.condition_roi_tree.pack(side="left", fill="both", expand=True)
        condition_roi_scroll_y.pack(side="right", fill="y")
        
        # Add Condition ROI Button
        self.add_condition_roi_btn = ttk.Button(self.condition_roi_window, text="New", command=self.open_add_condition_roi_window)
        self.add_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Delete Condition ROI Button
        self.delete_condition_roi_btn = ttk.Button(self.condition_roi_window, text="Remove", command=self.remove_condition_roi)
        self.delete_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Move Up Button
        self.move_up_condition_btn = ttk.Button(self.condition_roi_window, text="Move Up", command=lambda: self.move_condition_roi_order(-1))
        self.move_up_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Move Down Button
        self.move_down_condition_btn = ttk.Button(self.condition_roi_window, text="Move Down", command=lambda: self.move_condition_roi_order(1))
        self.move_down_condition_btn.pack(side="left", padx=5, pady=5)
        
        # Edit
        self.edit_condition_btn = ttk.Button(self.condition_roi_window, text="Edit", command=lambda: self.show_step_info("Edit Condition"))
        self.edit_condition_btn.pack(side="left", padx=5, pady=5)
        
        
        # Load existing data if available
        if self.designer.condition_rois_data:
            for item in self.designer.condition_rois_data:
                self.condition_roi_tree.insert("", "end", values=(item["order"], item["condition"], item["roi"], item["method"]))
        
        # Save Button
        self.save_condition_roi_btn = ttk.Button(self.condition_roi_window, text="Save", command=self.save_condition_rois)
        self.save_condition_roi_btn.pack(side="left", padx=5, pady=5)
        
        # Close Button
        ttk.Button(self.condition_roi_window, text="Close", command=self.condition_roi_window.destroy).pack(pady=10)
    
    def save_condition_rois(self):
        """Save the current list of condition ROIs."""
        condition_rois = []
        for child in self.condition_roi_tree.get_children():
            values = self.condition_roi_tree.item(child, "values")
            condition_rois.append({
                "order": values[0],
                "condition": values[1],
                "roi": values[2],
                "method": values[3]
            })
        
        self.designer.condition_rois_data = condition_rois
        
        if condition_rois:
            messagebox.showinfo("Save Successful", f"Condition ROIs saved successfully. ({len(condition_rois)} items)")
        else:
            messagebox.showwarning("Save Error", "No condition ROIs to save.")
    
    def open_add_condition_roi_window(self):
        """Add a condition ROI to the list."""
        add_condition_roi_window = tk.Toplevel(self.condition_roi_window)
        add_condition_roi_window.title("Add Condition ROI")
        add_condition_roi_window.geometry("300x200")
        
        condition_list = self.designer.get_condition_list()  # Get dynamic list from Check Condition
        
        ttk.Label(add_condition_roi_window, text="If this condition TRUE:").grid(row=0, column=0, padx=5, pady=5)
        self.condition_true_var = tk.StringVar()
        self.condition_true_combo = ttk.Combobox(add_condition_roi_window, textvariable=self.condition_true_var, values=condition_list, state="readonly")
        self.condition_true_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_roi_window, text="Create this ROI:").grid(row=1, column=0, padx=5, pady=5)
        self.create_roi_var = tk.StringVar()
        self.create_roi_entry = ttk.Entry(add_condition_roi_window, textvariable=self.create_roi_var)
        self.create_roi_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_condition_roi_window, text="By this method:").grid(row=2, column=0, padx=5, pady=5)
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(add_condition_roi_window, textvariable=self.method_var,
                                        values=['Boolean operation', 'Convert Dose to ROI'], state="readonly")
        self.method_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Boolean frame
        frame_boolean = ttk.Frame(add_condition_roi_window)
        ttk.Button(frame_boolean, text="Boolean operation", command=lambda: Boolean_Window(add_condition_roi_window, self.designer, use_extended_list=True)).grid(row=0, column=0, padx=5, pady=5)
        
        # Convert Dose to ROI frame
        frame_dose_to_roi = ttk.Frame(add_condition_roi_window)
        ttk.Label(frame_dose_to_roi, text="Convert Dose (Gy) to ROI").grid(row=0, column=0, padx=5, pady=5)
        self.dose_to_roi_var = tk.StringVar()
        self.dose_to_roi_entry = ttk.Entry(frame_dose_to_roi, textvariable=self.dose_to_roi_var)
        self.dose_to_roi_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def show_selected_method(self):
            """Show the relevant input based on method selection."""
            frame_boolean.grid_forget()
            frame_dose_to_roi.grid_forget()
            selection = self.method_var.get()
            if selection == 'Boolean operation':
                frame_boolean.grid(row=3, column=1, padx=5, pady=5)
            elif selection == 'Convert Dose to ROI':
                frame_dose_to_roi.grid(row=3, column=0, columnspan=2,padx=5, pady=5)
                
        self.method_combo.bind("<<ComboboxSelected>>", lambda event: show_selected_method(self))
        show_selected_method(self)  # Show the initial frame based on the default selection
        
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
        
    def remove_condition_roi(self):
        """Remove the selected condition ROI from the list."""
        selected_item = self.condition_roi_tree.selection()
        for item in selected_item:
            self.condition_roi_tree.delete(item)
    
    def move_condition_roi_order(self, direction):
        """Move the selected ROI item up or down and update order numbers."""
        selected_item = self.condition_roi_tree.selection()
        if selected_item:
            index = self.condition_roi_tree.index(selected_item)
            new_index = index + direction
            items = self.condition_roi_tree.get_children()
            if 0 <= new_index < len(items):
                self.condition_roi_tree.move(selected_item, "", new_index)
                self.update_condition_roi_order()
                
    def update_condition_roi_order(self):
        """Update order numbers in the ROI tree."""
        items = self.condition_roi_tree.get_children()
        for i, item in enumerate(items, start=1):
            values = self.condition_roi_tree.item(item, "values")
            self.condition_roi_tree.item(item, values=(i, values[1]))
            
    def show_step_info(self, message):
        """Display a message box with step information."""
        messagebox.showinfo("Step Information", message)
