from django.contrib import admin
from processing_employee_data.models import Employee
from processing_employee_data.models import Company
from processing_employee_data.models import Bank
from processing_employee_data.models import PersonalData

admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(Bank)
admin.site.register(PersonalData)
