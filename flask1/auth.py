from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import  db
from flask_login import login_user,login_required,logout_user,current_user
auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Dang nhap thanh cong',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))

            else:
                flash('Sai mat khau ',category='error')
        
        else:
            flash('Email khong dung voi bat ki tai khoan nao',category='error' )
    
    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        yourname=request.form.get('yourname')
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email da duoc su dung',category='error')

        if len(email)<4:
            flash('email can nhieu hon 3 ki tu', category='error')
        elif len(yourname)<2:
            flash('ten can nhieu hon 1 ki tu', category='error')
        elif password1!=password2:
            flash('mat khau nhap lai khong dung',category='error')
        elif len(password1)<7:
            flash('mat khau can it nhat 8 ki tu',category='error')
        else:
            new_user =User(email=email,username=yourname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('tai khoan duoc tao thanh cong',category='success')
            return redirect(url_for('views.home'))
     

    
    return render_template('sign_up.html',user=current_user)

