from django.contrib import admin
from .models import patient_table,department,doctors_information,qnty,slots,Tablets,appointments

# Register your models here.
admin.site.register(patient_table)
admin.site.register(department)
admin.site.register(doctors_information)
# admin.site.register(tab_database)
admin.site.register(qnty)
admin.site.register(slots)
admin.site.register(Tablets)
admin.site.register(appointments)