from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from auth import auth
from config import Config
from flask_cors import CORS
from routes.CRUDcustomers import inputCustomers_blueprint
from routes.customers import customers_blueprint
from routes.prediction import prediction_blueprint
from routes.sales import sales_blueprint
from routes.SalesPerformance import salesPerformance_blueprint
from routes.CRUDemployees import inputEmployees_blueprint
from routes.totalCustomer import get_customer_count_blueprint
from routes.motivationalCards import motivation_card_blueprint

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(inputCustomers_blueprint, url_prefix='/api/customers')
app.register_blueprint(prediction_blueprint, url_prefix='/api/predict')
app.register_blueprint(sales_blueprint, url_prefix='/api/sales-data')
app.register_blueprint(customers_blueprint, url_prefix='/api/customer-growth-data')
app.register_blueprint(salesPerformance_blueprint, url_prefix='/api/sales-performance')
app.register_blueprint(inputEmployees_blueprint, url_prefix='/api/employees')
app.register_blueprint(get_customer_count_blueprint, url_prefix='/api/customers/counts')
app.register_blueprint(motivation_card_blueprint, url_prefix='/api/motivation')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
