from django.db import models

# Create your models here.

class login(models.Model):
     username= models.CharField(max_length=100,primary_key=True)
     password= models.CharField(max_length=500)
     key=models.CharField(max_length=100)
     def __str__(self):
          return self.username

class department(models.Model):
     name=models.CharField(max_length=100,primary_key=True)
     def __str__(self):
          return self.name

class doctors_information(models.Model):
     doctor_name=models.CharField(max_length=100,primary_key=True)
     dept = models.ForeignKey(department, on_delete=models.CASCADE)
     def __str__(self):
          return self.doctor_name


class patient_table(models.Model):
     case_id= models.CharField(max_length=20,primary_key=True)
     patient_name=models.ForeignKey(login,on_delete=models.CASCADE)
     department=models.ForeignKey(department,on_delete=models.CASCADE)
     doctor=models.ForeignKey(doctors_information,on_delete=models.CASCADE)
     file_presciption=models.FileField(upload_to='prescription')
     next_date=models.DateField()
     status=models.CharField(max_length=20)
     def __str__(self):
          return (str(self.patient_name) +"(" +str(self.case_id)+")")
class qnty(models.Model):
     quantity=models.CharField(max_length=20,primary_key=True)
     def __str__(self):
          return self.quantity

# class tab_database(models.Model):
#      tab_name=models.CharField(max_length=500,primary_key=True)
#      mg=models.CharField(max_length=20)
#      def __str__(self):
#           return (str(self.tab_name)+" - "+str(self.mg))

class slots(models.Model):
     slot_name=models.CharField(max_length=20,primary_key=True)
     time=models.TimeField(auto_now=False, auto_now_add=False)
     def __str__(self):
          return self.slot_name


class Tablets(models.Model):
     case_id=models.ForeignKey(patient_table,on_delete=models.CASCADE)
     patient_name=models.ForeignKey(login,on_delete=models.CASCADE)
     tablet_name=models.CharField(max_length=1000,primary_key=True)
     slot=models.ForeignKey(slots,on_delete=models.CASCADE)
     quantity=models.ForeignKey(qnty,on_delete=models.CASCADE)
     prescribed=models.ForeignKey(doctors_information,on_delete=models.CASCADE)
     department=models.ForeignKey(department,on_delete=models.CASCADE)
     Comments=models.CharField(max_length=500)
     def __str__(self):
          return (str(self.case_id)+"("+str(self.patient_name)+")")


class appointments(models.Model):
     case_id=models.CharField(max_length=10,primary_key=True)
     name=models.CharField(max_length=200)
     email=models.EmailField()
     mob=models.CharField(max_length=200)
     date=models.DateField()
     dept=models.CharField(max_length=200)
     doc_name=models.CharField(max_length=200)
     def __str__(self):
          return self.case_id


