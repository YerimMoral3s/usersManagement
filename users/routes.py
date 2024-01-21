from flask import Blueprint, jsonify, request
from models.User import Users
from models.User_business_association import UserBusinessAssociation
from users.Utils import *
from datetime import timedelta, datetime


users_bp = Blueprint('api', __name__)

#TEST
@users_bp.route('/test', methods=['GET'])
def test():
    return jsonify(message='test'), 200

# Create user with email and password
@users_bp.route('/email_ps/<int:business_id>', methods=['POST'])
def create_user_email_ps(business_id):
    try:
        data = request.get_json()
        new_email = data['email']
        new_password = data['password']

        #validate email
        if not validate_email(new_email):
            return jsonify(message='Email is required'), 400 

        # check if the email already exists
        user_exists = find_user_by_email(new_email)

        # if user not exists create user, create association, create tokens, return info(user, tokens)
        if user_exists is None:
            # validate password security
            if not validate_password_security(new_password):
                return jsonify(message='Password must contain at least 8 characters, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character'), 400
            
            # hash password
            hashed_password = hash_password(new_password)

            # create new user
            new_user = Users(password=hashed_password, email=new_email)

            # save new user
            save_user(new_user)

            # create association between user and business
            new_user_business_association = UserBusinessAssociation(user_id=new_user.id, business_id=business_id)

            # save association
            save_user_business_association(new_user_business_association)

            # create tokens
            tokens = create_tokens(new_user.id)

            # save tokens
            save_user_tokens(new_user.id, business_id, tokens['access_token'], tokens['refresh_token'])

            response_data = {
                'user': new_user.to_dict(),
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token']
            }

            # return json response email
            return jsonify(response_data), 201
        else:
            # check if user is associated with business
            user_business_association = UserBusinessAssociation.query.filter_by(user_id=user_exists.id, business_id=business_id).first()

            # if user is associated with business return error
            if user_business_association is not None:
                return jsonify(message='User already exists'), 400

            # if user is not associated with business create association, create tokens, return info(user, tokens)
            else:
                # create association between user and business
                new_user_business_association = UserBusinessAssociation(user_id=user_exists.id, business_id=business_id)

                # save association
                save_user_business_association(new_user_business_association)

                # create tokens
                tokens = create_tokens(user_exists.id)

                # save tokens
                save_user_tokens(user_exists.id, business_id, tokens['access_token'], tokens['refresh_token'])

                response_data = {
                    'user': user_exists.to_dict(),
                    "access_token": tokens['access_token'],
                    "refresh_token": tokens['refresh_token']
                }

                # return json response email
                return jsonify(response_data), 201
    except:
        return jsonify(message='Problem with the user or password'), 400

# Log use with email and password
@users_bp.route('/email_ps/login/<int:business_id>', methods=['POST'])
def log_user(business_id):
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        # find_user
        user_exists = find_user_by_email(email)

        # if user not exists return error
        if user_exists is None:
            return jsonify(message='Problem with the user or password'), 400

        # check if user is associated with business
        user_business_association = UserBusinessAssociation.query.filter_by(user_id=user_exists.id, business_id=business_id).first()

        # if user is not associated with business return error
        if user_business_association is None:
            return jsonify(message='Problem with the user or password'), 400

        # if user is associated with business validate password and return tokens
        else:
            # validate password
            if not password_is_correct(password, user_exists.password):
                return jsonify(message='Problem with the user or password'), 400

            # create tokens
            tokens = create_tokens(user_exists.id)

            # save tokens
            save_user_tokens(user_exists.id, business_id, tokens['access_token'], tokens['refresh_token'])

            response_data = {
                'user': user_exists.to_dict(),
                "access_token": tokens['access_token'],
                "refresh_token": tokens['refresh_token']
            }

            # return json response email
            return jsonify(response_data), 201
    except:
        return jsonify(message='Problem with the user or password'), 400

            
# create or log user with email
@users_bp.route('/email/<int:business_id>', methods=['POST'])
def create_user_email(business_id):    
    try:

        data = request.get_json()
        new_email = data['data']

        #validate email
        if not validate_email(new_email):
            return jsonify(message='Email is required'), 400     

        #create a random password
        new_password = generate_random_password()

        # hash password
        hashed_password = hash_password(new_password)

        #password for email expire in 5 minutes
        password_email_expire = datetime.now() + timedelta(minutes=5)

        # check if the email already exists
        user_exists = find_user_by_email(new_email)

        # if user not exists create user, create association, create tokens, return info(user, tokens)
        if user_exists is None: 
        
            # create new user
            new_user = Users(email=new_email, password_email=hashed_password, password_email_expire=password_email_expire)

            # save new user
            save_user(new_user)

            # create association between user and business
            new_user_business_association = UserBusinessAssociation(user_id=new_user.id, business_id=business_id)

            # save association
            save_user_business_association(new_user_business_association)

            response_data = {
                'email': new_user.to_dict()["email"]
            }
            # TODO: send email to user with temporary password
            # send email to user with temporary password
            # send_email(new_email, new_password)

            return jsonify(response_data), 201

        else:
            # check if user is associated with business
            user_business_association = UserBusinessAssociation.query.filter_by(user_id=user_exists.id, business_id=business_id).first()

            if user_business_association is None:
                # update user password_email and password_email_expire
                updated_user(user_exists, {'password_email': hashed_password, 'password_email_expire': password_email_expire})

                # create association between user and business
                new_user_business_association = UserBusinessAssociation(user_id=user_exists.id, business_id=business_id)

                # save association
                save_user_business_association(new_user_business_association)

                response_data = {
                    'email': user_exists.to_dict()["email"]
                }
                # TODO: send email to user with temporary password
                # send email to user with temporary password
                # send_email(new_email, new_password)

                return jsonify(response_data), 201
            
            else:
                # update user password_email and password_email_expire
                updated_user(user_exists, {'password_email': hashed_password, 'password_email_expire': password_email_expire})

                response_data = {
                    'email': user_exists.to_dict()["email"]
                }

                # TODO: send email to user with temporary password
                # send email to user with temporary password
                # send_email(new_email, new_password)

                return jsonify(response_data), 201
    except:
        return jsonify(message='Problem with the user or password'), 400
        
# Validate refresh token
@users_bp.route('/refresh_token/<int:business_id>', methods=['POST'])
def refresh(business_id):
    try:
        data = request.get_json()
        refresh_token = data['refresh_token']
        user_id = data['user_id']

        # find session on tokens 
        session = Tokens.query.filter_by(user_id=user_id, business_id=business_id, refresh_token=refresh_token).first()

        # if session not exists return error

        if session is None:
            return jsonify(message='Problem with the session, not exist'), 400
        
        else:
            # if session exists validate refresh token is not expired
            decoded_token = decode_rt(refresh_token)

            # check if token is expired
            if decoded_token['exp'] < datetime.now().timestamp():
                return jsonify(message='Session expired'), 400

            # if token is not expired create new tokens and return them
            else:
                tokens = create_tokens(user_id)

                # save tokens
                update_user_tokens(user_id, business_id, tokens['access_token'], tokens['refresh_token'])

                response_data = {
                    "access_token": tokens['access_token'],
                    "refresh_token": tokens['refresh_token']
                }

                return jsonify(response_data), 201
    except:
        return jsonify(message='Problem with the session'), 400






