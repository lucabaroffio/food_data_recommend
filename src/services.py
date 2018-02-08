from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from model import Similarity_model

model = Similarity_model.load_model_from_file('../epicurious-recipes-with-rating-and-nutrition/recom_model.pkl')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ingredient', action='append', location='args')

class Recommendation(Resource):
	def get(self):
		args = parser.parse_args()
		input_ingredients = args['ingredient']
		rec = model.recommend_ingredients(input_ingredients)
		return rec, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(Recommendation, '/ingredients/recommendation')

if __name__ == '__main__':
    app.run(debug=True)
