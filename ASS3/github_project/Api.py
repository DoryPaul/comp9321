import flask
from flask import Flask,request,Response
import json
import datetime
from flask_restplus import Api,Resource,fields
import data_cleaning,calculate_weight

app = Flask(__name__)
api = Api(app,default = 'Assignment3',
          title = 'COMP9321 ASS3',
          description = 'This is the assignment3 of COMP9321 for heart disease.')

@api.route('/data_uniform')
class data_uniform(Resource):
    @api.response(200, '200 Successfully.')
    @api.response(404, '404 Error')
    @api.doc(descrption='Uniform data')
    def get(self):
        result = data_cleaning.data_uniform('clean_data.csv').to_json(orient='values')
        return result,200


@api.route('/weight')
class weight(Resource):
    @api.response(200, '200 Successfully.')
    @api.response(404, '404 Error')
    @api.doc(descrption='Calculate the weight.')
    def get(self):
        result = calculate_weight.weight()
        return result,200


if __name__ == '__main__':
    app.run()
