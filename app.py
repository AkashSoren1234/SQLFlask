from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:soren1234@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://vkifoffpqmpmcu:04a8d9e491193fb5beeb63ba3bede8e6debf7b6c768149125e51b32d73b0b138@ec2-52-7-39-178.compute-1.amazonaws.com:5432/den8k952esq9q3?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model): #databse model
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_ #if u dont give self, then it will pass null values to the database

@app.route("/")  #'@' is a function decorater
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])  #'@' is a function decorater
def success():
    if request.method=='POST': #sometimes we may get get method, to avoid that and take only post method we use if.
        email=request.form["email_name"]
        height=request.form["height_name"]
        #print(request.form)
        print(email,height)
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html")
        else:
            return render_template('index.html',
            text="This email already exits. Give another one!")
    #return render_template('index.html',
    #text="This email already exits. Give another one!")



if __name__=='__main__':
    app.debug=True
    app.run()
