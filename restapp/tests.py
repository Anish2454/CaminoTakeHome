from django.test import TestCase
from .models import RequestHeader, SelfReportedCashFlow, Address, Business, Owner, CFApplicationData, Application
from .serializers import ApplicationSerializer
import json

class ApplicationTestCase(TestCase):
    # To test the serializer, load the JSON provided in the description
    # saved in "test_application.json"
    def setUp(self):
        with open('restapp/test_application.json') as json_file:
            self.data = json.load(json_file)

    def test_serializer(self):
        # Serialize the data read from the JSON
        serializer = ApplicationSerializer(data=self.data)

        # Make sure it is interpreted as valid (since it is valid)
        self.assertEqual(serializer.is_valid(), True)

        # Make sure it is being written to the database
        # Verify the business name, but in the future: verify everything
        application = serializer.save()
        self.assertEqual(application.Business.Name, "Wow Inc")

    # Was Running low on time so these tests aren't
    # as robust as they should be :(
    def test_application_submission(self):
        response = self.client.post('/loanapp/', self.data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["Loan ID"], 1)

    def test_application_status(self):
        self.client.post('/loanapp/', self.data, content_type="application/json")
        response = self.client.get('/status/1/')
        self.assertEqual(response.data["Status"], "Approved")
