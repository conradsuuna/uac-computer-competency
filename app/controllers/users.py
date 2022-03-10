from flask import Blueprint, current_app, request, make_response, jsonify
from ..models.User import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
import traceback


auth_bp = Blueprint('auth_bp', __name__)

# registrater user
@auth_bp.route('/user/registration', methods=['POST'])
def deo_registration():
    try:
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form

        columns = ["username","first_name","surname","HIV_status","Phone_number"]
        for column in columns:
            if column not in data:
                return make_response(jsonify({'message': f'{column} is missing from payload!'}), 400)

        existing_user = User.query.filter(User.username == data['username']).first()
        if existing_user:
            return make_response(jsonify({'message': 'Username already exists!'}), 400)

        # create new User
        new_user = User(
            username = data['username'],
            first_name = data['first_name'],
            password = User.hash_password(data['password']),
            surname = data['surname'],
            age = data['age'],
            HIV_status = data['HIV_status'],
            Phone_number = data['Phone_number']
        )
        new_user.save()

        # access_token = create_access_token(identity = data['username'])
        # refresh_token = create_refresh_token(identity = data['username'])
        resp = jsonify({'message':'Account created successfully'})
        return make_response(resp, 201)
    except:
        return make_response(str(traceback.format_exc()),500)


# user login
@auth_bp.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        username = data['username']
        user = User.query.filter(User.username==username).first()###
        password = data['password']

        access_token = create_access_token(identity = data['username'])
        refresh_token = create_refresh_token(identity = data['username'])
        if not user:
            return make_response(jsonify({"message":"Account doesn't exist"}),400)

        if not user.is_password_valid(password):
            return make_response(jsonify({"message":"Invalid credentials"}),400)

        resp = jsonify({'access_token':access_token,
                        'refresh_token':refresh_token,
                        'message':'Login Successful'
                    })
        return make_response(resp,200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get all system users
@auth_bp.route('/user/get_users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        num_of_items = current_app.config['NUM_OF_ITEMS_PER_PAGE']
        page = request.args.get('page', 1, type=int)
        pagination_info = {}

        user_data = User.query.order_by(User.user_id.desc()).paginate(page, num_of_items, False)

        pagination_info['next_page'] = user_data.next_num
        pagination_info['prev_page'] = user_data.prev_num
        pagination_info['current_page'] = user_data.page
        pagination_info['no_of_pages'] = user_data.pages
        pagination_info['items_per_page'] = user_data.per_page
        pagination_info['total_items'] = user_data.total
        users = [z.serialise() for z in user_data.items]

        return make_response(jsonify({"data": users, "info": pagination_info}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get user by id
@auth_bp.route('/lac/get_user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        return make_response(jsonify(user.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)

