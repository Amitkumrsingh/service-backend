from django.test import TestCase
from django.urls import reverse
from .models import Vehicle, ServiceIssue
from datetime import datetime, timedelta

class VehicleModelTestCase(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(name="Car A", type="SUV")

    def test_vehicle_creation(self):
        """Test if a Vehicle object is created successfully."""
        self.assertEqual(Vehicle.objects.count(), 1)
        self.assertEqual(self.vehicle.name, "Car A")
        self.assertEqual(self.vehicle.type, "SUV")

    def test_vehicle_string_representation(self):
        """Test the string representation of Vehicle."""
        self.assertEqual(str(self.vehicle), "Car A")


class ServiceIssueModelTestCase(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(name="Car B", type="Sedan")
        self.service_issue = ServiceIssue.objects.create(
            vehicle=self.vehicle,
            issue="Brake issue",
            description="The brake pads need replacement.",
            cost=5000,
            created_at=datetime(2024, 11, 28)
        )

    def test_service_issue_creation(self):
        """Test if a ServiceIssue object is created successfully."""
        self.assertEqual(ServiceIssue.objects.count(), 1)
        self.assertEqual(self.service_issue.vehicle.name, "Car B")
        self.assertEqual(self.service_issue.cost, 5000)

    def test_service_issue_string_representation(self):
        """Test the string representation of ServiceIssue."""
        self.assertEqual(str(self.service_issue), "Car B - Brake issue")


class AnalyticsViewTestCase(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(name="Car C", type="Truck")
        # Create ServiceIssues with specific dates and costs
        ServiceIssue.objects.create(vehicle=self.vehicle, issue="Oil change", cost=3000, created_at=datetime(2024, 11, 25))
        ServiceIssue.objects.create(vehicle=self.vehicle, issue="Tire replacement", cost=8000, created_at=datetime(2024, 11, 27))
        ServiceIssue.objects.create(vehicle=self.vehicle, issue="Battery replacement", cost=5000, created_at=datetime(2024, 10, 15))

    def test_daily_revenue(self):
        """Test daily revenue calculation."""
        response = self.client.get(reverse('daily_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"labels": ["Nov 24", "Nov 25", "Nov 26", "Nov 27", "Nov 28", "Nov 29", "Nov 30"]', response.content)
        self.assertIn(b'"data": [0, 3000, 0, 8000, 0, 0, 0]', response.content)

    def test_monthly_revenue(self):
        """Test monthly revenue calculation."""
        response = self.client.get(reverse('monthly_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"labels": ["Dec 2023", "Jan 2024", "Feb 2024", "Mar 2024", "Apr 2024", "May 2024", "Jun 2024", "Jul 2024", "Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024"]', response.content)
        self.assertIn(b'"data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5000, 11000]', response.content)

    def test_yearly_revenue(self):
        """Test yearly revenue calculation."""
        response = self.client.get(reverse('yearly_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"labels": ["2023", "2024"]', response.content)
        self.assertIn(b'"data": [0, 16000]', response.content)
