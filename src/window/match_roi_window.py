import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MatchROI_Window:
    """Create a section for designing flow steps with labels for flow/user and Save Flow button."""
    """Open a new window for Match ROI step."""
    def __init__(self, parent, designer):
        self.designer = designer
        match_roi_window = tk.Toplevel(parent)
        match_roi_window.title("Match ROI")
        match_roi_window.geometry("600x400")

        # Bold Title Label
        title_label = tk.Label(match_roi_window, text="Match ROI", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # ROI tree with vertical scrollbar
        roi_tree_frame = ttk.Frame(match_roi_window)
        roi_tree_frame.pack(pady=5, fill="both", expand=True)
        
        roi_tree_scroll_y = ttk.Scrollbar(roi_tree_frame, orient="vertical")
        
        self.roi_tree = ttk.Treeview(roi_tree_frame, columns=("ROI name", "Possible ROI name"), show="headings",
                                    yscrollcommand=roi_tree_scroll_y.set, height=8)
        
        roi_tree_scroll_y.config(command=self.roi_tree.yview)
        
        self.roi_tree.heading("ROI name", text="ROI name")
        self.roi_tree.heading("Possible ROI name", text="Possible ROI name")
        
        self.roi_tree.column("ROI name", width=200)
        self.roi_tree.column("Possible ROI name", width=200)
        
        self.roi_tree.pack(side="left", fill="both", expand=True)
        roi_tree_scroll_y.pack(side="right", fill="y")
        
        # Load existing data if available
        if self.designer.match_roi_data:
            for item in self.designer.match_roi_data:
                self.roi_tree.insert("", "end", values=(item["roi_name"], item["possible_roi_name"]))

        # Add ROI Button
        self.add_roi_btn = ttk.Button(match_roi_window, text="Add ROI", command=lambda: self.open_add_roi_popup(match_roi_window))
        self.add_roi_btn.pack(side="left", pady=5)
        # Remove ROI Button
        self.remove_roi_btn = ttk.Button(match_roi_window, text="Remove Selected ROI", command=self.remove_match_roi)
        self.remove_roi_btn.pack(side="left", pady=5)
        # Edit ROI Button
        self.edit_roi_btn = ttk.Button(match_roi_window, text="Edit Selected ROI", command=lambda: self.show_step_info("Edit ROI"))
        self.edit_roi_btn.pack(side="left", pady=5)
        # Save ROI List Button
        self.save_roi_list = ttk.Button(match_roi_window, text="Save", command=lambda: self.save_match_roi_list())
        self.save_roi_list.pack(side="left", pady=5)
        # Close Button
        self.close_btn = ttk.Button(match_roi_window, text="Close", command=match_roi_window.destroy)
        self.close_btn.pack(pady=5)
        
    def open_add_roi_popup(self, parent):
        """Open a popup window to add ROI."""
        add_roi_popup = tk.Toplevel(parent)
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
        roi_name = self.roi_name_var.get().strip()
        if roi_name:
            possible_roi_name = self.possible_roi_name_var.get().strip()
            self.roi_tree.insert("", "end", values=(roi_name, possible_roi_name))
            popup.destroy()
        else:
            messagebox.showwarning("Input Error", "ROI Name cannot be empty.")

    def remove_match_roi(self):
        """Remove selected ROI item from the treeview."""
        selected_item = self.roi_tree.selection()
        for item in selected_item:
            self.roi_tree.delete(item)
            
    def save_match_roi_list(self):
        """Save the current list of matched ROI items."""
        roi_items = []
        for child in self.roi_tree.get_children():
            values = self.roi_tree.item(child, "values")
            roi_items.append({
                "roi_name": values[0],
                "possible_roi_name": values[1]
            })
        
        # Save to designer
        self.designer.match_roi_data = roi_items
        
        if roi_items:
            messagebox.showinfo("Save Successful", f"Matched ROI saved successfully. ({len(roi_items)} items)")
        else:
            messagebox.showwarning("Save Error", "No ROI items to save.")
    def show_step_info(self, step):
        """Popup with step description."""
        messagebox.showinfo("Step Info", f"Details about {step} step.")        
