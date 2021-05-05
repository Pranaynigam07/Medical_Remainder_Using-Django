from django.shortcuts import render,redirect
from .models import patient_table,Tablets,doctors_information,department,appointments
from cryptography.fernet import Fernet
from django.contrib import messages

import mysql.connector
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
mycursor=mydb.cursor()
print("hello")
#related to encryption and decryption
#######IMPORTANT DO NOT DISTURB THE BELOW CODE########
key=Fernet.generate_key()
suite=Fernet(key)


# Create your views here.

def index(request):
    return render(request,"index.html")

def login(request):
    if(request.method == "POST"):
        name=request.POST['user']
        pswd=request.POST['pass']
        query='select * from mainpage_login'
        mycursor.execute(query)
        res_set=mycursor.fetchall()
        flag=0
        for x in res_set:
            if(name in x):
                username=x
                flag+=1
        if(flag==0):
            print("user does not exists")
            messages.error(request,"User does not exists")
            #changes need to be done here
            return redirect('login')
        else:
            bytes_of_arr=str.encode(username[1])
            suite=Fernet(str.encode(username[2]))
            dec_pswd=(suite.decrypt(bytes_of_arr)).decode()
            if(name in username and pswd==dec_pswd):
                print("Username and passwords are matched")
                query='select username from user_table where username=%s'
                val=(name,)
                mycursor.execute(query,val)
                resultobject= mycursor.fetchall()
                for x in resultobject:
                    for j in x:
                        print(j)
                #taking the data and sending the data
                obj=patient_table.objects.all()
                tab_details=Tablets.objects.all()
                doctors_info=doctors_information.objects.all()
                dept=department.objects.all()
                obj1 = appointments.objects.all()
                return render(request,'userlogin.html',{'object1':j,'patient':obj,'tablet_details':tab_details,'dept':dept,'doc':doctors_info,'apt':obj1})
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('login')

    else:
        return render(request,"login.html")


def signup(request):
    if (request.method == "POST"):
        name = request.POST['username']
        pswd = request.POST['psswd']
        retype = request.POST['retype']
        email = request.POST['email']
        mobile = request.POST['mobile']
        if(pswd==retype):
            query='insert into user_table values(%s,%s,%s,%s,%s)'
            val=(name,pswd,email,mobile,key)
            mycursor.execute(query,val)
            mydb.commit()
            query='insert into mainpage_login values(%s,%s,%s)'
            pswd=suite.encrypt(str.encode(pswd))
            val=(name,pswd,key)
            mycursor.execute(query,val)
            mydb.commit()
            messages.success(request,"SignUp Successful")
            return redirect('login')
        else:
            messages.error(request,"Passwords mismatch")
            return redirect('login')



def userlogin(request):
    return render(request,"userlogin.html")

def appointment(request):
    if (request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        mob = request.POST['phone']
        dat = request.POST['date']
        depart = request.POST['department']
        doc = request.POST['doctor']
        obj = appointments.objects.all()
        for j in obj:
            latest_id = j.case_id
        lastnum=int(latest_id[5])+1
        new_id=latest_id[0:5]+str(lastnum)
        p=appointments(case_id=new_id,name=name,email=email,mob=mob,date=dat,dept=depart,doc_name=doc)
        p.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])

def userlogout(request):
    return redirect('/')
