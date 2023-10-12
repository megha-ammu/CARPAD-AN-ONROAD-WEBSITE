from enum import unique
from ssl import _create_unverified_context
from onroad import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))



class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80), nullable=False)
    usertype = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    approve = db.Column(db.String(200))
    reject = db.Column(db.String(200))
    status = db.Column(db.String(200))
    location = db.Column(db.String(200),default='')
    last_service = db.Column(db.String(50),default='')
    next_service = db.Column(db.String(50),default='')
    last_pollution = db.Column(db.String(50),default='')
    next_pollution = db.Column(db.String(50),default='')
    vehicle = db.Column(db.String(50),default='')
    vehicle_no = db.Column(db.String(50),default='')
    service = db.Column(db.String(50),default='')
    st = db.Column(db.String(50),default='')
  
class Documents(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    license = db.Column(db.String(50))
    license_data = db.Column(db.LargeBinary)
    status = db.Column(db.String(50),default='')



class PDocuments(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    pollution = db.Column(db.String(50))
    pollution_data = db.Column(db.LargeBinary)
    status = db.Column(db.String(50),default='')


class IDocuments(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    insurance = db.Column(db.String(50))
    insurance_data = db.Column(db.LargeBinary)
    status = db.Column(db.String(50),default='')




class Alldocs(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50))
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    status = db.Column(db.String(50),default='')
    st=db.Column(db.String(50),default='')

    


class Mechanic(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    email = db.Column(db.String(200),unique=True)
    contact = db.Column(db.String(200))
    location = db.Column(db.String(200))
    password = db.Column(db.String(200))
    cardno = db.Column(db.String(200),unique=True)
    amount =db.Column(db.String(200))
    cvv=db.Column(db.String(200))
    month=db.Column(db.String(200))
    year=db.Column(db.String(200))
    status = db.Column(db.String(200))
   



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    password = db.Column(db.String(200))
    cardno = db.Column(db.String(200),unique=True)
    amount =db.Column(db.String(200))
    cvv=db.Column(db.String(200))
    month=db.Column(db.String(200))
    year=db.Column(db.String(200))

   


class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    email= db.Column(db.VARCHAR)
    message= db.Column(db.String(200))





class ParkingSlot(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(200))
    address= db.Column(db.VARCHAR)
    type= db.Column(db.String(200))
    fee= db.Column(db.String(200))



class Services(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    mid= db.Column(db.String(200))
    service = db.Column(db.String(200))
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))




class ServiceBooking(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    mid= db.Column(db.String(200))
    uid= db.Column(db.String(200))
    service = db.Column(db.String(200))
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    mname = db.Column(db.String(200))
    memail = db.Column(db.String(200))
    mcontact = db.Column(db.String(200))
    cardno = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    month = db.Column(db.String(200))
    year = db.Column(db.String(200))
    amount = db.Column(db.String(200))
    status = db.Column(db.String(200))



class SlotBooking(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pid= db.Column(db.String(200))
    uid= db.Column(db.String(200))
    uname = db.Column(db.String(200))
    uemail = db.Column(db.String(200))
    ucontact = db.Column(db.String(200))
    location = db.Column(db.String(200))
    address = db.Column(db.String(200))
    type = db.Column(db.String(200))
    fee = db.Column(db.String(200))
    vehicle = db.Column(db.String(200))
    from_time = db.Column(db.String(200))
    to_time = db.Column(db.String(200))
    buk_date = db.Column(db.String(200))
    approve = db.Column(db.String(200))
    reject = db.Column(db.String(200))
    status = db.Column(db.String(200))
    pstatus = db.Column(db.String(200))
    cardno = db.Column(db.String(200))
    cvv = db.Column(db.String(200))
    month = db.Column(db.String(200))
    year = db.Column(db.String(200))
    amount = db.Column(db.String(200))







class Recovery(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    vehicle= db.Column(db.String(200))
    name= db.Column(db.String(200))
    email = db.Column(db.String(200))
    contact = db.Column(db.String(200))
 



