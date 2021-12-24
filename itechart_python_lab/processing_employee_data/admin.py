from django.contrib import admin
from processing_employee_data.models import (
    Bank,
    Company,
    Employee,
    PersonalData,
)

admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(Bank)
admin.site.register(PersonalData)
