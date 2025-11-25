"""
Agent 2: Health Explainer
Converts medical terminology into patient-friendly language

Team: Hilary C Bruton, Glen Sam, Oyinade Balogun, Kaleb
Course: ITAI 2376 - Boomer Health Summary Project
"""

import json
from typing import Dict, List

class HealthExplainer:
    """
    Agent 2: Translates medical jargon into plain English explanations
    that older adults can understand and act on.
    """
    
    def __init__(self):
        """Initialize with medical term explanations"""
        
        # Plain-language explanations for common diagnoses
        self.diagnosis_explanations = {
            'hypertension': {
                'simple': 'High Blood Pressure',
                'explanation': "Your blood pressure is higher than it should be. Think of it like a garden hose with too much water pressure - it puts extra strain on your blood vessels and heart. This is very common and manageable with medication and lifestyle changes.",
                'analogy': "Like a tire with too much air pressure - it works harder and wears out faster."
            },
            'high blood pressure': {
                'simple': 'High Blood Pressure',
                'explanation': "Your heart is pumping blood with more force than is healthy. Over time, this can damage your blood vessels and organs. The good news: it responds well to treatment.",
                'analogy': "Like turning up the pressure on a water system - everything works harder."
            },
            'diabetes': {
                'simple': 'High Blood Sugar',
                'explanation': "Your body has trouble managing sugar (glucose) in your blood. This happens because your body either doesn't make enough insulin or doesn't use it well. Left unmanaged, it can affect your eyes, kidneys, nerves, and heart.",
                'analogy': "Like a key that doesn't fit the lock properly - sugar can't get into your cells where it's needed."
            },
            'type 2 diabetes': {
                'simple': 'Blood Sugar Management Issue',
                'explanation': "Your body's ability to process sugar isn't working as well as it should. This is the most common type of diabetes and can often be managed with lifestyle changes, medication, or both.",
                'analogy': "Your body's sugar-handling system needs help - like needing reading glasses as you age."
            },
            'hyperlipidemia': {
                'simple': 'High Cholesterol',
                'explanation': "You have too much fat (cholesterol) in your blood. This can build up on artery walls like rust in pipes, making it harder for blood to flow. It's very manageable with diet changes and medication.",
                'analogy': "Like grease building up in kitchen pipes - it can clog the flow over time."
            },
            'high cholesterol': {
                'simple': 'High Cholesterol',
                'explanation': "There's too much fatty substance in your bloodstream. This can stick to your artery walls and increase heart disease risk. The good news: diet, exercise, and medication can control it.",
                'analogy': "Think of it like buildup in your arteries, similar to how mineral deposits build up in old pipes."
            },
            'congestive heart failure': {
                'simple': 'Heart Not Pumping Efficiently',
                'explanation': "Your heart isn't pumping blood as well as it should. This can cause fluid to build up in your lungs, legs, and other areas. It's a serious condition but can be managed with the right treatment and lifestyle changes.",
                'analogy': "Like a pump that's getting tired - it needs support to do its job properly."
            },
            'chf': {
                'simple': 'Heart Failure',
                'explanation': "CHF means Congestive Heart Failure. Your heart muscle has become weakened and can't pump blood efficiently. This causes fluid buildup. With treatment, many people live well with this condition.",
                'analogy': "Your heart needs help doing its pumping job - like an old pump that needs maintenance."
            },
            'copd': {
                'simple': 'Chronic Lung Disease',
                'explanation': "COPD (Chronic Obstructive Pulmonary Disease) makes it harder to breathe because your airways are inflamed and damaged. It's usually caused by smoking. While it can't be cured, treatment can help you breathe easier.",
                'analogy': "Like trying to breathe through a narrow straw - your airways are more restricted."
            },
            'asthma': {
                'simple': 'Breathing Condition',
                'explanation': "Your airways can suddenly narrow and swell, making it hard to breathe. Triggers include allergies, exercise, or cold air. With proper medication, most people control it well.",
                'analogy': "Like a garden hose that occasionally gets kinked - the flow gets restricted."
            },
            'atrial fibrillation': {
                'simple': 'Irregular Heartbeat',
                'explanation': "Your heart beats irregularly instead of in a steady rhythm. This can make you feel tired or short of breath, and it increases stroke risk. Medication can help control the rhythm.",
                'analogy': "Like a drum beating off-rhythm instead of keeping steady time."
            },
            'afib': {
                'simple': 'Irregular Heartbeat (AFib)',
                'explanation': "AFib is short for Atrial Fibrillation. Your heart's upper chambers quiver instead of beating effectively. This is common as we age and is manageable with medication.",
                'analogy': "Instead of a steady heartbeat, it's more like a flutter or quiver."
            },
            'osteoporosis': {
                'simple': 'Weak Bones',
                'explanation': "Your bones have become thinner and more fragile, making them easier to break. This is common as we age, especially in women after menopause. Calcium, vitamin D, and certain medications can help.",
                'analogy': "Like wood that's become brittle with age - it breaks more easily."
            },
            'arthritis': {
                'simple': 'Joint Pain and Stiffness',
                'explanation': "The protective cushioning in your joints has worn down, causing pain, stiffness, and sometimes swelling. While it can't be cured, pain management and movement can help you stay active.",
                'analogy': "Like a door hinge that's lost its lubrication - it gets stiff and creaky."
            },
            'gerd': {
                'simple': 'Acid Reflux',
                'explanation': "GERD (Gastroesophageal Reflux Disease) means stomach acid frequently flows back into your esophagus, causing heartburn. Diet changes and medication usually control it well.",
                'analogy': "Like a door that doesn't close properly - stomach acid leaks back up where it shouldn't."
            },
            'chronic kidney disease': {
                'simple': 'Kidney Function Decline',
                'explanation': "Your kidneys aren't filtering waste from your blood as well as they should. This develops slowly over time. Managing blood pressure and blood sugar helps protect your remaining kidney function.",
                'analogy': "Like a water filter that's getting clogged - it doesn't work as efficiently."
            },
            'ckd': {
                'simple': 'Chronic Kidney Disease',
                'explanation': "CKD means your kidneys are gradually losing their ability to filter blood. Controlling diabetes and blood pressure is key to slowing this down.",
                'analogy': "Your kidneys are like filters that need extra care to keep working."
            }
        }
        
        # Medication explanations (what they do, not medical advice)
        self.medication_explanations = {
            'lisinopril': "A blood pressure medication that helps relax your blood vessels, making it easier for your heart to pump blood.",
            'metformin': "Helps your body use insulin better and lowers blood sugar. Usually the first medication prescribed for Type 2 diabetes.",
            'atorvastatin': "A 'statin' that lowers cholesterol by reducing how much your liver produces. Helps prevent heart attacks and strokes.",
            'amlodipine': "Relaxes and widens your blood vessels to lower blood pressure and improve blood flow.",
            'furosemide': "A 'water pill' (diuretic) that helps your body get rid of extra fluid. Often used for heart failure or high blood pressure.",
            'lasix': "Another name for Furosemide - a water pill that reduces fluid buildup in your body.",
            'metoprolol': "A 'beta blocker' that slows your heart rate and reduces blood pressure, making your heart work less hard.",
            'omeprazole': "Reduces stomach acid production. Helps with heartburn, reflux, and ulcers.",
            'levothyroxine': "Replaces thyroid hormone when your thyroid doesn't make enough. Helps regulate your metabolism and energy.",
            'aspirin': "A blood thinner that helps prevent blood clots. Often used to reduce heart attack and stroke risk.",
            'warfarin': "A stronger blood thinner that prevents dangerous blood clots. Requires regular blood tests to monitor.",
            'gabapentin': "Treats nerve pain and sometimes used for certain seizure types. Helps calm overactive nerves.",
            'prednisone': "A steroid that reduces inflammation and immune system activity. Powerful but has side effects with long-term use.",
            'insulin': "Helps move sugar from your blood into your cells. Essential for people whose bodies don't make enough.",
            'albuterol': "Opens up your airways quickly. Used for asthma or breathing problems - usually in an inhaler.",
        }
        
        # Medical abbreviation translations
        self.abbreviation_explanations = {
            'BP': 'Blood Pressure',
            'HR': 'Heart Rate',
            'CHF': 'Congestive Heart Failure',
            'COPD': 'Chronic Obstructive Pulmonary Disease',
            'CAD': 'Coronary Artery Disease',
            'MI': 'Heart Attack (Myocardial Infarction)',
            'CVA': 'Stroke',
            'HTN': 'Hypertension (High Blood Pressure)',
            'DM': 'Diabetes Mellitus',
            'A1C': 'Average Blood Sugar (over 3 months)',
            'SOB': 'Shortness of Breath',
            'BID': 'Twice a day',
            'TID': 'Three times a day',
            'QD': 'Once a day',
            'PRN': 'As needed',
        }
    
    def explain_all(self, extracted_data: Dict) -> Dict:
        """
        Main method: Takes Agent 1's output and creates plain-language explanations
        
        Args:
            extracted_data: Dictionary from Agent 1
            
        Returns:
            Dictionary with explanations ready for Agent 3
        """
        
        explained_data = {
            'diagnoses_explained': self.explain_diagnoses(extracted_data.get('diagnoses', [])),
            'medications_explained': self.explain_medications(extracted_data.get('medications', [])),
            'abbreviations_explained': self.explain_abbreviations(extracted_data.get('flagged_terms', [])),
            'test_results_explained': self.explain_test_results(extracted_data.get('test_results', [])),
            'disclaimer': self.get_disclaimer(),
            'original_extraction': extracted_data  # Keep original for reference
        }
        
        return explained_data
    
    def explain_diagnoses(self, diagnoses: List[str]) -> List[Dict]:
        """Explain each diagnosis in plain language"""
        explained = []
        
        for diagnosis in diagnoses:
            dx_lower = diagnosis.lower()
            
            if dx_lower in self.diagnosis_explanations:
                info = self.diagnosis_explanations[dx_lower]
                explained.append({
                    'diagnosis': diagnosis,
                    'simple_name': info['simple'],
                    'explanation': info['explanation'],
                    'analogy': info.get('analogy', '')
                })
            else:
                # Generic explanation for unknown diagnoses
                explained.append({
                    'diagnosis': diagnosis,
                    'simple_name': diagnosis,
                    'explanation': f"{diagnosis} is a medical condition your doctor has identified. Ask your doctor to explain what this means for you specifically.",
                    'analogy': ''
                })
        
        return explained
    
    def explain_medications(self, medications: List[Dict]) -> List[Dict]:
        """Explain what each medication does (educational, not prescriptive)"""
        explained = []
        
        for med in medications:
            med_name = med.get('name', '').lower()
            med_dosage = med.get('dosage', 'See prescription')
            
            # Look for explanation
            explanation = self.medication_explanations.get(
                med_name,
                "This medication was prescribed by your doctor. Ask them or your pharmacist what it's for and how to take it properly."
            )
            
            explained.append({
                'medication': med.get('name', ''),
                'dosage': med_dosage,
                'what_it_does': explanation,
                'reminder': 'Take exactly as prescribed. Call your doctor if you have questions or side effects.'
            })
        
        return explained
    
    def explain_abbreviations(self, abbreviations: List[str]) -> List[Dict]:
        """Translate medical abbreviations"""
        explained = []
        
        for abbrev in abbreviations:
            meaning = self.abbreviation_explanations.get(
                abbrev.upper(),
                f"{abbrev} is a medical abbreviation. Ask your doctor what this means."
            )
            
            explained.append({
                'abbreviation': abbrev,
                'meaning': meaning
            })
        
        return explained
    
    def explain_test_results(self, test_results: List[Dict]) -> List[Dict]:
        """Explain what test results mean"""
        explained = []
        
        for test in test_results:
            test_name = test.get('test', '')
            value = test.get('value', '')
            
            # Provide context for common tests
            if 'blood pressure' in test_name.lower():
                explained.append({
                    'test': test_name,
                    'your_value': value,
                    'what_it_means': self.interpret_blood_pressure(value),
                    'normal_range': 'Normal is less than 120/80'
                })
            
            elif 'a1c' in test_name.lower():
                explained.append({
                    'test': test_name,
                    'your_value': value,
                    'what_it_means': self.interpret_a1c(value),
                    'normal_range': 'Normal is below 5.7%. Diabetes is 6.5% or higher.'
                })
            
            elif 'weight' in test_name.lower():
                explained.append({
                    'test': test_name,
                    'your_value': value,
                    'what_it_means': 'Your weight measurement. Track changes over time as your doctor advises.',
                    'normal_range': 'Varies by height and build'
                })
            
            else:
                explained.append({
                    'test': test_name,
                    'your_value': value,
                    'what_it_means': 'Ask your doctor to explain what this test result means for you.',
                    'normal_range': 'Varies'
                })
        
        return explained
    
    def interpret_blood_pressure(self, bp_value: str) -> str:
        """Provide context for blood pressure reading"""
        try:
            systolic = int(bp_value.split('/')[0])
            
            if systolic < 120:
                return "Your blood pressure is in the normal range. Keep up the good work!"
            elif systolic < 130:
                return "Your blood pressure is slightly elevated. Lifestyle changes can help bring it down."
            elif systolic < 140:
                return "Your blood pressure is in the 'high' range (Stage 1). Your doctor may recommend medication and lifestyle changes."
            else:
                return "Your blood pressure is significantly elevated (Stage 2). Follow your doctor's treatment plan closely."
        except:
            return "Blood pressure measurement recorded. Discuss with your doctor."
    
    def interpret_a1c(self, a1c_value: str) -> str:
        """Provide context for A1C test"""
        try:
            a1c_num = float(a1c_value.replace('%', ''))
            
            if a1c_num < 5.7:
                return "Your blood sugar control is normal. Great job!"
            elif a1c_num < 6.5:
                return "You're in the 'prediabetes' range. Lifestyle changes can help prevent diabetes."
            elif a1c_num < 7.0:
                return "Your diabetes is fairly well controlled, but there's room for improvement."
            elif a1c_num < 8.0:
                return "Your diabetes control needs improvement. Work with your doctor to adjust your plan."
            else:
                return "Your blood sugar has been quite high. It's important to work closely with your doctor."
        except:
            return "A1C test result recorded. This shows your average blood sugar over the past 3 months."
    
    def get_disclaimer(self) -> str:
        """Important medical disclaimer"""
        return """
⚠️ IMPORTANT DISCLAIMER:
This information is for educational purposes only and does not replace medical advice.
Always consult your healthcare provider for medical decisions, treatment plans, and 
questions about your specific health conditions. If you experience emergency symptoms
like chest pain, difficulty breathing, or severe symptoms, call 911 immediately.
        """.strip()
    
    def format_for_display(self, explained_data: Dict) -> str:
        """Format explained data for human-readable output"""
        output = []
        output.append("=" * 60)
        output.append("AGENT 2: PLAIN-LANGUAGE HEALTH EXPLANATION")
        output.append("=" * 60)
        output.append("")
        
        # Diagnoses
        if explained_data['diagnoses_explained']:
            output.append("🏥 YOUR DIAGNOSES EXPLAINED:")
            output.append("")
            for dx in explained_data['diagnoses_explained']:
                output.append(f"📌 {dx['diagnosis']} (also called: {dx['simple_name']})")
                output.append(f"   {dx['explanation']}")
                if dx['analogy']:
                    output.append(f"   💡 Think of it like: {dx['analogy']}")
                output.append("")
        
        # Medications
        if explained_data['medications_explained']:
            output.append("💊 YOUR MEDICATIONS EXPLAINED:")
            output.append("")
            for med in explained_data['medications_explained']:
                output.append(f"📌 {med['medication']} ({med['dosage']})")
                output.append(f"   What it does: {med['what_it_does']}")
                output.append(f"   ⚠️  {med['reminder']}")
                output.append("")
        
        # Test Results
        if explained_data['test_results_explained']:
            output.append("🔬 YOUR TEST RESULTS EXPLAINED:")
            output.append("")
            for test in explained_data['test_results_explained']:
                output.append(f"📌 {test['test']}: {test['your_value']}")
                output.append(f"   {test['what_it_means']}")
                output.append(f"   Normal range: {test['normal_range']}")
                output.append("")
        
        # Abbreviations
        if explained_data['abbreviations_explained']:
            output.append("📖 MEDICAL TERMS TRANSLATED:")
            for abbrev in explained_data['abbreviations_explained']:
                output.append(f"   • {abbrev['abbreviation']} = {abbrev['meaning']}")
            output.append("")
        
        # Disclaimer
        output.append(explained_data['disclaimer'])
        output.append("")
        output.append("=" * 60)
        output.append("Ready to send to Agent 3 (Lifestyle Coach)")
        output.append("=" * 60)
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Simulate Agent 1's output
    sample_agent1_output = {
        'diagnoses': ['Congestive Heart Failure', 'Hypertension', 'Type 2 Diabetes'],
        'medications': [
            {'name': 'Furosemide', 'dosage': '40mg'},
            {'name': 'Lisinopril', 'dosage': '20mg'},
            {'name': 'Metformin', 'dosage': '500mg'}
        ],
        'test_results': [
            {'test': 'Blood Pressure', 'value': '145/92'},
            {'test': 'A1C (Diabetes)', 'value': '7.8%'}
        ],
        'flagged_terms': ['CHF', 'BP', 'A1C']
    }
    
    # Create explainer
    explainer = HealthExplainer()
    
    # Generate explanations
    print("Testing Agent 2: Health Explainer\n")
    explained = explainer.explain_all(sample_agent1_output)
    
    # Display formatted output
    print(explainer.format_for_display(explained))
    
    # Show JSON for Agent 3
    print("\n\nJSON FORMAT (sent to Agent 3):")
    print(json.dumps(explained, indent=2))
