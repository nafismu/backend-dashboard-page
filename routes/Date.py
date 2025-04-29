from flask import Blueprint, jsonify
import datetime
import locale


date_blueprint = Blueprint('date', __name__)

@date_blueprint.route('/', methods=['GET'])
def get_date():
    
    date = datetime.datetime.now()
    time = date.strftime("%H:%M:%S")
    return jsonify({"date": date.strftime("%A-%d-%m-%Y"),"time": time})