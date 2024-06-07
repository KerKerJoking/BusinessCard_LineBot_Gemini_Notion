from flask import Flask, request, jsonify
import json, os, logging
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from config import LINE_ACCESS_TOKEN, LINE_SECRET
from gemini_namecard import Gemini_Namecard
from notion_write import Notion_Write

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = LINE_ACCESS_TOKEN
        secret = LINE_SECRET
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
            data = Gemini_Namecard(file_path)
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

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    image_dir = 'image'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    app.run()
