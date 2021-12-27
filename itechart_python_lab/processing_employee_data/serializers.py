from rest_framework import serializers
from processing_employee_data.models import (
    Bank,
    Company,
    Employee,
    PersonalData,
)


class BankSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    web_site = serializers.CharField(max_length=50)
    email = serializers.EmailField()

    def create(self, validated_data):
        return Bank.objects.create(**validated_data)

    def upfate(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.web_site = validated_data.get('web_site', instance.web_site)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


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
