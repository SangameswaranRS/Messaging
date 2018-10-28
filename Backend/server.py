# Written by Sangameswaran R S #

from flask import Flask, jsonify, make_response, request, json
from flask_cors import CORS, cross_origin
import sys
import pymysql
import hashlib
import time
from Crypto.Cipher import AES
import os
import base64

app =Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
SERVER_PORT=5959
db_name ="messagingapp"
db_host = "localhost"
db_port = 3306
db_user = "root"
db_password = "sanga"
key = os.urandom(16)
print('[INFO] Choosing AES Key as: '+ str(key))
cipher = AES.new(key, AES.MODE_ECB)
pad = '{'

def encryptUserId(userId):
    if len(str(userId)) %16 ==0:
        userIdPadded = userId
    else:
        userIdPadded = str(userId)
        for i in range(0,16-len(str(userId))%16):
            userIdPadded = userIdPadded + pad
    encryptedUserIdInBytes = base64.b64encode(cipher.encrypt(userIdPadded))
    encryptedUserIdInString = encryptedUserIdInBytes.decode('utf-8')
    return encryptedUserIdInString

def decryptUserId(encryptedUserId):
    encryptedUserIdInBytes = encryptedUserId.encode('utf-8')
    decryptedUserId = cipher.decrypt(base64.b64decode(encryptedUserIdInBytes))
    decryptedUserIdInString = decryptedUserId.decode('utf-8')
    return decryptedUserIdInString.strip('{')

@app.route("/test")
def testRoute():
    return make_response("Server Running")

@app.route("/user/signup" , methods=['POST'])
@cross_origin()
def signup():
    try:
        db = pymysql.connect(db_host, db_user, db_password, db_name)
        post_param = json.loads(request.data)
        insert_query = "insert into user values(0, %s, %s, %s);"
        cursor = db.cursor()
        cursor.execute(insert_query,(post_param["username"],post_param["password"],post_param["emailid"]))
        db.commit()
        success ={
            "statusCode":200,
            "message":"User Signed up, Login to continue."
        }
        return make_response(jsonify(success), 200)
    except Exception as e:
        print(e)
        errordict={
            "statusCode":500,
            "message": e.args[1]
        }
        return make_response(jsonify(errordict), 500)

@app.route("/user/login", methods=['POST'])
@cross_origin()
def login():
    try:
        db = pymysql.connect(db_host,db_user,db_password,db_name)
        cursor = db.cursor()
        post_params = json.loads(request.data)
        username = post_params["username"]
        passwordGiven = post_params["password"]
        sql = "select * from user where username = %s"
        cursor.execute(sql,(username))
        results = cursor.fetchall()
        if len(results) == 0:
            # User Not signed up
            userNotSignedUpError ={
                "statusCode": 500,
                "message": "User Not signed up"
            }
            return make_response(jsonify(userNotSignedUpError), 500)
        else:
            userData = results[0]
            if userData is not None:
                userId = userData[0]
                encryptedUserIdInString = encryptUserId(userId)
                if passwordGiven == userData[2]:
                    # Password is correct
                    success={
                        "statusCode": 200,
                        "message": "Logged in",
                        "userId": encryptedUserIdInString
                    }
                    return make_response(jsonify(success), 200)
                else:
                    passwordWrongError ={
                        "statusCode": 500,
                        "message": "wrong password"
                    }
                    return make_response(jsonify(passwordWrongError), 500)
            else:
                userNotSignedUpError ={
                "statusCode": 500,
                "message": "User Not signed up"
                }
                return make_response(jsonify(userNotSignedUpError), 500)
    except Exception as e:
        print(e)
        errordict={
            "statusCode":500,
            "message":e.args[1]
        }
        return make_response(jsonify(errordict), 500)

