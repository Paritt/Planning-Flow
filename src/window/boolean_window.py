import tkinter as tk
from tkinter import ttk

class Boolean_Window:
    """Boolean operation window for ROI algebra."""
    def __init__(self, parent, designer=None, use_extended_list=False):
        self.designer = designer
        self.boolean_window = tk.Toplevel(parent)
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
        # Get ROI list from designer if available (extended list includes Match ROI + Condition ROI)
        if self.designer:
            roi_list = self.designer.get_extended_roi_list() if use_extended_list else self.designer.get_roi_list()
        else:
            roi_list = ['PTV', 'CTV', 'GTV', 'Bladder', 'Rectum', 'Bowel', 'External']
        roi_a_combo = ttk.Combobox(frame_a, textvariable=self.roi_a,
                                values=roi_list, state="readonly")
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
                                    values=roi_list, state="readonly")
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
        save_button = tk.Button(self.boolean_window, text="Save", command=self.boolean_window.destroy)
        save_button.pack(pady=10)
