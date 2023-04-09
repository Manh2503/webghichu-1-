from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
def create_app():
    app=Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Manh250301@localhost/webghichu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models  import User,Note
    
    login_manager=LoginManager()

    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()
    return app



