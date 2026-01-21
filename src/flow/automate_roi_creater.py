from raystation import *
import raystation.v2025 as rs
from raystation.v2025 import get_current


class Automate_ROI_Creater:
    """
    Class to automate ROI creation using boolean operations in RayStation.
    Takes automate_roi_data from flow configuration and creates ROIs in order.
    """
    
    def __init__(self, automate_roi_data, matched_roi_dict, case, examination):
        """
        Initialize the Automate_ROI_Creater.
        
        Args:
            automate_roi_data: List of dictionaries with ROI creation configurations
            matched_roi_dict: Dictionary mapping flow ROI names to case ROI names
            case: RayStation case object
            examination: RayStation examination object
        """
        self.automate_roi_data = automate_roi_data
        self.matched_roi_dict = matched_roi_dict
        self.case = case
        self.examination = examination
        
    def create_all_rois(self):
        """
        Main method to create all automated ROIs in order.
        """
        if not self.automate_roi_data:
            print("No automated ROIs to create.")
            return
        
        # Sort by order
        sorted_roi_data = sorted(self.automate_roi_data, key=lambda x: int(x.get("order", 0)))
        
        print(f"\nCreating {len(sorted_roi_data)} automated ROIs...")
        
        for roi_entry in sorted_roi_data:
            order = roi_entry.get("order", "?")
            roi_name = roi_entry.get("roi_name", "")
            boolean_config = roi_entry.get("boolean_config", {})
            
            if not roi_name:
                print(f"  [{order}] Skipping - no ROI name provided")
                continue
            
            try:
                try:
                    existing_roi = self.case.PatientModel.RegionsOfInterest[roi_name]
                except:
                    existing_roi = None
                    
                if existing_roi is not None:
                    print(f"  [{order}] Modifying '{roi_name}'...", end=" ")
                else:
                    print(f"  [{order}] Creating '{roi_name}'...", end=" ")
                self._create_single_roi(roi_name, boolean_config)
                print("✓")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
    
    def _create_single_roi(self, roi_name, boolean_config):
        """
        Create a single ROI with boolean algebra geometry.
        
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
                Color="White",
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
