from rest_framework import serializers
from .models import RequestHeader, SelfReportedCashFlow, Address, Business, Owner, CFApplicationData, Application

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class SelfReportedCashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfReportedCashFlow
        fields = '__all__'

class CFApplicationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CFApplicationData
        fields = '__all__'

class RequestHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestHeader
        fields = '__all__'

# Models with Relational fields need to override the create function for proper
# deserialization
class OwnerSerializer(serializers.ModelSerializer):
    HomeAddress = AddressSerializer(required=True)
    class Meta:
        model = Owner
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('HomeAddress')
        HomeAddress = AddressSerializer.create(AddressSerializer(),
                       validated_data=address_data)
        owner, created = Owner.objects.update_or_create(HomeAddress=HomeAddress,
                          **validated_data)
        return owner

class BusinessSerializer(serializers.ModelSerializer):
    SelfReportedCashFlow = SelfReportedCashFlowSerializer(required=True)
    Address = AddressSerializer(required=True)
    class Meta:
        model = Business
        fields = '__all__'

    def create(self, validated_data):
        cashflow_data = validated_data.pop('SelfReportedCashFlow')
        address_data = validated_data.pop('Address')
        SelfReportedCashFlow = SelfReportedCashFlowSerializer.create(
                                SelfReportedCashFlowSerializer(),
                                validated_data=cashflow_data)
        Address = AddressSerializer.create(AddressSerializer(),
                    validated_data=address_data)
        business, created = Business.objects.update_or_create(Address=Address,
                                SelfReportedCashFlow=SelfReportedCashFlow,
                                **validated_data)
        return business

class ApplicationSerializer(serializers.ModelSerializer):
    RequestHeader = RequestHeaderSerializer(required=True)
    Business = BusinessSerializer(required=True)
    # Set many=True because there can be multiple owners
    Owners = OwnerSerializer(required=True, many=True)
    CFApplicationData = CFApplicationDataSerializer(required=True)
    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        header_data = validated_data.pop('RequestHeader')
        business_data = validated_data.pop('Business')
        owner_data = validated_data.pop('Owners')
        app_data = validated_data.pop('CFApplicationData')

        RequestHeader = RequestHeaderSerializer.create(RequestHeaderSerializer(),
                         validated_data=header_data)
        Business = BusinessSerializer.create(BusinessSerializer(),
                    validated_data=business_data)

        #Must deal with multiple owners
        os = OwnerSerializer(many=True, data=owner_data)
        if os.is_valid():
            Owners = os.save()

        CFApplicationData = CFApplicationDataSerializer.create(
                            CFApplicationDataSerializer(), validated_data=
                            app_data)
        application, created = Application.objects.update_or_create(
                                RequestHeader=RequestHeader,
                                Business=Business,
                                CFApplicationData=CFApplicationData)
        application.Owners.set(Owners)
        return application
