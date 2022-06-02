from flask import Flask, jsonify, request
from bson.json_util import dumps
import json
import pymongo
from twilio.rest import Client 
import os

app = Flask(__name__)

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://nayra1316:rafa123@cluster0.iqyprre.mongodb.net/?retryWrites=true&w=majority"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str)
myDB = client["Clients"]
myCollection = myDB["clients"]

def getLista():
    lista = list(myCollection.find({}))
    count = 0
    with open('collection.json', 'w') as file:
        file.write('{ "clients" : [')
        for document in lista:
            count+=1
            file.write(dumps(document))
            if count == len(lista):
                break;
            else:
                file.write(',')
        file.write(']}')

def sendMessage(number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body='Tu gas está próximo a vencer, por favor acude a tu banco más cercano a pagarlo!',
                                from_='whatsapp:+14155238886',
                                to='whatsapp:+521'+number
                            )

    print(message.sid)

@app.route("/clients")

def clients():
    getLista()
    x = open('collection.json')
    data = json.load(x)
    return data


@app.route("/sendNotif", methods = ["POST"])

def sendNotif():
    number = request.json
    sendMessage(number['number'])
    return 'received'

@app.route("/turnOffGas", methods = ["POST"])

def turnOffGas():
    print(request.json)
    return 'received'

if __name__ == "__main__":
    app.run(debug=True)
