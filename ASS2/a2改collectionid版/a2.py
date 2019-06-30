'''
COMP9321 2019 Term 1 Assignment Two Code Template
Student Name:YIZHENG YING
Student ID:z5141180
'''
import sqlite3
from sqlite3 import Error
import flask
from flask import Flask, jsonify,request
import json
import datetime
from flask_restplus import Api,Resource,fields,reqparse
import requests
import re

def create_db(db_file):
    '''
    uase this function to create a db, don't change the name of this function.
    db_file: Your database's name.
    '''
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ASS2
               (COLLECTION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               LOCATION     TEXT    NOT NULL,
               INDICATOR     TEXT    NOT NULL,
               INDICATOR_VALUE   TEXT    NOT NULL,
               CREATION_TIME      DATETIME   default (datetime('now', 'localtime')),
               ENTRIES    TEXT);''')
    except Error as e:
        print(e)
    finally:
        conn.commit()
        conn.close()



app = Flask(__name__)
api = Api(app,default = 'Assignment2',
          title = 'COMP9321 ASS2 z5141180',
          description = 'This is the assignment2 of COMP9321 for the world bank.\n z5141180 YIZHENG YING')
indicator = api.model('indicator_id', {'indicator_id': fields.String})


@api.route('/yyz')
class data_collection(Resource):

    @api.response(201,'201 Created')
    @api.response(200,'200 OK')
    @api.response(404,'404 Error')
    @api.doc(descrption='Get new data')
    @api.expect(indicator,validate = True)
    def post(self):
        url_input = request.json
        indicator_id = url_input['indicator_id']

        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        name = []
        c.execute('select INDICATOR from ASS2;')
        for item in c:
            name.append(item[0])
        if indicator_id in name:
            c.execute("select LOCATION,COLLECTION_ID,INDICATOR,CREATION_TIME from  ASS2 where INDICATOR ='%s';"%(indicator_id))
            data_dict = {}
            for result in c:
                data_dict['location'] = result[0]
                data_dict['collection_id'] = result[1]
                data_dict['creation_time'] = result[3]
                data_dict['indicator'] = result[2]
            return data_dict,200

        original_data = requests.get('http://api.worldbank.org/v2/countries/all/indicators/' + str(indicator_id) + '?date=2013:2018&format=json')
        original_data_dict = original_data.json()
        if 'message' in original_data_dict[0]:
            if original_data_dict[0]['message'][0]['key'] == 'Invalid value':
                return '{} does not exist.'.format(indicator_id),404

        c.execute('select COLLECTION_ID from ASS2;')
        temp_id = []
        for num_id in c:
            temp_id.append(num_id[0])
        result_dict = {}

        result_dict['location'] = "/yyz/"+str(temp_id[-1]+1)
        result_dict['collection_id'] = temp_id[-1]+1
        result_dict['indicator'] = original_data_dict[1][0]["indicator"]['id']
        result_dict['indicator_value'] = original_data_dict[1][0]["indicator"]['value']
        result_dict['entries'] = []
        time = datetime.datetime.now()
        result_dict['creation_time'] = time.strftime( '%Y-%m-%d %H:%M:%S' )


        for i in range(1,3):
            page_result = requests.get('http://api.worldbank.org/v2/countries/all/indicators/' + \
                             str(indicator_id) + '?date=2013:2018&format=json&page=' + str(i))
            page_dict = page_result.json()
            for item in page_dict[1]:
                temp_value = {}
                temp_value["country"] = item['country']['value']
                temp_value["date"] = item['date']
                temp_value["value"] = item['value']
                result_dict["entries"].append(temp_value)
        entries = result_dict["entries"]
        #entries = entries.replace("'",'"')
        entries = json.dumps(entries,indent=4)
        sqlstr = "insert into ASS2 (LOCATION,INDICATOR,INDICATOR_VALUE,CREATION_TIME,ENTRIES) " \
                 "VALUES('%s','%s','%s','%s','%s'); " % (result_dict['location'], result_dict['indicator'],result_dict['indicator_value'],result_dict['creation_time'], entries)
        c.execute(sqlstr)
        conn.commit()
        conn.close()
        show = {}
        show['location'] = result_dict['location']
        show['collection_id'] = result_dict['collection_id']
        show['creation_time'] = result_dict['creation_time']
        show['indicator'] = result_dict['indicator']
        return show,201

    @api.response(200, 'Retrieve All Collections')
    @api.doc(description="Retrieve all collections in the database")
    def get(self):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        result = []
        c.execute('select INDICATOR from ASS2;')
        temp_item = []
        for i in c:
            temp_item.append(i[0])
        for m in temp_item:
            temp = {}
            c.execute("select * from ASS2 where INDICATOR='%s';"%(m))
            for item in c:
                temp['location'] = item[1]
                temp['collection_id'] = item[0]
                temp['indicator'] = item[2]
                temp['creation_time'] = item[4]
            result.append(temp)

        conn.commit()
        conn.close()
        result = json.dumps(result, indent=4)
        return result, 200

@api.route('/yyz/<collection_id>')
class collection_delete(Resource):
    @api.response(200,'Retrieve The Collection')
    @api.response(404,'Invalid attempt')
    def get(self,collection_id):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        result_id = []
        c.execute('select COLLECTION_ID from ASS2;')
        for i in c:
            result_id.append(i[0])
        if int(collection_id) not in result_id:
            return {"message": "Collection {} is not in the databaset".format(collection_id)}, 404

        c.execute("select * from ASS2 where COLLECTION_ID ='%s'"%(collection_id))
        show_list = {}
        for result in c:
            show_list['location'] = result[1]
            show_list['collection_id'] = result[0]
            show_list['creation_time'] = result[4]
            show_list['indicator'] = result[2]
            show_list['entries'] = json.loads(result[5])
        show_list = json.dumps(show_list, indent=4)
        conn.close()
        return show_list,200

    @api.response(200,'Delete a data.')
    @api.response(404,'Data does not exist.')
    @api.doc(description='Delete a collection from sqlite')
    def delete(self,collection_id):
        print(collection_id)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        result_id = []
        c.execute('select COLLECTION_ID from ASS2;')
        for i in c:
            result_id.append(i[0])
        if int(collection_id) not in result_id:
            return {"message": "Collection {} is not in the databaset".format(collection_id)}, 404
        c.execute("delete from ASS2 where COLLECTION_ID ='%s'" % (collection_id))
        conn.commit()
        conn.close()
        return {"message": "Collection = {} is removed from the databaset!".format(collection_id)}, 200

@api.route('/yyz/<collection_id>/<year>/<country>')
class retrieve_indicator(Resource):
    @api.response(200,'Retrieve indicator successfully.')
    @api.response(404,'Data does not exist.')
    @api.doc(description='Retrieve economic indicator value for given country and a year')
    def get(self,collection_id,year,country):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        result_id = []
        c.execute('select COLLECTION_ID from ASS2;')
        for i in c:
            result_id.append(i[0])
        if int(collection_id) not in result_id:
            return {"message": "Collection {} is not in the databaset.".format(collection_id)}, 404
        c.execute("select INDICATOR ,ENTRIES from ASS2 where COLLECTION_ID ='%s'" % (collection_id))
        result = {}
        result["collection_id"] = collection_id

        for i in c:
            result["indicator"] = i[0]
            temp = str(json.loads(i[1])).split("[")[1].split("]")[0].split('},')
            for item in temp:
                if item[-1] != '}':
                    item = eval(item + '}')
                else:
                    item = eval(item)
                if year == item['date'] and country == item['country']:
                    result['country'] = item['country']
                    result['year'] = item['date']
                    result['value'] = item['value']

        conn.close()
        if len(result) < 3:
            return {"message": "The data of {} in {} is not in the databaset.".format(country,year)}, 404
        result = json.dumps(result,indent=4)
        return result,200

@api.route('/yyz/<collection_id>/<year>')
class retrieve_top_bottom(Resource):
    @api.response(200,'Retrieve top&bottom successfully.')
    @api.response(404,'Data does not exist.')
    @api.doc(description='Retrieve top/bottom economic indicator values for a given year')
    @api.param('q','The q is an optional parameter which can be top<N> or bottom<N> and  N can be an integer value between 1 and 100.')
    def get(self,collection_id,year):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        result_id = []
        c.execute('select COLLECTION_ID from ASS2;')
        for i in c:
            result_id.append(i[0])
        if int(collection_id) not in result_id:
            return {"message": "Collection {} is not in the databaset/ invalid input".format(collection_id)}, 404
        c.execute("select INDICATOR ,INDICATOR_VALUE,ENTRIES from ASS2 where COLLECTION_ID ='%s'" % (collection_id))
        result = {}
        temp_list = []

        for i in c:
            result['indicator'] = i[0]
            result['indicator_value'] = i[1]
            temp = str(json.loads(i[2])).split("[")[1].split("]")[0].split('},')
            for item in temp:
                if item[-1] != '}':
                    item = eval(item + '}')
                else:
                    item = eval(item)
                if year == item['date'] and item['value'] is not None:
                    temp_list.append(item)
            if temp_list == []:
                return {'message':"The year is wrong or this year's GDP value is none."},404

        q = request.args.get('q')
        if q is None:
            sorted(temp_list, key=lambda data: data['value'])
            result['entries'] = temp_list
            return result,200
        else:
            q =str(q)
            numlist = re.findall(r"\d", q)
            num = ''
            for m in numlist:
                num += m
            state = q.replace(num, '')
            num = int(num)
            entries = []
            if state not in ['top','bottom']:
                return {'message':'Wrong,the query should be top<N> or bottom<N>.'},404
            if num < 0 or num >100:
                return {'message': 'Wrong,top<N> or bottom<N> where 0<N<101.'},404
            if state == 'bottom':
                sort_list = sorted(temp_list, key=lambda data: data['value'])
                if len(sort_list) < num:
                    result['entries'] = sort_list
                else:
                    for i in range(num):
                        entries.append(sort_list[i])
                    result['entries'] = entries
            elif state == 'top':
                sort_list = sorted(temp_list, key=lambda s: float(s['value']),reverse=True)
                if len(sort_list) < num:
                    result['entries'] = sort_list
                else:
                    for i in range(num):
                        entries.append(sort_list[i])
                    result['entries'] = entries
        result = json.dumps(result)
        return result,200


##curl -i -H "Content-Type: application/json" -X POST -d "{\"indicator_id\" : \"NY.GDP.MKTP.CD\"}" http://localhost:5000/yyz
if __name__ == '__main__':
    create_db('data.db')
    app.run()
