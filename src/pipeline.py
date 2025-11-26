"""
Pipeline - Multi-Agent System Orchestrator
Connects Agent 1 (Extractor), Agent 2 (Explainer), and Agent 3 (Lifestyle Coach)

Team: Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb
Course: ITAI 2376 - Boomer Health Summary Project
"""

import json
from typing import Dict, Optional
from datetime import datetime

# Import our agents
from agent1_extractor import MedicalExtractor
from agent2_educator import HealthExplainer
from agent3_organizer import LifestyleCoach


class BoomerHealthPipeline:
    """
    Main pipeline that orchestrates all three agents to transform
    medical documents into patient-friendly health summaries
    """
    
    def __init__(self):
        """Initialize all three agents"""
        print("🚀 Initializing Boomer Health Summary System...")
        
        self.agent1 = MedicalExtractor()
        print("   ✅ Agent 1 (Medical Extractor) ready")
        
        self.agent2 = HealthExplainer()
        print("   ✅ Agent 2 (Health Explainer) ready")
        
        self.agent3 = LifestyleCoach()
        print("   ✅ Agent 3 (Lifestyle Coach) ready")
        
        print("✨ System ready to process medical documents!\n")
        
        # Track processing history for feedback loop (RL component)
        self.processing_history = []
    
    def process_document(self, 
                        document_text: str, 
                        input_method: str = "free_text",
                        patient_name: Optional[str] = None) -> Dict:
        """
        Main pipeline: Process a medical document through all three agents
        
        Args:
            document_text: Raw text from discharge paper, prescription, or user input
            input_method: "photo_ocr", "free_text", or "guided_form"
            patient_name: Optional patient name for personalization
            
        Returns:
            Complete health summary with all agent outputs
        """
        
        print("="*70)
        print(f"📄 PROCESSING MEDICAL DOCUMENT")
        print(f"   Input Method: {input_method}")
        print(f"   Patient: {patient_name or 'Anonymous'}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        print()
        
        # STAGE 1: Extract medical information
        print("🔍 STAGE 1: Extracting medical information...")
        extracted_data = self.agent1.extract_all(document_text, input_method)
        print(f"   ✅ Found {len(extracted_data['diagnoses'])} diagnoses")
        print(f"   ✅ Found {len(extracted_data['medications'])} medications")
        print(f"   ✅ Extraction quality: {extracted_data['extraction_quality'].upper()}")
        print()
        
        # STAGE 2: Explain in plain language
        print("💡 STAGE 2: Translating medical terms to plain language...")
        explained_data = self.agent2.explain_all(extracted_data)
        print(f"   ✅ Explained {len(explained_data['diagnoses_explained'])} diagnoses")
        print(f"   ✅ Explained {len(explained_data['medications_explained'])} medications")
        print()
        
        # STAGE 3: Generate action plan
        print("📋 STAGE 3: Creating personalized action plan...")
        action_plan = self.agent3.generate_action_plan(explained_data)
        print(f"   ✅ Generated {len(action_plan['diet_recommendations'])} diet tips")
        print(f"   ✅ Generated {len(action_plan['exercise_recommendations'])} exercise tips")
        print(f"   ✅ Generated {len(action_plan['questions_for_doctor'])} questions for doctor")
        print()
        
        # STAGE 4: Assemble final summary
        print("📦 STAGE 4: Assembling final health summary...")
        final_summary = self.assemble_final_summary(
            extracted_data,
            explained_data,
            action_plan,
            patient_name
        )
        print("   ✅ Health summary complete!")
        print()
        
        # Store in history for RL feedback
        self.processing_history.append({
            'timestamp': datetime.now().isoformat(),
            'input_method': input_method,
            'extraction_quality': extracted_data['extraction_quality'],
            'summary': final_summary
        })
        
        return final_summary
    
    def assemble_final_summary(self,
                              extracted_data: Dict,
                              explained_data: Dict,
                              action_plan: Dict,
                              patient_name: Optional[str] = None) -> Dict:
        """
        Assemble all agent outputs into one comprehensive summary
        """
        
        summary = {
            'patient_name': patient_name or "Patient",
            'generated_date': datetime.now().strftime('%B %d, %Y'),
            'generated_time': datetime.now().strftime('%I:%M %p'),
            
            # Section 1: What the Doctor Found
            'section_1_diagnoses': {
                'title': 'What Your Doctor Found',
                'diagnoses': explained_data['diagnoses_explained'],
                'test_results': explained_data['test_results_explained']
            },
            
            # Section 2: Your Medications
            'section_2_medications': {
                'title': 'Your Medications Explained',
                'medications': explained_data['medications_explained']
            },
            
            # Section 3: What You Should Do
            'section_3_action_plan': {
                'title': 'Your Action Plan',
                'diet': action_plan['diet_recommendations'],
                'exercise': action_plan['exercise_recommendations'],
                'daily_habits': action_plan['daily_habits'],
                'medication_reminders': action_plan['medication_reminders']
            },
            
            # Section 4: When to Get Help
            'section_4_warning_signs': {
                'title': 'Warning Signs - When to Get Help',
                'warning_signs': action_plan['warning_signs']
            },
            
            # Section 5: Questions for Your Doctor
            'section_5_questions': {
                'title': 'Questions to Ask Your Doctor',
                'questions': action_plan['questions_for_doctor']
            },
            
            # Section 6: Medical Terms Glossary
            'section_6_glossary': {
                'title': 'Medical Terms Explained',
                'abbreviations': explained_data['abbreviations_explained']
            },
            
            # Metadata
            'metadata': {
                'input_method': extracted_data['input_method'],
                'extraction_quality': extracted_data['extraction_quality'],
                'agent_versions': 'v1.0'
            },
            
            'disclaimer': explained_data['disclaimer']
        }
        
        return summary
    
    def format_summary_for_display(self, summary: Dict) -> str:
        """
        Format the complete summary for human-readable display
        (This is what gets shown to the patient)
        """
        
        output = []
        
        # Header
        output.append("╔" + "═"*68 + "╗")
        output.append("║" + " "*68 + "║")
        output.append("║" + "        🏥 YOUR HEALTH SUMMARY - EASY TO UNDERSTAND        ".center(68) + "║")
        output.append("║" + " "*68 + "║")
        output.append("╚" + "═"*68 + "╝")
        output.append("")
        
        output.append(f"Patient: {summary['patient_name']}")
        output.append(f"Date: {summary['generated_date']} at {summary['generated_time']}")
        output.append("")
        output.append("─"*70)
        
        # SECTION 1: Diagnoses
        section1 = summary['section_1_diagnoses']
        output.append("")
        output.append(f"📋 {section1['title'].upper()}")
        output.append("─"*70)
        
        for dx in section1['diagnoses']:
            output.append(f"\n✓ {dx['diagnosis']} (also called: {dx['simple_name']})")
            output.append(f"  {dx['explanation']}")
            if dx['analogy']:
                output.append(f"  💡 Think of it like: {dx['analogy']}")
        
        if section1['test_results']:
            output.append("\n📊 YOUR TEST RESULTS:")
            for test in section1['test_results']:
                output.append(f"  • {test['test']}: {test['your_value']}")
                output.append(f"    {test['what_it_means']}")
                output.append(f"    (Normal range: {test['normal_range']})")
        
        # SECTION 2: Medications
        section2 = summary['section_2_medications']
        output.append("\n")
        output.append("─"*70)
        output.append(f"💊 {section2['title'].upper()}")
        output.append("─"*70)
        
        for med in section2['medications']:
            output.append(f"\n✓ {med['medication']} ({med['dosage']})")
            output.append(f"  What it does: {med['what_it_does']}")
            output.append(f"  ⚠️  {med['reminder']}")
        
        # SECTION 3: Action Plan
        section3 = summary['section_3_action_plan']
        output.append("\n")
        output.append("─"*70)
        output.append(f"📝 {section3['title'].upper()}")
        output.append("─"*70)
        
        if section3['diet']:
            output.append("\n🥗 DIET & NUTRITION:")
            for i, tip in enumerate(section3['diet'], 1):
                output.append(f"  {i}. {tip}")
        
        if section3['exercise']:
            output.append("\n🏃 EXERCISE & ACTIVITY:")
            for i, tip in enumerate(section3['exercise'], 1):
                output.append(f"  {i}. {tip}")
        
        if section3['daily_habits']:
            output.append("\n📅 DAILY HABITS TO TRACK:")
            for i, habit in enumerate(section3['daily_habits'], 1):
                output.append(f"  {i}. {habit}")
        
        if section3['medication_reminders']:
            output.append("\n💊 MEDICATION REMINDERS:")
            for i, reminder in enumerate(section3['medication_reminders'], 1):
                output.append(f"  {i}. {reminder}")
        
        # SECTION 4: Warning Signs
        section4 = summary['section_4_warning_signs']
        output.append("\n")
        output.append("─"*70)
        output.append(f"⚠️  {section4['title'].upper()}")
        output.append("─"*70)
        
        for sign in section4['warning_signs']:
            output.append(f"  • {sign}")
        
        # SECTION 5: Questions for Doctor
        section5 = summary['section_5_questions']
        output.append("\n")
        output.append("─"*70)
        output.append(f"❓ {section5['title'].upper()}")
        output.append("─"*70)
        
        for i, question in enumerate(section5['questions'], 1):
            output.append(f"  {i}. {question}")
        
        # SECTION 6: Glossary
        if summary['section_6_glossary']['abbreviations']:
            section6 = summary['section_6_glossary']
            output.append("\n")
            output.append("─"*70)
            output.append(f"📖 {section6['title'].upper()}")
            output.append("─"*70)
            
            for abbrev in section6['abbreviations']:
                output.append(f"  • {abbrev['abbreviation']} = {abbrev['meaning']}")
        
        # Disclaimer
        output.append("\n")
        output.append("─"*70)
        output.append(summary['disclaimer'])
        output.append("─"*70)
        
        # Footer
        output.append("\n")
        output.append("Generated by Boomer Health Summary System")
        output.append(f"Team: Oyinade Balogun, Hilary C Bruton, Glen Sam, Kaleb")
        output.append("ITAI 2376 - AI Agents Final Project")
        
        return "\n".join(output)
    
    def save_summary_to_file(self, summary: Dict, filename: str = None):
        """Save summary to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"health_summary_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"💾 Summary saved to: {filename}")
        return filename
    
    def collect_feedback(self, summary_id: int, feedback: Dict):
        """
        Collect user feedback for reinforcement learning
        
        Args:
            summary_id: Index in processing_history
            feedback: Dict with 'clarity', 'helpfulness', 'completeness' ratings
        """
        if summary_id < len(self.processing_history):
            self.processing_history[summary_id]['feedback'] = feedback
            
            # Simple reward calculation
            reward = (
                feedback.get('clarity', 0) * 0.4 +
                feedback.get('helpfulness', 0) * 0.4 +
                feedback.get('completeness', 0) * 0.2
            )
            
            self.processing_history[summary_id]['reward'] = reward
            
            print(f"📊 Feedback recorded! Reward score: {reward:.2f}/5.0")
            
            # In a real system, this would update agent policies
            # For this project, we just log it
            return reward
        else:
            print("❌ Invalid summary ID")
            return None


# Example usage and testing
if __name__ == "__main__":
    # Create pipeline
    pipeline = BoomerHealthPipeline()
    
    # Sample discharge paper
    sample_document = """
    DISCHARGE SUMMARY
    Patient: Mary Johnson | Age: 72 | Date: November 25, 2025
    
    DISCHARGE DIAGNOSES:
    1. Congestive Heart Failure (CHF), acute exacerbation
    2. Hypertension, uncontrolled
    3. Type 2 Diabetes Mellitus
    
    VITAL SIGNS AT DISCHARGE:
    Blood Pressure: 142/88 mmHg
    Heart Rate: 78 bpm
    Weight: 198 lbs (up 12 lbs from baseline)
    A1C: 8.2%
    
    MEDICATIONS PRESCRIBED:
    1. Furosemide 40mg - Take one tablet by mouth once daily in the morning
    2. Lisinopril 20mg - Take one tablet by mouth once daily
    3. Metformin 1000mg - Take one tablet by mouth twice daily with meals
    4. Aspirin 81mg - Take one tablet by mouth once daily
    
    CHIEF COMPLAINT ON ADMISSION:
    Patient presented with shortness of breath, significant leg swelling,
    and fatigue for the past 3 days.
    
    HOSPITAL COURSE:
    Patient responded well to diuretic therapy. Fluid overload improved.
    Shortness of breath resolved. Patient is now able to lie flat without
    difficulty breathing.
    
    DISCHARGE INSTRUCTIONS:
    1. Weigh yourself every morning before breakfast and after using bathroom
    2. Call Dr. Smith if weight increases by 3 pounds in one day or 5 pounds in one week
    3. Limit sodium intake to 2000mg per day
    4. Avoid salty foods: chips, canned soups, deli meats, pickles, restaurant food
    5. Limit fluid intake to 2 liters (8 cups) per day
    6. Take all medications as prescribed
    7. Monitor blood pressure at home daily
    8. Walk 10-15 minutes daily as tolerated
    
    FOLLOW-UP APPOINTMENTS:
    - Cardiology: Dr. Sarah Smith - December 2, 2025 (1 week)
    - Primary Care: Dr. James Brown - December 9, 2025 (2 weeks)
    
    CALL YOUR DOCTOR IF YOU EXPERIENCE:
    - Sudden weight gain (3+ pounds in a day)
    - Increased swelling in legs or abdomen
    - Worsening shortness of breath
    - Chest pain or pressure
    - Dizziness or fainting
    
    SEEK EMERGENCY CARE (CALL 911) IF:
    - Severe chest pain
    - Extreme difficulty breathing
    - Confusion or altered mental status
    """
    
    # Process the document
    print("\n" + "="*70)
    print("DEMO: Processing Sample Discharge Paper")
    print("="*70 + "\n")
    
    summary = pipeline.process_document(
        document_text=sample_document,
        input_method="photo_ocr",
        patient_name="Mary Johnson"
    )
    
    # Display the formatted summary
    print("\n" + "="*70)
    print("FINAL PATIENT-FRIENDLY SUMMARY")
    print("="*70 + "\n")
    
    formatted_output = pipeline.format_summary_for_display(summary)
    print(formatted_output)
    
    # Save to file
    print("\n")
    pipeline.save_summary_to_file(summary)
    
    # Simulate user feedback (RL component)
    print("\n" + "="*70)
    print("REINFORCEMENT LEARNING: Collecting Feedback")
    print("="*70)
    feedback = {
        'clarity': 5,
        'helpfulness': 5,
        'completeness': 4
    }
    pipeline.collect_feedback(0, feedback)
