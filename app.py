from flask import Flask, request, jsonify
import json, os, logging
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from config import LINE_ACCESS_TOKEN, LINE_SECRET, GOOGLE_API_KEY, NOTION_API, NOTION_DB
from gemini_namecard import Gemini_Namecard
from notion_namecard import Notion_Write, Notion_Search, Format_Notion_Results

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)  # 取得收到的訊息內容
    logging.info("Received request body: %s", body)

    try:
        json_data = json.loads(body)  # json 格式化訊息內容
        access_token = LINE_ACCESS_TOKEN
        secret = LINE_SECRET
        line_bot_api = LineBotApi(access_token)  # 確認 token 是否正確
        handler = WebhookHandler(secret)  # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']  # 加入回傳的 headers
        handler.handle(body, signature)  # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']  # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']  # 取得 LINE 收到的訊息類型
        
        if type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            logging.info("Received text message: %s", msg)
            results = Notion_Search(msg, NOTION_API, NOTION_DB)  # 進行 Notion 搜尋
            if results:
                formatted_results = Format_Notion_Results(results)
                reply = f"搜尋結果：\n{formatted_results}" if results else "沒有找到相關結果。"
            else:
                reply = "沒有找到相關結果。"
        elif type == 'image':
            msgID = json_data['events'][0]['message']['id']  # 取得訊息 id
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            file_path = os.path.join(image_dir, f'{msgID}.jpg')
            with open(file_path, 'wb') as fd:
                fd.write(message_content.content)  # 以二進位的方式寫入檔案
            data = Gemini_Namecard(file_path,GOOGLE_API_KEY)
            if "Name" not in data or data["Name"] == "N/A":
                reply = "辨識失敗，請重新嘗試。"
            else:
                results = Notion_Search(data["Name"], NOTION_API, NOTION_DB)  # 進行 Notion 搜尋
                Notion_Write(data, msgID, NOTION_API, NOTION_DB)
                formatted_response = (
                    f"UUID: {msgID}, \n"
                    f"Name: {data.get('Name', 'N/A')}\n"
                    f"Title: {data.get('Title', 'N/A')}\n"
                    f"Address: {data.get('Address', 'N/A')}\n"
                    f"Email: {data.get('Email', 'N/A')}\n"
                    f"Phone: {data.get('Phone', 'N/A')}\n"
                    f"Company: {data.get('Company', 'N/A')}"
                )
                if results:
                    formatted_results = Format_Notion_Results(results)
                    formatted_response += (f"\n\n我們有找到相似的結果：\n\n{formatted_results}")
                    formatted_response += ("\n\n請輸入del UUID以刪除重複資料")

                reply = formatted_response  # 設定要回傳的訊息
        else:
            reply = "你傳的不是文字或圖片呦～"

        logging.info("Replying with message: %s", reply)
        line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
    except Exception as e:
        logging.error("Error processing request: %s", e)
        logging.error("Request body: %s", body)
    
    return 'OK'  # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    image_dir = 'image'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    app.run()
