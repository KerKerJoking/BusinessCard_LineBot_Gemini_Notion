import requests
import logging
from config import NOTION_API, NOTION_DB

def Notion_Write(namecard_json, Namecard_ID):
    try:
        NOTION_API_url = 'https://api.notion.com/v1/pages'
        headers = {
            "Authorization": f"Bearer {NOTION_API}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        new_page = {
            "parent": { "database_id": NOTION_DB },
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
        response = requests.post(NOTION_API_url, headers=headers, json=new_page)
        if response.status_code == 200:
            logging.info("Successfully added to Notion DB")
        else:
            logging.error("Failed to add to Notion DB: %s", response.status_code)
            logging.error(response.text)
    except Exception as e:
        logging.error("Notion error: %s", e)
