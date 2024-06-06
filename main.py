from flask import Flask, request

import json, os, PIL.Image, requests

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 載入 Google Gemini 相關函式庫
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

# 載入設定檔API Key
from config import GOOGLE_API_KEY, line_access_token, line_secret, Notion_api, Notion_DB

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容

    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = line_access_token
        secret = line_secret
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            print(msg)                                       # 印出內容
            response = model.generate_content(msg)
            print(response.text)
            reply = response.text
        elif type == 'image':
            msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            file_path = os.path.join(image_dir, f'{msgID}.jpg')
            with open(file_path, 'wb') as fd:
                fd.write(message_content.content)             # 以二進位的方式寫入檔案
            data = Gemini_namecard(file_path)
            Notion_Write(data,msgID)
            formatted_response = (
                f"Name: {data.get('Name', 'N/A')}\n"
                f"Title: {data.get('Title', 'N/A')}\n"
                f"Address: {data.get('Address', 'N/A')}\n"
                f"Email: {data.get('Email', 'N/A')}\n"
                f"Phone: {data.get('Phone', 'N/A')}\n"
                f"Company: {data.get('Company', 'N/A')}"
            )
            reply = formatted_response                         # 設定要回傳的訊息
        else:
            reply = '你傳的不是文字或圖片呦～'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

def Gemini_namecard(img_path):
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        ImagePrompt = "Here is a business card, and you are a business card secretary. Please organize the following information into JSON for me. If something is unclear, fill it with N/A. Only the JSON is needed:\n\nName, Title, Address, Email, Phone, Company.\n\nThe format for the Phone content should be #886-0123-456-789,1234. Ignore ,1234 if there is no extension.\n\nFor the same information in different languages, please put them in the same field separated by commas."
        img = PIL.Image.open(img_path)
        print("image oppen")
        response = model.generate_content([ImagePrompt, img], stream=True)
        print("get respond")
        response.resolve()
        print(response.text)
        raw_response = response.text
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:]
        if raw_response.endswith("```"):
            raw_response = raw_response[:-3]
        data = json.loads(raw_response)
        return data
    except:
        print("Gemini got somthing wrong!")  
        return "Gemini got somthing wrong!"

def Notion_Write(namecard_json,Namecard_ID):
    try:
        notion_api_url = 'https://api.notion.com/v1/pages'
        headers = {
            "Authorization": f"Bearer {Notion_api}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        new_page = {
            "parent": { "database_id": Notion_DB },
            "properties": {
                "UUID":{
                    "title":[
                        {
                            "text": {
                                "content": Namecard_ID
                            }
                        }
                    ]
                },
                "Name": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Name", "N/A")
                            }
                        }
                    ]
                },
                "Title": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Title", "N/A")
                            }
                        }
                    ]
                },
                "Address": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Address", "N/A")
                            }
                        }
                    ]
                },
                "Email": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Email", "N/A")
                            }
                        }
                    ]
                },
                "Phone": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Phone", "N/A")
                            }
                        }
                    ]
                },
                "Company": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Company", "N/A")
                            }
                        }
                    ]
                }
            }
        }
        response = requests.post(notion_api_url, headers=headers, json=new_page)
        if response.status_code == 200:
            print("Successfully added to Notion DB")
        else:
            print(f"Failed to add to Notion DB: {response.status_code}")
            print(response.text)
    except:
        print("Notion got somthing wrong!")  
    

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    image_dir = 'image'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    app.run()