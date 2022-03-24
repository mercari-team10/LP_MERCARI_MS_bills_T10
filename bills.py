import requests
import json
import os
import sys
import psycopg2
from config import config
from dotenv import load_dotenv
from flask import Flask,request
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import  rsa
import jwt


app = Flask(__name__)

key = None
load_dotenv()

def get_public_key() :
    global key
    r = requests.get(os.environ.get("PUBLIC_KEY_URL"))
    data = r.content
    key = load_pem_public_key(data)

get_public_key()

if key is None :
    print('Unable to retireve public key')
    sys.exit()


conn = None
try:
    # read connection parameters
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    print('Error connecting to Database')
    sys.exit()

# DONE
@app.route("/bills",methods=['GET'])
def get_bills() :
    args = request.get_json()
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['NHID']
    query = f'SELECT * from bills_db WHERE patient_id = %s'
    cur.execute(query,(nhid,))
    result = cur.fetchall()
    return result


# DONE
@app.route("/bills",methods=['POST'])
def add_charges() :
    args = request.get_json()
    hospital_id = args['hospital_id']
    charges = args['charges']
    time = args['time']
    type = args['type']
    url = args['url']
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['NHID']
    query = f'INSERT INTO bills_db(patient_id,hospital_id,time_stamp, cost,name,url) VALUES( %s, %s , to_timestamp(%s) , %d, %s, %s)'
    cur.execute(query,(nhid,hospital_id,time,charges,type,url,))
    return



if __name__ == "__main__":
    app.run(debug=True)
