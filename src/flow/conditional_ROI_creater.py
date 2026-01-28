try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *


class ConditionalROICreator:
    """
    Class to create ROIs conditionally based on check_conditions results.
    Only creates ROIs when their associated condition is met (True).
    Supports two methods: "Boolean operation" and "Convert Dose to ROI".
    """
    
    def __init__(self, condition_rois_data, matched_roi_dict, case, examination, plan):
        """
        Initialize the ConditionalROICreator.
        
        Args:
            condition_rois_data: List of conditional ROI configurations from flow JSON
            matched_roi_dict: Dictionary mapping flow ROI names to case ROI names
            case: RayStation case object
            examination: RayStation examination object
            plan: RayStation plan object (for dose distribution)
        """
        self.condition_rois_data = condition_rois_data
        self.matched_roi_dict = matched_roi_dict
        self.case = case
        self.examination = examination
        self.plan = plan
        
    def create_all_conditional_rois(self, met_condition):
        """
        Main method to create all conditional ROIs in order.
        Only creates ROIs where the associated condition is True.
        
        Args:
            met_condition: Dictionary mapping condition names to True/False
                        Example: {"Heart Dmean1500": True, "r1": False}
        """
        if not self.condition_rois_data:
            print("No conditional ROIs defined.")
            return
        
        # Sort by order
        sorted_roi_data = sorted(self.condition_rois_data, key=lambda x: int(x.get("order", 0)))
        
        print(f"\nProcessing {len(sorted_roi_data)} conditional ROI entries...")
        
        created_count = 0
        skipped_count = 0
        
        for roi_entry in sorted_roi_data:
            order = roi_entry.get("order", "?")
            condition_name = roi_entry.get("condition", "")
            roi_name = roi_entry.get("roi_name", "")
            method = roi_entry.get("method", "")
            
            # Check if condition is met
            condition_met = met_condition[condition_name]
            
            if not condition_met:
                print(f"  [{order}] Skipping '{roi_name}' - Condition '{condition_name}' not met")
                skipped_count += 1
                continue
            
            # Condition is met, create the ROI
            try:
                if method == "Boolean operation":
                    print(f"  [{order}] Creating '{roi_name}' via Boolean operation...", end=" ")
                    boolean_config = roi_entry.get("boolean_config", {})
                    self._create_boolean_roi(roi_name, boolean_config)
                    print("✓")
                    created_count += 1
                    
                elif method == "Convert Dose to ROI":
                    print(f"  [{order}] Creating '{roi_name}' via Dose conversion...", end=" ")
                    convert_dose = roi_entry.get("convert_dose", "")
                    self._create_dose_to_roi(roi_name, convert_dose)
                    print("✓")
                    created_count += 1
                    
                else:
                    print(f"  [{order}] Unknown method '{method}' for '{roi_name}'")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                skipped_count += 1
        
        print(f"\nConditional ROI Creation Summary: {created_count} created, {skipped_count} skipped")
    
    def _create_boolean_roi(self, roi_name, boolean_config):
        """
        Create ROI using boolean algebra geometry (similar to Automate_ROI_Creater).
        
        Args:
            roi_name: Name of the ROI to create
            boolean_config: Dictionary containing roi_a, operation, roi_b, and output settings
        """
        # Extract configuration
        roi_a_config = boolean_config.get("roi_a", {})
        roi_b_config = boolean_config.get("roi_b", {})
        operation = boolean_config.get("operation", "Union")
        output_config = boolean_config.get("output", {})
        
        # Get actual ROI names from matched dictionary
        roi_a_name = roi_a_config.get("name", "")
        roi_b_name = roi_b_config.get("name", "")
        
        # Replace with matched names if available
        if roi_a_name in self.matched_roi_dict:
            roi_a_name = self.matched_roi_dict[roi_a_name]
        if roi_b_name in self.matched_roi_dict:
            roi_b_name = self.matched_roi_dict[roi_b_name]
        
        # Check if ROI already exists
        existing_roi = None
        try:
            existing_roi = self.case.PatientModel.RegionsOfInterest[roi_name]
        except:
            pass
        
        # Create ROI if it doesn't exist
        if existing_roi is None:
            new_roi = self.case.PatientModel.CreateRoi(
                Name=roi_name,
                Color="Yellow",  # Different color for conditional ROIs
                Type="Control",
                TissueName=None,
                RbeCellTypeName=None,
                RoiMaterial=None
            )
        else:
            new_roi = existing_roi
        
        # Build ExpressionA
        expression_a = self._build_expression(roi_a_config, roi_a_name)
        
        # Build ExpressionB
        expression_b = self._build_expression(roi_b_config, roi_b_name)
        
        # Map operation to RayStation format
        result_operation = self._map_operation(operation)
        
        # Build output margin settings
        result_margin_settings = self._build_margin_settings(output_config)
        
        # Create algebra geometry
        new_roi.CreateAlgebraGeometry(
            Examination=self.examination,
            Algorithm="Auto",
            ExpressionA=expression_a,
            ExpressionB=expression_b,
            ResultOperation=result_operation,
            ResultMarginSettings=result_margin_settings
        )
    
    def _create_dose_to_roi(self, roi_name, convert_dose):
        """
        Create ROI from dose threshold using dose distribution.
        PLACEHOLDER: To be implemented with RayStation dose-to-ROI conversion.
        
        Args:
            roi_name: Name of the ROI to create
            convert_dose: Dose threshold in cGy (e.g., "3933" or "1500")
        """
        # Convert dose string to float
        try:
            dose_threshold = float(convert_dose)
        except (ValueError, TypeError):
            print(f"Invalid dose value: {convert_dose}")
            return
        
        # Check if ROI already exists
        existing_roi = None
        try:
            existing_roi = self.case.PatientModel.RegionsOfInterest[roi_name]
        except:
            pass
        
        # Create ROI if it doesn't exist
        if existing_roi is None:
            new_roi = self.case.PatientModel.CreateRoi(
                Name=roi_name,
                Color="Orange",  # Different color for dose-based ROIs
                Type="Control",
                TissueName=None,
                RbeCellTypeName=None,
                RoiMaterial=None
            )
        else:
            new_roi = existing_roi
        
        # Convert dose distribution to ROI
        new_roi.CreateRoiGeometryFromDose(
            DoseDistribution=self.plan.TreatmentCourse.TotalDose,
            ThresholdLevel=dose_threshold
        )
        
    
    def _build_expression(self, roi_config, roi_name):
        """
        Build an expression dictionary for ExpressionA or ExpressionB.
        
        Args:
            roi_config: Configuration for the ROI (contains margin_type and margins)
            roi_name: Name of the ROI (actual case name)
        
        Returns:
            Dictionary formatted for RayStation CreateAlgebraGeometry
        """
        # Get margin settings
        margin_settings = self._build_margin_settings(roi_config)
        
        # Build source roi names list
        source_roi_names = [roi_name] if roi_name else []
        
        return {
            'Operation': "Union",
            'SourceRoiNames': source_roi_names,
            'MarginSettings': margin_settings
        }
    
    def _build_margin_settings(self, config):
        """
        Build margin settings dictionary from configuration.
        
        Args:
            config: Configuration containing margin_type and margins
        
        Returns:
            Dictionary formatted for RayStation margin settings
        """
        margin_type = config.get("margin_type", "Expand")
        margins = config.get("margins", {})
        
        # Convert string values to float
        def to_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        return {
            'Type': margin_type,
            'Superior': to_float(margins.get("Superior", 0)),
            'Inferior': to_float(margins.get("Inferior", 0)),
            'Anterior': to_float(margins.get("Anterior", 0)),
            'Posterior': to_float(margins.get("Posterior", 0)),
            'Right': to_float(margins.get("Right", 0)),
            'Left': to_float(margins.get("Left", 0))
        }
    
    def _map_operation(self, operation):
        """
        Map operation name from flow config to RayStation format.
        
        Args:
            operation: Operation string from config (e.g., "Subtract", "Union", "Intersect")
        
        Returns:
            RayStation operation string (e.g., "Subtraction", "Union", "Intersection")
        """
        operation_map = {
            "Subtract": "Subtraction",
            "Union": "Union",
            "Intersect": "Intersection",
            "Intersection": "Intersection",
            "None": "None"
        }
        
        return operation_map.get(operation, "Union")
