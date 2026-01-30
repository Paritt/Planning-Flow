from tkinter import messagebox
try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *


class PlanCreater:
    """Create a plan and add beams based on loaded flow data."""
    
    def __init__(self, loaded_flow_data, case, examination, matched_roi_dict):
        """
        Initialize PlanCreater with flow data and case.
        
        Args:
            loaded_flow_data: Dictionary containing all workflow configuration
            case: RayStation case object
            examination_name: Name of the RayStation examination
        """
        self.flow_data = loaded_flow_data
        self.case = case
        self.patient = get_current('Patient')
        self.plan = None
        self.beam_set = None
        self.examination = examination
        self.structure_set = None
        self.iso_data = None
        self.matched_roi_dict = matched_roi_dict
        
        # Extract data from flow
        self.plan_name = loaded_flow_data.get("plan_name")
        self.machine = loaded_flow_data.get("machine")
        self.technique = loaded_flow_data.get("technique_data", "VMAT")
        self.vmat_beam_data = loaded_flow_data.get("vmat_beam_data", [])
        self.impt_beam_data = loaded_flow_data.get("impt_beam_data", [])
        self.isocenter_data = loaded_flow_data.get("isocenter_data", {})
        self.prescription_data = loaded_flow_data.get("prescription_data", {})
        
    def validate_prerequisites(self):
        """Check if examination and structure set are available."""
        try:
            # Get current examination
            if not self.examination:
                messagebox.showerror("No Examination", "Please open an examination before creating a plan.")
                return False
            
            examination_name = self.examination.Name
            print(f"Using examination: {examination_name}")
        except:
            messagebox.showerror("No Examination", "Please open an examination before creating a plan.")
            return False
        
        try:
            # Get structure set for the examination
            examination_name = self.examination.Name
            self.structure_set = self.case.PatientModel.StructureSets[examination_name]
            if not self.structure_set:
                messagebox.showerror("No Structure Set", f"No structure set found for examination '{examination_name}'.")
                return False
            print(f"Using structure set for: {examination_name}\n")
        except:
            messagebox.showerror("No Structure Set", f"Please create a structure set for the current examination.")
            return False
        
        return True
    
    def create_plan(self):
        """Create a new plan in the current case."""
        if not self.validate_prerequisites():
            return False
        
        try:
            print("Creating Plan...")
            examination_name = self.examination.Name
            
            # Create new plan
            self.plan = self.case.AddNewPlan(
                PlanName=self.plan_name,
                ExaminationName=examination_name
            )
            
            print(f"Plan '{self.plan_name}' created successfully")
            return True
            
        except Exception as e:
            messagebox.showerror("Plan Creation Error", f"Failed to create plan:\n{str(e)}")
            return False
    
    def create_beam_set(self):
        """Create a beam set with the specified technique."""
        try:
            print("Creating Beam Set...")
            
            examination_name = self.examination.Name
            num_fractions = int(self.prescription_data.get("num_fractions", 1))
            
            # Determine modality and treatment technique
            if self.technique == "VMAT":
                modality = "Photons"
                treatment_technique = "VMAT"
            elif self.technique == "IMPT":
                modality = "Protons"
                treatment_technique = "ProtonPencilBeamScanning"
            else:
                modality = "Photons"
                treatment_technique = "VMAT"
            
            # Create beam set
            self.beam_set = self.plan.AddNewBeamSet(
                Name=self.plan_name,
                ExaminationName=examination_name,
                MachineName=self.machine,
                Modality=modality,
                PatientPosition='HeadFirstSupine',
                TreatmentTechnique=treatment_technique,
                NumberOfFractions=num_fractions,
                CreateSetupBeams=True,
                UseLocalizationPointAsSetupIsocenter=False,
                UseUserSelectedIsocenterSetupIsocenter=False
            )
            
            self.patient.Save()
            self.plan.SetCurrent()
            self.beam_set.SetCurrent()
            
            print(f"Beam set created with {num_fractions} fractions")
            return True
            
        except Exception as e:
            messagebox.showerror("Beam Set Creation Error", f"Failed to create beam set:\n{str(e)}")
            return False
    
    def add_prescription(self):
        """Add prescription to the beam set."""
        try:
            print("Adding prescription...")
            
            primary_dose = self.prescription_data.get("primary_dose")
            prescription_roi = self.prescription_data.get("prescription_roi")
            prescription_roi = self.matched_roi_dict.get(prescription_roi, prescription_roi)
            
            if not primary_dose or not prescription_roi:
                print("No prescription data specified, skipping prescription")
                return True
            
            # Convert to float and ensure it's in cGy
            total_dose = float(primary_dose)
            
            # Add ROI prescription dose reference
            self.beam_set.AddRoiPrescriptionDoseReference(
                RoiName=prescription_roi,
                PrescriptionType="DoseAtVolume",
                DoseValue=total_dose,
                DoseVolume=95,
                RelativePrescriptionLevel=1
            )
            
            # Set default dose grid
            self.beam_set.SetDefaultDoseGrid(VoxelSize={'x': 0.2, 'y': 0.2, 'z': 0.2})
            
            print(f"Prescription added: {total_dose} cGy to {prescription_roi}")
            return True
            
        except Exception as e:
            messagebox.showerror("Prescription Error", f"Failed to add prescription:\n{str(e)}")
            return False
    
    def set_isocenter(self):
        """Set isocenter position based on flow data."""
        try:
            print("Setting isocenter...")
            
            method = self.isocenter_data.get("method", "Center of ROI")
            
            if method == "Center of ROI":
                roi_name = self.isocenter_data.get("roi_name")
                roi_name = self.matched_roi_dict.get(roi_name, roi_name)
                if not roi_name:
                    print("No ROI specified for isocenter, skipping")
                    return True
                
                # Get ROI center as isocenter
                examination_name = self.examination.Name
                roi_geometries = self.structure_set.RoiGeometries[roi_name]
                center = roi_geometries.GetCenterOfRoi()
                isocenter_position = {'x': center.x, 'y': center.y, 'z': center.z}
                print(f"Isocenter from ROI '{roi_name}' center")
                
            elif method == "POI":
                poi_name = self.isocenter_data.get("poi_name")
                if not poi_name:
                    print("No POI specified for isocenter, skipping")
                    return True
                
                # Get POI position as isocenter
                poi_geometry = self.structure_set.PoiGeometries[poi_name]
                point = poi_geometry.Point
                isocenter_position = {'x': point.x, 'y': point.y, 'z': point.z}
                print(f"Isocenter from POI '{poi_name}'")
            else:
                print(f"Unknown isocenter method: {method}, skipping")
                return True
            
            # Create isocenter data
            self.iso_data = self.beam_set.CreateDefaultIsocenterData(Position=isocenter_position)
            
            self.patient.Save()
            self.plan.SetCurrent()
            self.beam_set.SetCurrent()
            
            print(f"Isocenter set at position: {isocenter_position}")
            return True
            
        except Exception as e:
            messagebox.showerror("Isocenter Error", f"Failed to set isocenter:\n{str(e)}")
            return False
    
    def add_vmat_beams(self):
        """Add VMAT beams based on flow data."""
        try:
            print("Adding VMAT beams...")
            
            if not self.vmat_beam_data:
                print("No VMAT beam data found")
                return True
            
            if not self.iso_data:
                messagebox.showerror("Isocenter Error", "Isocenter must be set before adding beams")
                return False
            
            for idx, beam_config in enumerate(self.vmat_beam_data):
                beam_name = beam_config.get("beam_name", f"Beam_{idx+1}")
                energy = beam_config.get("energy", "10")
                gantry_start = float(beam_config.get("gantry_start", 181))
                gantry_stop = float(beam_config.get("gantry_stop", 179))
                rotation = beam_config.get("rotation", "CW")
                collimator = float(beam_config.get("collimator", 0))
                couch = float(beam_config.get("couch", 0))
                
                # Determine rotation direction
                if rotation.upper() == "CW":
                    arc_rotation = "Clockwise"
                elif rotation.upper() == "CCW":
                    arc_rotation = "CounterClockwise"
                else:
                    arc_rotation = "Clockwise"
                
                # Create arc beam
                self.beam_set.CreateArcBeam(
                    ArcStopGantryAngle=gantry_stop,
                    ArcRotationDirection=arc_rotation,
                    BeamQualityId=energy,
                    IsocenterData=self.iso_data,
                    Name=beam_name,
                    Description=f'{idx + 1}_{rotation.upper()}_{gantry_start}-{gantry_stop}',
                    GantryAngle=gantry_start,
                    CouchRotationAngle=couch,
                    CouchPitchAngle=0,
                    CouchRollAngle=0,
                    CollimatorAngle=collimator
                )
                
                # Edit arc optimization settings
                self.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[idx].ArcConversionPropertiesPerBeam.EditArcBasedBeamOptimizationSettings(
                    CreateDualArcs=False,
                    FinalGantrySpacing=2,
                    MaxArcDeliveryTime=40,
                    BurstGantrySpacing=None,
                    MaxArcMU=None
                )
                
                print(f"Added beam {idx + 1}: {beam_name}")
            
            # Edit setup beam names
            self.edit_setup_beams()
            
            self.patient.Save()
            print("All VMAT beams added successfully")
            return True
            
        except Exception as e:
            messagebox.showerror("Beam Addition Error", f"Failed to add VMAT beams:\n{str(e)}")
            return False
    
    def add_impt_beams(self):
        """Add IMPT beams based on flow data."""
        try:
            print("Adding IMPT beams...")
            
            if not self.impt_beam_data:
                print("No IMPT beam data found")
                return True
            
            if not self.iso_data:
                messagebox.showerror("Isocenter Error", "Isocenter must be set before adding beams")
                return False
            
            for idx, beam_config in enumerate(self.impt_beam_data):
                beam_name = beam_config.get("beam_name", f"Beam_{idx+1}")
                gantry = float(beam_config.get("gantry", 0))
                couch = float(beam_config.get("couch", 0))
                snout = beam_config.get("snout", "NONE")
                range_shifter = beam_config.get("range_shifter", "(None)")
                
                # Convert range_shifter to None if "(None)" or empty
                if range_shifter == "(None)" or not range_shifter:
                    range_shifter = None
                
                # Get computational settings
                comp_settings = beam_config.get("comp_settings", {})
                
                # Create PBS Ion beam
                self.beam_set.CreatePBSIonBeam(
                    ArcRotationDirection="None",
                    ArcStopGantryAngle=None,
                    SnoutId=snout,
                    RangeShifter=range_shifter,
                    MinimumAirGap=None,
                    MetersetRateSetting="",
                    IsocenterData=self.iso_data,
                    Name=beam_name,
                    Description=f'{int(gantry)}',
                    GantryAngle=gantry,
                    CouchRotationAngle=couch,
                    CouchPitchAngle=0,
                    CouchRollAngle=0,
                    CollimatorAngle=0
                )
                
                print(f"Created IMPT beam {idx + 1}: {beam_name}")
                
                # Configure beam optimization settings if comp_settings exist
                if comp_settings:
                    beam_settings = self.plan.PlanOptimizations[0].OptimizationParameters.TreatmentSetupSettings[0].BeamSettings[idx]
                    
                    # Set range shifter selection (Automatic or Manual)
                    range_shifter_selection = comp_settings.get('range_shifter_selection', 'Automatic')
                    beam_settings.AutoSelectRangeShifter = (range_shifter_selection == 'Automatic')
                    
                    # Set optimization types
                    beam_settings.OptimizationTypes = ["SpotWeights"]
                    
                    # Configure spot pattern properties
                    scanned_props = beam_settings.ScannedBeamProperties
                    
                    # Energy layer spacing
                    energy_spacing_scale = float(comp_settings.get('energy_layer_spacing_scale', 1.0))
                    scanned_props.EnergyLayerSeparationFactor = energy_spacing_scale
                    
                    # Spot spacing
                    spot_spacing_scale = float(comp_settings.get('spot_spacing_scale', 1.0))
                    scanned_props.SpotSpacingSeparationFactor = spot_spacing_scale
                    
                    # Scan direction angle
                    angle = float(comp_settings.get('angle', 0.0))
                    scanned_props.ScanDirectionAngle = angle
                    
                    # Spot pattern
                    spot_pattern = comp_settings.get('spot_pattern', 'Hexagonal')
                    scanned_props.SpotPattern = spot_pattern
                    
                    # Lateral margin scale
                    lateral_margin_scale = float(comp_settings.get('lateral_margin_scale', 1.0))
                    scanned_props.SpotSelectionLateralMarginScaleFactor = lateral_margin_scale
                    
                    # Distal and proximal margins
                    distal_margin = int(comp_settings.get('distal_margin', 1))
                    proximal_margin = int(comp_settings.get('proximal_margin', 1))
                    scanned_props.SpotSelectionDistalTargetLayerMargin = distal_margin
                    scanned_props.SpotSelectionProximalTargetLayerMargin = proximal_margin
                    
                    # Minimum radiologic depth
                    min_radiologic_depth = float(comp_settings.get('min_radiologic_depth', 0.0))
                    beam_settings.MinimumRadiologicDepthMargin = min_radiologic_depth
                    
                    # Layer repainting
                    layer_repainting_value = int(comp_settings.get('layer_repainting_value', 1))
                    scanned_props.RepaintingSettings.FixedNumberOfPaintings = layer_repainting_value
                    
                    # Set avoidance structures
                    avoidance_rois = comp_settings.get('avoidance_rois', [])
                    if avoidance_rois:
                        # Map ROI names using matched_roi_dict
                        mapped_rois = [self.matched_roi_dict.get(roi, roi) for roi in avoidance_rois]
                        beam_settings.SetAvoidanceStructures(RoiNames=mapped_rois)
                        print(f"  - Set avoidance ROIs: {mapped_rois}")
                    
                    print(f"  - Configured beam optimization settings")
            
            # Edit setup beam names
            self.edit_setup_beams()
            
            self.patient.Save()
            print("All IMPT beams added successfully")
            return True
            
        except Exception as e:
            messagebox.showerror("Beam Addition Error", f"Failed to add IMPT beams:\n{str(e)}")
            return False
    
    def edit_setup_beams(self):
        """Edit setup beam names and descriptions."""
        try:
            setup_beams = self.beam_set.PatientSetup.SetupBeams
            beam_keys = list(setup_beams.keys())
            
            # Rename first setup beam if it exists
            if len(beam_keys) > 0:
                setup_beams[beam_keys[0]].Name = "I1"
                setup_beams['I1'].Description = "kV AP"
            
            # Rename second setup beam if it exists
            if len(beam_keys) > 1:
                setup_beams[beam_keys[1]].Name = "I2"
                setup_beams['I2'].Description = "kV Lt Lat"
            
            # Rename third setup beam if it exists
            if len(beam_keys) > 2:
                setup_beams[beam_keys[2]].Name = "I3"
                setup_beams['I3'].Description = "CBCT"
                setup_beams['I3'].GantryAngle = 0
            
            print("Setup beams renamed successfully")
            
        except Exception as e:
            print(f"Warning: Could not edit setup beams: {str(e)}")
    
    def create_plan_step(self):
        """Execute the complete plan creation workflow."""
        # Create plan
        if not self.create_plan():
            return False
        
        # Create beam set
        if not self.create_beam_set():
            return False
        
        # Add prescription
        if not self.add_prescription():
            return False
        
        # Set isocenter
        if not self.set_isocenter():
            return False
        
    def add_beams_step(self):    
        # Add beams based on technique
        if self.technique == "VMAT":
            if not self.add_vmat_beams():
                return False
        elif self.technique == "IMPT":
            if not self.add_impt_beams():
                return False
        else:
            messagebox.showerror("Unknown Technique", f"Unknown technique: {self.technique}")
            return False
        
        print("Plan created successfully with all beams!")
        return True
