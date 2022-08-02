import datetime
import json
import  random
import time

import pymysql
from mydb import MySQL

host = 'localhost'
user='root'
password='Asd123dsa'
database='nahry'

db = pymysql.connect(user=user,password=password,database=database)
cus = db.cursor()

def barcodegen():

    while True:
        ran = random.randint(100000,999999)
        cus.execute('select 1 from profile where barcode = %s',(ran,))
        if(cus.rowcount == 0):
            return ran

def insertpatient():  # put application's code here


        first = "request.form['patient_name']"



        gender = 0

        m = 0


        dob = ""

        blood_group = 1

        comment = ""
        address = ""
        phone_no = ""
        occupation = ""
        weight = 0
        height = 0
        religion = ""
        cus.execute('select rgID from religion where rName = %s', (religion,))

        if (cus.rowcount == 0):
            cus.execute('insert into religion ( rName) value (%s)', (religion,))
            rgid = cus.lastrowid
        else:
            rgid = cus.fetchone()[0]



        barcode = barcodegen()

        cID = 8
        middle = ""
        last = "last"
        forth = ""
        cus.execute(
            'insert into profile (firstName, middle, lastName, forthName, address, aID, cID, barcode, gender, bID, married, rgID,daID, comment,occupation) values (%s,%s,%s,%s,%s,4,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (first, middle, last, forth, address, cID, barcode, gender, int(blood_group), m, rgid, 1, comment,
             occupation))
        pid = cus.lastrowid
        cus.execute("insert into impression(pID)values (%s)", (pid,))
        cus.execute("insert into phistory(pID)values (%s)", (pid,))
        if ((phone_no == "") or (phone_no == None)):
            pass
        else:
            cus.execute('insert into phone( pID, phone) value (%s,%s)', (pid, phone_no))

        cus.execute('insert into BMI( pID, weight,height) value (%s,%s,%s)', (pid, weight, height))

        data = json.dumps({"pID": pid, "barcode": barcode})
        db.commit()

        return str(data)


def bookapointments():  # put application's code here


    cID = 8
    date = datetime.datetime.now()

    pid = 8

    pay = 0

    cus.execute('select pID from profile where daID  != 1 and aID = 2 and cID = %s limit 1', (cID,))
    try:
        doc = cus.fetchone()[0]
    except:
        cus.execute('select pID from profile where daID  != 1 and aID = 5 and cID = %s limit 1', (cID,))
        doc = cus.fetchone()[0]

    cus.execute('select 1 from visit where forWhen = %s and patientID = %s and cID = %s and doctorID = %s ',
                (date, pid, cID, doc))
    if (cus.rowcount == 0):
        cus.execute('insert into visit(patientID, doctorID, cID,forWhen) values (%s,%s,%s,%s)', (pid, doc, cID, date))
        viID = cus.lastrowid

        cus.execute("insert into payment(pay, comment, viID) values (%s,'',%s)", (pay, viID))
        cus.execute("insert into  vdetail( viID) value (%s);", (viID,))

    db.commit()

    return str(({'suuv': 'susss'}))

def getpending():



    cID = 8

    date = datetime.datetime.now()
    datenow  =str(date.date())

    cus.execute('select fullname, barcode, pay as daybill, data, viID,pID,allvisit,paid from patientvisit2 where state = 0 and forWhen = date(%s) and cID = %s  ',(datenow,cID))


    return str((cus.fetchall()))


def getdone():

    cID = 8

    date = datetime.datetime.now()
    datenow  =str(date.date())
    cus.execute(
        'select fullname, barcode, pay as daybill, data, viID,pID,allvisit,paid from patientvisit2 where state = 1 and forWhen = date(%s) and cID = %s  ',
        (datenow, cID))

    return str((cus.fetchall()))
