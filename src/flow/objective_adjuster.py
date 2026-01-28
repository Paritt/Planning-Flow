import re
try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *


class ObjectiveAdjuster:
    """
    Class to adjust optimization objectives conditionally based on check_conditions results.
    Only adjusts objectives when their associated condition is met (True).
    Supports two adjustment types: "Add NEW function" and "Adjust OLD Function".
    """
    
    def __init__(self, function_adjustments_data, matched_roi_dict, case, plan):
        """
        Initialize the ObjectiveAdjuster.
        
        Args:
            function_adjustments_data: List of function adjustment configurations from flow JSON
            matched_roi_dict: Dictionary mapping flow ROI names to case ROI names
            case: RayStation case object
            plan: RayStation plan object
        """
        self.function_adjustments_data = function_adjustments_data
        self.matched_roi_dict = matched_roi_dict
        self.case = case
        self.plan = plan
        
        # Get plan optimization
        self.po = self.plan.PlanOptimizations[0]
    
    def adjust_objectives(self, met_condition):
        """
        Main method to adjust all conditional objectives.
        Only adjusts objectives where the associated condition is True.
        
        Args:
            met_condition: Dictionary mapping condition names to True/False
                          Example: {"Heart Dmean1500": True, "r1": False}
        """
        if not self.function_adjustments_data:
            print("No function adjustments defined.")
            return
        
        print(f"\nProcessing {len(self.function_adjustments_data)} function adjustment entries...")
        
        adjusted_count = 0
        skipped_count = 0
        
        for adjustment_entry in self.function_adjustments_data:
            condition_name = adjustment_entry.get("condition", "")
            adjustment_type = adjustment_entry.get("adjustment", "")
            tag = adjustment_entry.get("tag", "")
            func_type = adjustment_entry.get("type", "")
            roi_name = adjustment_entry.get("roi", "")
            description = adjustment_entry.get("description", "")
            weight = adjustment_entry.get("weight", "")
            
            # Check if condition is met
            condition_met = met_condition.get(condition_name, False)
            
            if not condition_met:
                print(f"  Skipping '{tag}' - Condition '{condition_name}' not met")
                skipped_count += 1
                continue
            
            # Condition is met, perform adjustment
            try:
                # Map ROI name to actual case ROI name
                actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
                
                if adjustment_type == "Add NEW function":
                    print(f"  Adding new function '{tag}' ({func_type})...", end=" ")
                    self._add_new_function(tag, func_type, actual_roi_name, description, weight)
                    print("✓")
                    adjusted_count += 1
                    
                elif adjustment_type == "Adjust OLD Function":
                    print(f"  Adjusting existing function '{tag}'...", end=" ")
                    self._adjust_existing_function(tag, func_type, description, weight)
                    print("✓")
                    adjusted_count += 1
                    
                else:
                    print(f"  Unknown adjustment type '{adjustment_type}' for '{tag}'")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                skipped_count += 1
        
        print(f"\nFunction Adjustment Summary: {adjusted_count} adjusted, {skipped_count} skipped")
    
    def _add_new_function(self, tag, func_type, roi_name, description, weight):
        """
        Add a new optimization function based on type and description.
        
        Args:
            tag: Unique identifier for the function
            func_type: Type of function (e.g., "Max Dose", "Min Dose", etc.)
            roi_name: ROI name (already mapped to case name)
            description: Description string containing parameter values
            weight: Weight value for the function
        """
        weight = float(weight)
        
        # Route to appropriate function based on type
        if func_type == "Max Dose":
            self._add_max_dose(tag, roi_name, description, weight)
        elif func_type == "Min Dose":
            self._add_min_dose(tag, roi_name, description, weight)
        elif func_type == "Max EUD":
            self._add_max_eud(tag, roi_name, description, weight)
        elif func_type == "Min EUD":
            self._add_min_eud(tag, roi_name, description, weight)
        elif func_type == "Target EUD":
            self._add_target_eud(tag, roi_name, description, weight)
        elif func_type == "Uniform Dose":
            self._add_uniform_dose(tag, roi_name, description, weight)
        elif func_type == "Dose fall-off":
            self._add_fall_off(tag, roi_name, description, weight)
        elif func_type == "Max DVH":
            self._add_max_dvh(tag, roi_name, description, weight)
        elif func_type == "Min DVH":
            self._add_min_dvh(tag, roi_name, description, weight)
        else:
            raise ValueError(f"Unknown function type: {func_type}")
    
    def _adjust_existing_function(self, tag, func_type, description, weight):
        """
        Adjust an existing optimization function by finding it by tag.
        Updates all parameters based on function type and description.
        
        Args:
            tag: Tag of the existing function to adjust
            func_type: Type of function (e.g., "Max Dose", "Min Dose", etc.)
            description: Description string containing new parameter values
            weight: New weight value for the function
        """
        # Find the function by tag
        target_function = None
        for f in self.po.Objective.ConstituentFunctions:
            if f.Tag == tag:
                target_function = f
                break
        
        if target_function is None:
            raise ValueError(f"Function with tag '{tag}' not found")
        
        weight = float(weight)
        
        # Route to appropriate adjustment based on function type
        if func_type == "MaxDose":
            self._adjust_max_dose(target_function, description, weight)
        elif func_type == "MinDose":
            self._adjust_min_dose(target_function, description, weight)
        elif func_type == "MaxEud":
            self._adjust_max_eud(target_function, description, weight)
        elif func_type == "MinEud":
            self._adjust_min_eud(target_function, description, weight)
        elif func_type == "TargetEud":
            self._adjust_target_eud(target_function, description, weight)
        elif func_type == "UniformDose":
            self._adjust_uniform_dose(target_function, description, weight)
        elif func_type == "DoseFallOff":
            self._adjust_fall_off(target_function, description, weight)
        elif func_type == "MaxDvh":
            self._adjust_max_dvh(target_function, description, weight)
        elif func_type == "MinDvh":
            self._adjust_min_dvh(target_function, description, weight)
        else:
            # Default: just update weight and dose level if available
            target_function.DoseFunctionParameters.Weight = weight
            try:
                dose_level = self._extract_dose(description)
                target_function.DoseFunctionParameters.DoseLevel = dose_level
            except:
                pass
        
    # ========== Helper methods to adjust existing functions ==========
    
    def _adjust_max_dose(self, target_function, description, weight):
        """Adjust Max Dose objective parameters."""
        dose_level = self._extract_dose(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_min_dose(self, target_function, description, weight):
        """Adjust Min Dose objective parameters."""
        dose_level = self._extract_dose(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_max_eud(self, target_function, description, weight):
        """Adjust Max EUD objective parameters."""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.EudParameterA = eud_parameter
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_min_eud(self, target_function, description, weight):
        """Adjust Min EUD objective parameters."""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.EudParameterA = eud_parameter
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_target_eud(self, target_function, description, weight):
        """Adjust Target EUD objective parameters."""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.EudParameterA = eud_parameter
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_uniform_dose(self, target_function, description, weight):
        """Adjust Uniform Dose objective parameters."""
        dose_level = self._extract_dose(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_fall_off(self, target_function, description, weight):
        """Adjust Dose Fall-off objective parameters."""
        high_dose = self._extract_high_dose(description)
        low_dose = self._extract_low_dose(description)
        distance = self._extract_distance(description)
        target_function.DoseFunctionParameters.HighDoseLevel = high_dose
        target_function.DoseFunctionParameters.LowDoseLevel = low_dose
        target_function.DoseFunctionParameters.LowDoseDistance = distance
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_max_dvh(self, target_function, description, weight):
        """Adjust Max DVH objective parameters."""
        dose_level = self._extract_dose(description)
        is_absolute_volume = self._extract_is_absolute_volume(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        if is_absolute_volume:
            absolute_volume = self._extract_absolute_volume(description)
            target_function.DoseFunctionParameters.Volume = absolute_volume
        else:
            percent_volume = self._extract_percent_volume(description)
            target_function.DoseFunctionParameters.PercentVolume = percent_volume
        target_function.DoseFunctionParameters.Weight = weight
    
    def _adjust_min_dvh(self, target_function, description, weight):
        """Adjust Min DVH objective parameters."""
        dose_level = self._extract_dose(description)
        is_absolute_volume = self._extract_is_absolute_volume(description)
        target_function.DoseFunctionParameters.DoseLevel = dose_level
        if is_absolute_volume:
            absolute_volume = self._extract_absolute_volume(description)
            target_function.DoseFunctionParameters.Volume = absolute_volume
        else:
            percent_volume = self._extract_percent_volume(description)
            target_function.DoseFunctionParameters.PercentVolume = percent_volume
        target_function.DoseFunctionParameters.Weight = weight
    
    
    
    # ========== Helper methods to add new functions ==========
    
    def _add_max_dose(self, tag, roi_name, description, weight):
        """Add Max Dose objective. Description: 'Max Dose 5000 cGy'"""
        dose_level = self._extract_dose(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MaxDose", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_min_dose(self, tag, roi_name, description, weight):
        """Add Min Dose objective. Description: 'Min Dose 3933 cGy'"""
        dose_level = self._extract_dose(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MinDose", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_max_eud(self, tag, roi_name, description, weight):
        """Add Max EUD objective. Description: 'Max EUD 2500 cGy, Parameter A 1'"""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MaxEud", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.EudParameterA = eud_parameter
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_min_eud(self, tag, roi_name, description, weight):
        """Add Min EUD objective. Description: 'Min EUD 2500 cGy, Parameter A 1'"""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MinEud", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.EudParameterA = eud_parameter
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_target_eud(self, tag, roi_name, description, weight):
        """Add Target EUD objective. Description: 'Target EUD 2500 cGy, Parameter A 1'"""
        dose_level = self._extract_dose(description)
        eud_parameter = self._extract_parameter_a(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="TargetEud", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.EudParameterA = eud_parameter
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_uniform_dose(self, tag, roi_name, description, weight):
        """Add Uniform Dose objective. Description: 'Uniform Dose 4140 cGy'"""
        dose_level = self._extract_dose(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="UniformDose", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_fall_off(self, tag, roi_name, description, weight):
        """
        Add Dose Fall-off objective.
        Description: 'Dose fall-off [H] 4140 cGy [L] 2070 cGy, Low dose distance 1.5 cm'
        """
        high_dose = self._extract_high_dose(description)
        low_dose = self._extract_low_dose(description)
        distance = self._extract_distance(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="DoseFallOff", RoiName=roi_name)
        o.DoseFunctionParameters.HighDoseLevel = high_dose
        o.DoseFunctionParameters.LowDoseLevel = low_dose
        o.DoseFunctionParameters.LowDoseDistance = distance
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_max_dvh(self, tag, roi_name, description, weight):
        """
        Add Max DVH objective.
        Description: 'Max DVH 500 cGy to 70% volume' or 'Max DVH 500 cGy to 0.1cc volume'
        """
        dose_level = self._extract_dose(description)
        is_absolute_volume = self._extract_is_absolute_volume(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MaxDvh", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        if is_absolute_volume:
            absolute_volume = self._extract_absolute_volume(description)
            o.DoseFunctionParameters.Volume = absolute_volume
        else:
            percent_volume = self._extract_percent_volume(description)
            o.DoseFunctionParameters.PercentVolume = percent_volume
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    def _add_min_dvh(self, tag, roi_name, description, weight):
        """
        Add Min DVH objective.
        Description: 'Min DVH 500 cGy to 70% volume' or 'Min DVH 500 cGy to 0.1cc volume'
        """
        dose_level = self._extract_dose(description)
        is_absolute_volume = self._extract_is_absolute_volume(description)
        
        o = self.po.AddOptimizationFunction(FunctionType="MinDvh", RoiName=roi_name)
        o.DoseFunctionParameters.DoseLevel = dose_level
        if is_absolute_volume:
            absolute_volume = self._extract_absolute_volume(description)
            o.DoseFunctionParameters.Volume = absolute_volume
        else:
            percent_volume = self._extract_percent_volume(description)
            o.DoseFunctionParameters.PercentVolume = percent_volume
        o.DoseFunctionParameters.Weight = weight
        o.Tag = tag
    
    # ========== Helper methods to extract values from descriptions ==========
    
    def _extract_dose(self, description):
        """Extract dose value from description (e.g., '5000 cGy' -> 5000)"""
        match = re.search(r'(\d+\.?\d*)\s*cGy', description)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract dose from: {description}")
    
    def _extract_parameter_a(self, description):
        """Extract Parameter A from description (e.g., 'Parameter A 1' -> 1)"""
        match = re.search(r'Parameter A\s+(\d+\.?\d*)', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract Parameter A from: {description}")
    
    def _extract_high_dose(self, description):
        """Extract high dose from fall-off description (e.g., '[H] 4140 cGy' -> 4140)"""
        match = re.search(r'\[H\]\s*(\d+\.?\d*)\s*cGy', description)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract high dose from: {description}")
    
    def _extract_low_dose(self, description):
        """Extract low dose from fall-off description (e.g., '[L] 2070 cGy' -> 2070)"""
        match = re.search(r'\[L\]\s*(\d+\.?\d*)\s*cGy', description)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract low dose from: {description}")
    
    def _extract_distance(self, description):
        """Extract distance from fall-off description (e.g., 'Low dose distance 1.5 cm' -> 1.5)"""
        match = re.search(r'Low dose distance\s+(\d+\.?\d*)\s*cm', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract distance from: {description}")
    
    def _extract_percent_volume(self, description):
        """Extract percent volume from DVH description (e.g., 'to 70% volume' -> 70)"""
        match = re.search(r'to\s+(\d+\.?\d*)\s*%', description)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract percent volume from: {description}")
    
    def _extract_is_absolute_volume(self, description):
        """Check if volume is absolute (cc) or relative (%)"""
        return 'cc' in description.lower() and '%' not in description
    
    def _extract_absolute_volume(self, description):
        """Extract absolute volume from DVH description (e.g., 'to 0.1cc volume' -> 0.1)"""
        match = re.search(r'to\s+(\d+\.?\d*)\s*cc', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract absolute volume from: {description}")
