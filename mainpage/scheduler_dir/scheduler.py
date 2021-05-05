from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
mycursor=mydb.cursor()

def start():
  scheduler = BackgroundScheduler()
  from mainpage.models import slots,patient_table
  ts=slots.objects.all()
  pt=patient_table.objects.all()
  for i in ts:
      #get time and add to job of sending email to the scheduler
        tt=i.time
        scheduler.add_job(printdata, "cron", hour=tt.hour, minute=tt.minute,args=[i.slot_name])
  # scheduler.add_job(printdata, "interval", minutes=1,id="weather_001",replace_existing=True)
  # scheduler.add_job(printdata, "cron", hour='18', minute='01',args=['Evening'])
  for j in pt:
      pt=str(j.next_date)+' 12:35:00' #change the time accordingly
      #scheduling the appointment remainder as prescribed by doctor
      scheduler.add_job(appt_remainder,'date',run_date=pt,args=[j.patient_name_id,j.case_id,j.next_date,j.doctor_id])
  scheduler.start()

def printdata(message):
    print("Now This is a Scheduled Message at :"+message)
    from mainpage.models import Tablets,slots
    from datetime import datetime
    # print(datetime.now())
    obj = Tablets.objects.all()
    for i in obj:
      query="select email,mobile from user_table where username=%s"
      name=(i.patient_name_id,)
      mycursor.execute(query, name)
      myresult = mycursor.fetchall()
      for k in myresult:
          if (i.slot_id == message):
            email=k[0];
            mobilenum=k[1]
            print("Sending Message to " + i.patient_name_id + "at: " + i.slot_id +"on email:"+email+"and mobile number:"+str(mobilenum))
            sendSMS(str(mobilenum),str(i.tablet_name),str(i.quantity_id),message,str(i.prescribed_id))
            sendEmail(str(email),str(i.tablet_name),str(i.quantity_id),message,str(i.prescribed_id))


def sendEmail(emailaddress,tab_name,quantity,message,doctorname):
    import smtplib
    gmail_user = ''
    gmail_password = ''
    sent_from = gmail_user
    to = ['']
    to.append(emailaddress)
    subject = 'Remainder Message for Tablets!!!!!'
    body = 'Remainder!!!!!!!\n\nYour Tablet Name '+tab_name+"\nQuantity: "+quantity+"\nOn: "+message+"\nPrescribed By: "+doctorname

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')

def sendSMS(number,tab_name,quantity,message,doctorname):
    import requests
    url = "https://www.fast2sms.com/dev/bulkV2"
    body = 'Remainder!!!!!!!%0D%0AYour%20Tablet%20Name%20' + tab_name + "%0D%0AQuantity:%20" + quantity + "%0D%0AOn:%20" + message + "%0D%0APrescribed By:%20" + doctorname

    payload = "message="+body+"&language=english&route=q&numbers="+number
    headers = {
        'authorization': "6DGs14AC80NWFpkzMJoyuYcqU7gRrVietjBPaHSmdlhQOKbvX9D2PWyceUTCmv7Sj0kw3AsIrM65oi18",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def appt_remainder(name_param,case_id,date,doctor_name):
    query = "select email,mobile from user_table where username=%s"
    name = (name_param,)
    mycursor.execute(query, name)
    myresult = mycursor.fetchall()
    for k in myresult:
        email=k[0]
        mobile=k[1]
    mobileremainder(mobile,case_id,date,doctor_name)
    emailremainder(email,case_id,date,doctor_name)
    print("Sending the remainder to:"+str(name_param))
def mobileremainder(mobile,case_id,date,doctor_name):
    #This function sends an remainder for appointment
    import requests
    url = "https://www.fast2sms.com/dev/bulkV2"
    body = 'Remainder!!!!!!!%0D%0AYour%20Appointment%20on%20' +str(date) + "%0D%0AFor Case_id%20" + case_id + "%0D%0APrescribed By:%20" + doctor_name

    payload = "message=" + body + "&language=english&route=q&numbers=" + str(mobile)
    headers = {
        'authorization': "",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def emailremainder(email,case_id,date,doctor_name):
    # This function sends an remainder for appointment
    import smtplib
    gmail_user = 'nigampranay7@gmail.com'
    gmail_password = '9985463456'
    sent_from = gmail_user
    to = ['nigampranay7@gmail.com']
    to.append(email)
    subject = 'Remainder Message for Appointment!!!!!'
    body = 'Remainder!!!!!!!\n\nYou Have appointment on: '+str(date)+"\nFor Case_ID: "+case_id+"\nPrescribed By: "+doctor_name

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')
