from django.urls import path
from .views import LoanApp, Status


urlpatterns = [
    path("loanapp/", LoanApp.as_view(), name="loanapp"),
    path("status/<int:loanid>/", Status.as_view(), name="status")
]
