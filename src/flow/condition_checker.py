import re
from tkinter import messagebox


class ConditionChecker:
    """
    Evaluates conditions from check_conditions data and returns which conditions are met.
    Used to determine if conditional ROIs and function adjustments should be applied.
    """
    
    def __init__(self, check_conditions_data, matched_roi_dict, case, plan_name):
        """
        Initialize the condition checker.
        
        Args:
            check_conditions_data: List of condition dictionaries from flow JSON
            matched_roi_dict: Dictionary mapping flow ROI names to case ROI names
            case: RayStation case object
            plan_name: Name of the plan to check conditions against
        """
        self.check_conditions_data = check_conditions_data
        self.matched_roi_dict = matched_roi_dict
        self.case = case
        self.plan_name = plan_name
        self.plan = None
        self.dose = None
        self.optimization_round = 0  # Track current optimization round
        
        # Get plan and dose distribution
        try:
            self.plan = self.case.TreatmentPlans[plan_name]
            # Use TotalDose instead of FractionDose
            self.dose = self.plan.TreatmentCourse.TotalDose
        except Exception as e:
            print(f"Warning: Could not access plan or dose: {str(e)}")
    
    def check_all_conditions(self):
        """
        Evaluate all conditions and return a dictionary of results.
        
        Returns:
            Dictionary mapping condition names to True/False
            Example: {"Heart Dmean1500": True, "Lung V20": False}
        """
        results = {}
        
        for condition in self.check_conditions_data:
            condition_name = condition.get("name", "")
            condition_type = condition.get("type", "")
            roi_name = condition.get("roi", "")
            criteria = condition.get("criteria", "")
            active_round_symbol = condition.get("active_round", "≥ 0").split()[0]
            active_round = condition.get("active_round", "≥ 0").split()[1]
            
            # Check if condition is active in current optimization round
            round_met = False
            if active_round_symbol == "≥":
                round_met = self.optimization_round >= int(active_round)
            elif active_round_symbol == ">":
                round_met = self.optimization_round > int(active_round)
            elif active_round_symbol == "=":
                round_met = self.optimization_round == int(active_round)
            elif active_round_symbol == "<":
                round_met = self.optimization_round < int(active_round)
            elif active_round_symbol == "≤":
                round_met = self.optimization_round <= int(active_round)
            else:
                print(f"Warning: Unknown active round symbol '{active_round_symbol}' for condition '{condition_name}'")
                round_met = False
                
            if not round_met:
                results[condition_name] = False
                # print(f"  ⏩ Condition NOT evaluated (inactive round): {condition_name}")
                continue
            else:
                print(f"  ▶️ Evaluating condition: {condition_name}")
                try:
                    # Evaluate based on condition type
                    if condition_type == "Alway TRUE":
                        results[condition_name], value = (True, self.optimization_round)
                    elif condition_type == "Max Dose":
                        results[condition_name], value = self._check_max_dose(roi_name, criteria)
                    elif condition_type == "Min Dose":
                        results[condition_name], value = self._check_min_dose(roi_name, criteria)
                    elif condition_type == "Max Dmean" or condition_type == "Min Dmean":
                        results[condition_name], value = self._check_dmean(roi_name, criteria)
                    elif condition_type == "Max DaV" or condition_type == "Min DaV":
                        results[condition_name], value = self._check_dav(roi_name, criteria)
                    elif condition_type == "Min VaD" or condition_type == "Max VaD":
                        results[condition_name], value = self._check_vad(roi_name, criteria)
                    else:
                        print(f"Warning: Unknown condition type '{condition_type}' for condition '{condition_name}'")
                        results[condition_name] = False
                        continue
                    
                    # Print result for all condition types
                    if results[condition_name]:
                        print(f"    ✅ Condition MET: {condition_name} - Value: {value:.2f} ({criteria})")
                    else:
                        print(f"    ❌ Condition NOT met: {condition_name} - Value: {value:.2f} ({criteria})")
                        
                except Exception as e:
                    print(f"  ⚠️ Error evaluating condition '{condition_name}': {str(e)}")
                    results[condition_name] = False
        
        return results
    
    def set_optimization_round(self, round_number):
        """Set the current optimization round number."""
        self.optimization_round = round_number
    
    def _check_max_dose(self, roi_name, criteria):
        """
        Check if max dose to ROI meets criteria.
        Criteria format: "Max Dose (cGy) ≥ 5000" or "Max Dose (cGy) ≤ 5000"
        Returns: (bool, float) - (condition_met, max_dose_value)
        """
        if not self.dose:
            print(f"Cannot check Max Dose for {roi_name}: No dose distribution available")
            return (False, 0.0)
        
        try:
            # Get actual ROI name from matched dictionary
            actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
            
            # Extract threshold and operator from criteria
            match = re.search(r'([≥≤><=]+)\s*(\d+\.?\d*)', criteria)
            if not match:
                print(f"Could not parse Max Dose criteria: {criteria}")
                return (False, 0.0)
            
            operator = match.group(1)
            threshold = float(match.group(2))
            
            # Get max dose from RayStation
            max_dose_value = self.dose.GetDoseStatistic(RoiName=actual_roi_name, DoseType='Max')
            
            # Compare based on operator
            if '≥' in  operator:
                return (max_dose_value >= threshold, max_dose_value)
            elif '≤' in operator:
                return (max_dose_value <= threshold, max_dose_value)
            else:
                return (False, max_dose_value)
                
        except Exception as e:
            print(f"Error checking Max Dose for {roi_name}: {str(e)}")
            return (False, 0.0)
    
    def _check_min_dose(self, roi_name, criteria):
        """
        Check if min dose to ROI meets criteria.
        Returns: (bool, float) - (condition_met, min_dose_value)
        """
        if not self.dose:
            print(f"Cannot check Min Dose for {roi_name}: No dose distribution available")
            return (False, 0.0)
        
        try:
            # Get actual ROI name from matched dictionary
            actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
            
            # Extract threshold and operator from criteria
            match = re.search(r'([≥≤><=]+)\s*(\d+\.?\d*)', criteria)
            if not match:
                print(f"Could not parse Min Dose criteria: {criteria}")
                return (False, 0.0)
            
            operator = match.group(1)
            threshold = float(match.group(2))
            
            # Get min dose from RayStation
            # PLACEHOLDER: Need to verify exact RayStation API
            min_dose_value = self.dose.GetDoseStatistic(RoiName=actual_roi_name, DoseType='Min')
            # Compare based on operator
            if '≥' in operator:
                return (min_dose_value >= threshold, min_dose_value)
            elif '≤' in operator:
                return (min_dose_value <= threshold, min_dose_value)
            else:
                return (False, min_dose_value)
                
        except Exception as e:
            print(f"Error checking Min Dose for {roi_name}: {str(e)}")
            return (False, 0.0)
    
    def _check_dmean(self, roi_name, criteria):
        """
        Check if mean dose to ROI meets criteria.
        Returns: (bool, float) - (condition_met, mean_dose_value)
        """
        if not self.dose:
            print(f"Cannot check Dmean for {roi_name}: No dose distribution available")
            return (False, 0.0)
        
        try:
            # Get actual ROI name from matched dictionary
            actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
            
            # Extract threshold and operator from criteria
            match = re.search(r'([≥≤><=]+)\s*(\d+\.?\d*)', criteria)
            if not match:
                print(f"Could not parse Dmean criteria: {criteria}")
                return (False, 0.0)
            
            operator = match.group(1)
            threshold = float(match.group(2))
            
            # Get mean dose from RayStation
            mean_dose_value = self.dose.GetDoseStatistic(RoiName=actual_roi_name, DoseType='Average')
            
            # Compare based on operator
            if '≥' in operator:
                return (mean_dose_value >= threshold, mean_dose_value)
            elif '≤' in operator:
                return (mean_dose_value <= threshold, mean_dose_value)
            else:
                return (False, mean_dose_value)
                
        except Exception as e:
            print(f"Error checking Dmean for {roi_name}: {str(e)}")
            return (False, 0.0)
    
    def _check_dav(self, roi_name, criteria):
        """
        Check if dose at volume (DaV) meets criteria.
        Criteria format: "D95% ≥ 3900 cGy" or "D10cc ≤ 2000 cGy"
        Returns: (bool, float) - (condition_met, actual_dose_at_volume)
        """
        if not self.dose:
            print(f"Cannot check DaV for {roi_name}: No dose distribution available")
            return (False, 0.0)
        
        try:
            # Get actual ROI name from matched dictionary
            actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
            
            # Extract volume, unit, operator, and dose from criteria
            # Format: "D{volume}{unit} {operator} {dose} cGy"
            # Example: "D95% ≥ 3900 cGy" or "D10cc ≤ 2000 cGy"
            pattern = r'D\s*(\d+\.?\d*)\s*(cc|%)\s*([≥≤><=]+)\s*(\d+\.?\d*)\s*cGy'
            match = re.search(pattern, criteria, re.IGNORECASE)
            
            if not match:
                print(f"Could not parse DaV criteria: {criteria}")
                return (False, 0.0)
            
            volume_value = float(match.group(1))
            volume_unit = match.group(2)
            operator = match.group(3)
            dose_threshold = float(match.group(4))
            
            # Get dose at specified volume from RayStation DVH
            if volume_unit == '%':
                # Relative volume (percentage)
                relative_volume = volume_value / 100.0
                dose_at_volume_array = self.dose.GetDoseAtRelativeVolumes(
                    RoiName=actual_roi_name, 
                    RelativeVolumes=[relative_volume]
                )
                actual_dose = dose_at_volume_array[0]
            else:
                # Absolute volume (cc) - need to convert to relative
                roi_geometry = self.case.PatientModel.StructureSets[0].RoiGeometries[actual_roi_name]
                total_volume = roi_geometry.GetRoiVolume()
                if total_volume > 0:
                    relative_volume = volume_value / total_volume
                    dose_at_volume_array = self.dose.GetDoseAtRelativeVolumes(
                        RoiName=actual_roi_name, 
                        RelativeVolumes=[relative_volume]
                    )
                    actual_dose = dose_at_volume_array[0]
                else:
                    print(f"Warning: ROI {actual_roi_name} has zero volume")
                    return (False, 0.0)
            
            # Compare based on operator
            if '≥' in operator:
                return (actual_dose >= dose_threshold, actual_dose)
            elif '≤' in operator:
                return (actual_dose <= dose_threshold, actual_dose)
            else:
                return (False, actual_dose)
        except Exception as e:
            print(f"Error checking DaV for {roi_name}: {str(e)}")
            return (False, 0.0)
    
    def _check_vad(self, roi_name, criteria):
        """
        Check if volume at dose (VaD) meets criteria.
        Criteria format: "V3900cGy ≥ 95%" or "V3900cGy ≥ 10cc" or "V2000cGy ≤ 20cc" or "V2000cGy ≤ 50%"
        Returns: (bool, float) - (condition_met, actual_volume_at_dose)
        """
        if not self.dose:
            print(f"Cannot check VaD for {roi_name}: No dose distribution available")
            return (False, 0.0)
        
        try:
            # Get actual ROI name from matched dictionary
            actual_roi_name = self.matched_roi_dict.get(roi_name, roi_name)
            
            # Extract dose, operator, volume threshold, and unit from criteria
            # Format: "V{dose}cGy {operator} {volume}{unit}"
            # Example: "V3900cGy ≥ 95%" or "V3900cGy ≥ 10cc" or "V2000cGy ≤ 20cc" or "V2000cGy ≤ 50%"
            pattern = r'V\s*(\d+\.?\d*)\s*cGy\s*([≥≤><=]+)\s*(\d+\.?\d*)\s*(cc|%)'
            match = re.search(pattern, criteria, re.IGNORECASE)
            
            if not match:
                print(f"Could not parse VaD criteria: {criteria}")
                return (False, 0.0)
            
            dose_level = float(match.group(1))
            operator = match.group(2)
            volume_threshold = float(match.group(3))
            volume_unit = match.group(4)
            
            # Get volume receiving specified dose from RayStation DVH
            relative_volume_array = self.dose.GetRelativeVolumeAtDoseValues(
                RoiName=actual_roi_name, 
                DoseValues=[dose_level]
            )
            relative_volume = relative_volume_array[0]
            
            if volume_unit == '%':
                # Return as percentage
                actual_volume = relative_volume * 100.0
            else:
                # Convert to absolute volume (cc)
                roi_geometry = self.case.PatientModel.StructureSets[0].RoiGeometries[actual_roi_name]
                total_volume = roi_geometry.GetRoiVolume()
                actual_volume = relative_volume * total_volume
            
            # Compare based on operator
            if '≥' in operator:
                return (actual_volume >= volume_threshold, actual_volume)
            elif '≤' in operator:
                return (actual_volume <= volume_threshold, actual_volume)
            else:
                return (False, actual_volume)
                
        except Exception as e:
            print(f"Error checking VaD for {roi_name}: {str(e)}")
            return (False, 0.0)