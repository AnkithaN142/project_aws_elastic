from flask import Flask,request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid


import numpy as np
import joblib

appy1 = Flask(__name__)

appy1.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:save1save@prop1.c2ohsocoqvbm.ap-south-1.rds.amazonaws.com/flaskaws'
appy1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(appy1)

class Forest(db.Model):
    Id=db.Column(db.Integer,primary_key=True)
    FFMC = db.Column(db.Float)
    DMC= db.Column(db.Float)
    DC=db.Column(db.Float)
    ISI=db.Column(db.Float)
    Temperature=db.Column(db.Float)
    RH=db.Column(db.Float)
    Wind=db.Column(db.Float)
    Rain=db.Column(db.Float)

    def __init__(self,Id,FFMC,DMC,DC,ISI,Temperature,RH,Wind,Rain):
        self.Id=Id
        self.FFMC=FFMC
        self.DC=DC
        self.DMC=DMC
        self.ISI=ISI
        self.Temperature=Temperature
        self.RH=RH
        self.Wind=Wind
        self.Rain=Rain

class Notify(db.Model):
        Sl = db.Column(db.Integer, primary_key=True)
        Name = db.Column(db.String(100),nullable=False),
        Phone = db.Column(db.Integer),
        Place=db.Column(db.String)

        def __init__(self,Sl,Name,Phone,Place):
            self.Sl=Sl
            self.Name=Name
            self.Phone=Phone
            self.Place=Place


model=joblib.load('forestfiremodel.pkl')

@appy1.route('/')
def hello_world():
    return render_template("index.html")

@appy1.route('/page')
def hello():
    return render_template("pre.html")

@appy1.route('/page1')
def next():
    return render_template("prep1.html")


@appy1.route('/page',methods=['POST','GET'])
def predict():

    # if request.method == "Post":
    #     forest = Forest(
    #         FFMC=request.form.get('value1'),
    #         DMC=request.form.get('value2'),
    #         DC=request.form.get('value3'),
    #         ISI=request.form.get('value4'),
    #         Temprature=request.form.get('value5'),
    #         RH=request.form.get('value6'),
    #         Wind=request.form.get('value7'),
    #         Rain=request.form.get('value8')
    #
    #     )
    #     print(forest)
    #     db.session.add(forest)
    #     db.session.commit()
    val0=0
    val1=0
    val2=0
    val3=0
    val4=0
    val5=0
    val6=0
    val7=0
    val8=uuid.uuid1()
    int_features=[float(x) for x in request.form.values()]

    final=[np.array(int_features)]
    for x in final:
        val0=x[0]
        val1=x[1]
        val2=x[2]
        val3=x[3]
        val4=x[4]
        val5=x[5]
        val6=x[6]
        val7=x[7]

    forest = Forest(
                Id=val8,
                FFMC=val0,
                DMC=val1,
                DC=val2,
                ISI=val3,
                Temperature=val4,
                RH=val5,
                Wind=val6,
                Rain=val7

            )

    db.session.add(forest)
    db.session.commit()

    print(int_features)
    print(final)
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)


    if (output>str(0.5) and output<str(0.7)):
        return render_template('pre.html',pred='There is a risk.\nProbability of fire occuring is {}'.format(output))
    elif output>str(0.7):
        return render_template('pre.html',pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output))
    else:
        return render_template('pre.html',pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output))




@appy1.route('/page1',methods=['POST','GET'])
def nexter():
    value0 = uuid.uuid1()
    value1 = 0
    value2 = 0
    value3 = 0
    if request.method == "POST":
        Name = request.form.get("value1")
        notify = Notify(

            Sl=value0,
            Name= request.form.get("value1"),
            Phone= request.form.get("value2"),
            Place= request.form.get("value3"),
        )
        db.session.add(notify)
        db.session.commit()
        print(Name)

    return render_template("prep1.html",out='Thanks for notifiying us')




if __name__ == '__main__':
    appy1.run(debug=True)