try:
    from raystation import *
    import raystation.v2025 as rs
    from raystation.v2025 import get_current
    import raystation.v2025.typing as rstype
except:
    from connect import *

class ClinicalGoalAdder:
    """
    Class to add clinical goals to a treatment plan in RayStation.
    Takes clinical goal template name from flow configuration and applies it to the plan.
    """
    
    def __init__(self, clinical_goal_data, matched_roi_dict, case, plan_name):
        """
        Initialize the ClinicalGoalAdder.
        
        Args:
            clinical_goal_data: Dictionary containing clinical goal template name and matched ROIs
            matched_roi_dict: Dictionary of matched ROI names
            case: RayStation case object
            plan_name: Name of the treatment plan
        """
        self.clinical_goal_data = clinical_goal_data
        self.matched_roi_dict = matched_roi_dict
        self.case = case
        self.plan_name = plan_name
        self.clinical_goal_template_name = clinical_goal_data.get('clinical_goal_template', '')
        self.matched_rois = clinical_goal_data.get('matched_rois', [])
        
        # Get plan
        self.plan = self.case.TreatmentPlans[self.plan_name]
        
    def add_clinical_goals(self):
        """
        Main method to add clinical goals from the specified template to the treatment plan.
        Creates AssociatedRoisAndPois dictionary from matched_rois data and applies template.
        """
        if not self.clinical_goal_template_name:
            print("❌ No clinical goal template name provided.")
            return
        
        print(f"📋 Adding clinical goals from template '{self.clinical_goal_template_name}'...")
        
        # Create AssociatedRoisAndPois dictionary
        associated_rois = {}
        for roi_mapping in self.matched_rois:
            template_roi = roi_mapping.get('template_roi', '')
            matched_roi = roi_mapping.get('matched_roi', '')
            
            if template_roi:
                # If matched_roi is empty or None, set to None to skip adding
                if matched_roi:
                    # Look up the actual ROI name in the patient case using matched_roi_dict
                    actual_roi_name = self.matched_roi_dict.get(matched_roi, matched_roi)
                    if actual_roi_name == '--Not Match--':
                        associated_rois[template_roi] = ""
                        print(f"  • {template_roi} → {matched_roi} → {actual_roi_name}")
                    else:
                        associated_rois[template_roi] = actual_roi_name
                        print(f"  • {template_roi} → {matched_roi} → {actual_roi_name}")
                else:
                    associated_rois[template_roi] = None
                    print(f"  • {template_roi} → [Not Matched - Will Skip]")
        # print("🔗 Associated ROIs and POIs prepared.")
        # print(associated_rois)
        # Load template and apply clinical goals
        try:
            patient_db = get_current('PatientDB')
            goal_template = patient_db.LoadTemplateClinicalGoals(templateName=self.clinical_goal_template_name)
            
            self.plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(
                Template=goal_template,
                AssociatedRoisAndPois=associated_rois,
                AssociatedBeamSets={  },
                AddClinicalGoalsDefinedOnTotalDose=True,
                ReplaceExistingClinicalGoals=True
            )
            
            print(f"✅ Clinical goals successfully applied from template '{self.clinical_goal_template_name}'")
            
        except Exception as e:
            print(f"❌ Error applying clinical goals: {str(e)}")
            raise
