from django.test import TestCase
from .models import Patient

class PatientModelTest(TestCase):
    def test_create_patient(self):
        # Create a patient object with all provided details
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            dob='2021-12-14',
            gender='male',
            marital_status='married',
            id_number='12345678',
            address='kabarak, downtown 123 street',
            phone_number='0787654321',
            email='johndoe@gmail.com',
            county='Uasin Gishu',
            subcounty='Kenya',
            emergency_name='Jane Doe',
            emergency_relationship='wife',
            emergency_phone_number='0712345678',
            created_at='2024-02-26 16:01:42.311141',
            medical_history="Occasional headaches and fatigue. Additionally, I'm..."
        )

        # Retrieve the patient from the database
        saved_patient = Patient.objects.get(id=patient.id)

        # Check if all input fields match the values provided
        self.assertEqual(saved_patient.first_name, 'John')
        self.assertEqual(saved_patient.last_name, 'Doe')
        self.assertEqual(saved_patient.dob.strftime('%Y-%m-%d'), '2021-12-14')
        self.assertEqual(saved_patient.gender, 'male')
        self.assertEqual(saved_patient.marital_status, 'married')
        self.assertEqual(saved_patient.id_number, '12345678')
        self.assertEqual(saved_patient.address, 'kabarak, downtown 123 street')
        self.assertEqual(saved_patient.phone_number, '0787654321')
        self.assertEqual(saved_patient.email, 'johndoe@gmail.com')
        self.assertEqual(saved_patient.county, 'Uasin Gishu')
        self.assertEqual(saved_patient.subcounty, 'Kenya')
        self.assertEqual(saved_patient.emergency_name, 'Jane Doe')
        self.assertEqual(saved_patient.emergency_relationship, 'wife')
        self.assertEqual(saved_patient.emergency_phone_number, '0712345678')
        self.assertEqual(saved_patient.medical_history, "Occasional headaches and fatigue. Additionally, I'm...")
