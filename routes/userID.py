from flask import jsonify, request, Blueprint
from models.users import User
from models import db
from flask_cors import cross_origin

user_id_blueprint = Blueprint('user_id', __name__)

@user_id_blueprint.route('/', methods=['GET'])
@cross_origin()  # This will add CORS headers to this route
def get_user_data():
    user = User.query.all()
    user_list = [{'id' : u.id, 'username': u.username} for u in user]
    return jsonify(user_list), 200