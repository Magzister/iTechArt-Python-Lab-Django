from datetime import datetime
from django.db.models import Q, F, Max, OuterRef, Subquery
from django.shortcuts import render
from processing_employee_data.permissions import is_admin, IsAdminOrReadOnly
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


DATE_FORMAT = '%Y-%m-%d'


@api_view(['GET', 'POST'])
@is_admin
def bank_list(request):
    """Return list of all banks or create a new one.

    Takes two dates (start_date and end_date)
    as a get parameter, and returns a company
    that was created in a given date period
    and has the most recent update date that
    does not exceed the older date of the
    received date period.
    """

    if request.method == 'GET':
        start_date_str = request.GET.get('start_date', '')
        end_date_str = request.GET.get('end_date', '')

        start_date = None
        end_date = None
        try:
            start_date = datetime.strptime(start_date_str, DATE_FORMAT)
            end_date = datetime.strptime(end_date_str, DATE_FORMAT)
        except ValueError as e:
            print(e)

        if start_date and end_date:
            banks = Bank.objects.filter(
                created_at__range=(start_date, end_date)
            ).filter(
                updated_at__lte=end_date
            )
        else:
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
@is_admin
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
    """Return list of all employees or create a new one.

    Takes a number and date as a post parameter.
    This view should increase the salary of
    employees who have a birthday on the
    received date by the received number
    """

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        amount_str = request.POST.get('amount', '')
        birth_date_str = request.POST.get('birth_date', '')

        amount = None
        birth_date = None
        try:
            amount = int(amount_str)
            birth_date = datetime.strptime(birth_date_str, DATE_FORMAT)
        except ValueError as e:
            print(e)

        if amount and birth_date:
            birthday_people = PersonalData.objects.filter(
                date_of_birth=birth_date
            ).update(
                salary=F('salary')+amount
            )
            return Response(status=status.HTTP_200_OK)

        serializer = EmployeePersonalDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    """Retrieve, update or delete a bank."""

    permission_classes = [IsAdminUser]

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


class CompanyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        many = False
        if isinstance(request.data, list):
            many = True

        serializer = CompanySerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyLastCreatedEmployee(APIView):
    """
    View that returns one last created employee for each company.
    """
    def get(self, requets):
        employees_last_created = Employee.objects.filter(
            company_id=OuterRef('company_id')
        ).order_by('-created_at')[:1]
        employees = Employee.objects.filter(
            pk__in=Subquery(employees_last_created.values('pk'))
        )
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
