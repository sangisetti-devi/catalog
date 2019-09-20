from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

#engine=create_engine('sqlite:///rgukt.db')
engine=create_engine('sqlite:///user.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()


app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='n151155@rguktn.ac.in'
app.config['MAIL_PASSWORD']='9553417832'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,9999999)



@app.route("/sample")
def demo():
    return "devi"

    
@app.route("/demo")
def d():
    return "<h1>hello<h1>"


@app.route("/details/<name>/<int:age>/<float:salary>")
def info(name,age,salary):
    return "hai {} age {} salary {}".format(name,age,salary)


@app.route("/admin")
def admin():
    return "hello admin"
@app.route("/student")
def student():
    return "hello student"
@app.route("/staff")
def staff():
    return "hello staff"

@app.route("/info/<name>")
def admin_info(name):
    if name=='admin':
        return redirect(url_for('admin'))
    elif name=='student':
        return redirect(url_for('student'))
    elif name=='staff':
        return redirect(url_for('staff'))
    else: 
        return "no url"



@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_ht(name,age,salary):
    return render_template('sample.html',n=name,a=age,s=salary)


@app.route("/table")
def tab():
           sno=int(input())
           name="devi"
           branch="e3cse"
           dept="cse"
           return render_template('taburl.html',s=sno,n=name,b=branch,d=dept)

data=[{'sno':1,'name':'devi','branch':'it','dept':'cse'},{'sno':2,'name':'ani','branch':'cse','dept':'developer'}]
@app.route("/multiple")
def dummy():
    return render_template('taburl.html',da=data)

@app.route("/table/<int:number>")
def table(number):
    return render_template('tabel.html',n=number)

@app.route("/fileupload")
def fileup():
    return render_template("file.html")
@app.route("/fileupload",methods=['GET','POST'])
def fileupl():
    return render_template("file.html")
@app.route("/success",methods=['GET','POST'])
def success():
    if request.method=='POST':
        f=request.files['file']
        f.save(f.filename)
        return render_template('success.html',f_name=f.filename)



    
@app.route("/email", methods=['POST','GET'])
def eamil_send():
    return render_template('email.html')
@app.route("/email_verify", methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message("ONE time password",sender="n151155@rguktn.ac.in",recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("vemail.html")
@app.route("/email_success",methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "in valid otp"



@app.route("/")
def index():
    return render_template('navigation.html')

@app.route("/show")
@login_required
def showData():
    register=session.query(Register).all()
    return render_template('show.html',reg=register)


@login_required
@app.route("/login",methods=['POST','GET'])
def loginPage():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))
    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()

            if user:
                login_user(user)
                return redirect(url_for('showData'))
            else:
                flash("INvalid login....")
        else:

             return render_template('login.html',title="login") 
    except Exception as e:
        flash("login failed....")
    else:
        return render_template('login.html',title="login") 


@app.route("/account",methods=['POST','GET'])
@login_required
def account():
    return render_template("account.html")


@app.route("/reg",methods=['POST','GET'])
def regpage():
    if request.method=='POST':
        newData=User(name=request.form['name'],
            
            email=request.form['email'],
            password=request.form['password'])
          
        session.add(newData)
        session.commit()
        flash("new data added")
      
        return redirect(url_for('index'))
    else:
         return render_template('register.html') 



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))



@app.route("/Register")
def boot():
     return render_template('register.html') 
@app.route("/navigation")
def nav():
    return render_template('navigation.html')


@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editdata(register_id):
    editeddata=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editeddata.name=request.form['name']
        editeddata.surname=request.form['surname']
        editeddata.mobile=request.form['mobile']
        editeddata.email=request.form['email']
        editeddata.branch=request.form['branch']
        editeddata.role=request.form['role']
        session.add(editeddata)
        session.commit()
        flash("new data is edited of...{}".format(editeddata.name))
        return redirect(url_for('showData'))
    else:
        return render_template('edit.html',register=editeddata)
@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deletedata(register_id):
    deleteddata=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        session.delete(deleteddata)
        session.commit()
        flash(" data is deleted ...{}".format(deleteddata.oldname))

        return redirect(url_for('showData'))
    else:
        return render_template('delete.html',register=deleteddata)





                        


    
     
if __name__=='__main__':
    app.run(debug=True)