def getdata():

    cID = 8

    datenow = str(datetime.datetime.now().date())






    cus.execute(
        'select count(1) as temp from patientvisit where state = 0 and forWhen = date(%s) and cID = %s ',
        (datenow, cID))

    todaynotfinshed = cus.fetchone()[0]
    cus.execute(
        'select count(1) as temp from patientvisit where state = 1 and forWhen = date(%s) and cID = %s ',
        (datenow, cID))
    todayfinshed = cus.fetchone()[0]
    cus.execute(
            'select count(1) as temp from patientvisit where state = 1 and  cID = %s ',
        ( cID,))
    allfinishedvist = cus.fetchone()[0]
    cus.execute(
        'select count(1) as temp from patientvisit where   cID = %s ',
        ( cID,))
    allvisit = cus.fetchone()[0]


    cus.execute(
        'select count(1) as temp from profile where aID = 4 and   cID = %s ',
        ( cID,))
    allpatient = cus.fetchone()[0]





    cus.execute(
        'select count(1) as temp from nonpatient where  cID = %s and forWhen = %s ',
        (cID,datenow))
    allnonp = cus.fetchone()
    try:
        allnonp = int(allnonp[0])
    except:
        allnonp = 0
    allnonp = str(allnonp)





    dmydata= {"tpen":todaynotfinshed,"tcomp":todayfinshed,"tnon":allnonp,'compa':allfinishedvist,'allapp':allvisit,"allpa":allpatient}
    dmydata  = json.dumps(dmydata)
    return str(dmydata)
def gettop():  # put application's code here

    cID = 8

    datenow = str(datetime.datetime.now().date())
    cus.execute(
        'select fullname, viID from patientvisit2 where state = 0 and forWhen = date(%s) and cID = %s  limit 2  ',
        (datenow, cID))
    x = 0
    first = ''
    second = ''

    for i in cus.fetchall():

        if(x == 0):
            first = i
        else:
            second = i
        x += 1
    data = [first, second]
    if second == '':
        data = [first]
    if first == '':
        data = []

    return str(json.dumps(data))
def getdatab():

    cID = 8

    date = datetime.datetime.now()

    datenow  =str(date.date())

    currentdate = str(datetime.datetime.now().date())
    today = r"Today's"
    if datenow != currentdate:
        today = datenow




    cus.execute(
        'select count(1) as me from patientvisit where  forWhen = date(%s) and data > 0 and cID = %s ',
        (datenow, cID))
    nofpt = cus.fetchone()
    try:
        allextrap = int(nofpt[0])
    except:
        allextrap = '0'
    cus.execute(
        'select count(1) as me from patientvisit where  forWhen = date(%s) and pay > 0 and cID = %s ',
        (datenow, cID))
    nofpt = cus.fetchone()
    try:
        allbillp = int(nofpt[0])
    except:
        allbillp = '0'


    cus.execute(
        'select sum(data) as alld,count(1) as me  from patientvisit where  forWhen = date(%s) and cID = %s ',
        (datenow, cID))
    doneextra = cus.fetchone()
    try:
        allextram = str(int(doneextra[0]))


    except:
        allextram = "0"

    cus.execute(
        'select sum(pay) as alld,count(1) as me from patientvisit where  forWhen = date(%s) and cID = %s ',
        (datenow, cID))
    allbill = cus.fetchone()

    try:
        allbillm = str(int(allbill[0]))


    except:
        allbillm = "0"

    dmydata= {"allextram":allextram,"allextrap":allextrap,"allbillm":allbillm,'allbillp':allbillp,'today':today}
    dmydata  = json.dumps(dmydata)

    return str(dmydata)

def getfulldate():


        pid = 6769
        root = []
        surp = []
        cus.execute(
            "select concat(p.firstName, ' ', p.middle, ' ', p.lastName, ' ', p.forthName) as fullname,gender,bID,married,barcode,comment,address,if(p2.phone is null, 0, p2.phone)  as phone,rName,occupation,weight,height,cast(Birthdate as date) as Birthdate from profile p left join (select phID, pID, phone from phonefix group by pID) p2 on p.pID = p2.pID left join (select pID, weight, height from bmifix group by pID) B on p.pID = B.pID, religion r where r.rgID = p.rgID and p.pID =%s",
            (pid,))
        mydata = cus.fetchone()

        anotherdic = {}


        cus.execute('select viID,dob,state from visitfix where  patientID = %s', (pid,))

        for book in cus.fetchall():

            stit = book[2]
            today = datetime.datetime.now().date()
            datenow = datetime.datetime.strptime(str(book[1]), "%Y-%m-%d").date()
            a = 'e'
            if (today == datenow):
                a = 'today'
            if (today > datenow):
                a = 'older'
            if (today < datenow):
                a = 'newer'

            root.append({'viID': book[0], 'dob': book[1], "state": a, 'done': stit})
        surp.append([anotherdic])
        surp.append(root)

        return str(json.dumps(surp))
cycles = 0
while True:
    insertpatient()
    bookapointments()
    getpending()
    getdone()
    getdata()
    gettop()
    getdatab()
    getfulldate()
    print(cycles)
    cycles += 1
    time.sleep(2)