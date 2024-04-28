from flask import Flask
from flask_restx import Api, Resource, fields
from XGB_deployment import pred_price


# Definición aplicación Flask
app = Flask(__name__)

# Definición API Flask
api = Api(
    app, 
    version='1.0', 
    title='Car Price Prediction - Group 25',
    description='Car price prediction API, group 25 ML and NLP')

ns = api.namespace('predict', 
     description='Car price Estimation')

# Definición argumentos o parámetros de la API
parser = api.parser()
parser.add_argument(
    'Year', 
    type=int, 
    required=True, 
    help='Year of manufacture of the car', 
    location='args')

parser.add_argument(
    'Mileage', 
    type=float, 
    required=True, 
    help='Mileage of the car', 
    location='args')

parser.add_argument(
    'State', 
    type=str, 
    required=True, 
    help='State in which the car is being sold (add a space before argument)', 
    location='args')

parser.add_argument(
    'Brand', 
    type=str, 
    required=True, 
    help='Brand of the car', 
    location='args')

parser.add_argument(
    'Model', 
    type=str, 
    required=True, 
    help='Model of the car', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.Float,
})

@ns.route('/')
class PricePredApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": pred_price([args['Year'],args['Mileage'],args['State'],args['Brand'],args['Model']])
        }, 200

if __name__ == '__main__':        
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000) 