import tkinter as tk
from tkinter import ttk
import re


class FunctionConfigFrame:
    """
    Reusable class for creating a function configuration frame with all necessary UI elements.
    Handles function tag, ROI name, weight, function type, and type-specific options.
    """

    # Function type options
    FUNCTION_TYPES = [
        'Min Dose', 'Max Dose', 'Min DVH', 'Max DVH', 'Uniform Dose',
        'Min EUD', 'Max EUD', 'Target EUD', 'Dose fall-off', 'Uniformity Constraint'
    ]

    # Volume unit options
    VOLUME_UNITS = ['%', 'cc']

    def __init__(self, parent, designer, mode="add", selected_data=None, disable_fields=None):
        """
        Initialize the function configuration frame.

        Args:
            parent: Parent widget
            designer: Designer object with get_roi_list() and other methods
            mode: "add" or "edit"
            selected_data: Dict with existing function data (for edit mode)
            disable_fields: List of field names to disable (e.g., ["function_type", "roi"])
        """
        self.parent = parent
        self.designer = designer
        self.mode = mode
        self.selected_data = selected_data or {}
        self.disable_fields = disable_fields or []
        
        # Store all input variables
        self.vars = {}
        self.frames = {}
        self.entries = {}
        self.combos = {}

        # Create main frame with horizontal layout
        self.main_frame = ttk.Frame(parent)
        
        # Create subframes
        self.config_frame = ttk.Frame(self.main_frame)  # Config frame (right side)
        self.content_frame = ttk.Frame(self.main_frame)  # Function frames (left side)
        self.name_frame = ttk.Frame(self.main_frame)  # Frame for function tag and ROI name (top y-fill)

        # Create UI elements
        self._create_name_frame()
        self._create_config_frame()
        self._create_common_fields()
        self._create_type_specific_frames()

    def _create_name_frame(self):
        """Create the name frame (top) for function tag and ROI name."""
        self.name_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        # ROI Name
        roi_frame = ttk.Frame(self.name_frame)
        roi_frame.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        ttk.Label(roi_frame, text="ROI Name:").pack(side="left", padx=5)
        self.vars["roi"] = tk.StringVar(value=self.selected_data.get("roi", ""))
        roi_combo = ttk.Combobox(
            roi_frame, textvariable=self.vars["roi"],
            values=self.designer.get_roi_list(), state="readonly"
        )
        roi_combo.pack(side="left", padx=5, fill="x", expand=True)
        self.combos["roi"] = roi_combo
        if "roi" in self.disable_fields:
            roi_combo.config(state="disabled")
            
        # Function tag
        tag_frame = ttk.Frame(self.name_frame)
        tag_frame.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        ttk.Label(tag_frame, text="Function tag:").pack(side="left", padx=5)
        self.vars["tag"] = tk.StringVar(value=self.selected_data.get("tag", ""))
        tag_entry = ttk.Entry(tag_frame, textvariable=self.vars["tag"])
        tag_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.entries["tag"] = tag_entry
        if "tag" in self.disable_fields:
            tag_entry.config(state="disabled")
        
        

    def _create_config_frame(self):
        """Create the config frame (right side) with objective/constraint and beam selection."""
        self.config_frame.pack(side="right", padx=10, pady=10, fill="both")
        
        # Objective/Constraint radio buttons
        
        self.vars["objective_constraint"] = tk.StringVar(value=self.selected_data.get("objective_constraint", "Objective"))
        radio_frame = ttk.Frame(self.config_frame)
        radio_frame.pack(anchor="w", pady=5)
        
        self.vars["objective_radio"] = ttk.Radiobutton(
            radio_frame, text="Objective", variable=self.vars["objective_constraint"],
            value="Objective", command=self._on_objective_constraint_change
        )
        self.vars["objective_radio"].pack(side="left", padx=5)
        
        self.vars["constraint_radio"] = ttk.Radiobutton(
            radio_frame, text="Constraint", variable=self.vars["objective_constraint"],
            value="Constraint", command=self._on_objective_constraint_change
        )
        self.vars["constraint_radio"].pack(side="left", padx=5)
        
        # Weight field (shown only for Objective)
        weight_frame = ttk.Frame(self.config_frame)
        weight_frame.pack(anchor="w", pady=5)
        ttk.Label(weight_frame, text="Weight:").pack(side="left", padx=5)
        self.vars["weight"] = tk.StringVar(value=self.selected_data.get("weight", "1.0"))
        self.weight_entry = ttk.Entry(weight_frame, textvariable=self.vars["weight"], width=10)
        self.weight_entry.pack(side="left", padx=5)
        self.weight_frame = weight_frame
        
        # Robust checkbox
        
        self.vars["is_robust"] = tk.BooleanVar(value=self.selected_data.get("is_robust", False))
        robust_check = ttk.Checkbutton(
            self.config_frame, text="Robust", variable=self.vars["is_robust"]
        )
        robust_check.pack(anchor="w", padx=5, pady=2)
        
        # Restrict function to beam checkbox
        self.vars["restrict_to_beam"] = tk.BooleanVar(value=self.selected_data.get("restrict_to_beam", False))
        restrict_check = ttk.Checkbutton(
            self.config_frame, text="Restrict function to beam", variable=self.vars["restrict_to_beam"],
            command=self._on_restrict_beam_change
        )
        restrict_check.pack(anchor="w", padx=5, pady=2)
        
        # Beam selection dropdown
        beam_frame = ttk.Frame(self.config_frame)
        beam_frame.pack(anchor="w", pady=5, padx=20)
        
        ttk.Label(beam_frame, text="Select Beam:").pack(side="left", padx=5)
        self.vars["selected_beam"] = tk.StringVar(value=self.selected_data.get("selected_beam", ""))
        
        beam_options = ["All beams individually"] + self.designer.get_beam_list()
        self.beam_combo = ttk.Combobox(
            beam_frame, textvariable=self.vars["selected_beam"],
            values=beam_options, state="readonly", width=20
        )
        self.beam_combo.pack(side="left", padx=5)
        self.beam_frame = beam_frame
        
        # Update UI state based on initial values
        self._on_objective_constraint_change()
        self._on_restrict_beam_change()

    def _on_objective_constraint_change(self):
        """Handle objective/constraint radio button change."""
        is_objective = self.vars["objective_constraint"].get() == "Objective"
        
        # Gray out weight if constraint
        if is_objective:
            self.weight_entry.config(state="normal")
        else:
            self.weight_entry.config(state="disabled")

    def _on_restrict_beam_change(self):
        """Handle restrict to beam checkbox change."""
        is_restricted = self.vars["restrict_to_beam"].get()
        
        if is_restricted:
            self.beam_combo.config(state="readonly")
        else:
            self.beam_combo.config(state="disabled")

    def _create_common_fields(self):
        """Create the common fields: function type and type-specific options."""
        self.content_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Common frame (top)
        common_frame = ttk.LabelFrame(self.content_frame, text="Function Configuration", padding=10)
        common_frame.pack(fill="x", padx=5, pady=5)
        
        # Store references for type-specific frame placement
        self.common_frame = common_frame
        self.type_frame_row = 0

    def _create_type_specific_frames(self):
        """Create frames for each function type."""
        
        # Function type selector in common frame
        ttk.Label(self.common_frame, text="Function type:").grid(row=self.type_frame_row, column=0, padx=5, pady=5, sticky="w")
        self.vars["type"] = tk.StringVar(value=self.selected_data.get("type", ""))
        function_combo = ttk.Combobox(
            self.common_frame, textvariable=self.vars["type"],
            values=self.FUNCTION_TYPES, state="readonly"
        )
        function_combo.grid(row=self.type_frame_row, column=1, padx=5, pady=5)
        self.combos["type"] = function_combo
        if "type" in self.disable_fields:
            function_combo.config(state="disabled")
        function_combo.bind("<<ComboboxSelected>>", lambda event: self._on_function_type_change())
        
        type_frame_row = self.type_frame_row + 1
        
        # Frame for Min Dose
        frame_min_dose = ttk.Frame(self.common_frame)
        ttk.Label(frame_min_dose, text="Min Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["min_dose_value"] = tk.StringVar()
        min_dose_entry = ttk.Entry(frame_min_dose, textvariable=self.vars["min_dose_value"])
        min_dose_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["min_dose_value"] = min_dose_entry
        self.frames["Min Dose"] = frame_min_dose

        # Frame for Max Dose
        frame_max_dose = ttk.Frame(self.common_frame)
        ttk.Label(frame_max_dose, text="Max Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["max_dose_value"] = tk.StringVar()
        max_dose_entry = ttk.Entry(frame_max_dose, textvariable=self.vars["max_dose_value"])
        max_dose_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["max_dose_value"] = max_dose_entry
        self.frames["Max Dose"] = frame_max_dose

        # Frame for Min DVH
        frame_min_dvh = ttk.Frame(self.common_frame)
        ttk.Label(frame_min_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["dose_value_min_dvh"] = tk.StringVar()
        min_dvh_dose = ttk.Entry(frame_min_dvh, textvariable=self.vars["dose_value_min_dvh"])
        min_dvh_dose.grid(row=0, column=1, padx=5, pady=5)
        self.entries["dose_value_min_dvh"] = min_dvh_dose
        ttk.Label(frame_min_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.vars["volume_value_min_dvh"] = tk.StringVar()
        min_dvh_volume = ttk.Entry(frame_min_dvh, textvariable=self.vars["volume_value_min_dvh"])
        min_dvh_volume.grid(row=1, column=1, padx=5, pady=5)
        self.entries["volume_value_min_dvh"] = min_dvh_volume
        self.vars["volume_unit_min_dvh"] = tk.StringVar()
        min_dvh_unit = ttk.Combobox(
            frame_min_dvh, textvariable=self.vars["volume_unit_min_dvh"],
            values=self.VOLUME_UNITS, state="readonly", width=5
        )
        min_dvh_unit.grid(row=1, column=2, padx=5, pady=5)
        self.combos["volume_unit_min_dvh"] = min_dvh_unit
        self.frames["Min DVH"] = frame_min_dvh

        # Frame for Max DVH
        frame_max_dvh = ttk.Frame(self.common_frame)
        ttk.Label(frame_max_dvh, text="Dose Level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["dose_value_max_dvh"] = tk.StringVar()
        max_dvh_dose = ttk.Entry(frame_max_dvh, textvariable=self.vars["dose_value_max_dvh"])
        max_dvh_dose.grid(row=0, column=1, padx=5, pady=5)
        self.entries["dose_value_max_dvh"] = max_dvh_dose
        ttk.Label(frame_max_dvh, text="Volume Level:").grid(row=1, column=0, padx=5, pady=5)
        self.vars["volume_value_max_dvh"] = tk.StringVar()
        max_dvh_volume = ttk.Entry(frame_max_dvh, textvariable=self.vars["volume_value_max_dvh"])
        max_dvh_volume.grid(row=1, column=1, padx=5, pady=5)
        self.entries["volume_value_max_dvh"] = max_dvh_volume
        self.vars["volume_unit_max_dvh"] = tk.StringVar()
        max_dvh_unit = ttk.Combobox(
            frame_max_dvh, textvariable=self.vars["volume_unit_max_dvh"],
            values=self.VOLUME_UNITS, state="readonly", width=5
        )
        max_dvh_unit.grid(row=1, column=2, padx=5, pady=5)
        self.combos["volume_unit_max_dvh"] = max_dvh_unit
        self.frames["Max DVH"] = frame_max_dvh

        # Frame for Min EUD
        frame_min_eud = ttk.Frame(self.common_frame)
        ttk.Label(frame_min_eud, text="Min EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["min_eud_value"] = tk.StringVar()
        min_eud_entry = ttk.Entry(frame_min_eud, textvariable=self.vars["min_eud_value"])
        min_eud_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["min_eud_value"] = min_eud_entry
        ttk.Label(frame_min_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.vars["a_param_min_eud"] = tk.StringVar()
        min_eud_param = ttk.Entry(frame_min_eud, textvariable=self.vars["a_param_min_eud"])
        min_eud_param.grid(row=1, column=1, padx=5, pady=5)
        self.entries["a_param_min_eud"] = min_eud_param
        self.frames["Min EUD"] = frame_min_eud

        # Frame for Max EUD
        frame_max_eud = ttk.Frame(self.common_frame)
        ttk.Label(frame_max_eud, text="Max EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["max_eud_value"] = tk.StringVar()
        max_eud_entry = ttk.Entry(frame_max_eud, textvariable=self.vars["max_eud_value"])
        max_eud_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["max_eud_value"] = max_eud_entry
        ttk.Label(frame_max_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.vars["a_param_max_eud"] = tk.StringVar()
        max_eud_param = ttk.Entry(frame_max_eud, textvariable=self.vars["a_param_max_eud"])
        max_eud_param.grid(row=1, column=1, padx=5, pady=5)
        self.entries["a_param_max_eud"] = max_eud_param
        self.frames["Max EUD"] = frame_max_eud

        # Frame for Target EUD
        frame_target_eud = ttk.Frame(self.common_frame)
        ttk.Label(frame_target_eud, text="Target EUD (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["target_eud_value"] = tk.StringVar()
        target_eud_entry = ttk.Entry(frame_target_eud, textvariable=self.vars["target_eud_value"])
        target_eud_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["target_eud_value"] = target_eud_entry
        ttk.Label(frame_target_eud, text="Parameter A (-150,150):").grid(row=1, column=0, padx=5, pady=5)
        self.vars["a_param_target_eud"] = tk.StringVar()
        target_eud_param = ttk.Entry(frame_target_eud, textvariable=self.vars["a_param_target_eud"])
        target_eud_param.grid(row=1, column=1, padx=5, pady=5)
        self.entries["a_param_target_eud"] = target_eud_param
        self.frames["Target EUD"] = frame_target_eud

        # Frame for Uniform Dose
        frame_uniform_dose = ttk.Frame(self.common_frame)
        ttk.Label(frame_uniform_dose, text="Uniform Dose (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["uniform_dose_value"] = tk.StringVar()
        uniform_dose_entry = ttk.Entry(frame_uniform_dose, textvariable=self.vars["uniform_dose_value"])
        uniform_dose_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["uniform_dose_value"] = uniform_dose_entry
        self.frames["Uniform Dose"] = frame_uniform_dose

        # Frame for Dose fall-off
        frame_dose_falloff = ttk.Frame(self.common_frame)
        ttk.Label(frame_dose_falloff, text="High dose level (cGy):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["high_dose_value"] = tk.StringVar()
        high_dose_entry = ttk.Entry(frame_dose_falloff, textvariable=self.vars["high_dose_value"])
        high_dose_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["high_dose_value"] = high_dose_entry
        ttk.Label(frame_dose_falloff, text="Low dose level (cGy):").grid(row=1, column=0, padx=5, pady=5)
        self.vars["low_dose_value"] = tk.StringVar()
        low_dose_entry = ttk.Entry(frame_dose_falloff, textvariable=self.vars["low_dose_value"])
        low_dose_entry.grid(row=1, column=1, padx=5, pady=5)
        self.entries["low_dose_value"] = low_dose_entry
        ttk.Label(frame_dose_falloff, text="Low dose distance (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.vars["low_dose_distance"] = tk.StringVar()
        low_distance_entry = ttk.Entry(frame_dose_falloff, textvariable=self.vars["low_dose_distance"])
        low_distance_entry.grid(row=2, column=1, padx=5, pady=5)
        self.entries["low_dose_distance"] = low_distance_entry
        self.frames["Dose fall-off"] = frame_dose_falloff

        # Frame for Uniformity Constraint
        frame_uniformity_constraint = ttk.Frame(self.common_frame)
        ttk.Label(frame_uniformity_constraint, text="Rel.std.dev (%):").grid(row=0, column=0, padx=5, pady=5)
        self.vars["rel_std_dev"] = tk.StringVar()
        rel_std_dev_entry = ttk.Entry(frame_uniformity_constraint, textvariable=self.vars["rel_std_dev"])
        rel_std_dev_entry.grid(row=0, column=1, padx=5, pady=5)
        self.entries["rel_std_dev"] = rel_std_dev_entry
        self.frames["Uniformity Constraint"] = frame_uniformity_constraint

        # Parse and populate values if in edit mode
        if self.mode == "edit" and self.selected_data.get("description"):
            self._parse_and_populate_values(
                self.selected_data.get("type", ""),
                self.selected_data.get("description", "")
            )

        # Show initial frame
        self._show_selected_frame()
        
        # Handle Uniformity Constraint special case
        self._enforce_uniformity_constraint()

    def _show_selected_frame(self):
        """Show the relevant frame based on function type selection."""
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show selected frame
        selection = self.vars["type"].get()
        if selection in self.frames:
            self.frames[selection].grid(row=self.type_frame_row + 1, column=0, columnspan=2, pady=5)

    def _on_function_type_change(self):
        """Handle function type selection change."""
        self._show_selected_frame()
        self._enforce_uniformity_constraint()

    def _enforce_uniformity_constraint(self):
        """Force Constraint mode for Uniformity Constraint function type."""
        is_uniformity = self.vars["type"].get() == "Uniformity Constraint"
        
        if is_uniformity:
            self.vars["objective_constraint"].set("Constraint")
            self.vars["objective_radio"].config(state="disabled")
            self.vars["constraint_radio"].config(state="disabled")
            self.weight_entry.config(state="disabled")
        else:
            self.vars["objective_radio"].config(state="normal")
            self.vars["constraint_radio"].config(state="normal")
            self._on_objective_constraint_change()

    def _parse_and_populate_values(self, function_type, description):
        """Parse the description and populate the corresponding input fields."""
        if function_type == "Min Dose":
            match = re.search(r'Min Dose (\S+) cGy', description)
            if match:
                self.vars["min_dose_value"].set(match.group(1))
        elif function_type == "Max Dose":
            match = re.search(r'Max Dose (\S+) cGy', description)
            if match:
                self.vars["max_dose_value"].set(match.group(1))
        elif function_type == "Min DVH":
            match = re.search(r'Min DVH (\S+) cGy to (\S+)(%)|(cc) volume', description)
            if match:
                self.vars["dose_value_min_dvh"].set(match.group(1))
                self.vars["volume_value_min_dvh"].set(match.group(2))
                self.vars["volume_unit_min_dvh"].set(match.group(3) if match.group(3) else match.group(4))
        elif function_type == "Max DVH":
            match = re.search(r'Max DVH (\S+) cGy to (\S+)(%)|(cc) volume', description)
            if match:
                self.vars["dose_value_max_dvh"].set(match.group(1))
                self.vars["volume_value_max_dvh"].set(match.group(2))
                self.vars["volume_unit_max_dvh"].set(match.group(3) if match.group(3) else match.group(4))
        elif function_type == "Min EUD":
            match = re.search(r'Min EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.vars["min_eud_value"].set(match.group(1))
                self.vars["a_param_min_eud"].set(match.group(2))
        elif function_type == "Max EUD":
            match = re.search(r'Max EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.vars["max_eud_value"].set(match.group(1))
                self.vars["a_param_max_eud"].set(match.group(2))
        elif function_type == "Target EUD":
            match = re.search(r'Target EUD (\S+) cGy, Parameter A (\S+)', description)
            if match:
                self.vars["target_eud_value"].set(match.group(1))
                self.vars["a_param_target_eud"].set(match.group(2))
        elif function_type == "Uniform Dose":
            match = re.search(r'Uniform Dose (\S+) cGy', description)
            if match:
                self.vars["uniform_dose_value"].set(match.group(1))
        elif function_type == "Dose fall-off":
            match = re.search(r'Dose fall-off \[H\] (\S+) cGy \[L\] (\S+) cGy, Low dose distance (\S+) cm', description)
            if match:
                self.vars["high_dose_value"].set(match.group(1))
                self.vars["low_dose_value"].set(match.group(2))
                self.vars["low_dose_distance"].set(match.group(3))
        elif function_type == "Uniformity Constraint":
            match = re.search(r'Uniformity Constraint Rel\.std\.dev (\S+) %', description)
            if match:
                self.vars["rel_std_dev"].set(match.group(1))

    def pack(self, **kwargs):
        """Pack the main frame."""
        self.main_frame.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the main frame."""
        self.main_frame.grid(**kwargs)

    def get_frame(self):
        """Return the main frame for manual layout management."""
        return self.main_frame

    def get_values(self):
        """Get all current values as a dictionary."""
        function_type = self.vars["type"].get().strip()
        description = self._build_description(function_type)

        return {
            "tag": self.vars["tag"].get().strip(),
            "type": function_type,
            "roi": self.vars["roi"].get().strip(),
            "weight": self.vars["weight"].get().strip(),
            "description": description,
            "objective_constraint": self.vars["objective_constraint"].get(),
            "is_robust": self.vars["is_robust"].get(),
            "restrict_to_beam": self.vars["restrict_to_beam"].get(),
            "selected_beam": self.vars["selected_beam"].get().strip()
        }

    def _build_description(self, function_type):
        """Build description string based on function type and values."""
        if function_type == "Min Dose":
            min_dose = self.vars["min_dose_value"].get().strip()
            return f"Min Dose {min_dose} cGy"
        elif function_type == "Max Dose":
            max_dose = self.vars["max_dose_value"].get().strip()
            return f"Max Dose {max_dose} cGy"
        elif function_type == "Min DVH":
            dose_level = self.vars["dose_value_min_dvh"].get().strip()
            volume_level = self.vars["volume_value_min_dvh"].get().strip()
            volume_unit = self.vars["volume_unit_min_dvh"].get().strip()
            return f"Min DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Max DVH":
            dose_level = self.vars["dose_value_max_dvh"].get().strip()
            volume_level = self.vars["volume_value_max_dvh"].get().strip()
            volume_unit = self.vars["volume_unit_max_dvh"].get().strip()
            return f"Max DVH {dose_level} cGy to {volume_level}{volume_unit} volume"
        elif function_type == "Min EUD":
            min_eud = self.vars["min_eud_value"].get().strip()
            a_param = self.vars["a_param_min_eud"].get().strip()
            return f"Min EUD {min_eud} cGy, Parameter A {a_param}"
        elif function_type == "Max EUD":
            max_eud = self.vars["max_eud_value"].get().strip()
            a_param = self.vars["a_param_max_eud"].get().strip()
            return f"Max EUD {max_eud} cGy, Parameter A {a_param}"
        elif function_type == "Target EUD":
            target_eud = self.vars["target_eud_value"].get().strip()
            a_param = self.vars["a_param_target_eud"].get().strip()
            return f"Target EUD {target_eud} cGy, Parameter A {a_param}"
        elif function_type == "Uniform Dose":
            uniform_dose = self.vars["uniform_dose_value"].get().strip()
            return f"Uniform Dose {uniform_dose} cGy"
        elif function_type == "Dose fall-off":
            high_dose = self.vars["high_dose_value"].get().strip()
            low_dose = self.vars["low_dose_value"].get().strip()
            low_distance = self.vars["low_dose_distance"].get().strip()
            return f"Dose fall-off [H] {high_dose} cGy [L] {low_dose} cGy, Low dose distance {low_distance} cm"
        elif function_type == "Uniformity Constraint":
            rel_std_dev = self.vars["rel_std_dev"].get().strip()
            return f"Uniformity Constraint Rel.std.dev {rel_std_dev} %"
        return ""

    def clear_values(self):
        """Clear all input values."""
        for var in self.vars.values():
            var.set("")
