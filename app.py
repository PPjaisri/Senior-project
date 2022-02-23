import re
import requests
import werkzeug
from flask import Flask
from flask_cors import CORS
from flask_restful import abort, reqparse

# import function สำหรับค้นหาหัวข้อข่าวที่เกี่ยวข้องและ similarity check
from Preprocess.tf_idf_all_headline_news_similarity import cosine_similarity_T

# import function สำหรับ OCR
from EasyOCR.EasyOCR_model import OCR_with_user_image

# import function สำหรับดึง user input ของ user จาก facebook
from News_fetcher.facebook import facebook

# import function สำหรับตรวจ link ที่ต้องมี domain เป็น www.facebook.com
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)


@app.route('/extension', methods=['GET', 'POST'])
def extension():
    input_add_args = reqparse.RequestParser()
    input_add_args.add_argument(
        "message", type=str, help="กรุณาระบุข้อความ input เป็นตัวอักษรความยาวไม่เกิน 1000 ตัวอักษร")
    input_add_args.add_argument(
        "image", type=werkzeug.datastructures.FileStorage, location='files')
    input_add_args.add_argument(
        "message_type", type=str, help="กรุณาระบุประเภท Input เป็นตัวอักษร")
    args = input_add_args.parse_args()

    message_type = ['link', 'content', 'image', 'image_url']

    # กรณีไม่ได้ระบุประเภทของ input
    if args['message_type'] not in message_type:
        abort(400, message="กรุณาระบุประเภทของ input เป็น link, content, image หรือ image_url")
    else:
        if args['message'].isspace():
            abort(422, message="กรุณาใส่ข้อความ , ลิงค์ หรือ URL ของรูปภาพ")
        # กรณีไม่มีข้อความ (message) แนบมาด้วย
        if args['message_type'] == 'link':
            # กรณีไม่มีลิงค์ (link) แนบมาด้วย
            if not args['message']:
                abort(422, message="กรุณาใส่ link ของ facebook")
            else:
                hostname = urlparse(args['message']).hostname
                # กรณีใส่ link ที่ domain ไม่ใช่ post ของ facebook
                if not re.search(hostname, 'facebook'):
                    abort(400, message="กรุณาระบุลิงค์ของโพสต์ Facebook")
                else:
                    try:
                        facebook_fetch = facebook(args["message"])
                        post_facebook = facebook_fetch.fetch_page()
                        all_result_with_url = cosine_similarity_T(
                            10, post_facebook["content"])

                        queryObject = {
                            "message": post_facebook["content"],
                            "message_type": args["message_type"],
                            "result": all_result_with_url
                        }
                    except:
                        abort(400, message="กรุณาระบุลิงค์ของโพสต์ให้ถูกต้อง")
        elif args['message_type'] == 'content':
            # กรณีไม่มีข้อความ (content) แนบมาด้วย
            if not args['message']:
                abort(422, message="กรุณาใส่ข้อความ")
            else:
                all_result_with_url = cosine_similarity_T(10, args["message"])

                queryObject = {
                    "message": args["message"],
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }
        elif args['message_type'] == 'image':
            # กรณีไม่มีรูปภาพ (image) แนบมาด้วย
            if not args['message']:
                abort(422, message="กรุณาอัพโหลดรูปภาพ")
            else:
                image_file = args['image']
                image_file.save("EasyOCR/OCR_User_Pic/tmp.jpg")

                text_from_image = OCR_with_user_image(
                    "EasyOCR/OCR_User_Pic/tmp.jpg")
                all_result_with_url = cosine_similarity_T(10, text_from_image)

                queryObject = {
                    "message": text_from_image,
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }
        else:
            # กรณีไม่มีลิงค์รูปภาพ (image_url) แนบมาด้วย
            if not args['message']:
                abort(422, message="กรุณาใส่ URL ของรูปภาพ")
            else:
                response = requests.get(args["message"])
                with open('EasyOCR/OCR_User_Pic/tmp.jpg', 'wb') as file:
                    file.write(response.content)

                text_from_image = OCR_with_user_image(
                    "EasyOCR/OCR_User_Pic/tmp.jpg")
                all_result_with_url = cosine_similarity_T(10, text_from_image)

                queryObject = {
                    "message": text_from_image,
                    "message_type": args["message_type"],
                    "result": all_result_with_url
                }

    return queryObject


if __name__ == '__main__':
    app.run()

