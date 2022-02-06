from email import message
import os
import base64
import werkzeug
from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS, cross_origin

# import function สำหรับค้นหาหัวข้อข่าวที่เกี่ยวข้องและ similarity check
from Preprocess.tf_idf_all_headline_news_similarity import cosine_similarity_T

# import function สำหรับ OCR
from EasyOCR.EasyOCR_model import OCR_with_user_image

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
# input_add_args.add_argument("message", type=str, help="กรุณาป้อนข้อความเป็นตัวอักษรและมีความยาวไม่เกิน 1000 ตัวอักษร")
input_add_args.add_argument("message", type=werkzeug.datastructures.FileStorage, location='files', help="กรุณา upload file รูปภาพ")
input_add_args.add_argument("message_type", type=str, help="กรุณาระบุประเภท Input เป็นตัวอักษร")
input_add_args.add_argument("facebook_access_token", type=str, help="กรุณาระบุประเภท Facebook Access Token เป็นตัวอักษร")

#design
class UserExtension(Resource):
    
    # To find the first document that matches a defined query,
    # find_one function is used and the query to match is passed
    # as an argument.
    @cross_origin(supports_credentials=True)
    def post(self):
        args = input_add_args.parse_args() #ข้อมูลที่ได้รับอยู่ในนี้
            
        if (args["message_type"] != "link") and (args["message_type"] != "content") and (args["message_type"] != "image"):
            abort(400 ,message = "กรุณาระบุประเภทของ input เป็น link , content หรือ image")
    
        if (args["message_type"] == "content" or args["message_type"] == "link") and (not args["message"]):
            abort(422, message = "กรุณาใส่ข้อความ , ลิงค์ หรือ รูปภาพ")
    
        #เพิ่ม if-condition กรณี search ผ่านรูป + ลิงค์ 

        if args["message_type"] == "content":
            all_result_with_url = cosine_similarity_T(10, args["message"])
            # result = result_similarity_check(all_result_with_url)
            
            queryObject = {
                # "input_id": 1,
                "message": args["message"],
                "message_type": args["message_type"],
                "result": all_result_with_url
            }
            
            
        if args["message_type"] == "image":
            # The image is retrieved as a file
            
            print("This is args :",args["message"]["lastModified"])
            
            image_file = args(strict=True).get("message", None)
            if image_file:
                image = image_file.read()
                image.save("EasyOCR/OCR_User_Pic/tmp.jpg")
                
            # photo = args["message"]
            
    
            # photo_data = base64.b64decode(photo)
            
            # print("This is photo :",args)
            
            # with open("EasyOCR/OCR_User_Pic/tmp.jpg", "w") as file:
            #     file.write(photo)
            
            # text_from_image = OCR_with_user_image("EasyOCR/OCR_User_Pic/tmp.jpg")
            # all_result_with_url = cosine_similarity_T(30, text_from_image)
            # result = result_similarity_check(all_result_with_url)
            
            queryObject = {
                # "input_id": 1,
                "message": args["message"],
                "message_type": args["message_type"],
                "result": args["image_file"]
            }
    
        # # print("This is queryObject : ", queryObject)
        # response = jsonify(queryObject)
        # # print("This is response : ", response)
        # response.headers.add('Access-Control-Allow-Origin', '*')

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