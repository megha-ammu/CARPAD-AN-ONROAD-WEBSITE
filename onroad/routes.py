from msilib.schema import File
from flask import Flask, render_template, request, redirect,send_file,  flash, abort, url_for
from onroad import app,db,mail
from onroad import app,db,mail
from onroad import app
from onroad.models import *
from onroad.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message
from io import BytesIO
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from datetime import datetime as dt
from datetime import datetime,date
# from datetime import timedelta
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'C:/Users/mmegh/Desktop/CARPAD-AN ONROAD WEBSITE/onroad/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from datetime import datetime, timedelta


@app.route('/home')
def home():
    # y=dt.now().year
    # m=dt.now().month
    # d=dt.now().day
    d=str(date.today())
    f=Login.query.filter_by(usertype="user",st="fill").all()
    
    my_str= "24052010"
    date_tup = (int(my_str[4:]),int(my_str[2:4]),int(my_str[:2]))
    g=date(*date_tup)
    # days = datetime. timedelta(5)
    # n = d- days
    n = date.today()-timedelta(days=2)
    h = g-timedelta(days=2)
    return render_template('home.html',d=d,n=n,h=h,f=f) 
    # print(new_date)

    
    # h=Login.query.all()
    # for i in h:
    #     if d<i.next_service:
    #         service_sendmail(i.username,i.next_service)
           
            
    # return render_template('home.html',d=d,h=h)




def service_sendmail(username,next_service):
    h=Login.query.filter_by(usertype="user").all()
    for i in h:
        msg = Message('Service Alert',
                  recipients=[i.username])
        msg.body = f'''Your Next Service Date is on {i.next_service} '''
        mail.send(msg)



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/lessons')
def lessons():
    return render_template("lessons.html")

@app.route('/success')
def success():
    return render_template("success.html")
@app.route('/admin_index')
def admin_index():
    return render_template("admin_index.html")





@app.route('/user_index/<id>')
def user_index(id):
    return render_template("user_index.html")





@app.route('/mechanic_index/<id>')
def mechanic_index(id):
    return render_template("mechanic_index.html")





@app.route('/')
def index():
    d=str(date.today())
    h=Login.query.filter_by(usertype="user",st="fill").all()
    for i in h:
        if (d>=i.service and d<i.next_service):
            service_sendmail(i.username,i.next_service)
    return render_template("index.html")




@app.route('/icons')
def icons():
    return render_template("icons.html")


@app.route('/meet')
def meet():
    return render_template("meet.html")




@app.route('/pswd_success')
def pswd_success():
    return render_template("pswd_success.html")


@app.route('/up_success')
def up_success():
    return render_template("up_success.html")


@app.route('/pay_success')
def pay_success():
    return render_template("pay_success.html")




@app.route('/v_success')
def v_success():
    return render_template("v_success.html")
    



@app.route('/d_success')
def d_success():
    return render_template("d_success.html")






@app.route('/login', methods=["GET","POST"])
def login():

   
    if request.method=="POST":
         username=request.form['username']
         password=request.form['password']
         admin = Login.query.filter_by(username=username, password=password,usertype= 'admin').first()
         mechanic=Login.query.filter_by(username=username,password=password, usertype= 'mechanic',approve='Approved').first()
         user=Login.query.filter_by(username=username,password=password, usertype= 'user').first()
         if admin:
             login_user(admin)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/admin_index') 
        
             
         elif mechanic:
             login_user(mechanic)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/mechanic_index/'+str(mechanic.id))
     
         
         elif user:
             login_user(user)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/user_index/'+str(user.id)) 
         else:
             d="Invalid Username or Password!"
             return render_template("login.html",d=d)


    
    return render_template("login.html")

          
     
    




