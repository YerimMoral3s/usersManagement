from app import db, bcrypt
from models.User import Users
from models.Business import Business
from models.Tokens import Tokens
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


from app import db, bcrypt

def validate_password_security(password):
    # check if password contains at least 8 characters
    if len(password) < 8:
        return False
    # check if password contains at least 1 uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # check if password contains at least 1 lowercase letter
    if not any(char.islower() for char in password):
        return False
    # check if password contains at least 1 number
    if not any(char.isdigit() for char in password):
        return False
    # check if password contains at least 1 special character
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '}', '[', ']', '|', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '`', '~']
    if not any(char in special_characters for char in password):
        return False
    return True

def save_user(user):
    db.session.add(user)
    db.session.commit()
    return user

def find_user_by_id(id):    
    user = Users.query.filter_by(id=id).first()
    return user

def find_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    return user

def find_business_by_id(business_id):
    business = Business.query.filter_by(id=business_id).first()
    return business

def hash_password(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password

def password_is_correct(password, hashed_password):
    is_correct = bcrypt.check_password_hash(hashed_password, password)
    return is_correct

def save_user_business_association(user_business_association):
    db.session.add(user_business_association)
    db.session.commit()
    return user_business_association

def create_tokens(user_id):
    access_token_expires = timedelta(minutes=10)
    refresh_token_expires = timedelta(days=30)

    # create access token
    access_token = create_access_token(identity=user_id, expires_delta=access_token_expires)
    # create refresh token
    refresh_token = create_refresh_token(identity=user_id, expires_delta=refresh_token_expires)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def save_tokens(user_id, business_id, access_token, refresh_token):
    #create token
    new_tokens = Tokens(user_id=user_id, business_id=business_id, access_token=access_token, refresh_token=refresh_token)
    # save token
    db.session.add(new_tokens)
    db.session.commit()
    return new_tokens

def generate_random_password():
    import random
    import string
    password_characters = string.digits 
    password = ''.join(random.choice(password_characters) for i in range(4))
    return password

def updated_user(user, data):
    user.password_email = data['password_email']
    user.password_email_expire = data['password_email_expire']
    db.session.commit()
    return user

def validate_email(email):
    import re
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    else:
        return False
    
