import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .boolean_window import Boolean_Window


class AutomateROI_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Automate ROI step."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.roi_window = tk.Toplevel(parent)
        self.roi_window.title("Automate ROI")
        self.roi_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(self.roi_window, text="Automate ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for ROI List (Supports Ordering and Functions) with vertical scrollbar
        roi_tree_frame = ttk.Frame(self.roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("Order", "ROI Name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("Order", text="Order")
        self.roi_tree.heading("ROI Name", text="ROI Name")
        
        self.roi_tree.column("Order", width=80)
        self.roi_tree.column("ROI Name", width=300)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")
        
        # Load existing data if available
        if self.designer.automate_roi_data:
            for item in self.designer.automate_roi_data:
                boolean_config = item.get("boolean_config")
                item_id = self.roi_tree.insert("", "end", values=(item["order"], item["roi_name"]))
                if boolean_config:
                    self.roi_tree.item(item_id, tags=(str(boolean_config),))

        # Button Frame for New, Remove, Edit Function, and Save
        button_frame = ttk.Frame(self.roi_window)
        button_frame.pack(pady=5)

        self.new_roi_btn = ttk.Button(button_frame, text="New", command=self.open_new_roi_popup)
        self.new_roi_btn.pack(side="left", padx=5)
        self.remove_roi_btn = ttk.Button(button_frame, text="Remove", command=self.remove_roi)
        self.remove_roi_btn.pack(side="left", padx=5)
        
        self.move_up_btn = ttk.Button(button_frame, text="Move Up", command=lambda: self.move_roi_order(-1))
        self.move_up_btn.pack(side="left", padx=5)

        self.move_down_btn = ttk.Button(button_frame, text="Move Down", command=lambda: self.move_roi_order(1))
        self.move_down_btn.pack(side="left", padx=5)

        self.edit_function_btn = ttk.Button(button_frame, text="Edit", command=self.edit_roi_function)
        self.edit_function_btn.pack(side="left", padx=5)

        self.save_roi_btn = ttk.Button(button_frame, text="Save", command=self.save_roi_list)
        self.save_roi_btn.pack(side="left", padx=5)
        # Close Button
        self.close_btn = ttk.Button(self.roi_window, text="Close", command=self.roi_window.destroy)
        self.close_btn.pack(pady=10)
        
    def open_automate_roi_window(self, parent):
        """Open a new window for Automate ROI step."""
        roi_window = tk.Toplevel(parent)
        roi_window.title("Automate ROI")
        roi_window.geometry("800x400")
        # Bold Title Label
        title_label = tk.Label(roi_window, text="Automate ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Treeview for ROI List (Supports Ordering and Functions) with vertical scrollbar
        roi_tree_frame = ttk.Frame(roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("Order", "ROI Name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("Order", text="Order")
        self.roi_tree.heading("ROI Name", text="ROI Name")
        
        self.roi_tree.column("Order", width=80)
        self.roi_tree.column("ROI Name", width=300)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")

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
        self.close_btn = ttk.Button(self.roi_window, text="Close", command=self.roi_window.destroy)
        self.close_btn.pack(pady=10)

    def open_new_roi_popup(self):
        """Open a popup window to add a new ROI item."""
        new_roi_popup = tk.Toplevel(self.roi_window)
        new_roi_popup.title("Add ROI")
        new_roi_popup.geometry("150x150")

        ttk.Label(new_roi_popup, text="ROI Name:").pack(pady=5)
        self.roi_name_var = tk.StringVar()
        self.roi_name_entry = ttk.Entry(new_roi_popup, textvariable=self.roi_name_var)
        self.roi_name_entry.pack(pady=5)
        
        self.current_boolean_data = None

        ttk.Button(new_roi_popup, text="Add Function", command=self.open_boolean_window_for_new).pack(pady=5)

        ttk.Button(new_roi_popup, text="Add", command=lambda: self.add_roi(new_roi_popup)).pack(pady=5)
    
    def add_roi(self, popup):
        """Add a new ROI item with function to the list."""
        roi_name = self.roi_name_var.get().strip()
        if roi_name:
            order = len(self.roi_tree.get_children()) + 1
            # Store boolean data in tree item
            self.roi_tree.insert("", "end", values=(order, roi_name), tags=(str(self.current_boolean_data),))
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "ROI Name is required.")

    def remove_roi(self):
        """Remove selected ROI item from the treeview."""
        selected_item = self.roi_tree.selection()
        for item in selected_item:
            self.roi_tree.delete(item)

    def edit_roi_function(self):
        """Edit the function of the selected ROI item."""
        selected_item = self.roi_tree.selection()
        if selected_item:
            item_values = self.roi_tree.item(selected_item[0], "values")
            item_tags = self.roi_tree.item(selected_item[0], "tags")
            current_boolean_data = eval(item_tags[0]) if item_tags and item_tags[0] != 'None' else None
            
            # Open edit popup
            edit_popup = tk.Toplevel(self.roi_window)
            edit_popup.title("Edit ROI")
            edit_popup.geometry("300x150")
            
            ttk.Label(edit_popup, text="ROI Name:").pack(pady=5)
            edit_roi_name_var = tk.StringVar(value=item_values[1])
            edit_roi_name_entry = ttk.Entry(edit_popup, textvariable=edit_roi_name_var)
            edit_roi_name_entry.pack(pady=5)
            
            # Store the current boolean data for editing
            self.edit_boolean_data = current_boolean_data
            
            def open_boolean_for_edit():
                """Open Boolean window with preloaded data and callback."""
                def save_boolean_callback(boolean_data):
                    self.edit_boolean_data = boolean_data
                    messagebox.showinfo("Boolean Updated", "Boolean configuration updated!")
                
                Boolean_Window(edit_popup, self.designer, callback=save_boolean_callback, preload_data=self.edit_boolean_data)
            
            ttk.Button(edit_popup, text="Edit Boolean Function", command=open_boolean_for_edit).pack(pady=5)
            
            def save_edit():
                """Save the edited ROI."""
                new_name = edit_roi_name_var.get().strip()
                if new_name:
                    # Update tree item
                    self.roi_tree.item(selected_item[0], values=(item_values[0], new_name), tags=(str(self.edit_boolean_data),))
                    edit_popup.destroy()
                else:
                    messagebox.showwarning("Input Error", "ROI Name is required.")
            
            ttk.Button(edit_popup, text="Save", command=save_edit).pack(pady=5)
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
        roi_items = []
        for child in self.roi_tree.get_children():
            values = self.roi_tree.item(child, "values")
            tags = self.roi_tree.item(child, "tags")
            boolean_data = eval(tags[0]) if tags and tags[0] != 'None' else None
            roi_items.append({
                "order": values[0],
                "roi_name": values[1],
                "boolean_config": boolean_data
            })
        
        # Save to designer
        self.designer.automate_roi_data = roi_items
        
        if roi_items:
            messagebox.showinfo("Save Successful", f"ROI list saved successfully. ({len(roi_items)} items)")
        else:
            messagebox.showwarning("Save Error", "No ROI items to save.")
            
    def open_boolean_window_for_new(self):
        """Open a new window for Boolean function editing with callback."""
        def save_boolean_callback(boolean_data):
            self.current_boolean_data = boolean_data
            messagebox.showinfo("Boolean Saved", "Boolean configuration saved!")
        
        Boolean_Window(self.roi_window, self.designer, callback=save_boolean_callback)
    
    def open_boolean_window(self):
        """Open a new window for Boolean function editing (for edit function)."""
        Boolean_Window(self.roi_window, self.designer)
