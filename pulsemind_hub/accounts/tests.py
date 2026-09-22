from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser

class AccountsModelAndViewsTestCase(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username='testpatient',
            email='patient@test.com',
            password='Password123!',
            role='PATIENT'
        )
        self.doctor = CustomUser.objects.create_user(
            username='testdoctor',
            email='doctor@test.com',
            password='Password123!',
            role='DOCTOR',
            specialization='Cardiology',
            consultation_fee=50.00
        )

    def test_user_roles(self):
        self.assertTrue(self.patient.is_patient)
        self.assertFalse(self.patient.is_doctor)
        self.assertTrue(self.doctor.is_doctor)
        self.assertEqual(str(self.doctor), "Dr. testdoctor (Doctor)")

    def test_login_view(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testpatient',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
