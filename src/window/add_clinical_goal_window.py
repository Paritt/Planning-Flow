import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *

class Clinical_Goal_Window:
    """Open a new window for adding clinical goals from template."""
    def __init__(self, parent, designer):
        self.designer = designer
        self.window = tk.Toplevel(parent)
        self.window.title("Add Clinical Goal from Template")
        self.window.geometry("400x200")
        
        self.patient_db = get_current('PatientDB')
        clinical_goal_list = [i['Name'] for i in self.patient_db.GetClinicalGoalTemplateInfo()]
        self.matched_dict = {}
        
        # Select Clinical Goal Template
        ttk.Label(self.window, text="Select Clinical Goal Template:").pack(padx=10, pady=10)
        self.template_var = tk.StringVar()
        self.template_dropdown = ttk.Combobox(self.window, textvariable=self.template_var, values=clinical_goal_list, state="readonly", width=40)
        self.template_dropdown.pack(padx=10, pady=5)
        
        # Match ROI Button
        ttk.Button(self.window, text="Match ROI", command=self.match_roi).pack(pady=10)
        
        # Close Button
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)
        
        # Load existing data if available
        if hasattr(self.designer, 'clinical_goal_data') and self.designer.clinical_goal_data:
            self.load_existing_data()
        
    def match_roi(self):
        """Match ROIs for the selected clinical goal template."""
        selected_template = self.template_var.get()
        if not selected_template:
            messagebox.showwarning("No Template Selected", "Please select a clinical goal template.")
            return
        
        goal = self.patient_db.LoadTemplateClinicalGoals(templateName=selected_template)
        need_match_rois_list = [i.OrganData.ResponseFunctionTissueName for i in goal.FunctionToRoiMaps]
        
        # Remove duplicates while preserving order
        unique_rois = []
        seen = set()
        for roi in need_match_rois_list:
            if roi not in seen:
                unique_rois.append(roi)
                seen.add(roi)
        
        # Auto-match ROIs
        available_rois = self.designer.get_roi_list()
        self.matched_dict = {}
        has_unmatched = False
        
        for template_roi in unique_rois:
            if template_roi in available_rois:
                self.matched_dict[template_roi] = template_roi
            else:
                self.matched_dict[template_roi] = None
                has_unmatched = True
        
        # Open matching window if there are unmatched ROIs
        if has_unmatched:
            self._open_match_window(unique_rois, available_rois)
        else:
            messagebox.showinfo("Auto-Matched", "✅ All ROIs are automatically matched!")
            self._save_to_designer(selected_template)
    
    def _open_match_window(self, unique_rois, available_rois):
        """Open a window for manual ROI matching."""
        match_window = tk.Toplevel(self.window)
        match_window.title('Match Clinical Goal ROIs')
        
        # Make window stay on top
        match_window.attributes('-topmost', True)
        match_window.grab_set()
        match_window.focus_force()
        
        available_rois_with_blank = ["--Not Match--"] + available_rois
        
        # Calculate window height based on number of ROIs
        window_height = min(600, 50 + len(unique_rois) * 35 + 60)
        match_window.geometry(f'400x{window_height}')
        
        # Store combo boxes
        combo_boxes = {}
        
        def create_row(root_frame, template_roi, row_n):
            """Create a row for ROI matching."""
            # Label for template ROI name
            lb_roi = tk.Label(root_frame, text=template_roi)
            lb_roi.grid(column=0, row=row_n, padx=5, pady=2)
            lb_roi.config(width=20, height=2)
            
            # Check if already matched
            matched_name = self.matched_dict.get(template_roi)
            if matched_name and matched_name in available_rois:
                # Show matched status
                lb_matched = tk.Label(root_frame, text=f'Matched: {matched_name}')
                lb_matched.grid(column=1, row=row_n, padx=5, pady=2)
                lb_matched.config(width=30, height=2)
                # Store the already matched name
                combo_boxes[template_roi] = matched_name
            else:
                # Create dropdown for manual selection
                combo_var = tk.StringVar()
                combo = ttk.Combobox(root_frame, values=available_rois_with_blank, 
                                    textvariable=combo_var)
                combo.grid(column=1, row=row_n, padx=5, pady=2)
                combo.config(width=30)
                combo.current(0)  # Set to "--Not Match--" by default
                combo_boxes[template_roi] = combo
        
        # Create rows for all unique ROIs
        for idx, template_roi in enumerate(unique_rois):
            create_row(match_window, template_roi, idx)
        
        # Apply button
        def on_apply():
            # Check if all ROIs have been matched
            unmatched_rois = []
            
            for roi_name, combo_or_string in combo_boxes.items():
                if isinstance(combo_or_string, str):
                    # Already matched, this is OK
                    pass
                else:
                    # Check if user selected something from combo box
                    selected = combo_or_string.get()
                    if not selected or selected == "--Not Match--":
                        unmatched_rois.append(roi_name)
            
            # If there are unmatched ROIs, show error
            if unmatched_rois:
                messagebox.showerror(
                    "Incomplete Matching",
                    f"Please match all ROIs before applying.\n\nUnmatched ROIs:\n" + 
                    "\n".join(f"- {roi}" for roi in unmatched_rois)
                )
                return
            
            # All ROIs are matched, collect selections
            for roi_name, combo_or_string in combo_boxes.items():
                if isinstance(combo_or_string, str):
                    # Already matched, keep the value
                    self.matched_dict[roi_name] = combo_or_string
                else:
                    # Get from combo box
                    selected = combo_or_string.get()
                    if selected != "--Not Match--":
                        self.matched_dict[roi_name] = selected
            
            match_window.destroy()
            # Save after successful matching
            selected_template = self.template_var.get()
            self._save_to_designer(selected_template)
        
        button_apply = tk.Button(match_window, text='Apply', command=on_apply)
        button_apply.grid(column=1, row=len(unique_rois), pady=15)
        button_apply.config(width=10)
        
        # Wait for window to close before continuing
        match_window.wait_window()
    
    def _save_to_designer(self, template_name):
        """Save matched ROIs to designer."""
        matched_rois = []
        for template_roi, matched_roi in self.matched_dict.items():
            if matched_roi:
                matched_rois.append({
                    "template_roi": template_roi,
                    "matched_roi": matched_roi
                })
        
        self.designer.clinical_goal_data = {
            "clinical_goal_template": template_name,
            "matched_rois": matched_rois
        }
        
        messagebox.showinfo("Saved", f"Clinical goal configuration saved successfully. ({len(matched_rois)} ROIs matched)")
        self.window.destroy()
    
    def load_existing_data(self):
        """Load existing clinical goal data."""
        data = self.designer.clinical_goal_data
        if 'clinical_goal_template' in data:
            self.template_var.set(data['clinical_goal_template'])
