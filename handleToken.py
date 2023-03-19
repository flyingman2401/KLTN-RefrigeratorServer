from datetime import datetime, timedelta
import databaseAccess
import jwt

def checkToken(token, secretKey, userInformationCollection):
    data = jwt.decode(token, key=secretKey, algorithms="HS256", options={"verify_signature": True})
    email = data['email']
    exp = data['exp']
    
    user = databaseAccess.findUser(userInformationCollection, email)
    if not user or user['token'] != token:
        return None
        
    if datetime.utcnow().timestamp() > exp:
        return None
    
    return email

def generateToken(email, secretKey, userCollection):
    token = jwt.encode(
        {
            'email': email,
            'exp' : datetime.utcnow() + timedelta(days = 7)
        }, 
        secretKey
    )
    if databaseAccess.saveUserToken(userCollection, email, token):
        return token
    else:
        return None
