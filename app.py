import requests
import werkzeug
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flask_cors import CORS, cross_origin

# import function สำหรับค้นหาหัวข้อข่าวที่เกี่ยวข้องและ similarity check
from Preprocess.tf_idf_all_headline_news_similarity import cosine_similarity_T

# import function สำหรับ OCR
from EasyOCR.EasyOCR_model import OCR_with_user_image

# import function สำหรับดึง user input ของ user จาก facebook
from News_fetcher.facebook import facebook

# import function สำหรับตรวจ link ที่ต้องมี domain เป็น www.facebook.com
from urllib.parse import urlparse

app = Flask(__name__)
cors = CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

#design

class UserExtension(Resource):
    
    # To find the first document that matches a defined query,
    # find_one function is used and the query to match is passed
    # as an argument.
    @cross_origin(supports_credentials=True)
    def post(self):
        
        # Request Parser สำหรับรับข้อมูลจาก frontend
        input_add_args = reqparse.RequestParser()
        input_add_args.add_argument("message", type=str, help="กรุณาระบุข้อความ input เป็นตัวอักษรความยาวไม่เกิน 1000 ตัวอักษร")
        input_add_args.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
        input_add_args.add_argument("message_type", type=str, help="กรุณาระบุประเภท Input เป็นตัวอักษร")
        args = input_add_args.parse_args()
        
        # กรณีไม่ได้ระบุประเภทของ input
        if (args["message_type"] != "link") and (args["message_type"] != "content") and (args["message_type"] != "image") and (args["message_type"] != "image_url"):
            abort(400 ,message = "กรุณาระบุประเภทของ input เป็น link , content , image หรือ image_url")

        # กรณีใส่ link ที่ domain ไม่ใช่ post ของ facebook
        if (args["message_type"] == "link") and (urlparse(args["message"]).hostname != "www.facebook.com"):
            abort(400 ,message = "กรุณาระบุลิงค์ของโพสต์ Facebook")

        # กรณีไม่มีข้อความ (message) แนบมาด้วย 
        if (args["message_type"] == "content" or args["message_type"] == "link" or args["message_type"] == "image_url") and (not args["message"] or args["message"].isspace()):
            abort(422, message = "กรุณาใส่ข้อความ , ลิงค์ หรือ URL ของรูปภาพ")
        
        # กรณีไม่มีรูปภาพ (image) แนบมาด้วย 
        if (args["message_type"] == "image") and (not args["image"]):
            abort(422, message = "กรุณาอัพโหลดรูปภาพ")
            
    
        #เพิ่ม if-condition กรณี search ผ่านรูป + ลิงค์ 

        if args["message_type"] == "content":
            all_result_with_url = cosine_similarity_T(10, args["message"])
            
            queryObject = {
                "message": args["message"],
                "message_type": args["message_type"],
                "result": all_result_with_url
            }
            
        elif args["message_type"] == "image":
            try:
                image_file = args['image']
                image_file.save("EasyOCR/OCR_User_Pic/tmp.jpg")
                
                text_from_image = OCR_with_user_image("EasyOCR/OCR_User_Pic/tmp.jpg")
                all_result_with_url = cosine_similarity_T(10, text_from_image)
                
                queryObject = {
                    "message": text_from_image,
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }
            except:
                abort(422 ,message = "กรุณาอัพโหลดไฟล์รูปภาพ .JPG หรือ .PNG")
            
        elif args["message_type"] == "image_url":
            try:
                response = requests.get(args["message"])
                with open('EasyOCR/OCR_User_Pic/tmp.jpg', 'wb') as file:
                    file.write(response.content)
                
                text_from_image = OCR_with_user_image("EasyOCR/OCR_User_Pic/tmp.jpg")
                all_result_with_url = cosine_similarity_T(10, text_from_image)
                
                queryObject = {
                    "message": text_from_image,
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }
            except:
                abort(422 ,message = "ขออภัย เราไม่รองรับลิงค์รูปภาพนี้ กรุณาตรวจสอบลิงค์ หรือบันทึกรูปภาพแล้วค้นหาผ่านการอัพโหลดแทน")
            
        elif args["message_type"] == "link":
            try:
                facebook_fetch = facebook(args["message"])
                post_facebook = facebook_fetch.fetch_page()
                all_result_with_url = cosine_similarity_T(10, post_facebook["content"])

                queryObject = {
                    "message": post_facebook["content"],
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }
            except:
                abort(422 ,message = "กรุณาระบุลิงค์ของโพสต์ให้ถูกต้อง")
             
        return queryObject
        
#call
api.add_resource(UserExtension,"/extension")

if __name__ == "__main__":
    app.run(debug=True)
