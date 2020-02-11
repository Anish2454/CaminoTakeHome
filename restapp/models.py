from django.db import models
from django_mysql.models import JSONField

# Create your models here.
class Address(models.Model):
    Address1 = models.CharField(max_length=1024)
    Address2 = models.CharField(max_length=1024, null=True)
    City = models.CharField(max_length=1024)
    State = models.CharField(max_length=1024)
    Zip = models.CharField(max_length=1024)

    def __str__(self):
        return " ".join([self.Address1, self.Address2, self.City, self.State,
        self.Zip])

class SelfReportedCashFlow(models.Model):
    AnnualRevenue = models.FloatField("AnnualRevenue")
    MonthlyAverageBankBalance = models.FloatField("MonthlyAverageBankBalance")
    MonthlyAverageCreditCardVolume = models.FloatField("MonthlyAverageCreditCardVolume")

class Business(models.Model):
    Name = models.CharField(max_length=1024)
    SelfReportedCashFlow = models.OneToOneField(SelfReportedCashFlow, on_delete=models.CASCADE)
    Address = models.OneToOneField(Address, on_delete=models.CASCADE)
    TaxID = models.CharField(max_length=1024)
    Phone = models.CharField(max_length=1024)
    NAICS = models.CharField(max_length=1024)
    HasBeenProfitable = models.BooleanField()
    HasBankruptedInLast7Years = models.BooleanField()
    InceptionDate = models.DateTimeField()

    def __str__(self):
        return self.Name

class Owner(models.Model):
    Name = models.CharField(max_length=1024)
    FirstName = models.CharField(max_length=1024)
    LastName = models.CharField(max_length=1024)
    Email = models.CharField(max_length=1024)
    HomeAddress = models.OneToOneField(Address, on_delete=models.CASCADE)
    DateOfBirth = models.DateTimeField()
    HomePhone = models.CharField(max_length=1024)
    SSN = models.CharField(max_length=1024)
    PercentageOfOwnership = models.FloatField()

    def __str__(self):
        return self.Name

class RequestHeader(models.Model):
    CFRequestId = models.CharField(max_length=1024)
    RequestDate = models.DateTimeField()
    CFApiUserId = models.CharField(max_length=1024, null=True)
    CFApiPassword = models.CharField(max_length=1024, null=True)
    IsTestLead = models.BooleanField()

class CFApplicationData(models.Model):
    RequestedLoanAmount = models.FloatField()
    StatedCreditHistory = models.IntegerField()
    LegalEntityType = models.CharField(max_length=1024)
    FilterID = models.CharField(max_length=1024)

class Application(models.Model):
    RequestHeader = models.OneToOneField(RequestHeader, on_delete=models.CASCADE)
    Business = models.OneToOneField(Business, on_delete=models.CASCADE)
    #Multiple Owners
    Owners = models.ManyToManyField(Owner)
    CFApplicationData = models.OneToOneField(CFApplicationData, on_delete=models.CASCADE)
