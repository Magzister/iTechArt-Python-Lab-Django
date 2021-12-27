from django.shortcuts import render
from processing_employee_data.models import (
    Bank,
    Company,
    Employee,
    PersonalData,
)
from processing_employee_data.serializers import (
    BankSerializer,
    CompanySerializer,
    EmployeeSerializer,
    EmployeePersonalDataSerializer,
)
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView



@api_view(['GET', 'POST'])
def bank_list(request):
    """Return list of all banks or create a new one."""

    if request.method == 'GET':
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def bank_detail(request, pk):
    """Retrieve, update or delete a bank."""

    try:
        bank = Bank.objects.get(pk=pk)
    except Bank.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankSerializer(bank)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BankSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeList(APIView):
    """Return list of all employees or create a new one."""

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeePersonalDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    """Retrieve, update or delete a bank."""

    def get_employee(self, pk):
        try:
            return Employee.objects.select_related('personal_data').get(pk=pk)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        employee = self.get_employee(pk)
        serializer = EmployeePersonalDataSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_employee(pk)
        serializer = EmployeePersonalDataSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_employee(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
