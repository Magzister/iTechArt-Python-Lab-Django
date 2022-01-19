import processing_employee_data.views as views


from django.urls import path


urlpatterns = [
    path('employees', views.EmployeeList.as_view(), name='employee_list'),
    path('employees/<int:pk>', views.EmployeeDetail.as_view(), name='employee_detail'),
    path('banks', views.bank_list, name='bank_list'),
    path('banks/<int:pk>', views.bank_detail, name='bank_detail'),
    path('companies', views.CompanyList.as_view(), name='company_list'),
    path('companies/<int:pk>', views.CompanyDetail.as_view(), name='company_detail'),
    path('companies/lce', views.CompanyLastCreatedEmployee.as_view(), name='last_created_employee')
]