@app.route('/admin_add_parkingslots',methods=['GET', 'POST'])
def admin_add_parkingslots():
    if request.method == 'POST':
        location = request.form['location']
        address = request.form['address']
        type = request.form['type']
        if type=="Public":
            fee="Free"
        else:
            fee = request.form['fee']
        my_data = ParkingSlot(location=location,address=address,type=type,fee=fee)
        db.session.add(my_data)
        db.session.commit()
        return redirect('/admin_manage_slots')
    else :
        return render_template("admin_add_parkingslots.html")




@app.route('/admin_add_recovery',methods=['GET', 'POST'])
def admin_add_recovery():
    if request.method == 'POST':
        vehicle = request.form['vehicle']
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        my_data = Recovery(vehicle=vehicle,name=name,contact=contact,email=email)
        db.session.add(my_data)
        db.session.commit()
        return redirect('/admin_view_recovery')
    else :
        return render_template("admin_add_recovery.html")




@app.route('/user_register',methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']
        my_data = User(name=name,email=email,contact=contact,password=password,cardno=cardno,cvv=cvv,month=month,year=year,amount=amount)
        my_data1 = Login(name=name,username=email,contact=contact,password=password,usertype="user")
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        flash("Registered successfully! Please Login..")
        return redirect('/login')
        
    else :
        return render_template("user_register.html")




@app.route('/mech_register',methods=['GET', 'POST'])
def mech_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        location = request.form['location']
        password = request.form['password']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        month = request.form['month']
        year = request.form['year']
        amount = request.form['amount']
        my_data = Mechanic(name=name,email=email,location=location,contact=contact,password=password,cardno=cardno,cvv=cvv,month=month,year=year,amount=amount,status="mech")
        my_data1 = Login(name=name,username=email,location=location,contact=contact,password=password,usertype="mechanic",approve="Approve",reject="Reject",status="mech")
        try:

            db.session.add(my_data) 
            db.session.add(my_data1) 
            db.session.commit()
            m_sendmail(email)
        except:
            return "Invalid Username or Password"
            
        d="Your Registeration will be confirmed soon.."
        return render_template("mech_register.html",d=d)
        
    else :
        return render_template("mech_register.html")






@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')



@app.route('/approve/<int:id>')
def approve(id):
    c= Login.query.get_or_404(id)
    c.approve = "Approved"
    c.reject="Reject"
    db.session.commit()
    a_sendmail(c.username)
    return redirect('/admin_view_mechanics')


@app.route('/reject/<int:id>')
def reject(id):
    c= Login.query.get_or_404(id)
    c.reject = 'Rejected'
    c.approve="Approve"
    db.session.commit()
    r_sendmail(c.username)
    return redirect('/admin_view_mechanics')






@app.route('/approve_slot/<int:id>')
def approve_slot(id):
    c= SlotBooking.query.get_or_404(id)
    c.approve = "Approved"
    c.status = "Approved"
    c.reject="Reject"
    db.session.commit()
    apsl_sendmail(c.uemail)
    return redirect('/admin_view_slotbookings')


@app.route('/reject_slot/<int:id>')
def reject_slot(id):
    c= SlotBooking.query.get_or_404(id)
    c.reject = 'Rejected'
    c.status = 'Rejected'
    c.approve="Approve"
    db.session.commit()
    rjsl_sendmail(c.uemail)
    return redirect('/admin_view_slotbookings')

def m_sendmail(email):
    
    msg = Message('Registered Successfully',
                  recipients=[email])
    msg.body = f''' Congratulations , Your  Registeration is completed successfully... Please wait for the Confirmation '''
    mail.send(msg)

def a_sendmail(username):
    
    msg = Message('Approved Successfully',
                  recipients=[username])
    msg.body = f''' Congratulations , Your  Registeration is approved successfully... Now You can login using username and password '''
    mail.send(msg)

def r_sendmail(username):
  
    msg = Message('Registeration Rejected',
                  recipients=[username])
    msg.body = f''' Sorry , Your  Registeration is rejected. '''
    mail.send(msg)




def apsl_sendmail(username):
    
    msg = Message('Approved Successfully',
                  recipients=[username])
    msg.body = f''' Congratulations , Your  Slot Booking is approved successfully... Now You can park your vehicle at your booking time. '''
    mail.send(msg)

def rjsl_sendmail(username):
  
    msg = Message('Slot Booking Rejected',
                  recipients=[username])
    msg.body = f''' Sorry , Your  Slot Booking  is rejected due to unavailability of slots at your booking time. '''
    mail.send(msg)




@login_required
@app.route('/admin_view_mechanics',methods=["GET","POST"])
def admin_view_mechanics():
    obj = Login.query.filter_by(usertype="mechanic",status="mech").all()
    return render_template("admin_view_mechanics.html",obj=obj)




@login_required
@app.route('/admin_view_slotbookings',methods=["GET","POST"])
def admin_view_slotbookings():
    obj = SlotBooking.query.all()
    return render_template("admin_view_slotbookings.html",obj=obj)


@login_required
@app.route('/user_view_mechanics',methods=["GET","POST"])
def user_view_mechanics():
    obj = Login.query.filter_by(usertype="mechanic",approve="Approved").all()
    return render_template("user_view_mechanics.html",obj=obj)



@login_required
@app.route('/user_view_slots',methods=["GET","POST"])
def user_view_slots():
    obj = ParkingSlot.query.all()
    return render_template("user_view_slots.html",obj=obj)


@login_required
@app.route('/admin_view_users',methods=["GET","POST"])
def admin_view_users():
    obj = User.query.all()
    return render_template("admin_view_users.html",obj=obj)




@login_required
@app.route('/user_view_recovery',methods=["GET","POST"])
def user_view_recovery():
    obj = Recovery.query.all()
    return render_template("user_view_recovery.html",obj=obj)



@app.route('/admin_add_mechanics',methods=['GET', 'POST'])
def admin_add_mechanics():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        location = request.form['location']
        password = request.form['password']
        my_data = Mechanic(name=name,email=email,location=location,contact=contact,password=password,status="admin")
        my_data1 = Login(name=name,username=email,location=location,contact=contact,password=password,usertype="mechanic",approve="Approved",status="admin")
        db.session.add(my_data) 
        db.session.add(my_data1) 
        db.session.commit()
        ad_sendmail(email,password)
        # flash("Registered successfully! Please Login..")
        return redirect('/admin_mechanics')
        
    else :
        return render_template("admin_add_mechanics.html")


@app.route('/add_services/<int:id>',methods=['GET', 'POST'])
def add_services(id):
    if request.method == 'POST':
        service = request.form['service']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        my_data = Services(mid=current_user.id,name=name,email=email,contact=contact,service=service)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/manage_services/'+str(current_user.id))
        
    else :
        return render_template("add_services.html")


@login_required
@app.route('/manage_services/<int:id>',methods=["GET","POST"])
def manage_services(id):
    obj = Services.query.filter_by(mid=id).all()
    return render_template("manage_services.html",obj=obj)


@login_required
@app.route('/admin_mechanics',methods=["GET","POST"])
def admin_mechanics():
    obj = Login.query.filter_by(usertype="mechanic",status="admin",approve="Approved").all()
    return render_template("admin_mechanics.html",obj=obj)




@login_required
@app.route('/admin_manage_slots',methods=["GET","POST"])
def admin_manage_slots():
    obj = ParkingSlot.query.all()
    return render_template("admin_manage_slots.html",obj=obj)




@login_required
@app.route('/admin_view_recovery',methods=["GET","POST"])
def admin_view_recovery():
    obj = Recovery.query.all()
    return render_template("admin_view_recovery.html",obj=obj)


@login_required
@app.route('/user_view_services/<int:id>',methods=["GET","POST"])
def user_view_services(id):
    obj = Services.query.filter_by(mid=id).all()
    return render_template("user_view_services.html",obj=obj)


@login_required
@app.route('/parking_slots',methods=["GET","POST"])
def parking_slots():
    return render_template("parking_slots.html")


@app.route('/delete_mechanic/<int:id>')
@login_required
def delete_mechanic(id):
    delet = Login.query.get_or_404(id)
    # d=Mechanic.query.get_or_404(delet.id)
    try:
        db.session.delete(delet)
        # db.session.delete(d)
        db.session.commit()
        return redirect('/admin_mechanics')
    except:
        return 'There was a problem deleting that task'


@app.route('/delete_doc/<int:id>')
@login_required
def delete_doc(id):
    delet = Alldocs.query.get_or_404(id)
    
    # try:
    db.session.delete(delet)
    # os.remove(delet.filename)
    delet.status=''
    db.session.commit()
    return redirect('/d_success')
    # except:
    #     return 'There was a problem deleting that task'




# @app.route('/delete_pollution/<int:id>')
# @login_required
# def delete_pollution(id):
#     delet = PDocuments.query.get_or_404(id)
#     # d=Mechanic.query.get_or_404(delet.id)
#     try:
#         db.session.delete(delet)
#         delet.status=''
#         # db.session.delete(d)
#         db.session.commit()
#         return redirect('/d_success')
#     except:
#         return 'There was a problem deleting that task'

    

# @app.route('/delete_insurance/<int:id>')
# @login_required
# def delete_insurance(id):
#     delet = IDocuments.query.get_or_404(id)
#     # d=Mechanic.query.get_or_404(delet.id)
#     try:
#         db.session.delete(delet)
#         delet.status=''
#         # db.session.delete(d)
#         db.session.commit()
#         return redirect('/d_success')
#     except:
#         return 'There was a problem deleting that task'


@app.route('/delete_recovery/<int:id>')
@login_required
def delete_recovery(id):
    delet = Recovery.query.get_or_404(id)
    # d=Mechanic.query.get_or_404(delet.id)
    try:
        db.session.delete(delet)
        # db.session.delete(d)
        db.session.commit()
        return redirect('/admin_view_recovery')
    except:
        return 'There was a problem deleting that task'




@app.route('/delete_slot/<int:id>')
@login_required
def delete_slot(id):
    delet = ParkingSlot.query.get_or_404(id)
    # d=Mechanic.query.get_or_404(delet.id)
    try:
        db.session.delete(delet)
        # db.session.delete(d)
        db.session.commit()
        return redirect('/admin_manage_slots')
    except:
        return 'There was a problem deleting that task'



@app.route('/delete_service/<int:id>')
@login_required
def delete_service(id):
    delet = Services.query.get_or_404(id)
    # d=Mechanic.query.get_or_404(delet.id)
    try:
        db.session.delete(delet)
        # db.session.delete(d)
        db.session.commit()
        return redirect('/manage_services/'+str(current_user.id))
    except:
        return 'There was a problem deleting that task'




def ad_sendmail(email,password):
    msg = Message(' Successfully Added',
                  recipients=[email])
    msg.body = f''' You can login using your Email ID and  Your Password is, {password}  '''
    mail.send(msg)






@app.route('/user_request_service/<id>/<uid>',methods=['GET', 'POST'])
def user_request_service(id,uid):
    y=Services.query.filter_by(id=id).first()
    m=Login.query.filter_by(id=y.mid).first()
    u=Login.query.filter_by(id=uid).first()
    if request.method == 'POST':
        mid = request.form['mid']
        uid = request.form['uid']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        mname = request.form['mname']
        memail = request.form['memail']
        mcontact = request.form['mcontact']
        service=request.form['service']
        my_data = ServiceBooking(mid=mid,uid=uid,name=name,email=email,contact=contact,mname=mname,status="Not Paid",memail=memail,mcontact=mcontact,service=service)
        db.session.add(my_data) 
        db.session.commit()
        buk_sendmail(email)
        mbuk_sendmail(memail)
        
        return redirect('/payment/'+str(my_data.id))
        
    else :
        return render_template("user_request_service.html",m=m,u=u,y=y)




@app.route('/payment/<int:id>',methods=["GET","POST"])
def payment(id):
    c= ServiceBooking.query.get_or_404(id)
    if request.method == 'POST':
        c.cardno =  request.form['cardno']
        c.month =  request.form['month']
        c.year =  request.form['year']
        c.cvv =  request.form['cvv']
        c.amount =  request.form['amount']
        c.status="Success"
        db.session.commit()
        p_sendmail(c.email)
        mp_sendmail(c.memail)
        return redirect('/success')
    else:
        return render_template('payment.html',c=c)



@app.route('/pay_slot/<int:id>',methods=["GET","POST"])
def pay_slot(id):
    c= SlotBooking.query.get_or_404(id)
    if request.method == 'POST':
        c.cardno =  request.form['cardno']
        c.month =  request.form['month']
        c.year =  request.form['year']
        c.cvv =  request.form['cvv']
        c.amount =  request.form['amount']
        c.pstatus="Paid"
        db.session.commit()
        pay_sendmail(c.uemail)
        # mp_sendmail(c.memail)
        return redirect('/pay_success')
    else:
        return render_template('pay_slot.html',c=c)




@app.route('/edit_slot/<int:id>',methods=["GET","POST"])
def edit_slot(id):
    c= ParkingSlot.query.get_or_404(id)
    if request.method == 'POST':
        c.location =  request.form['location']
        c.address =  request.form['address']
        c.type =  request.form['type']
        c.fee =  request.form['fee']
        db.session.commit()
        return redirect('/admin_manage_slots')
    else:
        return render_template('edit_slot.html',c=c)




@app.route('/edit_recovery/<int:id>',methods=["GET","POST"])
def edit_recovery(id):
    c= Recovery.query.get_or_404(id)
    if request.method == 'POST':
        c.vehicle =  request.form['vehicle']
        c.name =  request.form['name']
        c.email =  request.form['email']
        c.contact =  request.form['contact']
        db.session.commit()
        return redirect('/admin_view_recovery')
    else:
        return render_template('edit_recovery.html',c=c)

def buk_sendmail(email):
  
    msg = Message('Booking Successful',
                  recipients=[email])
    msg.body = f''' Your Booking is Successful '''
    mail.send(msg)

def pay_sendmail(uemail):
  
    msg = Message('Payment Successful',
                  recipients=[uemail])
    msg.body = f''' Your Payment is Successful '''
    mail.send(msg)

def mbuk_sendmail(memail):
  
    msg = Message('New User Request',
                  recipients=[memail])
    msg.body = f''' You have new user reuest. Please Login to view more details'''
    mail.send(msg)


def p_sendmail(email):
  
    msg = Message('Payment Successful',
                  recipients=[email])
    msg.body = f''' Your Payment is Successful '''
    mail.send(msg)

def mp_sendmail(memail):
  
    msg = Message('Payment Received',
                  recipients=[memail])
    msg.body = f''' Login to view more details '''
    mail.send(msg)



@login_required
@app.route('/user_view_payments/<int:id>',methods=["GET","POST"])
def user_view_payments(id):
    obj = ServiceBooking.query.filter_by(uid=id,status="Success").all()
    return render_template("user_view_payments.html",obj=obj)



@login_required
@app.route('/user_view_slotbookings/<int:id>',methods=["GET","POST"])
def user_view_slotbookings(id):
    obj = SlotBooking.query.filter_by(uid=id).all()
    return render_template("user_view_slotbookings.html",obj=obj)




@login_required
@app.route('/mechanic_view_payments/<int:id>',methods=["GET","POST"])
def mechanic_view_payments(id):
    obj = ServiceBooking.query.filter_by(mid=id,status="Success").all()
    return render_template("mechanic_view_payments.html",obj=obj)





@login_required
@app.route('/admin_view_payments',methods=["GET","POST"])
def admin_view_payments():
    obj = ServiceBooking.query.filter_by(status="Success").all()
    return render_template("admin_view_payments.html",obj=obj)





@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        my_data = Contact(name=name, email=email,message=message)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/')
    else :
        return render_template("contact.html")




@login_required
@app.route('/user_contact/<id>', methods = ['GET','POST'])
def user_contact(id):
    d=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        my_data = Contact(name=name, email=email,message=message)
        db.session.add(my_data) 
        db.session.commit()
   
        return redirect('/user_index/'+str(current_user.id))
    else :
        return render_template("user_contact.html",d=d)




@login_required
@app.route('/mech_contact/<id>', methods = ['GET','POST'])
def mech_contact(id):
    d=Login.query.filter_by(id=id).first()
 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        my_data = Contact(name=name, email=email,message=message)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/mechanic_index/'+str(current_user.id))
    else :
        return render_template("mechanic_contact.html",d=d)




@login_required
@app.route('/admin_view_feedbacks',methods=["GET","POST"])
def admin_view_feedbacks():
    obj = Contact.query.all()
    return render_template("admin_view_feedbacks.html",obj=obj)





@app.route('/user_profile/<int:id>',methods=["GET","POST"])
@login_required
def user_profile(id):
    d = Login.query.get_or_404(id)
    return render_template("user_profile.html",d=d)



@app.route('/all_documents/<int:id>',methods=["GET","POST"])
@login_required
def all_documents(id):
    d=Alldocs.query.filter_by(uid=id).all()
    # e=PDocuments.query.filter_by(uid=id).all()
    # f=IDocuments.query.filter_by(uid=id).all()
    return render_template("all_documents.html",d=d)



@app.route('/edit_profile/<int:id>',methods=["GET","POST"])
@login_required
def edit_profile(id):
    d = Login.query.get_or_404(id)
    if request.method == 'POST':
        
        d.name = request.form['name']
        d.username = request.form['username']
        d.contact = request.form['contact']
        db.session.commit()
        return redirect('/user_profile/'+str(d.id))
    return render_template("edit_profile.html",d=d)




@app.route('/vehicle_details/<int:id>',methods=["GET","POST"])
@login_required
def vehicle_details(id):
    d = Login.query.get_or_404(id)
    if request.method == 'POST':
        
        d.vehicle = request.form['vehicle']
        d.vehicle_no = request.form['vehicle_no']
        d.last_service = request.form['last_service']
        d.next_service = request.form['next_service']
        d.last_pollution = request.form['last_pollution']
        d.next_pollution = request.form['next_pollution']
        y=d.next_service
        date_tup = (int(y[:4]),int(y[5:7]),int(y[8:]))
        g=date(*date_tup)

        d.service=g-timedelta(days=2)
        d.st="fill"
        db.session.commit()
        return redirect('/v_success')
    return render_template("vehicle_details.html",d=d)




@app.route('/change_password/<int:id>',methods=["GET","POST"])
@login_required
def change_password(id):
    d = Login.query.get_or_404(id)
    if request.method == 'POST':
        
        d.password = request.form['password']
        db.session.commit()
        return redirect('/pswd_success')
    return render_template("change_password.html",d=d)



@app.route('/upload_documents/<int:id>',methods=["GET","POST"])
@login_required
def upload_documents(id):
    d=Login.query.filter_by(id=id).first()
    l=Alldocs.query.filter_by(uid=id,st="l").first()
    i=Alldocs.query.filter_by(uid=id,st="i").first()
    p=Alldocs.query.filter_by(uid=id,st="p").first()
    return render_template("upload_documents.html",d=d,l=l,p=p,i=i)



@app.route('/upload_license/<int:id>',methods=["GET","POST"])
@login_required
def upload_license(id):
    d=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        uid=request.form['uid']
        license = request.files['license']
        if license:
            filename = license.filename
            license.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        obj=Documents(uid=uid,license=license.filename,license_data=license.read(),status="Uploaded")
        obj1=Alldocs(uid=uid,filename=license.filename,data=license.read(),st="l",status="Uploaded")
        db.session.add(obj1)
        db.session.add(obj)
        db.session.commit()
        return redirect('/up_success')
    return render_template("upload_license.html",d=d)



@app.route('/upload_pollution/<int:id>',methods=["GET","POST"])
@login_required
def upload_pollution(id):
    d=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        uid=request.form['uid']
        pollution = request.files['pollution']
        if pollution:
            filename = pollution.filename
            pollution.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        obj=PDocuments(uid=uid,pollution=pollution.filename,pollution_data=pollution.read(),status="Uploaded")
        obj1=Alldocs(uid=uid,filename=pollution.filename,data=pollution.read(),st="p",status="Uploaded")
        db.session.add(obj1)
        db.session.add(obj)
        db.session.commit()
        return redirect('/up_success')
    return render_template("upload_pollution.html",d=d)



@app.route('/upload_insurance/<int:id>',methods=["GET","POST"])
@login_required
def upload_insurance(id):
    d=Login.query.filter_by(id=id).first()
    if request.method == 'POST':
        uid=request.form['uid']
        insurance = request.files['insurance']
        if insurance:
            filename = insurance.filename
            insurance.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        obj=IDocuments(uid=uid,insurance=insurance.filename,insurance_data=insurance.read(),status="Uploaded")
        obj1=Alldocs(uid=uid,filename=insurance.filename,data=insurance.read(),st="i",status="Uploaded")
        db.session.add(obj1)
        db.session.add(obj)
        db.session.commit()
        return redirect('/up_success')
    return render_template("upload_insurance.html",d=d)






@app.route('/user_book_slot/<id>/<pid>',methods=['GET', 'POST'])
def user_book_slot(id,pid):
    u=Login.query.filter_by(id=id).first()
    p=ParkingSlot.query.filter_by(id=pid).first()
    if request.method == 'POST':
        pid = request.form['pid']
        uid = request.form['uid']
        uname = request.form['uname']
        uemail = request.form['uemail']
        ucontact = request.form['ucontact']
        location = request.form['location']
        address = request.form['address']
        type = request.form['type']
        # noh = request.form['noh']
        fee=request.form['fee']
        # amount=request.form['amount']
        vehicle=request.form['vehicle']
        buk_date=request.form['buk_date']
        from_time=request.form['from_time']
        to_time=request.form['to_time']
        my_data = SlotBooking(pid=pid,uid=uid,uname=uname,pstatus="PAY",to_time=to_time,from_time=from_time,uemail=uemail,vehicle=vehicle,ucontact=ucontact,location=location,address=address,type=type,fee=fee,buk_date=buk_date,approve="Approve",reject="Reject",status="Waiting for Confirmation")
        db.session.add(my_data) 
        db.session.commit()
        slot_usendmail(uemail)
        # slot_asendmail(memail)
        
        return redirect('/user_view_slotbookings/'+str(my_data.uid))
        
    else :
        return render_template("user_book_slot.html",u=u,p=p)




def slot_usendmail(email):
  
    msg = Message('Booking Successful',
                  recipients=[email])
    msg.body = f''' Your Slot Booking is Successful.Please wait for the Confirmation '''
    mail.send(msg)




@app.route('/download_doc/<id>')
def download_license(id):
    upload = Alldocs.query.get_or_404(id)
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True) 



# @app.route('/download_pollution/<id>')
# def download_pollution(id):
#     upload = Alldocs.query.query.get_or_404(id)
#     return send_file(BytesIO(upload.pollution_data), attachment_filename=upload.pollution, as_attachment=True) 



# @app.route('/download_insurance/<id>')
# def download_insurance(id):
#     upload = Alldocs.query.query.get_or_404(id)
#     return send_file(BytesIO(upload.insurance_data), attachment_filename=upload.insurance, as_attachment=True) 



