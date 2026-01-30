try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *
import re


class ObjectiveAdder:
    """
    Class to add optimization objectives/functions to a RayStation plan.
    Parses initial_functions data and adds them to the plan optimization.
    """
    
    def __init__(self, initial_functions_data, case, plan_name, matched_roi_dict, robust_settings):
        """
        Initialize the ObjectiveAdder.
        
        Args:
            initial_functions_data: List of function dictionaries from flow config
            case: RayStation case object
            plan_name: Name of the plan to add objectives to
            matched_roi_dict: Dictionary mapping flow ROI names to case ROI names
            robust_settings: Dictionary of robustness settings
        """
        self.initial_functions_data = initial_functions_data
        self.case = case
        self.plan_name = plan_name
        self.matched_roi_dict = matched_roi_dict
        self.robust_settings = robust_settings
        
        # Get plan and plan optimization
        self.plan = self.case.TreatmentPlans[plan_name]
        self.po = self.plan.PlanOptimizations[0]
    
    def add_initial_objectives(self):
        """
        Main method to add all initial objectives to the plan.
        """
        if not self.initial_functions_data:
            print("No initial objectives to add.")
            return
        
        print(f"\nAdding {len(self.initial_functions_data)} objectives...")
        
        for func_entry in self.initial_functions_data:
            tag = func_entry.get("tag", "")
            func_type = func_entry.get("type", "")
            roi_name = func_entry.get("roi", "")
            description = func_entry.get("description", "")
            weight = func_entry.get("weight", "1")
            
            # Map ROI name if it's in matched dictionary
            if roi_name in self.matched_roi_dict:
                roi_name = self.matched_roi_dict[roi_name]
            
            try:
                print(f"  Adding '{tag}' ({func_type})...", end=" ")
                self._add_single_function(tag, func_type, roi_name, description, weight)
                print("✓")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                
        if have_robustness := getattr(self.plan, 'RobustSettings', None):
            print("Configuring robustness settings...", end=" ")
            self._set_robustness()
            print("✓")
    
    def _set_robustness(self):
        """
        Placeholder for adding robustness settings if needed.
        Currently not implemented.
        """
        self.po.OptimizationParameters.SaveRobustnessParameters(PositionUncertaintyAnterior=self.robust_settings.get('anterior', 0.0),
                                                                        PositionUncertaintyPosterior=self.robust_settings.get('posterior', 0.0),
                                                                        PositionUncertaintySuperior=self.robust_settings.get('superior', 0.0),
                                                                        PositionUncertaintyInferior=self.robust_settings.get('inferior', 0.0),
                                                                        PositionUncertaintyLeft=self.robust_settings.get('left', 0.0), 
                                                                        PositionUncertaintyRight=self.robust_settings.get('right', 0.0), 
                                                                        DensityUncertainty=self.robust_settings.get('density', 0.0)/100, 
                                                                        UseReducedSetOfDensityShifts=False, 
                                                                        PositionUncertaintySetting="Universal", IndependentLeftRight=True, 
                                                                        IndependentAnteriorPosterior=True, IndependentSuperiorInferior=True, 
                                                                        ComputeExactScenarioDoses=False, NamesOfNonPlanningExaminations=[], 
                                                                        PatientGeometryUncertaintyType="PerTreatmentCourse", 
                                                                        PositionUncertaintyType="PerTreatmentCourse", 
                                                                        TreatmentCourseScenariosFactor=1000, 
                                                                        PositionUncertaintyList=None, 
                                                                        PositionUncertaintyFormation="Automatic", 
                                                                        RobustMethodPerTreatmentCourse="WeightedPowerMean" if self.robust_settings.get('method', '') == 'Composite worst cases (minimax)' else "VoxelwiseWorstCase")
        self.Patient.Save()
    
    def _check_robust_function(self):
        """
        Check if there is robust function.
        
        Args:
            func_type: Type of function (string)
        Returns:
            bool: True if robustness function, False otherwise
        """
        pass
    
    def _add_single_function(self, tag, func_type, roi_name, description, weight):
        """
        Add a single optimization function based on type and description.
        
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
            o.DoseFunctionParameters.IsAbsoluteVolume = True
            o.DoseFunctionParameters.AbsoluteVolume = absolute_volume
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
            o.DoseFunctionParameters.IsAbsoluteVolume = True
            o.DoseFunctionParameters.AbsoluteVolume = absolute_volume
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
        match = re.search(r'to\s+(\d+\.?\d*)%\s*volume', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract percent volume from: {description}")
    
    def _extract_is_absolute_volume(self, description):
        """Detect if description uses absolute volume (cc) or percent volume (%)"""
        return 'cc' in description.lower()
    
    def _extract_absolute_volume(self, description):
        """Extract absolute volume from DVH description (e.g., 'to 0.1cc volume' -> 0.1)"""
        match = re.search(r'to\s+(\d+\.?\d*)\s*cc\s*volume', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract absolute volume from: {description}")
