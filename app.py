from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy, Model
from flask_mongoengine import MongoEngine
import pymongo
import json
import os
import db

# Replace your URL here. Don't forget to replace the password.
connection_url = 'mongodb+srv://pp:DcDuOKtZ56iFKsq6@cluster0.uojms.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('Example')
# Table
TestUserInput = Database.TestUserInput

#Request Parser สำหรับเพิ่มข้อมูลลง db (ใน post method)
input_add_args = reqparse.RequestParser()
input_add_args.add_argument("message", type=str, help="กรุณาป้อนข้อความเป็นตัวอักษรและมีความยาวไม่เกิน 1000 ตัวอักษร")
input_add_args.add_argument("message_type", type=str, help="กรุณาระบุประเภท Input เป็นตัวอักษร")

resource_field = {
    "input_id":fields.Integer,
    "message":fields.String,
    "message_type":fields.String,
} #นิยามกฎเกณฑ์สำหรับเตรียมบันทึกข้อมูล

#design
# @cross_origin()
class UserExtension(Resource):
    
    # To find the first document that matches a defined query,
    # find_one function is used and the query to match is passed
    # as an argument.
    @marshal_with(resource_field)
    def get(self, input_id):
        queryObject = {"input_id": input_id}
        query = TestUserInput.find_one(queryObject)
        if not query:
            abort(404, message="ไม่พบข้อมูล Input ที่คุณร้องขอ")
        query.pop('_id')
        return query, 200
    
    # To insert a single document into the database,
    # insert_one() function is used
    @marshal_with(resource_field)
    def post(self,input_id):
        queryObject = {"input_id": input_id}
        result = TestUserInput.find_one(queryObject)
        if result:
            abort(409, message="รหัส Input นี้เคยบันทึกไปแล้ว")
        
        args = input_add_args.parse_args() #ข้อมูลที่ได้รับอยู่ในนี้
        if not args["message"]:
            abort(422, message="กรุณาใส่ข้อความ , ลิงค์ หรือ รูปภาพ")
        
        queryObject = {
        'input_id': input_id,
        'message': args["message"],
        'message_type': args["message_type"],
    }
        
        input = TestUserInput.insert_one(queryObject)
        return queryObject, 201
        
#call
api.add_resource(UserExtension,"/extension/<int:input_id>")

if __name__ == "__main__":
    app.run(debug=True)