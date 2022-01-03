from django.db import models


def company_directory_path(instance, filename):
    """File will be uploaded to MEDIA_PATH/company_<name>/<filename>"""
    return 'company_{0}/{1}'.format(instance.name, filename)


class CreateUpdateInfo(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Bank(CreateUpdateInfo):
    name = models.CharField(max_length=30)
    web_site = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        db_table = 'bank'

    def __str__(self):
        return self.name


class Company(CreateUpdateInfo):
    name = models.CharField(max_length=30)
    web_site = models.CharField(max_length=50)
    email = models.EmailField()
    post_index = models.CharField(max_length=20)
    logo = models.ImageField(
        upload_to=company_directory_path,
        null=True,
        blank=True
    )
    bank = models.ManyToManyField(
        Bank,
        related_name='company',
        blank=True
    )

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name


class PersonalData(CreateUpdateInfo):
    date_of_birth = models.DateField()
    home_address = models.CharField(max_length=80)
    salary = models.PositiveIntegerField()

    class Meta:
        db_table = 'personal_data'


class Employee(CreateUpdateInfo):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    job_position = models.CharField(max_length=30)
    is_manager = models.BooleanField()
    is_admin = models.BooleanField()
    phone_number = models.CharField(max_length=25)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    personal_data = models.OneToOneField(
        PersonalData,
        on_delete=models.CASCADE,
        related_name='owner'
    )

    class Meta:
        db_table = 'employee'

    def __str__(self):
        return self.surname + ' ' + self.name
