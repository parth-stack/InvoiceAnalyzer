from flask import Flask,render_template,request,jsonify,abort
import pandas as pd
import os
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


###########################################################################################################################

APP = Flask(__name__)

CORS(APP)    # api available to all ports

APP.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.sqlite'
db=SQLAlchemy(APP)

class Data(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    uploaded=db.Column(db.Integer)
    invalid=db.Column(db.Integer)
    vendor=db.Column(db.Integer)
    amount=db.Column(db.Integer)

with APP.app_context():
    # create new instance of db or brings old db.
    # only required for local db.sqlite file
    db.create_all()

###########################################################################################################################

def process(df):
    try:
        df.to_sql(name='invoice', con=db.engine, index=False, if_exists='replace')
        ## validating database columns
        temp1 = int(db.engine.execute("SELECT COUNT(*) FROM invoice;").fetchall()[0][0])
        db.engine.execute('''DELETE FROM invoice WHERE `Invoice Numbers` IN (
                            SELECT `Invoice Numbers` FROM 
                            (
                              SELECT `Invoice Numbers`, COUNT(*) AS CNT
                              FROM invoice
                              GROUP BY `Invoice Numbers`
                              HAVING `CNT`>1
                            )
                          );
        ''')
        temp2 = int(db.engine.execute("SELECT COUNT(*) FROM invoice;").fetchall()[0][0])
        temp3 = temp1 - temp2
        dat = Data.query.all()[0]
        dat.uploaded += temp2
        dat.invalid += temp3
        dat.vendor += int(db.engine.execute("SELECT COUNT(DISTINCT `Vendor Code`) FROM invoice").fetchall()[0][0])
        dat.amount += int(db.engine.execute("SELECT SUM(`Amt in loc.cur.`) FROM invoice").fetchall()[0][0])
        db.session.commit()
        
        ## reading directly from database
        df = pd.read_sql(sql="SELECT * from invoice",con=db.engine)
        return df
    except Exception as e:
        print('\n process \n',e)
        return df

###########################################################################################################################

@APP.route('/')
def index():
    return render_template("index.html")

###########################################################################################################################


@APP.route('/data',methods=['POST'])
def uploadData():
    try:
        inputFile = request.files.get('inputFile',None)
        readFile = pd.read_excel(inputFile)
        df = pd.DataFrame(readFile)
        df = process(df)
        return df.to_html()
    except Exception as e:
        return ' /data '+str(e)


###########################################################################################################################

@APP.route('/api/v1',methods=['GET'])
def api():
    if(request.args.get('query')=='status'):
        # entry = Data(uploaded=0,invalid=0,vendor=0,amount=0)
        # db.session.add(entry)
        # db.session.commit()
        data = dict()
        try:
            dat = Data.query.all()[0]
            # print(dat)
            data['uploaded'] = dat.uploaded
            data['invalid'] = dat.invalid
            data['vendor'] = dat.vendor
            data['amount'] = dat.amount
        except Exception as e:
            print('\n /api/v1 \n',e)
        finally:
            return jsonify(data)
            
    if(request.args.get('query')=='clear'):
        try:
            dat = Data.query.all()[0]
            dat.uploaded = 0
            dat.invalid = 0
            dat.vendor = 0
            dat.amount = 0
            db.session.commit()
            db.engine.execute("DROP TABLE INVOICE")
            return 'cleared'
        except Exception as e:
            return str(e)

    abort(400)


###########################################################################################################################