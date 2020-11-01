from flask import Flask,render_template,request,jsonify,abort
import pandas as pd
import os
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)

CORS(APP)    # api available to all ports

APP.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.sqlite'
db=SQLAlchemy(APP)

# variables
data = dict()
data['uploaded'] = 0
data['invalid'] = 0
data['vendor'] = 0
data['amount'] = 0


def process(df):
    global data
    try:
        df.to_sql(name='invoice', con=db.engine, index=False, if_exists='replace')
        ## validating database columns
        data['uploaded'] = int(db.engine.execute("SELECT COUNT(*) FROM invoice;").fetchall()[0][0])
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
        data['invalid'] = data['uploaded'] - int(db.engine.execute("SELECT COUNT(*) FROM invoice;").fetchall()[0][0])
        data['uploaded'] = int(db.engine.execute("SELECT COUNT(*) FROM invoice;").fetchall()[0][0])
        ## reading directly from database
        df = pd.read_sql(sql="SELECT * from invoice",con=db.engine)
        return df
    except Exception as e:
        return df

@APP.route('/')
def index():
    return render_template("index.html")

@APP.route('/data',methods=['POST'])
def uploadData():
    try:
        inputFile = request.files.get('inputFile',None)
        readFile = pd.read_excel(inputFile)
        df = pd.DataFrame(readFile)
        df = process(df)
        return df.to_html()
    except Exception as e:
        return ' Internal Error for dev '+str(e)

@APP.route('/api/v1',methods=['GET'])
def api():
    global data
    if(request.args.get('query')=='status'):
        try:
            data['vendor'] = int(db.engine.execute("SELECT COUNT(DISTINCT `Vendor Code`) FROM invoice").fetchall()[0][0])
            data['amount'] = int(db.engine.execute("SELECT SUM(`Amt in loc.cur.`) FROM invoice").fetchall()[0][0])
        except Exception as e:
            print('\n Internal Error \n',e)
            data = data.fromkeys(data, 0)
        finally:
            return jsonify(data)
            
    if(request.args.get('query')=='clear'):
        try:
            db.engine.execute("DROP TABLE INVOICE")
            return 'cleared'
        except Exception as e:
            return str(e)

    abort(400)