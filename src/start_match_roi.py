from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current
import tkinter as tk
from tkinter import ttk, StringVar, Label, Button, Toplevel, messagebox


class MatchROI:
    def __init__(self, match_roi_data, case):
        """
        Initialize the MatchROI class.
        
        Args:
            match_roi_data: List of dictionaries with structure:
                [{"roi_name": "PTV_4140", "possible_roi_name": "PTV, PTV4140, PTV41.4"}, ...]
            case: RayStation case object
        """
        self.match_roi_data = match_roi_data
        self.case = case
        self.matched_dict = {}
        self.has_unmatched = False
        
    def get_case_roi_names(self):
        """Get all ROI names from the current case."""
        try:
            return [r.Name for r in self.case.PatientModel.RegionsOfInterest]
        except:
            return []
    
    def auto_match(self):
        """
        Automatically match ROIs from flow data to case ROIs.
        First tries exact match, then searches through possible_roi_name list.
        """
        case_roi_names = self.get_case_roi_names()
        
        for roi_entry in self.match_roi_data:
            flow_roi_name = roi_entry.get("roi_name")
            possible_names = roi_entry.get("possible_roi_name", "")
            
            # Try exact match first
            if flow_roi_name in case_roi_names:
                self.matched_dict[flow_roi_name] = flow_roi_name
            else:
                # Try possible names (comma-separated list)
                matched = False
                if possible_names:
                    possible_list = [name.strip() for name in possible_names.split(",") if name.strip()]
                    for possible_name in possible_list:
                        if possible_name in case_roi_names:
                            self.matched_dict[flow_roi_name] = possible_name
                            matched = True
                            break
                
                # Mark as unmatched if still not found
                if not matched:
                    self.matched_dict[flow_roi_name] = None
                    self.has_unmatched = True
    
    def get_matched_dict(self):
        """
        Main method to get matched ROI dictionary.
        Returns dictionary mapping flow roi_name to actual case roi_name.
        """
        # First, perform automatic matching
        self.auto_match()
        
        # If there are unmatched ROIs or user wants to review, open GUI
        if self.has_unmatched or True:  # Always show GUI for review
            self._open_match_window()
        
        # Filter out any None or --Not Match-- values before returning
        return {k: v for k, v in self.matched_dict.items() if v is not None}
    
    def _open_match_window(self):
        """Open a window for manual ROI matching."""
        match_window = Toplevel()
        match_window.title('Match ROI')
        
        # Make window stay on top
        match_window.attributes('-topmost', True)
        match_window.grab_set()
        match_window.focus_force()
        
        case_roi_names = self.get_case_roi_names()
        case_roi_names_with_blank = ["----", "--Not Match--"] + case_roi_names
        
        # Calculate window height based on number of ROIs
        window_height = min(600, 50 + len(self.match_roi_data) * 35 + 60)
        match_window.geometry(f'320x{window_height}')
        
        # Store combo boxes and matched ROI labels
        combo_boxes = {}
        
        def create_row(root_frame, flow_roi_name, row_n):
            """Create a row for ROI matching."""
            # Label for flow ROI name
            lb_roi = Label(root_frame, text=flow_roi_name)
            lb_roi.grid(column=0, row=row_n, padx=5, pady=2)
            lb_roi.config(width=15, height=2)
            
            # Check if already matched
            matched_name = self.matched_dict.get(flow_roi_name)
            if matched_name and matched_name in case_roi_names:
                # Show matched status with the actual matched name
                lb_matched = Label(root_frame, text=f'Matched: {matched_name}')
                lb_matched.grid(column=1, row=row_n, padx=5, pady=2)
                lb_matched.config(width=27, height=2)
                # Store the already matched name for apply
                combo_boxes[flow_roi_name] = matched_name
            else:
                # Create dropdown for manual selection
                combo_var = StringVar()
                combo = ttk.Combobox(root_frame, values=case_roi_names_with_blank, 
                                    textvariable=combo_var)
                combo.grid(column=1, row=row_n, padx=5, pady=2)
                combo.config(width=27)
                combo.current(0)  # Set to "----" by default
                combo_boxes[flow_roi_name] = combo
        
        # Create rows for all ROIs in flow
        for idx, roi_entry in enumerate(self.match_roi_data):
            flow_roi_name = roi_entry.get("roi_name")
            create_row(match_window, flow_roi_name, idx)
        
        # Cancel button
        def on_cancel():
            # Keep existing matches, clear unmatched
            self.matched_dict = {k: v for k, v in self.matched_dict.items() if v is not None}
            match_window.destroy()
        
        button_cancel = Button(match_window, text='Cancel', command=on_cancel)
        button_cancel.grid(column=0, row=len(self.match_roi_data), pady=15)
        button_cancel.config(width=10)
        
        # Apply button
        def on_apply():
            # First, check if all ROIs have been matched or explicitly set to None
            unmatched_rois = []
            
            for roi_name, combo_or_string in combo_boxes.items():
                if isinstance(combo_or_string, str):
                    # Already matched, this is OK
                    pass
                else:
                    # Check if user selected something from combo box
                    selected = combo_or_string.get()
                    if not selected or selected == "----":
                        unmatched_rois.append(roi_name)
            
            # If there are unmatched ROIs, show error and don't close window
            if unmatched_rois:
                messagebox.showerror(
                    "Incomplete Matching",
                    f"Please match all ROIs before applying.\n\nUnmatched ROIs:\n" + 
                    "\n".join(f"- {roi}" for roi in unmatched_rois)
                )
                return  # Don't close the window
            
            # All ROIs are matched, collect selections
            for roi_name, combo_or_string in combo_boxes.items():
                if isinstance(combo_or_string, str):
                    # Already matched, keep the value
                    self.matched_dict[roi_name] = combo_or_string
                else:
                    # Get from combo box
                    selected = combo_or_string.get()
                    self.matched_dict[roi_name] = selected
            
            match_window.destroy()
        
        button_apply = Button(match_window, text='Apply', command=on_apply)
        button_apply.grid(column=1, row=len(self.match_roi_data), pady=15)
        button_apply.config(width=10)
        
        # Wait for window to close before continuing
        match_window.wait_window()