@app.route("/user/sendMessage", methods=['POST'])
@cross_origin()
def send_message():
    try:
        db = pymysql.connect(db_host, db_user, db_password, db_name)
        cursor = db.cursor()
        post_params = json.loads(request.data)
        userId = decryptUserId(request.headers['uid'])
        destinationUserId = decryptUserId(post_params["destinationUserId"])
        message = post_params["message"]
        messageHash = hashlib.sha512(message.encode()).hexdigest()
        currentEpoch = int(time.time())
        if userId is not None and destinationUserId is not None and message is not None and currentEpoch is not None:
            # Request Valid
            retreiveDestinationUserMessagesQuery = "select * from messages where destinationUID=%s"
            cursor.execute(retreiveDestinationUserMessagesQuery,(destinationUserId))
            destinationUserIdMessages = cursor.fetchall()
            messageFoundFlag = False
            for i in range(0,len(destinationUserIdMessages)):
                induividualMessageTuple = destinationUserIdMessages[i]
                currentMessageHash = induividualMessageTuple[3]
                if currentMessageHash == messageHash:
                    messageFoundFlag = True
            if messageFoundFlag:
                # Message already sent
                messageAlreadySentToUserError = {
                    "statusCode": 500,
                    "message": "Message Already sent to destination User"
                }
                return make_response(jsonify(messageAlreadySentToUserError), 500)
            else:
                # New message
                insertMessageQuery = "insert into messages values(0,%s,%s,%s,%s,%s);"
                cursor.execute(insertMessageQuery,(userId,destinationUserId,messageHash, currentEpoch, message))
                db.commit()
                messageSentResponse={
                    "statusCode":200,
                    "message": "Message Sent"
                }
                return make_response(jsonify(messageSentResponse), 200)
        else:
            badRequestError ={
                "statusCode": 400,
                "message": "Bad Request"
            }
            return make_response(jsonify(badRequestError), 400)
    except Exception as e:
        print(e)
        failureResponse ={
            "statusCode": 500,
            "message": e.args[1]
        }
        return make_response(jsonify(failureResponse), 500)


@app.route("/user/getMessages", methods=['GET'])
@cross_origin()
def get_message():
    try:
        db = pymysql.connect(db_host, db_user, db_password, db_name)
        cursor = db.cursor()
        selectUserMessagesQuery = "select * from messages join user on messages.sourceUID = user.userId where destinationUID=%s;"
        userId = decryptUserId(request.headers['uid'])
        if userId is not None:
            cursor.execute(selectUserMessagesQuery, (userId))
            results = cursor.fetchall()
            resultDict = []
            for i in range(0, len(results)):
                induividualMessageTuple = results[i]
                message = {
                    "messageId": induividualMessageTuple[0],
                    "sourceUID": induividualMessageTuple[1],
                    "destinationUID": induividualMessageTuple[2],
                    "sha512Hash": induividualMessageTuple[3],
                    "messageTimeEpoch": induividualMessageTuple[4],
                    "message": induividualMessageTuple[5],
                    "sender": induividualMessageTuple[7]
                }
                resultDict.append(message)
            successResponse = {
                "statusCode": 200,
                "message": resultDict
            }
            return make_response(jsonify(successResponse), 200)
        else:
            badRequestError = {
                "statusCode": 400,
                "message": "Bad Request"
            }
            return make_response(jsonify(badRequestError), 400)
    except Exception as e:
        print(e)
        failureResponse ={
            "statusCode": 500,
            "message": e.args[1]
        }
        return make_response(jsonify(failureResponse), 500)

@app.route("/user/getUserData", methods=['GET'])
@cross_origin()
def get_user_data():
    try:
        db = pymysql.connect(db_host, db_user, db_password, db_name)
        cursor = db.cursor()
        selectUserDetailsQuery = "select userid, username from user;"
        cursor.execute(selectUserDetailsQuery)
        results = cursor.fetchall()
        users=[]
        for i in range(0, len(results)):
            individualTuple = results[i]
            user = {
                "userId":  encryptUserId(individualTuple[0]),
                "userName": individualTuple[1]
            }
            users.append(user)
        success ={
            "statusCode":200,
            "message": users
        }
        return make_response(jsonify(success), 200)
    except Exception as e:
        error={
            "statusCode":500,
            "message": e.args[1]
        }
        return make_response(jsonify(error), 500)

# Run the server at port 5959
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)
