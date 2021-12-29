from rest_framework import serializers
from processing_employee_data.models import (
    Bank,
    Company,
    Employee,
    PersonalData,
)


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'surname', 'company']


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = '__all__'


class EmployeePersonalDataSerializer(serializers.ModelSerializer):
    personal_data = PersonalDataSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
