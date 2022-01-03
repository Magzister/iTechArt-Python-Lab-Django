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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'created_at', 'company_id']


class CompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)

    class Meta:
        model = Company
        fields = ['name', 'web_site', 'email', 'post_index', 'employees']


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = '__all__'


class EmployeePersonalDataSerializer(serializers.ModelSerializer):
    personal_data = PersonalDataSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
