from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404

from .serializers import ApplicationSerializer, BusinessSerializer
from .models import Application

from dateutil import parser
import datetime
from django.utils import timezone

# Create your views here.

# Accepts JSON for loan
class LoanApp(APIView):
    def post(self, request):
        data = request.data
        self.determine_duplicate(data)
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            application = serializer.save()
            return Response(status=200, data={"Loan ID": application.id})
        return Response(status=400, data=serializer.errors)

    # If the Business is the same and the amount requested is the same, then
    # mark this as a duplicate and delete the previous entry
    def determine_duplicate(self, data):
        applications = Application.objects.all()
        for a in applications:
            app_data = ApplicationSerializer(a).data
            b1 = data["Business"]["Name"]
            b2 = app_data["Business"]["Name"]
            amount1 = int(data["CFApplicationData"]["RequestedLoanAmount"])
            amount2 = int(app_data["CFApplicationData"]["RequestedLoanAmount"])
            if b1==b2 and amount1==amount2:
                a.delete()
        return None

class Status(APIView):
    def get(self, request, loanid):
        application = get_object_or_404(Application, pk=loanid)
        data = ApplicationSerializer(application).data
        return Response(self.determine_status(data))

    def determine_status(self, data):
        # Use the timestamp to determine the loan status
        timestamp = parser.parse(data["RequestHeader"]["RequestDate"])
        now = timezone.now()
        diff = now - timestamp

        #If it's been less than a week, the loan is still pending
        if diff <= datetime.timedelta(weeks=1):
            return {"Status": "Pending", "Time Elapsed": str(diff)}

        #Otherwise, you're approved!
        return {"Status": "Approved", "Time Elapsed": str(diff)}
