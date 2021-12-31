from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS, cross_origin
from flask_mongoengine import MongoEngine
import pymongo
import json
import os
import db

from Preprocess.tf_idf_all_headline_news_similarity import cosine_similarity_T, preprocess

# Replace your URL here. Don't forget to replace the password.
# Pass_link = ""
# with open('MongoPassword.txt') as Passfile:
#     Pass_link = Passfile.read()
# connection_url = Pass_link

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
# client = pymongo.MongoClient(connection_url)

# Database
# Database = client.get_database('Example')
# Table
# TestUserInput = Database.TestUserInput

#Request Parser สำหรับเพิ่มข้อมูลลง db (ใน post method)
input_add_args = reqparse.RequestParser()
input_add_args.add_argument("message", type=str, help="กรุณาป้อนข้อความเป็นตัวอักษรและมีความยาวไม่เกิน 1000 ตัวอักษร")
input_add_args.add_argument("message_type", type=str, help="กรุณาระบุประเภท Input เป็นตัวอักษร")

#design
class UserExtension(Resource):
    
    # To find the first document that matches a defined query,
    # find_one function is used and the query to match is passed
    # as an argument.
    @cross_origin(supports_credentials=True)
    def post(self):
        args = input_add_args.parse_args() #ข้อมูลที่ได้รับอยู่ในนี้
        
        if not args["message"]:
            abort(422, message="กรุณาใส่ข้อความ , ลิงค์ หรือ รูปภาพ")
    
        result = cosine_similarity_T(10, args["message"])
        
        queryObject = {
            # "input_id": 1,
            "message": args["message"],
            "message_type": args["message_type"],
            "result": result
        }
    
        # print("This is queryObject : ", queryObject)
        response = jsonify(queryObject)
        # print("This is response : ", response)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return queryObject
    
    # To insert a single document into the database,
    # insert_one() function is used
    # @marshal_with(resource_field)
    # def post(self,input_id):
    #     queryObject = {"input_id": input_id}
    #     result = TestUserInput.find_one(queryObject)
    #     if result:
    #         abort(409, message="รหัส Input นี้เคยบันทึกไปแล้ว")
        
    #     args = input_add_args.parse_args() #ข้อมูลที่ได้รับอยู่ในนี้
    #     if not args["message"]:
    #         abort(422, message="กรุณาใส่ข้อความ , ลิงค์ หรือ รูปภาพ")
        
    #     queryObject = {
    #     'input_id': input_id,
    #     'message': args["message"],
    #     'message_type': args["message_type"],
    # }
        
    #     input = TestUserInput.insert_one(queryObject)
    #     return queryObject, 201
        
#call
api.add_resource(UserExtension,"/extension")

if __name__ == "__main__":
    app.run(debug=True)